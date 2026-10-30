#!/usr/bin/env python3
"""Offline v1.3.1 public release audit; standard library, no device access.

Checks the release independently against pinned executable component identities,
strict archive scope, complete sparse HEX, host tools, EN/PL manuals and privacy.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FW = ROOT/'firmware/v1.3.1'
DOC = ROOT/'docs/en/v1.3.1'
PL_DOC = ROOT/'docs/pl/v1.3.1'
PINNED = {
    'stage2': (28672, '26dbb8bb63bb30f77b8cff8f506d9a612b0dc69abd41f86ef4e25b0eb7fd02f5'),
    'assets': (12288, '9cfd25014c85cf9f0b7d9099efc33c69355558f3a63ab12c807c2aeb89ae1d6e'),
    'Update.bin': (102293, 'b5a08ac715e5e254f98f91bceb37838494012cb663f2e0f1ea9bb9fbc2a24c0c'),
    'M300APP.M3B': (102280, 'abfd33606636113063d5918e12c41b8f46f19f51783ab3c745c6f5246a2d3030'),
    'RESTORE.BIN': (146496, '350d7f9235dedc813ea3d005d51a24f5b0e56a74465a6e14d728e5e4e3d15916'),
}
RATES = (115200,250000,500000,750000,1000000,1500000)
FORBIDDEN = {'.c','.h','.s','.asm','.elf','.map','.mfd','.so'}
TEXT = {'.md','.txt','.py','.command','.json','.cff','.yml','.yaml'}
SERIAL = re.compile(r'\bZ[0-9A-F]{8}\b')

class Checks:
    def __init__(self):
        self.count = 0
        self.groups = {}
    def ok(self, test, message, group):
        self.count += 1
        self.groups[group] = self.groups.get(group,0)+1
        if not test:
            raise AssertionError(f'{group}: {message}')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def check_identity(c, data, key):
    size,digest = PINNED[key]
    c.ok(len(data)==size and sha(data)==digest,'Pinned component '+key,'firmware')

def archive(c, path):
    with zipfile.ZipFile(path) as z:
        c.ok(z.testzip() is None,path.name+' CRC','archives')
        names = z.namelist()
        c.ok(len(names)==len(set(names)),path.name+' duplicate names','archives')
        files = {}
        for i in z.infolist():
            p = PurePosixPath(i.filename)
            c.ok(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'ZIP path '+i.filename,'archives')
            mode = i.external_attr >> 16
            c.ok(not stat.S_ISLNK(mode) and (not stat.S_IFMT(mode) or stat.S_ISREG(mode)),'ZIP type '+i.filename,'archives')
            c.ok(p.suffix.lower() not in FORBIDDEN,'Private firmware source/binary analysis '+i.filename,'privacy')
            c.ok(not p.name.startswith(('UID_','DATA_','BOOT_A','BOOT_B','FLASH_A','FLASH_B')),'Private device file '+i.filename,'privacy')
            data = z.read(i)
            if p.suffix.lower() in TEXT:
                c.ok(not SERIAL.search(data.decode('utf-8')),'Raw printer serial '+i.filename,'privacy')
            files[i.filename] = data
        return files

def intel_hex(c, data):
    out={};upper=0;done=False
    for line in data.decode('ascii').splitlines():
        c.ok(not done and line.startswith(':'),'HEX prefix / data after EOF','hex')
        row=bytes.fromhex(line[1:]);n=row[0];kind=row[3];addr=int.from_bytes(row[1:3],'big')
        c.ok(len(row)==n+5 and sum(row)%256==0,'HEX record checksum/length','hex')
        if kind==4:
            c.ok(n==2 and addr==0,'HEX extended address','hex')
            upper=int.from_bytes(row[4:-1],'big')<<16
        elif kind==0:
            for i,b in enumerate(row[4:-1]):
                a=upper+addr+i
                c.ok(a not in out,'HEX duplicate address','hex')
                out[a]=b
        elif kind==1:
            c.ok(n==0 and addr==0,'HEX EOF','hex');done=True
        else:
            raise AssertionError('Unexpected HEX record')
    c.ok(done and len(out)==40960,'Complete two-slot HEX','hex')
    return out

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true');args=p.parse_args(argv)
    c=Checks()
    manifest=json.loads((FW/'RELEASE_MANIFEST.json').read_text())
    c.ok(manifest['version']==manifest['installer']=='1.3.1','Current release identity','release')
    c.ok(manifest['scope'].startswith('single qualified device'),'Retained scope','release')
    c.ok(tuple(manifest['baud_menu'])==RATES and manifest['legacy_saved_baud']==[19200,57600],'Rate table','release')
    c.ok(manifest['default_baud']==250000 and manifest['default_uart_on_bootwait'] is False,'Default settings','release')
    c.ok(all(manifest['owner_confirmed_hardware'][k] is True for k in ('UPGRADE','FACTORY','STLINK','UART_1500000','standalone_oled')),'Owner hardware confirmation','release')
    c.ok(manifest['firmware_binaries_rebuilt_for_publication'] is False,'No unqualified firmware rebuild','release')
    expected_names={'M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip','M300Boot_v1.3.1_SD_UPGRADE.zip','M300Boot_v1.3.1_STLINK.zip','M300_BACKUP_0.5.5_UART.zip'}
    c.ok({x['name'] for x in manifest['assets']}==expected_names and len(manifest['assets'])==4,'Exact asset catalog','release')
    for a in manifest['assets']:
        data=(FW/a['name']).read_bytes()
        c.ok(len(data)==a['bytes'] and sha(data)==a['sha256'],'Catalog hash '+a['name'],'release')
    listed=[]
    for line in (FW/'SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split('  ',1)
        c.ok(name in expected_names|{'RELEASE_MANIFEST.json'},'Checksum allowlist','release')
        c.ok(sha((FW/name).read_bytes())==digest,'Release checksum '+name,'release');listed.append(name)
    c.ok(len(listed)==5 and set(listed)==expected_names|{'RELEASE_MANIFEST.json'},'Complete checksums','release')
    f=archive(c,FW/'M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip')
    u=archive(c,FW/'M300Boot_v1.3.1_SD_UPGRADE.zip')
    s=archive(c,FW/'M300Boot_v1.3.1_STLINK.zip')
    b=archive(c,FW/'M300_BACKUP_0.5.5_UART.zip')
    shared={'RESTORE.BIN','M3FLASH.BIN','M3INFO.BIN','ZBACK2.BIN','ZINFO2.DAT'}
    c.ok(set(f)==shared|{'Update.bin'} and set(u)==shared|{'M300APP.M3B'},'Exactly six flat files per SD route','archives')
    for key in shared:
        c.ok(f[key]==u[key],'Shared card component '+key,'archives')
        if key!='RESTORE.BIN':
            size=262144 if key in ('M3FLASH.BIN','ZBACK2.BIN') else 1024
            c.ok(f[key]==b'\xa5'*size,'Blank template, never a device snapshot '+key,'privacy')
    for key,data in [('Update.bin',f['Update.bin']),('M300APP.M3B',u['M300APP.M3B']),('RESTORE.BIN',u['RESTORE.BIN'])]:
        check_identity(c,data,key)
    c.ok((FW/'M300_BACKUP_0.5.5_UART.zip').read_bytes()==(ROOT/'firmware/v1.1/M300_BACKUP_0.5.5_UART.zip').read_bytes(),'Diagnostic remains byte-identical','archives')
    stage='03_TARGET_FULL/M300Boot_v1.3.1_FULL_STAGE2_0x08001000.bin'
    assets='03_TARGET_FULL/M300Boot_v1.3.1_FULL_ASSETS_0x0803A000.bin'
    hx='03_TARGET_FULL/M300Boot_v1.3.1_FULL_SPARSE.hex'
    allowed={stage,assets,hx,'tools/stlink_preflight.py','tools/verify_sd_i2.py','tools/verify_package.py','00_START_HERE_EN.md','00_START_TUTAJ_PL.md','LICENSE','MANIFEST_SHA256.json'}
    c.ok(set(s)==allowed,'STLINK exact publication allowlist','privacy')
    check_identity(c,s[stage],'stage2');check_identity(c,s[assets],'assets')
    m=intel_hex(c,s[hx])
    wanted=set(range(0x08001000,0x08008000))|set(range(0x0803A000,0x0803D000))
    c.ok(set(m)==wanted,'HEX only the two full padded slots','hex')
    c.ok(bytes(m[i] for i in range(0x08001000,0x08008000))==s[stage],'HEX stage2 equals BIN','hex')
    c.ok(bytes(m[i] for i in range(0x0803A000,0x0803D000))==s[assets],'HEX assets equals BIN','hex')
    inner=json.loads(s['MANIFEST_SHA256.json'])
    c.ok(inner['version']=='1.3.1' and set(inner['files'])==allowed-{'MANIFEST_SHA256.json'},'Inner package catalog','archives')
    for name,item in inner['files'].items():
        c.ok(len(s[name])==item['bytes'] and sha(s[name])==item['sha256'],'Inner checksum '+name,'archives')
    for name in ('stlink_preflight.py','verify_sd_i2.py','verify_package.py'):
        c.ok(s['tools/'+name]==(ROOT/'tools'/name).read_bytes(),'Installed and packaged tool identity '+name,'host')
    sys.path.insert(0,str(ROOT/'tools'))
    import ibtool, m300_service, m300_console, verify_sd_i2
    for data in (u['M300APP.M3B'],u['RESTORE.BIN']):
        meta=ibtool.inspect(data)
        c.ok(meta['application_base']=='0x8008000' and ibtool.pack(data[64:])==data,'M3B exact reconstruction','protocol')
        corrupt=bytearray(data);corrupt[-1]^=1
        try:
            ibtool.inspect(corrupt)
        except ValueError:
            pass
        else:
            raise AssertionError('Corrupt M3B accepted')
    c.ok(tuple(m300_console.RATES)==tuple(m300_service.BAUDRATES)==RATES,'Public host supports all six visible rates','host')
    for route,data in [('factory',f),('upgrade',u)]:
        key={'factory':'01_SD_FACTORY_OEMV3','upgrade':'02_SD_UPGRADE_M300BOOT'}[route]
        c.ok(set(verify_sd_i2.CARD_MANIFEST[key])==set(data),'Host card catalog '+route,'host')
        for name,item in verify_sd_i2.CARD_MANIFEST[key].items():
            c.ok(len(data[name])==item['bytes'] and sha(data[name])==item['sha256'],'Host card pin '+name,'host')
    files=[x for x in ROOT.rglob('*') if x.is_file() and not any(k in x.relative_to(ROOT).parts for k in ('.git','__pycache__','.pytest_cache'))]
    for x in files:
        c.ok(not x.is_symlink() and x.suffix.lower() not in FORBIDDEN,'Public tree privacy '+str(x.relative_to(ROOT)),'privacy')
        if x.suffix.lower() in TEXT:
            text=x.read_text()
            c.ok(not SERIAL.search(text),'Raw serial in '+str(x.relative_to(ROOT)),'privacy')
        if x.suffix=='.py':
            ast.parse(x.read_text(),filename=str(x),feature_version=(3,9));c.ok(True,'Python 3.9 syntax '+x.name,'host')
    links=0
    for x in files:
        if x.suffix!='.md':
            continue
        for url in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',x.read_text()):
            dest=url.split('#',1)[0].split('?',1)[0]
            if not dest or dest.startswith(('http://','https://','mailto:')):
                continue
            c.ok((x.parent/dest).exists(),'Markdown link '+str(x.relative_to(ROOT))+': '+url,'links');links+=1
    for name in ('installation.md','original-backup.md','features-and-console.md','uart-examples.md','stlink-and-recovery.md','troubleshooting.md'):
        c.ok((DOC/name).stat().st_size>1000 and (PL_DOC/name).stat().st_size>1000,'Complete EN/PL pair '+name,'docs')
        c.ok('/pl/' in (DOC/name).read_text() and '/en/' in (PL_DOC/name).read_text(),'Paired language links '+name,'docs')
    for x in (ROOT/'docs/assets/v1.3.1').glob('*.png'):
        data=x.read_bytes()
        c.ok(data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==(1024,256),'Native 256x64 preview x4 '+x.name,'docs')
    c.ok('docs/en/README.md' in (ROOT/'README.md').read_text() and 'README_PL.md' in (ROOT/'README.md').read_text(),'English documentation and language entry','docs')
    c.ok('docs/pl/README.md' in (ROOT/'README_PL.md').read_text() and 'README.md' in (ROOT/'README_PL.md').read_text(),'Polish documentation and language entry','docs')
    for name in ('m300_console.py','m300_service.py','ibtool.py','verify_sd_i2.py','stlink_preflight.py','verify_package.py'):
        run=subprocess.run([sys.executable,str(ROOT/'tools'/name),'--help'],capture_output=True,text=True)
        c.ok(run.returncode==0,'Executable CLI '+name,'host')
    for x in (ROOT/'tools').glob('*.command'):
        c.ok(subprocess.run(['bash','-n',str(x)],capture_output=True).returncode==0,'Shell syntax '+x.name,'host')
    report={'result':'PASS','version':'1.3.1','checks':c.count,'groups':c.groups,'relative_markdown_links_verified':links,
            'firmware_rebuilt':False,'device_access_performed':False,'owner_confirmed_routes':['UPGRADE','FACTORY','STLINK'],
            'scope':'Offline publication checks; hardware evidence is the owner report, not this script'}
    print(json.dumps(report,indent=2) if args.json else f'PASS_PUBLICATION_V131 {c.count} checks; {links} links')
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (AssertionError,ValueError,OSError,KeyError) as e:
        print('FAIL_PUBLICATION_V131:',e,file=sys.stderr)
        raise SystemExit(1)
