#!/usr/bin/env python3
"""M300 0.5.5: only PING, INFO and fixed-range DUMP requests; never programs a printer.
Python 3.9+ / pyserial. Read-only backup for a separately identified M300 Rev.5.3/HW05; not installation approval.
No session uses ST-Link debug access; the ST-Link VCP is only a serial transport.
"""
from __future__ import annotations
import argparse
import datetime as dt
import glob
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys
import time
import uuid
import zlib
import csv
import zipfile
import audit_reference

VERSION = '0.5.5-host-public-backup1'
READ_TIMEOUT = 0.02  # configured ONCE before port open, never changed in the read loop
FIRMWARE_VERSION = '0.5.5'
COMMAND_BYTE_GAP = 0.002  # 2 ms; UART remains 250000 8N1
QUIET_SECONDS = 0.05  # drain final READY/heartbeat before next command
MAX_CONTROL_ATTEMPTS = 3
PROTOCOL = {
    'BOOT': (0x08000000, 32768, 128),
    'DATA': (0x0803E000, 8192, 128),
    'FLASH256': (0x08000000, 262144, 128),
    'FLASH512': (0x08000000, 524288, 128),
    'SIZE': (0x1FFFF7E0, 2, 128),
    'UID': (0x1FFFF7E8, 12, 128),
    'OPTIONS': (0x1FFFF800, 16, 128),
    'SYSROM': (0x1FFFF000, 2048, 128),
    'REGS': (0, 128, 128),
    'BKP': (0x40006C04, 84, 128),
}
MAX_LINE = 2048

class Link:
    """Bounded newline assembler: partial pyserial reads are not complete frames."""
    def __init__(self, ser, log=None, raw_log=None):
        self.ser, self.log, self.raw_log = ser, log, raw_log
        self.buffer = bytearray()
        self.ready = False
        self.sync_recoveries = 0
        self.rx_bytes = 0
        self.last_rx = time.monotonic()
        self.ping_verified = False
        self.initial_probe_attempts = 0
        self.initial_tail_skipped = False
        self.flash_size_kib = None  # set only after two agreeing SIZE reads
    def line(self, deadline):
        while True:
            if b'\n' in self.buffer:
                pos = self.buffer.index(10)
                raw = bytes(self.buffer[:pos+1]); del self.buffer[:pos+1]
                if len(raw) > MAX_LINE: raise ValueError('Oversized UART line')
                if self.log:
                    self.log.write('RX '+repr(raw)+'\n'); self.log.flush()
                line = raw.rstrip(b'\r\n')
                if line: return line
                continue
            remaining = deadline-time.monotonic()
            if remaining <= 0:
                raise TimeoutError('Timeout waiting for complete UART reply; partial bytes are not accepted')
            n = max(1, min(int(getattr(self.ser, 'in_waiting', 0)), 4096))
            # MACFIX: pySerial's timeout setter reconfigures the open port.
            # On macOS a nonstandard baudrate uses IOSSIOSPEED; repeatedly
            # reapplying it while bytes arrive can disrupt the VCP transport.
            # Keep READ_TIMEOUT fixed at port-open time. Deadline precision is
            # bounded by that 20 ms timeout; no setting is mutated here.
            chunk = self.ser.read(n)

            if chunk:
                if self.raw_log:
                    self.raw_log.write(chunk)
                    self.raw_log.flush()
                self.rx_bytes += len(chunk)
                self.last_rx = time.monotonic()
                self.buffer.extend(chunk)
                if b'\n' not in self.buffer and len(self.buffer) > MAX_LINE:
                    raise ValueError('UART stream has no bounded line terminator')
        raise TimeoutError('Timeout waiting for complete UART reply; partial bytes are not accepted')
    def send(self, command):
        allowed = {'PING', 'INFO'} | {'DUMP '+k for k in PROTOCOL}
        if command not in allowed:
            raise ValueError('Command outside read-only whitelist')
        if not self.ready:
            raise RuntimeError('Nie wysylam polecenia: brak koncowego READY')
        self.settle()
        self._transmit(command)

    def probe_ping(self):
        """Initial read-only probe only. Does NOT authorize INFO/DUMP.
        Caller must first establish a quiet receive interval, with no partial line.
        """
        if self.buffer:
            raise RuntimeError('Nie wysylam PING w srodku niepelnej linii RX')
        self._transmit('PING')

    def _transmit(self, command):
        if command.startswith('DUMP FLASH'):
            expected = select_flash_kind(self.flash_size_kib)
            if command != 'DUMP '+expected:
                raise ValueError('Full-Flash command exceeds or differs from verified SIZE scope')
        data = (command+'\n').encode('ascii')
        if self.log:
            self.log.write('TX '+repr(data)+'\n'); self.log.flush()
        self.ready = False
        # RX in 0.5.5 is polled. Pace short host commands; bulk RX stays unchanged.
        # This does not change UART baud or enable any MCU write operation.
        for byte in data:
            if self.ser.write(bytes([byte])) != 1:
                raise OSError('Incomplete serial command write')
            self.ser.flush()
            time.sleep(COMMAND_BYTE_GAP)

    def settle(self):
        """Never transmit over the tail of READY or a complete idle heartbeat.
        Unexpected data is not silently discarded. No reset_input_buffer() is used.
        """
        hard = time.monotonic()+2.0
        while time.monotonic()<hard:
            try:
                line = self.line(min(hard,time.monotonic()+QUIET_SECONDS))
            except TimeoutError:
                if self.buffer:
                    raise TimeoutError('Niepelna linia UART przed poleceniem; nie wyslano nowych danych')
                return
            check_version(line)
            if line in (b'READY', b'M300RDP/0.5.5 ALIVE READY'):
                continue
            raise RuntimeError('Nieoczekiwane dane miedzy poleceniami: '+repr(line[:160]))
        raise TimeoutError('UART nie osiagnal przerwy miedzy poleceniami')


