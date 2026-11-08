#!/usr/bin/env python3
"""Offline v1.4 public release audit; standard library, no device access.

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
import zlib

ROOT = Path(__file__).resolve().parents[1]
FW = ROOT/'firmware/v1.4'
HOST = ROOT/'tools'
DOC = ROOT/'docs/en/v1.4'
PL_DOC = ROOT/'docs/pl/v1.4'
# Filled with independently observed build identities before publication.
PINNED = {'stage2': (28672, 'faa278235c20a7507d8d1d2306d1208ed89d2fa0fab6de6f273da7f9b3dbf598'), 'assets': (12288, '9519fb00f591d62383c5e5faea71e923ff5ea071dae89116916b2ee7b6cd9c5c'), 'Update.bin': (102357, 'af36eb27ffcc578217369d4500538b9499569be12dd0dad73976789a35bece8a'), 'M300APP.M3B': (102340, '55007605d0d3eb2a3237f68ae7a0c379a188d928305809ea897ce126aea46b8d'), 'RESTORE.BIN': (146496, '350d7f9235dedc813ea3d005d51a24f5b0e56a74465a6e14d728e5e4e3d15916')}

RATES = (115200,250000,500000,750000,1500000)
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

def cyan_png(data):
    """Decode RGB8 PNG rows, including all five PNG filters, without Pillow."""
    if data[:8]!=b'\x89PNG\r\n\x1a\n':
        raise ValueError('Not a PNG')
    width,height,depth,colour,compression,filtering,interlace=struct.unpack('>IIBBBBB',data[16:29])
    if (depth,colour,compression,filtering,interlace)!=(8,2,0,0,0):
        raise ValueError('Preview must be noninterlaced RGB8 PNG')
    offset=8;compressed=bytearray()
    while offset<len(data):
        n=struct.unpack_from('>I',data,offset)[0];kind=data[offset+4:offset+8]
        payload=data[offset+8:offset+8+n]
        if zlib.crc32(kind+payload)&0xffffffff!=struct.unpack_from('>I',data,offset+8+n)[0]:
            raise ValueError('PNG chunk CRC')
        if kind==b'IDAT':compressed.extend(payload)
        offset+=12+n
        if kind==b'IEND':break
    raw=zlib.decompress(compressed);stride=width*3
    if len(raw)!=height*(stride+1):raise ValueError('PNG pixel extent')
    previous=bytearray(stride);pixels=set()
    for y in range(height):
        mode=raw[y*(stride+1)];row=bytearray(raw[y*(stride+1)+1:(y+1)*(stride+1)])
        if mode>4:raise ValueError('PNG filter')
        for x in range(stride):
            left=row[x-3] if x>=3 else 0;up=previous[x];corner=previous[x-3] if x>=3 else 0
            if mode==1:predictor=left
            elif mode==2:predictor=up
            elif mode==3:predictor=(left+up)//2
            elif mode==4:
                v=left+up-corner;distances=(abs(v-left),abs(v-up),abs(v-corner))
                predictor=(left,up,corner)[distances.index(min(distances))]
            else:predictor=0
            row[x]=(row[x]+predictor)&255
        pixels.update(tuple(row[x:x+3]) for x in range(0,stride,3));previous=row
    return (width,height),pixels

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true');args=p.parse_args(argv)
    c=Checks()
    manifest=json.loads((FW/'RELEASE_MANIFEST.json').read_text())
    c.ok(manifest['version']==manifest['installer']=='1.4','Current release identity','release')
    c.ok(manifest['scope'].startswith('single qualified device'),'Retained scope','release')
    c.ok(tuple(manifest['baud_menu'])==RATES and manifest['unsupported_legacy_saved_baud']==[19200,57600,1000000],'Rate table','release')
    c.ok(manifest['default_baud']==250000 and manifest['default_uart_on_bootwait'] is False,'Default settings','release')
    c.ok(manifest['hardware_tested'] is False,'No unsupported 1.4 hardware qualification','release')
    c.ok(manifest['firmware_binaries_rebuilt_for_publication'] is True,'Release was rebuilt from 1.4 sources','release')
    expected_names={'M300Boot_v1.4_SD_FACTORY_OEMV3.zip','M300Boot_v1.4_SD_UPGRADE.zip','M300Boot_v1.4_STLINK.zip','M300_BACKUP_0.5.5_UART.zip'}
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
    f=archive(c,FW/'M300Boot_v1.4_SD_FACTORY_OEMV3.zip')
    u=archive(c,FW/'M300Boot_v1.4_SD_UPGRADE.zip')
    s=archive(c,FW/'M300Boot_v1.4_STLINK.zip')
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
    stage='03_TARGET_FULL/M300Boot_v1.4_FULL_STAGE2_0x08001000.bin'
    assets='03_TARGET_FULL/M300Boot_v1.4_FULL_ASSETS_0x0803A000.bin'
    hx='03_TARGET_FULL/M300Boot_v1.4_FULL_SPARSE.hex'
    allowed={stage,assets,hx,'tools/stlink_preflight.py','tools/verify_sd_i2.py','tools/verify_package.py','00_START_HERE_EN.md','00_START_TUTAJ_PL.md','LICENSE','MANIFEST_SHA256.json'}
    c.ok(set(s)==allowed,'STLINK exact publication allowlist','privacy')
    check_identity(c,s[stage],'stage2');check_identity(c,s[assets],'assets')
    m=intel_hex(c,s[hx])
    wanted=set(range(0x08001000,0x08008000))|set(range(0x0803A000,0x0803D000))
    c.ok(set(m)==wanted,'HEX only the two full padded slots','hex')
    c.ok(bytes(m[i] for i in range(0x08001000,0x08008000))==s[stage],'HEX stage2 equals BIN','hex')
    c.ok(bytes(m[i] for i in range(0x0803A000,0x0803D000))==s[assets],'HEX assets equals BIN','hex')
    inner=json.loads(s['MANIFEST_SHA256.json'])
    c.ok(inner['version']=='1.4' and set(inner['files'])==allowed-{'MANIFEST_SHA256.json'},'Inner package catalog','archives')
    for name,item in inner['files'].items():
        c.ok(len(s[name])==item['bytes'] and sha(s[name])==item['sha256'],'Inner checksum '+name,'archives')
    for name in ('stlink_preflight.py','verify_sd_i2.py','verify_package.py'):
        c.ok(s['tools/'+name]==(HOST/name).read_bytes(),'Installed and packaged tool identity '+name,'host')
    # Executable version checks exclude untouched OEM RESTORE and historical
    # installer source-allowlist labels. The active BOOT never advertises old 1M.
    boot=s[stage]+s[assets]
    app=u['M300APP.M3B'][64:]
    c.ok(b'1.4' in boot and b'1.4' in app,'BOOT and intermediary carry 1.4','firmware')
    c.ok(b'M300BOOT v1.4' in boot,'Exact boot console version','firmware')
    c.ok(b'M300INSTALL 1.4' in app and b'SD installer 1.4' in app,'Exact intermediary console and OLED versions','firmware')
    c.ok(b'1000000\0' not in app,'No stale 1M menu label in intermediary','firmware')
    for rate in RATES:
        c.ok(str(rate).encode()+b'\0' in boot,'Visible BOOT label '+str(rate),'firmware')
    c.ok(b'1000000\0' not in boot,'Removed 1M menu label','firmware')
    c.ok(f['Update.bin'][:13]==b'ZRTXUPD39.8.7','Retained technical OEM envelope','protocol')
    c.ok(u['M300APP.M3B'][:8]==b'M3BOOT1\0','Native application envelope','protocol')
    # Exact persisted code mapping: holes retain historical index positions.
    table=struct.pack('<8I',0,0,115200,250000,500000,750000,0,1500000)
    c.ok(table in boot,'Executable five-rate table with legacy index holes','firmware')
    sys.path.insert(0,str(HOST))
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
    c.ok(tuple(m300_console.RATES)==tuple(m300_service.BAUDRATES)==RATES,'Public host supports exactly the five active rates','host')
    for name in ('m300_console.py','m300_service.py','ibtool.py'):
        code=(HOST/name).read_text();tree=ast.parse(code)
        constants={}
        for node in tree.body:
            if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
                try:constants[node.targets[0].id]=ast.literal_eval(node.value)
                except (ValueError,TypeError):pass
        baud_options=[node for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='add_argument' and node.args and isinstance(node.args[0],ast.Constant) and node.args[0].value=='--baud']
        c.ok(len(baud_options)==1,'Unique baud option '+name,'host')
        keywords={x.arg:x.value for x in baud_options[0].keywords}
        choice=keywords['choices'];actual=constants[choice.id] if isinstance(choice,ast.Name) else ast.literal_eval(choice)
        c.ok(tuple(actual)==RATES,'Exact CLI baud choices '+name,'host')
        c.ok(ast.literal_eval(keywords['default'])==250000,'Host default '+name,'host')
    # Each rejection occurs in argparse, before any file creation or serial open.
    invalid_rates=(19200,57600,1000000,2000000,0,-1,2147483647)
    commands={
        'm300_console.py':['--port','/dev/__m300_audit_no_port__'],
        'm300_service.py':['dump','--port','/dev/__m300_audit_no_port__','SIZE','--out','/__m300_audit_no_output__'],
        'ibtool.py':['serial','/__m300_audit_no_package__.M3B','--port','/dev/__m300_audit_no_port__'],
    }
    for name,arguments in commands.items():
        for rate in invalid_rates:
            result=subprocess.run([sys.executable,str(HOST/name),*arguments,'--baud',str(rate)],capture_output=True,text=True)
            c.ok(result.returncode==2 and 'invalid choice' in result.stderr,'Reject baud '+str(rate)+' before I/O: '+name,'cli_negative_baud')
    launcher=HOST/'KONSOLA_M300_v1.4.command'
    text=launcher.read_text()
    c.ok((HOST/'m300_console.py').read_text() in text,'Standalone launcher embeds exact canonical console','host')
    c.ok('1.3.1' not in text and '1000000' not in text,'Launcher identity and five-rate scope','host')
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
    for x in (ROOT/'docs/assets/v1.4').glob('*.png'):
        data=x.read_bytes()
        dimensions,colours=cyan_png(data)
        c.ok(dimensions in ((256,64),(1024,256)),'Native 256x64 or x4 preview '+x.name,'docs')
        c.ok({(0,0,0),(0,255,255)}<=colours and all(r==0 and g==b and g%17==0 for r,g,b in colours),'Native 16-level cyan bitmap on black '+x.name,'docs')
    c.ok(len(list((ROOT/'docs/assets/v1.4').glob('*.png')))>=7,'At least seven authentic UI previews','docs')
    c.ok('docs/en/README.md' in (ROOT/'README.md').read_text() and 'README_PL.md' in (ROOT/'README.md').read_text(),'English documentation and language entry','docs')
    c.ok('docs/pl/README.md' in (ROOT/'README_PL.md').read_text() and 'README.md' in (ROOT/'README_PL.md').read_text(),'Polish documentation and language entry','docs')
    for name in ('m300_console.py','m300_service.py','ibtool.py','verify_sd_i2.py','stlink_preflight.py','verify_package.py'):
        run=subprocess.run([sys.executable,str(ROOT/'tools'/name),'--help'],capture_output=True,text=True)
        c.ok(run.returncode==0,'Executable CLI '+name,'host')
    for x in (ROOT/'tools').glob('*.command'):
        c.ok(subprocess.run(['bash','-n',str(x)],capture_output=True).returncode==0,'Shell syntax '+x.name,'host')
    report={'result':'PASS','version':'1.4','checks':c.count,'groups':c.groups,'relative_markdown_links_verified':links,
            'firmware_rebuilt':True,'device_access_performed':False,'hardware_tested':False,
            'scope':'Offline complete publication checks; no physical printer qualification'}
    print(json.dumps(report,indent=2) if args.json else f'PASS_PUBLICATION_V14 {c.count} checks; {links} links')
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (AssertionError,ValueError,OSError,KeyError) as e:
        print('FAIL_PUBLICATION_V14:',e,file=sys.stderr)
        raise SystemExit(1)
