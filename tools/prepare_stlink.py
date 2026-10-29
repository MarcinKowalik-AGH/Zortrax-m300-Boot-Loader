#!/usr/bin/env python3
"""OFFLINE ONLY: construct a PERSONAL 256-KiB recovery/programming image.
Never connects to ST-Link, changes RDP/WRP, erases a chip or auto-programs.
Requires two matching private backups, measured SIZE, UID and Option Bytes.
"""
from __future__ import annotations
import argparse, hashlib, json, os, struct, sys
from pathlib import Path
import check_backup_profile as backup
import ibtool
PINNED={
 'M300Boot_v1.1_FULL_STAGE2_0x08001000.bin':(28672,'f475e62a3941a8e4d0f0f78b376b2f55c5dd3196033fb5f1e40089bd9b3dd74e'),
 'M300Boot_v1.1_FULL_ASSETS_0x0803A000.bin':(12288,'c12148a90fc69a3dc2dae133962dbd9abca0f23547adada53a685ef4339917c1'),
 'RESTORE.BIN':(146496,'350d7f9235dedc813ea3d005d51a24f5b0e56a74465a6e14d728e5e4e3d15916')}
def imagefile(root:Path,name:str)->bytes:
 n,digest=PINNED[name];b=backup.read(root/name,n)
 if backup.sha(b)!=digest:raise ValueError('Release image checksum mismatch: '+name)
 return b

def build(v:dict,root:Path,mode:str)->tuple[bytes,dict]:
 report=backup.inspect(v)
 if report['mismatched_fields']:raise ValueError('Different/unknown profile: '+','.join(report['mismatched_fields']))
 original=v['flash'];out=bytearray(original)
 restore=imagefile(root,'RESTORE.BIN');metadata=ibtool.inspect(restore);payload=restore[64:]
 if len(payload)!=146432 or metadata['application_base']!='0x8008000':raise ValueError('Wrong stock image')
 if report['source_boot']=='OEM_v3':
  if original[0x3a000:0x3e000]!=b'\xff'*0x4000:raise ValueError('Reserved stock region is not erased; do not overwrite unknown data')
 elif mode=='oem':
  raise ValueError('OEM recovery requires your own backup with the original OEM v3, not a custom-boot snapshot')
 # This is a reconstructed image: preserve identity/NVM and OEM prefix; restore exact stock payload.
 out[0x8000:0x3a000]=b'\xff'*0x32000
 out[0x8000:0x8000+len(payload)]=payload
 if mode=='m300':
  out[0x1000:0x8000]=imagefile(root,'M300Boot_v1.1_FULL_STAGE2_0x08001000.bin')
  out[0x3a000:0x3d000]=imagefile(root,'M300Boot_v1.1_FULL_ASSETS_0x0803A000.bin')
  out[0x3d000:0x3d800]=b'\xff'*2048
  out[0x3d000:0x3d040]=restore[:64]
  out[0x3d040:0x3d044]=struct.pack('<I',0xB007C0DE)
  # Existing custom journal is preserved, OEM journal has been confirmed blank.
 else:
  out[0x3a000:0x3e000]=original[0x3a000:0x3e000]
 if out[:4096]!=original[:4096] or out[0x3e000:]!=original[0x3e000:]:raise ValueError('Protected range modified')
 return bytes(out), {'kind':mode,'status':'PASS_PERSONAL_IMAGE_OFFLINE',
 'program_address':'0x08000000','bytes':len(out),'image_sha256':backup.sha(out),
 'source_flash_sha256':backup.sha(original),'source_boot':report['source_boot'],
 'stock_payload_sha256':metadata['sha256'],'factory_and_nvm_preserved':True,
 'oem_prefix_preserved':True,'hardware_flash_restore_tested':False,
 'option_bytes_included':False,'uid_included':False,
 'note':'Constructed from your private backup + exact stock 1.3.1. Not a pristine factory dump. No chip access performed.'}

def tohex(b:bytes)->str:
 out=[]
 def record(addr,typ,data):
  d=bytes([len(data),addr>>8,addr&255,typ])+data
  return ':'+d.hex().upper()+f'{(-sum(d))&255:02X}'
 upper=None
 for i in range(0,len(b),16):
  address=0x08000000+i
  if upper!=address>>16:upper=address>>16;out.append(record(0,4,upper.to_bytes(2,'big')))
  out.append(record(address&65535,0,b[i:i+16]))
 out.append(':00000001FF');return '\n'.join(out)+'\n'

def main()->int:
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--backup',type=Path,required=True,help='Private audit folder or four completed SD backup files')
 p.add_argument('--mode',choices=['m300','oem'],required=True)
 p.add_argument('--out',type=Path,required=True,help='NEW private output directory; existing directories refused')
 p.add_argument('--images',type=Path,default=Path(__file__).resolve().parent)
 a=p.parse_args();os.umask(0o077)
 try:
  if a.out.exists():raise ValueError('Output already exists; refusing to overwrite')
  content,report=build(backup.load(a.backup),a.images,a.mode)
  a.out.mkdir(parents=False,mode=0o700)
  stem='M300_'+('BOOT_v1.1_STOCK_1.3.1' if a.mode=='m300' else 'OEM_V3_STOCK_1.3.1')+'_PERSONAL_256KiB'
  (a.out/(stem+'.bin')).write_bytes(content);(a.out/(stem+'.hex')).write_text(tohex(content),encoding='ascii')
  (a.out/'MANIFEST.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
  hashes=[]
  for f in sorted(a.out.iterdir()):hashes.append(backup.sha(f.read_bytes())+'  '+f.name)
  (a.out/'SHA256SUMS.txt').write_text('\n'.join(hashes)+'\n',encoding='ascii')
  print(json.dumps(report,indent=2));print('PRIVATE OUTPUT:',a.out)
  print('No ST-Link operation was performed. Read the ST-LINK manual before any programming.')
  return 0
 except (ValueError,OSError) as e:print('FAIL:',e,file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