def serial_class_with_configuration_lock(base):
    """One session, one configuration; fail rather than reconfigure mid-stream.
    This guard detects accidental future settings-property writes after open().
    It is not a claim about commands performed internally by an OS/USB driver.
    """
    class LockedSessionSerial(base):
        def __init__(self, *args, **kwargs):
            self.reconfiguration_count = 0
            self.blocked_reconfigurations = 0
            self._configuration_locked = False
            super().__init__(*args, **kwargs)

        def _reconfigure_port(self, *args, **kwargs):
            if self._configuration_locked:
                self.blocked_reconfigurations += 1
                raise RuntimeError('MACFIX: zablokowano ponowna konfiguracje otwartego portu; zachowaj log')
            self.reconfiguration_count += 1
            return super()._reconfigure_port(*args, **kwargs)

        def open(self):
            super().open()
            self._configuration_locked = True
    return LockedSessionSerial


def check_version(line):
    if line.startswith(b'M300RDP/') and not line.startswith(b'M300RDP/0.5.5 '):
        raise RuntimeError('Dziala inna wersja aplikacji: '+line.decode('ascii',errors='replace')+'. Nie wyslano kolejnego polecenia.')


def consume_ready(link, deadline):
    """Consume the explicit end-of-response marker; ALIVE is not a substitute."""
    while True:
        line = link.line(deadline)
        check_version(line)
        if line == b'READY':
            link.ready = True
            return
        if line == b'M300RDP/0.5.5 ALIVE READY':
            continue
        raise RuntimeError('Oczekiwano READY po odpowiedzi: '+repr(line[:160]))


def parse_frame(line: bytes, seq: int, expected_length: int = 128) -> bytes:
    p=line.rstrip(b'\r\n').split(b' ')
    if len(p)!=4 or p[0]!=b'D': raise ValueError('Invalid data frame')
    if not re.fullmatch(rb'[0-9A-Fa-f]{8}',p[1]) or int(p[1],16)!=seq:
        raise ValueError('Frame sequence mismatch')
    if not re.fullmatch(rb'[0-9A-Fa-f]{8}',p[2]): raise ValueError('Invalid CRC field')
    if not 1 <= expected_length <= 128: raise ValueError('Invalid frame length')
    if len(p[3]) != expected_length*2 or not re.fullmatch(rb'[0-9A-Fa-f]+',p[3]):
        raise ValueError('Invalid hex payload length for exact range')
    data=bytes.fromhex(p[3].decode('ascii'))
    if (zlib.crc32(data)&0xffffffff)!=int(p[2],16): raise ValueError('Frame CRC32 mismatch')
    return data

def parse_begin(line: bytes, kind: str) -> None:
    p=line.rstrip(b'\r\n').split(b' ')
    if len(p)!=5 or p[:2]!=[b'BEGIN',kind.encode('ascii')]: raise ValueError('Unexpected BEGIN')
    if (int(p[2],16),int(p[3]),int(p[4]))!=PROTOCOL[kind]:
        raise ValueError('Unexpected address/length/chunk: dump refused')

def parse_end(line: bytes, kind: str, sha: str) -> None:
    p=line.rstrip(b'\r\n').split(b' ')
    if len(p)!=3 or p[:2]!=[b'END',kind.encode('ascii')]: raise ValueError('Unexpected END')
    if not re.fullmatch(rb'[0-9A-Fa-f]{64}',p[2]) or p[2].decode().lower()!=sha:
        raise ValueError('End SHA256 mismatch')

def validate_device_info(text: str) -> dict:
    if not text.startswith('INFO '): raise ValueError('Not an INFO reply')
    fields={}
    for token in text[5:].split(' '):
        if '=' not in token: raise ValueError('Malformed INFO token')
        k,v=token.split('=',1)
        if k in fields: raise ValueError('Duplicate INFO key')
        fields[k]=v
    need={'MCU','CPUID','ID_SOURCE','PCB_REV','HW','FLASH_KIB','OBR','WRPR','VTOR',
          'DEBUG_ACTIVE','PROFILE_OK','SCOPE','RDP_UNCHANGED'}
    if not need.issubset(fields): raise ValueError('Incomplete 0.5.5 INFO')
    dev=int(fields['MCU'],16);cpu=int(fields['CPUID'],16)
    if dev not in (0,0x414): raise ValueError('Nonzero foreign device ID refused')
    expected='PRIOR_SWD_414_NO_DBGID' if dev==0 else 'RUNTIME_DBGID_414'
    if fields['ID_SOURCE']!=expected: raise ValueError('Wrong identity evidence tag')
    if (cpu&0xFF0FFFF0)!=0x410FC230: raise ValueError('Unexpected CPU (requires Cortex-M3)')
    if fields['PCB_REV']!='5.3_PRIOR_PHOTO' or fields['HW']!='05_PRIOR_MENU':
        raise ValueError('Not the prequalified HW05 profile')
    if fields['FLASH_KIB']!='512_PRIOR_SWD': raise ValueError('Wrong stored profile label')
    if int(fields['VTOR'],16)!=0x08008000: raise ValueError('Wrong application vector base')
    obr=int(fields['OBR'],16);wrpr=int(fields['WRPR'],16)
    if not (0<=obr<=0xffffffff and 0<=wrpr<=0xffffffff): raise ValueError('Invalid register range')
    if obr&1: raise ValueError('Option-byte load error: do not change option bytes')
    if fields['DEBUG_ACTIVE']!='0': raise ValueError('Active debugger: dump refused')
    if fields['PROFILE_OK']!='1' or fields['RDP_UNCHANGED']!='1': raise ValueError('Device refused profile')
    if fields['SCOPE']!='FULL_AUDIT_055': raise ValueError('Wrong read scope')
    return fields

