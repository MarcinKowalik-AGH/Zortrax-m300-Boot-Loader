#!/bin/bash
set -euo pipefail
exec python3 - "$@" <<'PY_M300_I4_VERIFY'
#!/usr/bin/env python3
"""Read-only card/backup verifier. No serial, ST-Link, deletion or writes."""
from __future__ import annotations
import argparse,hashlib,json,struct,sys,zlib
from pathlib import Path
# Replaced at package build time with the exact observed manifest and identities.
CARD_MANIFEST = {'01_SD_FACTORY_OEMV3': {'M3FLASH.BIN': {'bytes': 262144, 'sha256': 'b9b8561490d31103a2783ddcbf67ffcb6aa02b1aa71a9800aad615aeb20c8c55'}, 'M3INFO.BIN': {'bytes': 1024, 'sha256': 'e75809e0d15667ce44e6aa5c64689a4917b245eb0920094ff0b017dc0612a17a'}, 'RESTORE.BIN': {'bytes': 146496, 'sha256': '350d7f9235dedc813ea3d005d51a24f5b0e56a74465a6e14d728e5e4e3d15916'}, 'Update.bin': {'bytes': 101589, 'sha256': 'c10c26c82749569186eb3bae3edb8cad2a0b9f330f7f4e0c7b3bb16c6b973b84'}, 'ZBACK2.BIN': {'bytes': 262144, 'sha256': 'b9b8561490d31103a2783ddcbf67ffcb6aa02b1aa71a9800aad615aeb20c8c55'}, 'ZINFO2.DAT': {'bytes': 1024, 'sha256': 'e75809e0d15667ce44e6aa5c64689a4917b245eb0920094ff0b017dc0612a17a'}}, '02_SD_UPGRADE_M300BOOT': {'M300APP.M3B': {'bytes': 101608, 'sha256': '91a30d569cfe1ec21082fce64e3666817653bc19aa48e2574d8e533455960525'}, 'M3FLASH.BIN': {'bytes': 262144, 'sha256': 'b9b8561490d31103a2783ddcbf67ffcb6aa02b1aa71a9800aad615aeb20c8c55'}, 'M3INFO.BIN': {'bytes': 1024, 'sha256': 'e75809e0d15667ce44e6aa5c64689a4917b245eb0920094ff0b017dc0612a17a'}, 'RESTORE.BIN': {'bytes': 146496, 'sha256': '350d7f9235dedc813ea3d005d51a24f5b0e56a74465a6e14d728e5e4e3d15916'}, 'ZBACK2.BIN': {'bytes': 262144, 'sha256': 'b9b8561490d31103a2783ddcbf67ffcb6aa02b1aa71a9800aad615aeb20c8c55'}, 'ZINFO2.DAT': {'bytes': 1024, 'sha256': 'e75809e0d15667ce44e6aa5c64689a4917b245eb0920094ff0b017dc0612a17a'}}}
BOOT_ALLOWLIST = [{'version': '1.0-rc1', 'stage_sha256': 'c069d7f77a791b061188319a13a3ae4a902493bfbb161bdfd133a29d6209c9a7', 'assets_sha256': '207e936e8ec128804a62270599e59c10b4cc219e25b9898e806dd70302f69f36', 'source_archive': 'M300Boot_v1.0-rc1_KOMPLET_2026-10-27.zip', 'source_archive_sha256': 'be63cc7f68bc2c3eae58e1ef28f485125084c2a0cfff7794c8a6ff4e825b7558'}, {'version': '1.0-rc2', 'stage_sha256': 'd499c24cb17103957bd4451e65319b2487014d7a532c9b3b4d597870ad698624', 'assets_sha256': 'e8ee4a4e59c3b3b1665d2278de287cd6710c135c288270cbe4524f5f721e4d47', 'source_archive': 'M300Boot_v1.0-rc2_KOMPLET_2026-10-27.zip', 'source_archive_sha256': '5f751e463e262e74a195708c749f6adf6082af40a97df11d419a6b1f3eb60bed'}, {'version': '1.0-rc3', 'stage_sha256': 'de33ad5b02eada3c61743a2b3582615091d47ba45d2db322ed5ec5f9b2d46e87', 'assets_sha256': '1b7386fc8d23205ffb211a5e812b6d05d6fd5dee93d8a8fbb9ad9ea725face7e', 'source_archive': 'M300Boot_v1.0-rc3_KOMPLET_2026-10-28.zip', 'source_archive_sha256': '61df4e7f119a331624f9aa6cc4e52c4b479bd4004345673479a8af58d1517e08'}, {'version': '1.1', 'stage_sha256': 'f475e62a3941a8e4d0f0f78b376b2f55c5dd3196033fb5f1e40089bd9b3dd74e', 'assets_sha256': 'c12148a90fc69a3dc2dae133962dbd9abca0f23547adada53a685ef4339917c1', 'source': 'Built from included source/build/FULL'}]
UID_SHA = '36718d5166f28402a21046cf8f75edd0ce5f0160227e6ac40d7bb097bc2f4a7e'
OPTIONS_SHA = '47cf264caf31417cc5ed042d3a3248b1a523da0736b93138b23e6c938ebf4c6e'
PREFIX_SHA = '710e50741e1aac5e6338c29bb49e06b452d72053ea78e4267d839863891d58b6'
OEM_SHA = 'dcc69ce6ad7d4ca46ba9363239f1f39863559e286fa3e53abfeb5eb47c82de3a'

