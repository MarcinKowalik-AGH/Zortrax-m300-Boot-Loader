#!/usr/bin/env python3
"""Offline public GitHub publication audit for M300 boot v1.1 (stdlib only).

Never connects to an MCU, ST-Link or GitHub; never writes to Flash or disables RDP.
Firmware assets must remain byte-identical to the hardware-tested i4 release.
"""
from __future__ import annotations
import argparse, ast, hashlib, io, json, pathlib, re, struct, sys, tempfile, zipfile, zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FW = ROOT / 'firmware' / 'v1.1'

class Checker:
    def __init__(self):
        self.count = 0
        self.groups: dict[str, int] = {}
        self.details: dict[str, object] = {}
    def ok(self, condition: bool, message: str, group='generic'):
        self.count += 1
        self.groups[group] = self.groups.get(group, 0) + 1
        if not condition:
            raise AssertionError(f'FAIL [{group}] {message}')
    def report(self):
        return {'result':'PASS','scope':'Offline public release validation; no printer or GitHub write',
                'version':'1.1', 'installer':'1.1-i4',
                'checks':self.count, 'groups':self.groups, **self.details}

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def hex_to_map(data: bytes, c: Checker):
    """Parse Intel HEX and require correct line checksums/no address overlap."""
    addr_hi=0; out={}; done=False
    for ln, line in enumerate(data.decode('ascii').splitlines(), 1):
        c.ok(line.startswith(':'),f'HEX line {ln} prefix','hex')
        row=bytes.fromhex(line[1:]);size=row[0]
        c.ok(len(row)==size+5 and sum(row)%256==0,f'HEX line {ln} checksum','hex')
        off=int.from_bytes(row[1:3],'big');typ=row[3];payload=row[4:-1]
        if typ==4:
            c.ok(size==2 and off==0,f'HEX line {ln} ELA','hex')
            addr_hi=int.from_bytes(payload,'big')<<16
        elif typ==0:
            for i, b in enumerate(payload):
                a=addr_hi+off+i
                c.ok(a not in out,f'HEX overlap at 0x{a:08X}','hex')
                out[a]=b
        elif typ==1:
            c.ok(size==0 and off==0, 'Bad EOF record','hex')
            done=True
        else: raise AssertionError(f'Unsupported HEX record {typ}')
    c.ok(done,'HEX is missing EOF','hex')
    return out

def zip_files(path: pathlib.Path, c: Checker) -> dict[str,bytes]:
    with zipfile.ZipFile(path) as z:
        c.ok(z.testzip() is None, f'{path.name} CRC', 'archives')
        names=z.namelist()
        c.ok(len(names)==len(set(names)),f'{path.name} duplicate names','archives')
        for name in names:
            p=pathlib.PurePosixPath(name)
            c.ok(not p.is_absolute() and '..' not in p.parts and '\\' not in name,f'Zip path unsafe {name}','archives')
            # Archives are flat, regular files; no symlinks, devices, or directories.
            c.ok('/' not in name and not name.endswith('/'),f'Unexpected zip directory {name}','archives')
        return {name:z.read(name) for name in names}

