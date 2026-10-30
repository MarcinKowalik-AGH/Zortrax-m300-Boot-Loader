#!/usr/bin/env python3
"""Offline ST-Link plan/readback checker. No USB, serial or programmer access."""
from __future__ import annotations
import argparse,hashlib,json,struct,sys
from pathlib import Path
from verify_sd_i2 import BOOT_ALLOWLIST,OEM_SHA,PREFIX_SHA,UID_SHA

R=Path(__file__).resolve().parents[1]
SIZE=0x40000
REGIONS=((0x3a000,0x3d000,'M300Boot_v1.3.1_FULL_ASSETS_0x0803A000.bin'),
         (0x1000,0x8000,'M300Boot_v1.3.1_FULL_STAGE2_0x08001000.bin'))
FACTORY_SHA='fc8445c612fcdec3d236ae67451371bf462eceabd23943b1844c9c239b684bb4'
# USER/DATA/WRP remain the qualified values. Only an ALREADY unprotected
# RDP pair A5/5A is accepted; this utility never changes it.
OPTIONS_RDP0=bytes.fromhex('a55aff00ff00ff00ff00ff00ff00ff00')
STOCK=((144976,'417a8701c1ecfc3f8927a1cfe7ccb40c51f13d4f339bdb084cc1d1c2380fb74f'),
       (145624,'593494421cc3f3511aea7c811774ae27e36420a0ecd3935ef7783be0aa0c5825'),
       (146392,'11e2ea439d33436418bbeb51579cc7c12ef0a329019829bcf7e5eccbfc863b75'))
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path,size=None):
    if path.is_symlink() or not path.is_file():raise ValueError('Require a regular file: '+str(path))
    if size is not None and path.stat().st_size!=size:raise ValueError('Unexpected size: '+str(path))
    return path.read_bytes()
def vectors(app,n):
    sp,pc=struct.unpack_from('<II',app)
    return 0x20000000<sp<=0x2000bc00 and not sp&7 and pc&1 and 0x08008008<=pc&~1<=0x08008000+n-2
def app_ok(before):
    meta=before[0x3d000:0x3d800];app=before[0x8000:0x3a000]
    if meta==b'\xff'*2048:
        return any(sha(app[:n])==s and vectors(app,n) for n,s in STOCK)
    magic,hs,ver,target,base,n,flags,reserved,digest=struct.unpack_from('<8sHHIIIII32s',meta)
    return ((magic,hs,ver,target,base,flags,reserved)==(b'M3BOOT1\0',64,1,0x3143334d,0x08008000,0,0)
            and 8<=n<=len(app) and meta[64:68]==bytes.fromhex('dec007b0')
            and meta[68:]==b'\xff'*(2048-68) and vectors(app,n)
            and hashlib.sha256(app[:n]).digest()==digest)
def source_kind(before):
    if sha(before[:32768])==OEM_SHA:
        if before[0x3a000:0x3f000]!=b'\xff'*0x5000:raise ValueError('OEM reserved areas are not erased')
        return 'OEM_V3'
    for x in BOOT_ALLOWLIST:
        if sha(before[0x1000:0x8000])==x['stage_sha256'] and sha(before[0x3a000:0x3d000])==x['assets_sha256']:
            end=0x3dc00 if x.get('bootwait_journal',False) else 0x3da00
            if before[end:0x3e000]!=b'\xff'*(0x3e000-end):raise ValueError('Unknown data after owned settings journals')
            return x['version']
    raise ValueError('Unrecognized source boot; no programming plan')
