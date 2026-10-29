#!/usr/bin/env python3
"""M300Boot v1.1 host: fixed port configuration, paced read-only commands.
No RDP/WRP change, no flash/program/BOOT/REBOOT command. Python3.9 + pyserial.
"""
from __future__ import annotations
import argparse,datetime,glob,hashlib,json,os,re,sys,time,uuid,zipfile,zlib
from pathlib import Path
REGIONS={'FLASH':262144,'BOOT':32768,'NVM':8192,'FACTORY':2048,'SYSROM':2048,'SIZE':2,'UID':12,'OPTIONS':16}
RATES=(19200,57600,115200,250000,500000)
class Link:
 def __init__(self,port,baud,folder):
  try: import serial
  except ImportError: raise RuntimeError('Brak pyserial: python3 -m pip install pyserial')
  self.s=serial.Serial(port=None,baudrate=baud,timeout=0.02,write_timeout=5,bytesize=8,parity='N',stopbits=1,xonxoff=False,rtscts=False,dsrdtr=False)
  self.s.dtr=False;self.s.rts=False;self.s.port=port
  self.buf=bytearray();self.rx=(folder/'UART_RX.raw').open('xb');self.log=(folder/'UART.log').open('x');self.baud=baud
  self.s.open();self.log.write('PORT '+port+' BAUD '+str(baud)+' 8N1\n');self.log.flush()
 def close(self):self.s.close();self.rx.close();self.log.close()
 def line(self,seconds=5):
  end=time.monotonic()+seconds
  while time.monotonic()<end:
   if b'\n'in self.buf:
    i=self.buf.index(10);b=bytes(self.buf[:i+1]);del self.buf[:i+1];self.log.write('RX '+repr(b)+'\n');self.log.flush();return b.rstrip(b'\r\n').removeprefix(b'M300> ').strip()
   b=self.s.read(1 if not self.s.in_waiting else min(self.s.in_waiting,4096))
   if b:self.buf.extend(b);self.rx.write(b);self.rx.flush()
   if len(self.buf)>8192:raise RuntimeError('Przepelnienie bufora linii UART; dane zapisane w UART_RX.raw')
  return None
 def send(self,text):
  self.log.write('TX '+repr(text)+'\n');self.log.flush()
  for x in (text+'\n').encode('ascii'):self.s.write(bytes([x]));time.sleep(.008)
  self.s.flush()
 def response(self,seconds=10,required=None):
  out=[];matched=required is None;end=time.monotonic()+seconds
  while time.monotonic()<end:
   line=self.line(min(1,max(.01,end-time.monotonic())))
   if line is None:continue
   if line.startswith(b'ERROR '):raise RuntimeError(line.decode(errors='replace'))
   if required is not None and line.startswith(required):matched=True
   if line==b'READY':
    if matched:return out
    continue
   out.append(line)
  raise TimeoutError('Brak koncowego READY; zachowano surowe dane')
 def handshake(self,wait=45):
  end=time.monotonic()+wait;attempt=0
  # Initially allow boot/renderer to finish. Do not reconfigure port during RX.
  ready=False
  while time.monotonic()<end:
   line=self.line(1)
   if line:print('UART:',line.decode(errors='replace'),flush=True)
   if line==b'READY':ready=True;break
   if line is None and attempt<3:
    self.send('');attempt+=1
  if not ready:raise TimeoutError('Brak READY M300Boot. Nie wgrywaj nic ponownie; zachowaj log.')
  self.send('ECHO OFF');r=self.response(required=b'DONE ECHO_OFF')
  if b'DONE ECHO_OFF'not in r:raise RuntimeError('Brak potwierdzenia ECHO OFF')
  self.send('INFO');r=self.response(required=b'M300BOOT v1.1');info=b'\n'.join(r)
  for line in r:print('UART:',line.decode(errors='replace'))
  if b'M300BOOT v1.1'not in info or b'BOARD_CHECK OK'not in info:raise RuntimeError('Niepotwierdzony M300Boot v1.1 / hardware')
  self.send('PING');p=self.response(required=b'PONG ')
  if not any(x.startswith(b'PONG ')for x in p):raise RuntimeError('Brak PONG')
  return info.decode('ascii','replace')
 def dump(self,region,output):
  if output.exists():raise FileExistsError(output)
  length=REGIONS[region];self.send('DUMP '+region);deadline=time.monotonic()+max(30,length*30/self.baud+30);data=bytearray();started=False;digest=None;done=False
  while time.monotonic()<deadline:
   line=self.line(2)
   if line is None:continue
   if line.startswith(b'ERROR '):raise RuntimeError(line.decode(errors='replace'))
   if not started:
    if line.startswith(b'BEGIN_DUMP '):
     parts=line.split()
     if parts!=[b'BEGIN_DUMP',region.encode(),str(length).encode()]:raise ValueError('Wrong region/length')
     started=True
    continue
   if line.startswith(b'DATA '):
    p=line.split()
    if len(p)!=4 or not re.fullmatch(b'[0-9a-fA-F]+',p[3]) or len(p[3])%2:raise ValueError('Invalid DATA')
    block=bytes.fromhex(p[3].decode());off=int(p[1],16);crc=int(p[2],16)
    if not 1<=len(block)<=128 or off!=len(data) or off+len(block)>length:raise ValueError('DATA order/range')
    if zlib.crc32(block)&0xffffffff!=crc:raise ValueError('CRC mismatch')
    data.extend(block)
   elif line.startswith(b'END_DUMP SHA256 '):
    digest=line.split()[-1].decode()
    if len(data)!=length or hashlib.sha256(data).hexdigest()!=digest:raise ValueError('Final hash/length mismatch')
   elif line==b'DONE OK':done=True
   elif line==b'READY':
    if not done or not digest:raise ValueError('Premature READY')
    with output.open('xb')as f:f.write(data)
    print('PASS',output.name,len(data),digest,flush=True);return bytes(data)
   elif line:raise ValueError('Unexpected inside DUMP: '+repr(line))
  raise TimeoutError('DUMP timeout')