def main() -> int:
    c=Checker()
    manifest=json.loads((FW/'RELEASE_MANIFEST.json').read_text('utf-8'))
    c.ok(manifest['version']=='1.1' and manifest['installer']=='1.1-i4','wrong version','release')
    c.ok(manifest['scope'].startswith('single qualified device'),'public release inaccurately presented as universal','release')
    assets={}
    for item in manifest['assets']:
        f=FW/item['name'];data=f.read_bytes(); assets[item['name']]=data
        c.ok(len(data)==item['bytes'],f'{f.name} length','release')
        c.ok(digest(data)==item['sha256'],f'{f.name} hash','release')
    c.ok(len(assets)==4,'Expected four release ZIPs','release')
    sums=(FW/'SHA256SUMS.txt').read_text().splitlines();checked=[]
    sha_targets={**assets,'RELEASE_MANIFEST.json':(FW/'RELEASE_MANIFEST.json').read_bytes()}
    for line in sums:
        hash_value, name=line.split('  ',1)
        c.ok(name in sha_targets,f'Unknown asset in SHA256SUMS: {name}','release')
        c.ok(digest(sha_targets[name])==hash_value,f'SHA256SUMS mismatch {name}','release')
        checked.append(name)
    c.ok(set(checked)==set(sha_targets),'SHA256SUMS missing assets','release')
    f=zip_files(FW/'M300Boot_v1.1_SD_FACTORY_OEMV3_i4.zip',c)
    u=zip_files(FW/'M300Boot_v1.1_SD_UPGRADE_i4.zip',c)
    s=zip_files(FW/'M300Boot_v1.1_STLINK_LOCAL_BUILDER.zip',c)
    b=zip_files(FW/'M300_BACKUP_0.5.5_UART.zip',c)
    expected={'RESTORE.BIN':146496,'M3FLASH.BIN':262144,'M3INFO.BIN':1024,'ZBACK2.BIN':262144,'ZINFO2.DAT':1024}
    c.ok(set(f)==set(expected)|{'Update.bin'},'FACTORY requires six exact files','archives')
    c.ok(set(u)==set(expected)|{'M300APP.M3B'},'UPGRADE requires six exact files','archives')
    c.ok(len(f['Update.bin'])==101589,'FACTORY updater bytes','archives')
    c.ok(len(u['M300APP.M3B'])==101608,'UPGRADE intermediary bytes','archives')
    for name,n in expected.items():
        c.ok(len(f[name])==len(u[name])==n,f'SD {name} lengths','archives')
        c.ok(f[name]==u[name],f'SD {name} differs by route','archives')
        if name!='RESTORE.BIN':c.ok(f[name]==b'\xa5'*n,f'SD {name} not a clean template','archives')
    c.ok(s['RESTORE.BIN']==u['RESTORE.BIN'],'STLink RESTORE differs','archives')
    c.ok('Update.bin' in b and len(b['Update.bin'])==6037,'0.5.5 backup diagnostic missing','archives')
    c.ok('read_flash_m300_055.py' in b,'backup host missing','archives')
    c.ok('BOOT_A.bin' not in b and 'DATA_A.bin' not in b,'private backup leaked','privacy')
    # M3B packet integrity + negative test of authenticated-by-hash only.
    sys.path.insert(0,str(ROOT/'tools'))
    import ibtool
    for name,data in [('UPGRADE',u['M300APP.M3B']),('STOCK',u['RESTORE.BIN'])]:
        meta=ibtool.inspect(data)
        c.ok(meta['application_base']=='0x8008000' and meta['format']=='M3BOOT1',f'{name} M3B base','protocol')
        c.ok(ibtool.pack(data[64:])==data,f'{name} M3B package reconstruction','protocol')
        corrupt=bytearray(data);corrupt[-1]^=1
        try:ibtool.inspect(bytes(corrupt))
        except ValueError:pass
        else:raise AssertionError(f'{name} corrupt M3B accepted')
        c.ok(meta['signature'].startswith('NONE'),'M3B should not claim signature authentication','protocol')
    c.ok(ibtool.inspect(u['RESTORE.BIN'])['payload_bytes']==146432,'Stock payload size','protocol')
    stage=s['M300Boot_v1.1_FULL_STAGE2_0x08001000.bin']
    ress=s['M300Boot_v1.1_FULL_ASSETS_0x0803A000.bin']
    c.ok(len(stage)==28672 and digest(stage)==manifest['target_stage2_sha256'],'stage2 integrity','hex')
    c.ok(len(ress)==12288 and digest(ress)==manifest['target_assets_sha256'],'assets integrity','hex')
    # Avoid per-byte instrumentation count by parsing raw HEX record checks once per record.
    image_map=hex_to_map(s['M300Boot_v1.1_FULL_SPARSE.hex'],c)
    c.ok(0<len(image_map)<=40960,'Sparse HEX size bounded','hex')
    c.ok(min(image_map)==0x08001000 and max(image_map)<=0x0803CFFF,'Sparse HEX address range','hex')
    c.ok(all(image_map.get(0x08001000+i,0xff)==v for i,v in enumerate(stage)),'Stage2 differs between HEX and BIN, including omitted FF tail','hex')
    c.ok(all(image_map.get(0x0803A000+i,0xff)==v for i,v in enumerate(ress)),'Assets differ between HEX and BIN, including omitted FF tail','hex')
    c.ok(not any(x in image_map for x in (0x08000000,0x08000FFF,0x0803D000,0x0803E000,0x0803FFFF)), 'Sparse HEX overlaps protected data','hex')
    # Public source audit: host Python only, no private snapshots or firmware source
    published=[p for p in ROOT.rglob('*') if p.is_file() and not any(x in p.parts for x in ('.git','__pycache__'))]
    c.ok(all(p.suffix.lower() not in ('.c','.h','.s','.asm','.elf','.map','.mfd') for p in published),'Firmware source or project secrets','privacy')
    c.ok(all('PERSONAL' not in p.name or p.suffix.lower() in ('.md',) for p in published),'Personal firmware file accidentally staged','privacy')
    text_files=[p for p in published if p.suffix.lower() in ('.md','.txt','.py','.command','.json','.cff','.yml','.yaml')]
    for p in text_files:
        c.ok(not re.search(r'\bZ[0-9A-F]{8}\b',p.read_text(errors='replace')),f'Possible raw printer serial leaked: {p.relative_to(ROOT)}','privacy')
    for p in (ROOT/'tools').glob('*.py'):
        code=p.read_text('utf-8')
        ast.parse(code,filename=str(p),feature_version=(3,9))
        c.ok(True,'Python 3.9 syntax: '+p.name,'host')
    for p in (ROOT/'tools').glob('*.command'):
        c.ok(p.read_text(encoding='utf-8').startswith('#!/bin/bash'), 'command shell header: '+p.name,'host')
    # Cross-check protocol fixtures without printer connection.
    import m300_service
    chunk=b'\x00\x01';crc=zlib.crc32(chunk)&0xffffffff
    stream=iter([b'BEGIN_DUMP SIZE 2\n',f'DATA 00000000 {crc:08x} 0001\n'.encode(),f'END_DUMP SHA256 {digest(chunk)}\n'.encode()])
    c.ok(m300_service.parse_dump(lambda:next(stream), 'SIZE')==chunk,'UART CRC/SHA read-only SIZE','host')
    bad=iter([b'BEGIN_DUMP SIZE 2\n',b'DATA 00000000 deadbeef 0001\n'])
    try:m300_service.parse_dump(lambda:next(bad), 'SIZE')
    except ValueError:pass
    else:raise AssertionError('UART invalid CRC accepted')
    # Relative links, README and docs versions, all actual file paths (GitHub-style anchors ignored).
    link_count=0
    pattern=re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')
    for p in [q for q in published if q.suffix.lower()=='.md']:
        data=p.read_text(encoding='utf-8')
        for url in pattern.findall(data):
            link=url.strip().split('#',1)[0]
            if not link or link.startswith(('https://','http://','mailto:','#')):continue
            link=link.split('?',1)[0]
            c.ok((p.parent/link).exists(), f'Broken local link from {p.relative_to(ROOT)}: {url}', 'links')
            link_count+=1
    c.ok((ROOT/'docs/v1.1/README.md').exists() and (ROOT/'docs/README.md').exists(),'Versioned docs index missing','structure')
    for name in ('INSTALACJA_PL.md','INSTALLATION_EN.md','KOPIA_ORYGINALU_PL.md','ORIGINAL_BACKUP_EN.md',
                 'KONSOLA_UART_PRZYKLADY_PL.md','UART_EXAMPLES_EN.md','RELEASE_MANIFEST.md','TESTED_HARDWARE.md'):
        c.ok((ROOT/'docs/v1.1'/name).exists(),f'Missing v1.1 canonical docs: {name}','structure')
    for fn in ['BOOT_MAIN_MENU.png','INSTALLER_MAIN_MENU.png','BOOT_PROGRESS_50.png','INSTALLER_PROGRESS_50.png']:
        png=(ROOT/'docs/v1.1/images'/fn).read_bytes()
        c.ok(png[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',png[16:24])==(1024,256),f'Unexpected PNG {fn}','structure')
    c.ok((ROOT/'docs/en/v1.1/README.md').read_text().count('](')>=6,'Archived v1.1 documentation index incomplete','structure')
    c.details.update({'relative_markdown_links_verified':link_count,
                      'public_files_audited':len(published),
                      'release_zip_assets_unchanged':True,
                      'hardware_test_performed_during_this_audit':False,
                      'original_release_assets_rebuilt':False,
                      'latest_reference':'Inventure boot v1.5-HW2, docs/v1.5 current, docs/v1.4 archived',
                      'private_reference_test':'executed offline separately, not part of public CI'})
    parser=argparse.ArgumentParser();parser.add_argument('--json',action='store_true');args=parser.parse_args()
    print(json.dumps(c.report(),ensure_ascii=False,indent=2) if args.json else f"PASS_PUBLICATION_AUDIT {c.count} assertions; {link_count} local links")
    return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (Exception,AssertionError) as e:
        print(f'FAIL_PUBLICATION_AUDIT: {e}',file=sys.stderr)
        raise SystemExit(1)