def sha(b):return hashlib.sha256(b).hexdigest()
def read(directory:Path,name:str,size:int)->bytes:
 p=directory/name
 if not p.is_file() or p.is_symlink():raise ValueError('Brak zwyklego pliku: '+str(p))
 if p.stat().st_size!=size:raise ValueError('Nieprawidlowy rozmiar: '+name)
 return p.read_bytes()
def verify_card(directory:Path,route:str)->dict:
 key={'factory':'01_SD_FACTORY_OEMV3','upgrade':'02_SD_UPGRADE_M300BOOT'}[route]
 wrong='M300APP.M3B' if route=='factory' else 'Update.bin'
 if (directory/wrong).exists():raise ValueError('Pomieszane sciezki: usun z karty niewlasciwy plik '+wrong+' po zachowaniu jego kopii. Ten skrypt niczego nie usuwa.')
 for name,m in CARD_MANIFEST[key].items():
  b=read(directory,name,m['bytes'])
  if sha(b)!=m['sha256']:raise ValueError('SHA-256 inny niz swiezy zestaw: '+name+'. Dla zapisanych kopii uzyj --backups, nie zastepuj ich szablonami.')
 return {'status':'PASS_SD_I4_CARD_FILES','route':route,'files':6,'fat_cluster_separation':'Not checked by host file API; checked by actual installer before writes.'}
def verify_backups(directory:Path)->dict:
 snapshots=[];infos=[]
 for fn,info in [('M3FLASH.BIN','M3INFO.BIN'),('ZBACK2.BIN','ZINFO2.DAT')]:
  b=read(directory,fn,262144);i=read(directory,info,1024)
  if i[:8]!=b'M3BACK01' or struct.unpack_from('<III',i,8)!=(0x10001,262144,0x08000000):raise ValueError('Nieprawidlowy naglowek '+info)
  if zlib.crc32(i[:1020])!=int.from_bytes(i[1020:],'little'):raise ValueError('Nieprawidlowe CRC '+info)
  if i[32:64]!=hashlib.sha256(b).digest():raise ValueError('Nieprawidlowy hash kopii '+fn)
  if int.from_bytes(i[64:66],'little')!=256:raise ValueError('Nieprawidlowa pojemnosc')
  if sha(i[20:32])!=UID_SHA or sha(i[592:608])!=OPTIONS_SHA:raise ValueError('Inny egzemplarz lub opcje')
  if sha(b[:4096])!=PREFIX_SHA:raise ValueError('Niezgodny chroniony poczatek OEM')
  snapshots.append(b);infos.append(i)
 if snapshots[0]!=snapshots[1] or infos[0]!=infos[1]:raise ValueError('Kopie A/B roznia sie')
 b=snapshots[0];source='UNKNOWN'
 if sha(b[:32768])==OEM_SHA:source='OEM_V3'
 else:
  for v in BOOT_ALLOWLIST:
   if sha(b[0x1000:0x8000])==v['stage_sha256'] and sha(b[0x3a000:0x3d000])==v['assets_sha256']:source=v['version'];break
 if source=='UNKNOWN':raise ValueError('Nieznany bootloader w kopii')
 return {'status':'PASS_SD_I4_BACKUPS_X2','flash_bytes_each':262144,'flash_sha256':sha(b),'source_boot':source,'options_sha256':OPTIONS_SHA,'uid_sha256':UID_SHA,'scope':'Snapshot AFTER installing intermediary, BEFORE replacing boot; not pre-update stock. No restore-to-MCU test.'}
def main(argv=None):
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
 g.add_argument('--card',type=Path);g.add_argument('--backups',type=Path);p.add_argument('--route',choices=['factory','upgrade'],default='upgrade');a=p.parse_args(argv)
 try:
  result=verify_card(a.card,a.route) if a.card else verify_backups(a.backups)
  print(json.dumps(result,ensure_ascii=False,indent=2));return 0
 except (ValueError,OSError) as e:print('FAIL:',e,file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())

PY_M300_I4_VERIFY