def select_port():
    paths=sorted(set(glob.glob('/dev/cu.usbmodem*')+glob.glob('/dev/cu.usbserial*')))
    if len(paths)!=1: raise ValueError('Podaj --port. Widoczne porty: '+', '.join(paths))
    return paths[0]

def wait_banner(link, seconds):
    """Observe fresh startup, or actively probe an already running silent .055.
    Only PING may be sent before version confirmation. No DUMP is sent here.
    START never authorizes a command until its final READY; a silent session
    can be checked without depending on a periodic DWT-based ALIVE message.
    """
    print('AUTOSIZE: stale 250000 8N1; zakres Flash bedzie wybrany dopiero po dwoch zgodnych odczytach SIZE.',flush=True)
    print('Jesli drukarka jest wylaczona, wlacz ja TERAZ BEZ KARTY SD. Nie wgrywaj firmware.',flush=True)
    start=time.monotonic();end=start+seconds
    next_probe=start+1.0;next_progress=start+5.0
    pending=False;pong=False;recoverable=False
    probe_deadline=0.0;attempts=0;banner=None;starting=False
    max_attempts=3
    first_line=True
    while time.monotonic()<end:
        now=time.monotonic()
        if now>=next_progress:
            print('SYNC: %.0f s | odebrano %d B | proby PING %d/%d | nadal przed zrzutem.' %
                  (now-start,link.rx_bytes,attempts,max_attempts),flush=True)
            next_progress=now+5.0
        try:
            line=link.line(min(end,time.monotonic()+0.1))
        except TimeoutError:
            now=time.monotonic()
            if link.buffer and now-link.last_rx>=2.0:
                raise TimeoutError('Odebrano niepelna linie UART bez konca: '+repr(bytes(link.buffer[:100])) )
            if pending and now>=probe_deadline:
                if pong:
                    raise TimeoutError('Odebrano PONG 0.5.5, ale brak koncowego READY. Nie wyslano INFO ani DUMP.')
                if recoverable:
                    raise TimeoutError('Odrzucona komenda bez koncowego READY. Nie ponawiam transmisji w ciemno.')
                pending=False
                next_probe=now+0.3
                print('SYNC: brak odpowiedzi na PING %d/%d; jeszcze nie wyslano DUMP.' % (attempts,max_attempts),flush=True)
                if attempts>=max_attempts:
                    print('SYNC: trzy PING bez odpowiedzi. Pozostaje nasluch do limitu; wlacz ponownie drukarke BEZ KARTY. Nie zmieniaj firmware.',flush=True)
            if (not pending and not starting and attempts<max_attempts and
                now>=next_probe and now-link.last_rx>=0.20 and not link.buffer):
                attempts+=1;link.initial_probe_attempts=attempts
                print('SYNC: wysylam tylko PING %d/%d do juz dzialajacej aplikacji.' % (attempts,max_attempts),flush=True)
                link.probe_ping()
                pending=True;pong=False;recoverable=False
                probe_deadline=time.monotonic()+2.0
            continue
        # Opening a stream may begin in the middle of one READY line.
        # Discard ONLY one exact proper suffix at the first complete line,
        # before any command is sent. This never authorizes a dump or INFO.
        # Raw bytes remain in UART_RX.raw and the line stays in UART.log.
        was_first=first_line;first_line=False
        if was_first and attempts==0 and line in (b'EADY',b'ADY',b'DY',b'Y'):
            link.initial_tail_skipped=True
            if link.log:
                link.log.write('INITIAL_READY_TAIL '+repr(line)+'; fresh PING+READY still required\n');link.log.flush()
            print('SYNC: koncowka pierwszej linii '+repr(line)+'; czekam na pelna gotowosc lub odpowiedz na PING.',flush=True)
            continue
        check_version(line)
        if line == b'M300RDP/0.5.5 FULL_AUDIT HW05 START':
            banner=line.decode('ascii');starting=True
            print('UART:',banner,flush=True)
            continue
        if line.startswith((b'BEGIN ',b'D ',b'END ')):
            raise RuntimeError('Odebrano trwajacy zrzut z poprzedniej sesji; nie wysylam kolejnych polecen. Zachowaj log.')
        if line == b'M300RDP/0.5.5 ALIVE READY':
            if not pending:
                link.ready=True
                print('GOTOWOSC 0.5.5: ALIVE READY',flush=True)
                return line.decode('ascii')
            continue
        if line.startswith(b'PONG '):
            if line != b'PONG 0.5.5':
                raise RuntimeError('Inna wersja odpowiedziala: '+line.decode('ascii',errors='replace')+'. Nie wyslano DUMP.')
            if not pending:
                print('SYNC: spozniony PONG; czekam na READY i wykonam nowe uzgodnienie.',flush=True)
                continue
            if pong or recoverable:
                raise RuntimeError('Niejednoznaczna odpowiedz na PING; nie wyslano DUMP.')
            pong=True
            continue
        if line in (b'ERR COMMAND_DISCARDED',b'ERR UNKNOWN_COMMAND (send HELP)'):
            if pong:
                raise RuntimeError('ERR po PONG, odpowiedz niejednoznaczna; nie wyslano DUMP.')
            recoverable=True
            print('SYNC: '+line.decode('ascii')+'; czekam na READY przed kolejnym PING.',flush=True)
            continue
        if line.startswith(b'ERR '):
            raise RuntimeError(line.decode('ascii',errors='replace'))
        if line.startswith(b'INFO '):
            # Unsolicited startup INFO is logged, not used to authorize a dump.
            print('UART: odebrano INFO; czekam na koncowe READY.',flush=True)
            continue
        if line==b'READY':
            link.ready=True;starting=False
            if pending and pong and not recoverable:
                link.ping_verified=True
                print('SYNC: PONG 0.5.5 + READY. Aplikacja odpowiada.',flush=True)
                return 'M300RDP/0.5.5 VERIFIED_BY_PING_READY'
            if recoverable:
                link.sync_recoveries+=1;recoverable=False
            # New START/READY or a complete discarded command: normal control
            # exchange now sends a fresh PING and requires the exact .055 reply.
            print('GOTOWOSC: READY; sprawdzam wersje przez PING, potem INFO.',flush=True)
            return banner or 'READY_WITH_VERSION_CHECK_PENDING'
        raise RuntimeError('Nieoczekiwana linia przed uzgodnieniem: '+repr(line[:160])+'. Nie wyslano DUMP.')
    raise TimeoutError('Koniec oczekiwania: odebrano %d B, brak potwierdzonej gotowosci 0.5.5. Nie wyslano DUMP.' % link.rx_bytes)