def choose_port(explicit):
 if explicit:return explicit
 ports=sorted(set(glob.glob('/dev/cu.usbmodem*')+glob.glob('/dev/cu.usbserial*')))
 if len(ports)==1:return ports[0]
 raise ValueError('Podaj --port. Wykryte porty: '+', '.join(ports))
def main(argv=None):
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--port');ap.add_argument('--baud',type=int,choices=RATES,default=250000);ap.add_argument('--dump-all',action='store_true');ap.add_argument('--out',type=Path);a=ap.parse_args(argv)
 stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'_'+uuid.uuid4().hex[:6]
 out=a.out or Path.home()/'Desktop'/('M300Boot_V11_'+stamp);out.mkdir(parents=True,exist_ok=False)
 link=None;result={'status':'STARTED','firmware':'M300Boot v1.1','hardware_flashing':False}
 try:
  port=choose_port(a.port);link=Link(port,a.baud,out);print('PORT OTWARTY:',port,a.baud,'8N1. Pozostan w menu M300Boot v1.1. Konsola tylko odczytuje.',flush=True)
  result['info']=link.handshake();result['status']='PASS_CONSOLE_V11'
  if a.dump_all:
   files={}
   for name in REGIONS:
    blobs=[]
    for label in ('A','B'):
     p=out/(name+'_'+label+'.bin');b=link.dump(name,p);blobs.append(b);files[p.name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    if blobs[0]!=blobs[1]:raise ValueError('A/B differ for '+name)
   flash=(out/'FLASH_A.bin').read_bytes()
   for region,start in [('BOOT',0),('NVM',0x3e000),('FACTORY',0x3f800)]:
    b=(out/(region+'_A.bin')).read_bytes()
    if flash[start:start+len(b)]!=b:raise ValueError('FLASH differs from '+region)
   result.update(status='PASS_V11_BACKUP_X2',files=files)
  print(result['status'],flush=True)
 except KeyboardInterrupt:result.update(status='INTERRUPTED');print('Przerwano bez zapisu MCU.')
 except Exception as e:result.update(status='FAIL',error=str(e));print('FAIL:',e)
 finally:
  if link:link.close()
  (out/'MANIFEST.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
  zp=out.with_suffix('.zip')
  with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED)as z:
   for p in out.iterdir():
    if p.is_file():z.write(p,out.name+'/'+p.name)
  print('LOG/ARCHIWUM:',zp)
 return 0 if result['status'].startswith('PASS')else 2
if __name__=='__main__':sys.exit(main())
