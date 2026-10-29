#!/usr/bin/env python3
"""M300Boot v1.1 (rc3-compatible format): receive read-only UART dumps; verify SD backups/logs.
This program has NO erase, Flash programming, OTP-write or option-write command.
"""
from __future__ import annotations
import argparse, hashlib, json, re, struct, sys, time, zlib
from pathlib import Path
from typing import Callable
REGIONS={'FLASH':262144,'BOOT':32768,'NVM':8192,'FACTORY':2048,'SYSROM':2048,'SIZE':2,'UID':12,'OPTIONS':16}
BAUDRATES=(19200,57600,115200,250000,500000)
EVENTS=['?','RESET','CHECK','INSTALL_BEGIN','INSTALL_END','ERROR','BOOT','BACKUP','DUMP','LOGSAVE','RECOVERY_CLEAR','USER_RESET','SKIPPED']

def crc(data: bytes) -> int:
    return zlib.crc32(data)&0xffffffff

def parse_dump(readline: Callable[[],bytes], region: str, deadline: float=120) -> bytes:
    """Require sequential offset, every chunk CRC and final full SHA-256."""
    expected=REGIONS[region];limit=time.monotonic()+deadline;start=False;out=bytearray()
    while time.monotonic()<limit:
        raw=readline()
        if len(raw)>2048:raise ValueError('Oversized UART frame')
        if not raw:continue
        line=raw.strip()
        if line.startswith(b'M300> '):line=line[6:]
        if line.startswith(b'ERROR '):raise ValueError(line.decode('ascii','replace'))
        if not start:
            if line.startswith(b'BEGIN_DUMP '):
                parts=line.split()
                if len(parts)!=3 or parts[1]!=region.encode() or int(parts[2])!=expected:
                    raise ValueError('Wrong dump region or size')
                start=True
            continue
        if line.startswith(b'DATA '):
            parts=line.split()
            if len(parts)!=4:raise ValueError('Invalid DATA header')
            off=int(parts[1],16);checksum=int(parts[2],16)
            if not re.fullmatch(b'[0-9a-fA-F]+',parts[3]) or len(parts[3])%2:raise ValueError('Invalid hex data')
            chunk=bytes.fromhex(parts[3].decode('ascii'))
            if not 1<=len(chunk)<=128 or off!=len(out) or len(out)+len(chunk)>expected:
                raise ValueError('Missing, duplicated or oversized chunk')
            if crc(chunk)!=checksum:raise ValueError('Chunk CRC mismatch')
            out.extend(chunk)
        elif line.startswith(b'END_DUMP SHA256 '):
            digest=line.split()[-1].decode('ascii')
            if len(out)!=expected or digest!=hashlib.sha256(out).hexdigest():
                raise ValueError('Incomplete dump or final SHA-256 mismatch')
            return bytes(out)
        else:raise ValueError(f'Unexpected output inside dump: {line[:100]!r}')
    raise TimeoutError('No complete dump. Keep the printer in the bootloader service menu.')

def dump_timeout(region: str, baud: int) -> float:
    if baud not in BAUDRATES:raise ValueError('Unsupported UART baud rate')
    # Hex encoding, frame headers and 8N1 wire bits: leave transport margin.
    return max(120.0,REGIONS[region]*3.0*10.0/baud+30.0)

def receive(port: str, region: str, output: Path, baud: int=250000) -> dict:
    # Share the tested fixed-configuration line reader; do not use read_until
    # on pySerial with repeated changes to timeout on macOS.
    from m300_console import Link
    import uuid
    if output.exists(): raise FileExistsError(f'Refusing to overwrite {output}')
    logs=output.parent/(output.name+'.uart_'+uuid.uuid4().hex[:6]);logs.mkdir()
    link=Link(port,baud,logs)
    try:
        link.handshake()
        data=link.dump(region,output)
        return {'region':region,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'output':str(output),'logs':str(logs)}
    finally: link.close()


def verify_backup(flash: bytes, info: bytes) -> dict:
    if len(flash)!=262144 or len(info)!=1024:raise ValueError('Expected 262144 B Flash and 1024 B info')
    if info[:8]!=b'M3BACK01' or struct.unpack_from('<III',info,8)!=(0x10001,262144,0x08000000):
        raise ValueError('Not a completed M3BACK01 backup (possibly blank SD template)')
    if struct.unpack_from('<I',info,1020)[0]!=crc(info[:1020]):raise ValueError('Info CRC mismatch')
    digest=hashlib.sha256(flash).digest()
    if info[32:64]!=digest:raise ValueError('Flash SHA-256 does not match backup metadata')
    return {'verified':True,'flash_bytes':len(flash),'sha256':digest.hex(),
            'mcu_uid':info[20:32].hex(),'flash_size_kib':struct.unpack_from('<H',info,64)[0],'option_bytes_hex':info[592:608].hex(),
            'note':'Snapshot of current Flash, not necessarily the factory bootloader.'}

def decode_log(blob: bytes) -> dict:
    if len(blob)!=4096 or blob[:8]!=b'M3LOG001':raise ValueError('Not a saved M3LOG001 history snapshot')
    if crc(blob[:4092])!=struct.unpack_from('<I',blob,4092)[0]:raise ValueError('Log file CRC mismatch')
    if struct.unpack_from('<I',blob,8)[0]!=432:raise ValueError('Unexpected state version')
    state=blob[512:944]
    if struct.unpack_from('<I',state,0)[0]!=0x3153334D or struct.unpack_from('<I',state,428)[0]!=0x33c0de13:
        raise ValueError('Invalid state markers')
    if crc(state[:424])!=struct.unpack_from('<I',state,424)[0]:raise ValueError('State CRC mismatch')
    fields=struct.unpack_from('<10I',state)
    _,seq,boots,flags,strikes,pending,recovery,head,count,total=fields
    if head>=24 or count>24:raise ValueError('Invalid ring bounds')
    events=[]
    for i in range(count):
        b,ms,k,arg=struct.unpack_from('<4I',state,40+((head+24-count+i)%24)*16)
        events.append({'boot':b,'uptime_ms':ms,'event':EVENTS[k] if k<len(EVENTS) else str(k),'arg_hex':f'{arg:08x}'})
    return dict(uid=blob[16:28].hex(),sequence=seq,boots=boots,reset_flags=f'{flags:08x}',
                watchdog_resets=strikes,recovery=bool(recovery),total_events=total,events=events)

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
    d=sub.add_parser('dump');d.add_argument('--port',required=True);d.add_argument('region',choices=REGIONS);d.add_argument('--out',type=Path,required=True)
    d.add_argument('--baud',type=int,choices=BAUDRATES,default=250000,help='Must match the saved UART selection; hold encoder at boot for recovery at 250000')
    v=sub.add_parser('verify-backup');v.add_argument('flash',type=Path);v.add_argument('info',type=Path)
    l=sub.add_parser('decode-log');l.add_argument('log',type=Path)
    a=p.parse_args()
    try:
        if a.cmd=='dump':result=receive(a.port,a.region,a.out,a.baud)
        elif a.cmd=='verify-backup':result=verify_backup(a.flash.read_bytes(),a.info.read_bytes())
        else:result=decode_log(a.log.read_bytes())
        print(json.dumps(result,indent=2));return 0
    except (OSError,ValueError,RuntimeError,TimeoutError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