def control_exchange(link, command, seconds):
    """One bounded PING/INFO transaction at a time; wait for its final READY.
    Only a complete COMMAND_DISCARDED / UNKNOWN_COMMAND response may be retried.
    No DUMP is retried, and no timeout/corrupt transfer is converted to PASS.
    """
    if command not in ('PING','INFO'):
        raise ValueError('Retries are allowed only for PING/INFO')
    deadline=time.monotonic()+seconds
    for attempt in range(1,MAX_CONTROL_ATTEMPTS+1):
        if time.monotonic()>=deadline:
            break
        link.send(command)
        result=None
        recoverable_error=None
        while True:
            line=link.line(deadline)
            check_version(line)
            if line==b'READY':
                link.ready=True
                if recoverable_error is not None:
                    break
                if result is None:
                    raise RuntimeError('READY bez odpowiedzi na '+command)
                return result
            if line==b'M300RDP/0.5.5 ALIVE READY':
                continue
            if line in (b'ERR COMMAND_DISCARDED',b'ERR UNKNOWN_COMMAND (send HELP)'):
                if result is not None or recoverable_error is not None:
                    raise RuntimeError('Niejednoznaczna odpowiedz kontrolna')
                recoverable_error=line
                continue  # MUST consume final READY before any retry
            if line.startswith(b'ERR '):
                raise RuntimeError(line.decode('ascii',errors='replace'))
            if (command=='PING' and line==b'PONG 0.5.5') or (command=='INFO' and line.startswith(b'INFO ')):
                if result is not None or recoverable_error is not None:
                    raise RuntimeError('Zdublowana lub niejednoznaczna odpowiedz na '+command)
                result=line
                continue
            raise RuntimeError('Nieoczekiwana odpowiedz na '+command+': '+repr(line[:160]))
        link.sync_recoveries+=1
        if link.log:
            link.log.write('SYNC_RETRY '+command+' '+str(attempt)+' '+repr(recoverable_error)+'\n');link.log.flush()
        action=('ponawiam tylko '+command) if attempt<MAX_CONTROL_ATTEMPTS else 'limit ponowien osiagniety'
        print('SYNC: '+recoverable_error.decode('ascii')+'; odebrano READY; '+action+' ('+str(attempt)+'/'+str(MAX_CONTROL_ATTEMPTS)+').',flush=True)
    raise RuntimeError('Nie udalo sie zsynchronizowac '+command+'; nie rozpoczęto kolejnego odczytu. Zachowaj UART.log.')


def verify_ping(link, seconds=12):
    if not link.ready:
        raise RuntimeError('Handshake requires READY/ALIVE first')
    if not link.ping_verified:
        control_exchange(link,'PING',seconds)
    link.ping_verified = False
    print('PONG 0.5.5 — komunikacja dwukierunkowa OK',flush=True)
    print('KONTROLA: odczytuje INFO; czekam na pelna odpowiedz i READY.',flush=True)
    line=control_exchange(link,'INFO',seconds)
    text=line.decode('ascii');fields=validate_device_info(text)
    print('UART:',text,flush=True)
    if int(fields['MCU'],16)==0:
        print('MCU=0: uzyto jawnie wczesniejszej identyfikacji SWD 0x414; nie jest to nowy pomiar ID.',flush=True)
    return text,fields