def construct(a,b,uid,options,images=None):
    images = Path(images) if images is not None else R/'03_TARGET_FULL'
    if len(a)!=SIZE or a!=b:raise ValueError('Require two matching independent 256 KiB reads')
    if sha(uid)!=UID_SHA:raise ValueError('Unqualified MCU identity')
    if options!=OPTIONS_RDP0:raise ValueError('Require RDP ALREADY OFF and qualified USER/DATA/WRP; never unprotect to continue')
    if sha(a[:4096])!=PREFIX_SHA or sha(a[0x3f800:])!=FACTORY_SHA:raise ValueError('Unqualified OEM prefix/factory page')
    source=source_kind(a)
    if not app_ok(a):raise ValueError('Application/metadata not validated; use a separately qualified recovery procedure')
    current=next(x for x in BOOT_ALLOWLIST if x['version']=='1.3.1')
    expected=bytearray(a);writes=[]
    for lo,hi,name in REGIONS:
        data=read(images/name,hi-lo)
        target_sha=current['assets_sha256' if lo==0x3a000 else 'stage_sha256']
        if sha(data)!=target_sha:raise ValueError('Modified target segment: '+name)
        expected[lo:hi]=data
        writes.append({'file':name,'address':hex(0x08000000+lo),'bytes':len(data),'sha256':sha(data),'pages':list(range(lo//2048,hi//2048))})
    manifest={'status':'PASS_OFFLINE_STLINK_PLAN','version':'1.3.1','source':source,'device_access_performed':False,'owner_confirmed_stlink':True,
              'before_sha256':sha(a),'expected_readback_sha256':sha(expected),'uid_sha256':sha(uid),'options_hex':options.hex(),
              'changed':bytes(expected)!=a,'write_order':writes,'protected_ranges':'All bytes outside the two listed slots must remain identical.',
              'instruction':'Keep MCU halted. Verify each write and entire 256 KiB readback. Never erase all, change options or run automatically.'}
    return bytes(expected),manifest
def verify(plan,before,after,uid,options,images=None):
    if plan.get('version')!='1.3.1' or plan.get('status')!='PASS_OFFLINE_STLINK_PLAN':raise ValueError('Invalid plan')
    if len(before)!=SIZE or len(after)!=SIZE or sha(before)!=plan['before_sha256']:raise ValueError('Wrong preflight snapshot or readback size')
    expected,_=construct(before,before,uid,options,images)
    if sha(expected)!=plan['expected_readback_sha256'] or sha(uid)!=plan['uid_sha256'] or options.hex()!=plan['options_hex']:raise ValueError('Plan/identity/options changed')
    if after!=expected:raise ValueError('Readback differs from the complete expected image; keep MCU halted')
    return {'status':'PASS_STLINK_READBACK_ALL_256K','version':'1.3.1','sha256':sha(after),'outside_target_bytes_unchanged':True,'uid_and_options_unchanged':True,'device_access_performed':False,'owner_confirmed_stlink':True}
def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='mode',required=True)
    p=sub.add_parser('plan');p.add_argument('--backup-a',required=True,type=Path);p.add_argument('--backup-b',required=True,type=Path)
    p.add_argument('--uid',required=True,type=Path);p.add_argument('--options',required=True,type=Path);p.add_argument('--out-dir',required=True,type=Path);p.add_argument('--images',type=Path,default=R/'03_TARGET_FULL',help='Directory containing the two exact v1.3.1 segments')
    p=sub.add_parser('verify');p.add_argument('--plan',required=True,type=Path);p.add_argument('--before',required=True,type=Path);p.add_argument('--after',required=True,type=Path)
    p.add_argument('--uid-after',required=True,type=Path);p.add_argument('--options-after',required=True,type=Path);p.add_argument('--images',type=Path,default=R/'03_TARGET_FULL')
    a=ap.parse_args(argv)
    try:
        if a.mode=='plan':
            _,m=construct(read(a.backup_a,SIZE),read(a.backup_b,SIZE),read(a.uid,12),read(a.options,16),a.images)
            a.out_dir.mkdir(parents=True,exist_ok=False)
            (a.out_dir/'PRIVATE_STLINK_PLAN.json').write_text(json.dumps(m,indent=2)+'\n')
        else:m=verify(json.loads(read(a.plan)),read(a.before,SIZE),read(a.after,SIZE),read(a.uid_after,12),read(a.options_after,16),a.images)
        print(json.dumps(m,indent=2));return 0
    except (OSError,ValueError,KeyError,StopIteration,struct.error) as e:print('FAIL:',e,file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
