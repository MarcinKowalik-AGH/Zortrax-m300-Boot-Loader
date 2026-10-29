#!/usr/bin/env python3
"""Create PREALLOCATED files for M300 boot v1.1; never overwrite a backup.
Use an already formatted, checked FAT16/FAT32 card. No formatting is performed.
"""
from pathlib import Path
import argparse, os, sys
FILES={'M3FLASH.BIN':262144,'M3INFO.BIN':1024,'M3LOG.BIN':4096}
def prepare(folder:Path):
    if not folder.is_dir():raise ValueError('Choose the existing root directory of your SD card')
    for name,size in FILES.items():
        p=folder/name
        if p.exists():
            print(f'KEPT EXISTING: {p} ({p.stat().st_size} B)');continue
        with p.open('xb') as f:
            f.write(b'\xa5'*size);f.flush();os.fsync(f.fileno())
        if p.stat().st_size!=size:raise IOError('Short template write')
        print(f'CREATED: {p} ({size} B)')
    print('Eject the card safely. The bootloader replaces file contents, not timestamps.')
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('sd_root',type=Path);a=p.parse_args()
    try:prepare(a.sd_root)
    except (OSError,ValueError) as e:print(f'ERROR: {e}',file=sys.stderr);return 1
    return 0
if __name__=='__main__':raise SystemExit(main())