def capture_one(link, kind, dst: Path):
    address,count,chunk=PROTOCOL[kind]
    if dst.exists(): raise FileExistsError('Nie nadpisuje '+str(dst))
    link.send('DUMP '+kind)
    end=time.monotonic()+15
    while True:
        line=link.line(end)
        if line.startswith(b'BEGIN '): break
        if line.startswith(b'ERR '): raise RuntimeError('Urzadzenie odrzucilo zrzut: '+line.decode())
        if line==b'READY' or line.startswith(b'M300RDP/0.5.5 '): continue
        raise ValueError('Unexpected data before BEGIN: '+repr(line[:120]))
    parse_begin(line,kind)
    sha=hashlib.sha256();part=dst.with_suffix(dst.suffix+'.partial')
    with part.open('xb') as f:
        for seq in range((count+chunk-1)//chunk):
            expected=min(chunk,count-seq*chunk)
            data=parse_frame(link.line(time.monotonic()+15),seq,expected)
            sha.update(data);f.write(data)
            if (seq+1)%256==0 or min((seq+1)*chunk,count)==count:
                print(f'{dst.name}: {min((seq+1)*chunk,count)}/{count} B, CRC OK',flush=True)
        f.flush();os.fsync(f.fileno())
    parse_end(link.line(time.monotonic()+20),kind,sha.hexdigest())
    consume_ready(link,time.monotonic()+5)  # END is not the command-ready boundary
    if part.stat().st_size!=count: raise ValueError('Wrong file size')
    # link() refuses overwriting an existing file; both names are in one new directory.
    os.link(str(part),str(dst));part.unlink()
    print('PASS',dst.name,sha.hexdigest(),flush=True)
    return {'name':dst.name,'address':f'0x{address:08X}','bytes':count,'sha256':sha.hexdigest(),
            'frame_crc32':'PASS','mcu_sha256':'PASS'}

def save_manifest(out, report):
    # Local metadata only; no call goes to the MCU.
    tmp=out/'MANIFEST.json.tmp'
    with tmp.open('w',encoding='utf-8') as f:
        json.dump(report,f,indent=2,ensure_ascii=False);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(str(tmp),str(out/'MANIFEST.json'))

REG_NAMES = ["CPUID", "DBGMCU_IDCODE", "VTOR", "DHCSR", "FLASH_OBR", "FLASH_WRPR",
             "FLASH_ACR", "FLASH_SR", "FLASH_CR", "RCC_CR", "RCC_CFGR", "RCC_CSR",
             "RCC_AHBENR", "RCC_APB2ENR", "RCC_APB1ENR", "AFIO_MAPR"]

def sha256(b): return hashlib.sha256(b).hexdigest()

def decode_regs(b):
    if len(b)!=128 or b[:8]!=b"M3AUD055": raise ValueError("Invalid REGS signature")
    return {name: int.from_bytes(b[8+4*i:12+4*i], "little") for i,name in enumerate(REG_NAMES)}

def decode_options(raw,regs):
    if len(raw)!=16: raise ValueError("OPTIONS length")
    labels=['RDP','USER','DATA0','DATA1','WRP0','WRP1','WRP2','WRP3']
    pairs=[]
    for i,k in enumerate(labels):
        v,n=raw[i*2:i*2+2]
        state='ERASED_FF_FF' if v==n==255 else ('COMPLEMENT_OK' if v^n==255 else 'INVALID_COMPLEMENT')
        pairs.append({'name':k,'value':v,'complement':n,'state':state})
    if any(x['state']=='INVALID_COMPLEMENT' for x in pairs):
        raise ValueError('Invalid option/complement pair; preserve raw files, no option programming')
    protected=not(raw[0]==0xA5 and raw[1]==0x5A)
    wrp=sum(raw[8+i*2]<<(8*i) for i in range(4))
    if protected != bool(regs['FLASH_OBR']&2) or wrp!=regs['FLASH_WRPR']:
        raise ValueError('Raw options disagree with loaded OBR/WRPR')
    for i,shift in [(2,2),(4,10),(6,18)]:
        if raw[i] != ((regs['FLASH_OBR']>>shift)&255):
            raise ValueError('USER/DATA raw options disagree with OBR')
    return {'raw_hex':raw.hex(),'pairs':pairs,'rdp_active':protected,
            'wrp_word':f'0x{wrp:08X}', 'shadow_match':True,
            'restore_warning':'Evidence only. NEVER replay option bytes blindly; RDP regression erases main Flash.'}

def select_flash_kind(size_kib):
    """No probing above advertised memory. .055 supports these two exact ranges."""
    if size_kib == 256: return 'FLASH256'
    if size_kib == 512: raise ValueError('This release is qualified for 256 KiB only; small copies preserved. No upper-half read.')
    raise ValueError('Niepotwierdzona lub nieobslugiwana pojemnosc Flash: '+str(size_kib)+
                     ' KiB. Nie wysylam zadania pelnego odczytu.')


def audit_captured(out: Path,report: dict):
    """Strict offline content validation; also used by the fake-UART regression tests."""
    def data(n): return (out/n).read_bytes()
    size_a=data('SIZE_A.bin');size_b=data('SIZE_B.bin')
    if len(size_a)!=2 or size_a!=size_b: raise ValueError('Invalid or inconsistent SIZE pair')
    size_kib=int.from_bytes(size_a,'little');flash_kind=select_flash_kind(size_kib)
    flash_bytes=size_kib*1024
    for kind in ['BOOT','DATA','SIZE','OPTIONS','UID','SYSROM','BKP',flash_kind]:
        suffix='_POST_UPDATE' if kind==flash_kind else ''
        a=data(kind+suffix+'_A.bin');b=data(kind+suffix+'_B.bin')
        if len(a)!=PROTOCOL[kind][1] or a!=b: raise ValueError('Two reads disagree: '+kind)
    boot=data('BOOT_A.bin');nv=data('DATA_A.bin');flash=data(flash_kind+'_POST_UPDATE_A.bin')
    if flash[:32768]!=boot or flash[0x3e000:0x40000]!=nv: raise ValueError(flash_kind+' disagrees with BOOT/DATA')
    if len(flash)!=flash_bytes: raise ValueError('Full image length disagrees with measured SIZE')
    rom=data('SYSROM_A.bin');uid=data('UID_A.bin')
    if rom[0x7e0:0x7e2]!=data('SIZE_A.bin') or rom[0x7e8:0x7f4]!=uid:
        raise ValueError('SYSROM signature bytes disagree with separate SIZE/UID')
    if uid==bytes(12) or uid==b'\xff'*12: raise ValueError('Uniform UID: preserve reads but do not certify identity')
    regs_a=decode_regs(data('REGS_BEFORE.bin'));regs_b=decode_regs(data('REGS_AFTER.bin'))
    for key in ['FLASH_OBR','FLASH_WRPR','CPUID','VTOR']:
        if regs_a[key]!=regs_b[key]: raise ValueError('Registers changed during audit: '+key)
    if regs_b['DHCSR']&1 or regs_b['FLASH_OBR']&1: raise ValueError('Debug active or option load error at end')
    options=decode_options(data('OPTIONS_A.bin'),regs_b)
    info=report.get('info_fields',{})
    if info and (int(info['OBR'],16)!=regs_a['FLASH_OBR'] or int(info['WRPR'],16)!=regs_a['FLASH_WRPR']):
        raise ValueError('INFO/REGS protection mismatch')
    msp,reset=struct.unpack_from('<II',boot)
    if not(0x20000000<msp<=0x20010000 and msp%8==0 and reset&1 and 0x08000000<=(reset&~1)<0x08008000):
        raise ValueError('Implausible OEM boot vector')
    appbase=0x8000
    magic,n=struct.unpack_from('<II',flash,appbase+0x1c)
    if magic!=0x12345678 or n!=audit_reference.APP_BYTES: raise ValueError('Service application metadata mismatch')
    app=flash[appbase:appbase+n]
    if sha256(app)!=audit_reference.APP_SHA256: raise ValueError('Installed .055 differs from released bytes')
    mac=flash[appbase+n:appbase+n+20]
    # No OEM crypto key in this public tool. Pin the entire released diagnostic payload instead.
    if sha256(flash[appbase:appbase+audit_reference.PAYLOAD_BYTES]) != audit_reference.PAYLOAD_SHA256:
        raise ValueError('Installed .055 payload differs from the pinned release')
    payload_end=appbase+((n+20+63)//64)*64
    if flash[appbase+n+20:payload_end]!=b'\xcd'*(payload_end-appbase-n-20): raise ValueError('Wrong application padding')
    # Identify all differences outside the three application pages rather than assume upper Flash is empty.
    page_rows=[];unexpected=[]
    for i in range(flash_bytes//2048):
        block=flash[2048*i:2048*(i+1)];h=sha256(block)
        baseline=audit_reference.PRIOR_PAGE_SHA256.get(str(i))
        excluded=i in audit_reference.APP_UPDATE_PAGES
        row={'page':i,'start':f'0x{0x08000000+i*2048:08X}', 'bytes':2048,
             'sha256':h,'all_ff':block==b'\xff'*2048,
             'prior_054_sha256':baseline or '',
             'expected_application_change':excluded,
             'prior_equal':(h==baseline) if baseline else ''}
        page_rows.append(row)
        if baseline and h!=baseline and not excluded: unexpected.append(i)
    with (out/'FLASH_PAGE_SHA256.csv').open('x',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(page_rows[0]));w.writeheader();w.writerows(page_rows)
    report['unexpected_changed_pages_vs_054']=unexpected
    if unexpected: raise ValueError('Changed pages outside .055 update: '+str(unexpected))
    extracted={'NVM_A.bin':(0x3e800,2048),'NVM_B.bin':(0x3f000,2048),
               'FACTORY.bin':(0x3f800,2048),'RESERVED_3E000.bin':(0x3e000,2048),
               'LOWER256_POST_UPDATE.bin':(0,262144)}
    if size_kib==512: extracted['UPPER256.bin']=(0x40000,262144)
    report['derived_files']=[]
    for name,(off,length) in extracted.items():
        value=flash[off:off+length]
        if len(value)!=length: raise ValueError('Derived slice out of range: '+name)
        with (out/name).open('xb') as f:f.write(value)
        report['derived_files'].append({'name':name,'address':hex(0x08000000+off),'bytes':length,
                                       'sha256':sha256(value),'source':'derived slice of '+flash_kind+'_POST_UPDATE_A.bin, not a third read'})
    details={'size_kib_internal':size_kib,'flash_bytes':flash_bytes,
             'flash_end_inclusive':hex(0x08000000+flash_bytes-1),
             'size_source':'two matching 16-bit SIZE reads at 0x1FFFF7E0; cross-checked in SYSROM',
             'prior_swd_report_kib':512,
             'prior_swd_size_matches_measured':size_kib==512,
             'firmware_info_size_label':'512_PRIOR_SWD is a historical string, NOT a new measurement','uid_hex_address_order':uid.hex(),
             'option_bytes':options,'registers_before':regs_a,'registers_after':regs_b,
             'bkp_dr1_to_dr42':list(struct.unpack('<42H',data('BKP_A.bin'))),
             'bkp_note':'Two reads of battery-backed data registers in service runtime, not the previous stock session.',
             'boot_sha256':sha256(boot),'data_sha256':sha256(nv),'flash_sha256':sha256(flash),'full_flash_file':flash_kind+'_POST_UPDATE_A.bin',
             'boot_msp':hex(msp),'boot_reset':hex(reset),'application_sha256':sha256(app),
             'application_tail20':mac.hex(),'previous_054_protected_regions_unchanged':None,
             'upper_half_read':size_kib==512,
             'upper_half_all_ff':(flash[262144:]==b'\xff'*262144) if size_kib==512 else None,
             'upper_half_sha256':sha256(flash[262144:]) if size_kib==512 else None,'restoration_tested':False}
    with (out/'AUDIT_DETAILS.json').open('x',encoding='utf-8') as f:json.dump(details,f,ensure_ascii=False,indent=2);f.write('\n')
    report['audit']=details
    report['status']=f'PASS_FULL_AUDIT_{size_kib}K_X2'
    report['restoration_tested']=False
    lines=['# M300 HW05 — archiwum pamięci 0.5.5', '',
           '**Wynik: '+report['status']+'**', '',
           f'Dwa niezależne odczyty {flash_bytes} B są identyczne. CRC32 każdej ramki oraz SHA-256 całości są zgodne.',
           'BOOT i DATA mają zgodne kopie A/B i pokrywają się z pełną Flash. Brak prywatnego wzorca sprzed instalacji; nie stwierdzamy niezmienności względem niego.',
           'UID, SIZE i raw Option Bytes oraz SYSROM odczytano dwa razy; sprawdzono nakładające się obszary.',
           'Opcje porównano z OBR/WRPR; nie dokonano ich zapisu.', '',
           '## To nie jest fabryczny obraz sprzed aktualizacji',
           'W slocie aplikacji jest diagnostyka 0.5.5. Archiwum zachowuje stan PO jej zainstalowaniu.',
           'Oryginalny Update.bin 1.3.1 i stare backupy trzeba zachować osobno. Nie nadpisuj ich.',
           'To nie jest dowód odtworzenia sprzętu ani gotowy wsad nowego bootloadera.', '',
           '## Identyfikacja / integralność',
           f'- Pojemność odczytana wewnętrznie: {size_kib} KiB.',
           f'- UID (bajty w kolejności adresowej): `{uid.hex()}`.',
           f'- {flash_kind} SHA-256: `{sha256(flash)}`.',
           f'- BOOT SHA-256: `{sha256(boot)}`.',f'- DATA SHA-256: `{sha256(nv)}`.',
           '', '## Granice audytu',
           'Objęto główną Flash, udokumentowany obszar systemowy ST, UID, rozmiar, 16 B opcji, 42 rejestry BKP i wybrane rejestry diagnostyczne.',
           'Nie wykonywano testu grzałek/silników/czujników, nie odkrywano zewnętrznych pamięci, nie wykonywano kopii RAM starego programu.',
           'SYSROM i UID są źródłami identyfikacji, nie plikami do programowania; OPTIONS nie wolno wgrywać automatycznie.',
           '', '## Pliki pochodne',
           'NVM_A/B, FACTORY, RESERVED_3E000, LOWER256 są wycięte z pełnego odczytu A, nie odczytane trzeci raz. UPPER256 istnieje tylko przy SIZE=512.',
           'Dwie kopie na jednym dysku nie zastępują kopii na innym nośniku. Dane są prywatne.', '']
    (out/'RAPORT_PL.md').write_text('\n'.join(lines),encoding='utf-8')

def write_archive(out: Path):
    hashes=[]
    for f in sorted(out.iterdir()):
        if f.is_file() and f.name!='SHA256SUMS.txt': hashes.append(sha256(f.read_bytes())+'  '+f.name)
    (out/'SHA256SUMS.txt').write_text('\n'.join(hashes)+'\n',encoding='utf-8')
    dest=out.parent/(out.name+'.zip')
    with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(out.iterdir()):
            if f.is_file():z.write(f,out.name+'/'+f.name)
    with zipfile.ZipFile(dest) as z:
        if z.testzip() is not None:raise ValueError('Local ZIP CRC check failed')
    print('ARCHIWUM DO ZACHOWANIA:',dest,flush=True)
    return dest

def backup(link, out, report):
    def capture(kind,name):
        report['captures'].append(capture_one(link,kind,out/name));save_manifest(out,report)
    capture('REGS','REGS_BEFORE.bin')
    for kind in ['BOOT','DATA','OPTIONS','UID','SIZE']:
        for label in ['A','B']:capture(kind,kind+'_'+label+'.bin')
        if (out/(kind+'_A.bin')).read_bytes()!=(out/(kind+'_B.bin')).read_bytes():raise ValueError('Read pair mismatch: '+kind)
    size=int.from_bytes((out/'SIZE_A.bin').read_bytes(),'little')
    report['flash_size_kib_measured']=size;save_manifest(out,report)
    flash_kind=select_flash_kind(size)
    link.flash_size_kib=size
    report['flash_kind_selected']=flash_kind
    report['flash_scope_bytes']=size*1024
    report['prior_swd_size_report_kib']=512
    report['prior_swd_size_report_matches']=size==512
    save_manifest(out,report)
    print(f'POTWIERDZONO WEWNETRZNIE: {size} KiB. Dwa pelne odczyty przez DUMP {flash_kind}.',flush=True)
    if size==256:
        print('INFO 512_PRIOR_SWD to stara etykieta. Pelna glowna Flash tego egzemplarza: 0x08000000-0x0803FFFF.',flush=True)
    for kind in [flash_kind,'SYSROM','BKP']:
        for label in ['A','B']:
            capture(kind,kind+('_POST_UPDATE' if kind==flash_kind else '')+'_'+label+'.bin')
    capture('REGS','REGS_AFTER.bin')
    audit_captured(out,report);save_manifest(out,report)
    print('\n'+report['status'],flush=True)
    print('KATALOG KOPII:',out,flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--port');ap.add_argument('--out')
    ap.add_argument('--wait-seconds',type=int,default=90)
    ap.add_argument('--probe-only',action='store_true')
    # Full audit is the default, not a hidden opt-in switch.
    args=ap.parse_args()
    os.umask(0o077)  # New backup/ZIP contains private device identity and factory records.
    if not 5<=args.wait_seconds<=600: ap.error('--wait-seconds must be 5..600')
    try: import serial
    except ImportError:
        print('Brak pyserial. Zainstaluj: python3 -m pip install --user pyserial',file=sys.stderr);return 2
    stamp=dt.datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:6]
    out=Path(args.out).expanduser().resolve() if args.out else Path.home()/'Desktop'/('M300_AUDYT_055_PUBLIC_'+stamp)
    report={'purpose':'M300 HW05 read-only backup; no approval to install a device-locked release','status':'IN_PROGRESS','host_version':VERSION,
            'firmware_version':FIRMWARE_VERSION,'host_only_update':True,
            'serial_configuration_policy':'Fixed READ_TIMEOUT=0.02 before open; port settings locked after open',
            'sync_policy':'bounded PING during initial silence; exact PONG 0.5.5 + READY and INFO required before DUMP; no dump retries',
            'captures':[],'started':dt.datetime.now(dt.timezone.utc).isoformat(),
            'factory_dump_full_original':False,'service_app_replaced_stock':True,
            'full_flash_requested':True,'size_policy':'two agreeing SIZE reads; this public release allows 256 KiB only','no_mcu_flash_write_commands':True}
    ser=None;created=False
    try:
        port=args.port or select_port()
        out.mkdir(parents=False,exist_ok=False,mode=0o700);created=True
        report['port']=port;save_manifest(out,report)
        with (out/'UART.log').open('x',encoding='utf-8') as log, (out/'UART_RX.raw').open('xb') as raw_log:
            serial_type = serial_class_with_configuration_lock(serial.Serial)
            ser=serial_type(port=None,baudrate=250000,bytesize=8,parity='N',stopbits=1,
                              timeout=READ_TIMEOUT,write_timeout=3,xonxoff=False,rtscts=False,dsrdtr=False,
                              exclusive=True)
            ser.dtr=False;ser.rts=False;ser.port=port;ser.open()
            print('PORT OTWARTY:',port,'| 250000 8N1 | RDP/WRP bez zmian',flush=True)
            print('KATALOG:',out,flush=True)
            link=Link(ser,log,raw_log)
            report['serial_reconfigurations_at_open']=ser.reconfiguration_count
            report['pyserial_version']=getattr(serial,'VERSION','unknown')
            log.write('HOST '+VERSION+' | pySerial '+report['pyserial_version']+' | fixed timeout='+str(READ_TIMEOUT)+' | initial_reconfigurations='+str(ser.reconfiguration_count)+'\n');log.flush()
            report['banner']=wait_banner(link,args.wait_seconds)
            info,fields=verify_ping(link)
            report['device_info']=info;report['info_fields']=fields;report['sync_recoveries']=link.sync_recoveries;report['initial_probe_attempts']=link.initial_probe_attempts;report['serial_reconfigurations']=ser.reconfiguration_count;save_manifest(out,report)
            if args.probe_only:
                report['status']='PASS_UART_PROBE_055_NO_DUMP';save_manifest(out,report)
                print(report['status']);return 0
            backup(link,out,report)
            report['serial_reconfigurations']=ser.reconfiguration_count
            report['blocked_reconfigurations']=ser.blocked_reconfigurations
            report['rx_bytes']=link.rx_bytes
            report['initial_ready_tail_skipped']=link.initial_tail_skipped
            save_manifest(out,report)
        write_archive(out)
        return 0
    except KeyboardInterrupt:
        report['status']='INTERRUPTED';report['error']='Ctrl+C'
        if created and (out/'MANIFEST.json').exists(): save_manifest(out,report)
        print('\nPrzerwano. Nie wylaczono RDP i nie zapisano Flash. Pliki niepelne maja .partial.');return 130
    except (OSError,ValueError,RuntimeError,TimeoutError) as e:
        report['status']='FAIL';report['error']=str(e)
        report['next_step']='Preserve UART.log. Firmware 0.5.5 stays installed; no automatic reflash or RDP/WRP change.'
        # Do not modify pre-existing output directories on a mkdir failure.
        if created:
            try: save_manifest(out,report)
            except OSError: pass
        if created and ser is not None:
            report['serial_reconfigurations']=getattr(ser,'reconfiguration_count',None)
            report['blocked_reconfigurations']=getattr(ser,'blocked_reconfigurations',None)
            try: save_manifest(out,report)
            except OSError: pass
        print('FAIL:',e,file=sys.stderr)
        print('Zachowaj log. Nie zmieniaj RDP/WRP ani nie uruchamiaj masowego kasowania.',file=sys.stderr)
        return 2
    finally:
        if ser is not None: ser.close()

if __name__=='__main__': raise SystemExit(main())
