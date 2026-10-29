#!/usr/bin/env python3
"""Offline validation of two M300 backups. No device/network access or writes.
Public build: retains the existing i4 identity gate; never patches an installer.
"""
from __future__ import annotations
import argparse, hashlib, json, struct, sys, zlib
from pathlib import Path
PROFILE = {
 'uid_sha256':'36718d5166f28402a21046cf8f75edd0ce5f0160227e6ac40d7bb097bc2f4a7e',
 'options_sha256':'47cf264caf31417cc5ed042d3a3248b1a523da0736b93138b23e6c938ebf4c6e',
 'factory_sha256':'fc8445c612fcdec3d236ae67451371bf462eceabd23943b1844c9c239b684bb4',
 'prefix_sha256':'710e50741e1aac5e6338c29bb49e06b452d72053ea78e4267d839863891d58b6',
 'oem_boot_sha256':'dcc69ce6ad7d4ca46ba9363239f1f39863559e286fa3e53abfeb5eb47c82de3a'}
KNOWN = {
 '1.0-rc1': ('c069d7f77a791b061188319a13a3ae4a902493bfbb161bdfd133a29d6209c9a7','207e936e8ec128804a62270599e59c10b4cc219e25b9898e806dd70302f69f36'),
 '1.0-rc2': ('d499c24cb17103957bd4451e65319b2487014d7a532c9b3b4d597870ad698624','e8ee4a4e59c3b3b1665d2278de287cd6710c135c288270cbe4524f5f721e4d47'),
 '1.0-rc3': ('de33ad5b02eada3c61743a2b3582615091d47ba45d2db322ed5ec5f9b2d46e87','1b7386fc8d23205ffb211a5e812b6d05d6fd5dee93d8a8fbb9ad9ea725face7e'),
 '1.1': ('f475e62a3941a8e4d0f0f78b376b2f55c5dd3196033fb5f1e40089bd9b3dd74e','c12148a90fc69a3dc2dae133962dbd9abca0f23547adada53a685ef4339917c1')}
def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()
def read(p:Path,n:int)->bytes:
 if p.is_symlink() or not p.is_file() or p.stat().st_size!=n:raise ValueError(f'Expected ordinary file of {n} bytes: {p.name}')
 b=p.read_bytes()
 if len(b)!=n:raise ValueError('File length changed during read')
 return b

def pair(d:Path,name:str,n:int)->bytes:
 a,b=read(d/(name+'_A.bin'),n),read(d/(name+'_B.bin'),n)
 if a!=b:raise ValueError('Two reads disagree: '+name)
 return a

def load(d:Path)->dict:
 if (d/'M3FLASH.BIN').exists():
  out=[]
  for flashn,infon in [('M3FLASH.BIN','M3INFO.BIN'),('ZBACK2.BIN','ZINFO2.DAT')]:
   f=read(d/flashn,262144);i=read(d/infon,1024)
   if i[:8]!=b'M3BACK01' or struct.unpack_from('<III',i,8)!=(0x10001,262144,0x08000000):raise ValueError('Incomplete SD backup/template')
   if zlib.crc32(i[:1020])!=int.from_bytes(i[1020:],'little') or i[32:64]!=hashlib.sha256(f).digest():raise ValueError('SD backup CRC/SHA mismatch')
   out.append((f,i))
  if out[0]!=out[1]:raise ValueError('SD A/B copies differ')
  f,i=out[0];uid,options,size=i[20:32],i[592:608],i[64:66]
 else:
  if (d/'FLASH256_POST_UPDATE_A.bin').exists():name='FLASH256_POST_UPDATE'
  elif (d/'FLASH_A.bin').exists():name='FLASH'
  else:raise ValueError('No paired 256-KiB files. Expected FLASH256_POST_UPDATE_A/B.bin or FLASH_A/B.bin, with UID/SIZE/OPTIONS A/B.')
  f=pair(d,name,262144);uid=pair(d,'UID',12);options=pair(d,'OPTIONS',16);size=pair(d,'SIZE',2)
 if size!=b'\x00\x01':raise ValueError('Measured SIZE must be 256 KiB, not a GUI estimate')
 if uid in (bytes(12),b'\xff'*12):raise ValueError('Uniform/missing UID')
 for j in range(0,16,2):
  if options[j]^options[j+1]!=255:raise ValueError('Invalid Option Bytes complement')
 return {'flash':f,'uid':uid,'options':options,'size':size}

def device_info(f:bytes)->dict:
 page=f[0x3f800:0x40000];result={'model':'Zortrax M300 (target profile)','hardware':None,'serial':None,'operating_minutes':None}
 if int.from_bytes(page[72:76],'little')==0xaabb0103 and 0xe0<=page[76]<=0xef:result['hardware']=page[76]-0xe0
 if int.from_bytes(page[24:28],'little')==0xaabb0401:result['serial']='Z'+page[28:32].hex().upper()
 a,b=f[0x3e800:0x3f000],f[0x3f000:0x3f800];ha,hb=int.from_bytes(a[:2],'little'),int.from_bytes(b[:2],'little')
 active=a if ha==0 and hb in (65535,0xeeee) else b if hb==0 and ha in (65535,0xeeee) else None
 if active:
  lengths=[4,2,2,2,2,4,4];pos=4;last=None
  while pos+2<=2048:
   k=int.from_bytes(active[pos:pos+2],'little')
   if k==65535:break
   if k>6 or pos+2+lengths[k]>2048:return result
   if k==0:last=int.from_bytes(active[pos+2:pos+6],'little')
   pos+=2+lengths[k]
  if active[pos:]==b'\xff'*(2048-pos):result['operating_minutes']=last
 return result

def inspect(v:dict)->dict:
 f=v['flash'];found={
 'uid_sha256':sha(v['uid']),'options_sha256':sha(v['options']),
 'factory_sha256':sha(f[0x3f800:]),'prefix_sha256':sha(f[:4096])}
 boot='UNRECOGNIZED'
 if sha(f[:32768])==PROFILE['oem_boot_sha256']:boot='OEM_v3'
 else:
  for name,(st,ass) in KNOWN.items():
   if (sha(f[0x1000:0x8000]),sha(f[0x3a000:0x3d000]))==(st,ass):boot=name;break
 mismatches=[k for k,val in found.items() if val!=PROFILE[k]]
 if boot=='UNRECOGNIZED':mismatches.append('source_boot')
 info=device_info(f)
 if info['hardware']!=5:mismatches.append('HW05')
 return {'status':'PASS_I4_PROFILE_MATCH' if not mismatches else 'BACKUP_VALID_BUT_INSTALL_PROFILE_MISMATCH',
 'source_boot':boot,'flash_bytes':len(f),'flash_sha256':sha(f),'boot_sha256':sha(f[:32768]),
 'data_sha256':sha(f[0x3e000:]),'mismatched_fields':mismatches,
 'backup_pair_equal':True,'device':info,
 'warning':'Private report: do not upload identifiers or backup files to public GitHub. A profile match is necessary, not sufficient, for installation.'}

def main()->int:
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('directory',type=Path);a=p.parse_args()
 try:
  r=inspect(load(a.directory));print(json.dumps(r,ensure_ascii=False,indent=2));return 0 if not r['mismatched_fields'] else 3
 except (ValueError,OSError) as e:print('FAIL:',e,file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
