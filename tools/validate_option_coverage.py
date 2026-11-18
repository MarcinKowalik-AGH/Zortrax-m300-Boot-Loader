#!/usr/bin/env python3
"""Check complete UI/command documentation against a source-derived inventory.

The inventory was extracted from the matching private C implementation, with
native execution of its actual menu functions. CI does not contain that private
firmware source; this check prevents documented options from disappearing.
Meaning and installation order are also subject to the recorded source review.
"""
import argparse,hashlib,json,re
from pathlib import Path
from urllib.parse import unquote,urlsplit

def normalize(text):
    return re.sub(r'\s+',' ',text).strip().casefold()

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true');p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--version',choices=('1.4','1.4.1'),default='1.4.1');a=p.parse_args(argv)
    root=a.root;version=a.version;inventory=json.loads((root/f'docs/reports/v{version}/DOCUMENTED_OPTIONS.json').read_text());count=0;groups={}
    def check(ok,message,group):
        nonlocal count
        count+=1;groups[group]=groups.get(group,0)+1
        if not ok:raise ValueError(group+': '+message)
    check(inventory['version']==version,'Inventory version','inventory')
    check(len(inventory['boot_pages'])==13 and sum(len(x['items'])for x in inventory['boot_pages'])==50,'All 13 native BOOT pages / 50 initial positions','inventory')
    check(len(inventory['boot_commands'])==27 and len(inventory['installer_commands'])==9 and len(inventory['installer_items'])==7,'Complete accepted dispatch forms','inventory')
    for lang in ['en','pl']:
        path=root/f'docs/{lang}/v{version}/features-and-console.md';text=normalize(path.read_text())
        for page in inventory['boot_pages']:
            check(normalize(page['title'])in text,f'{lang} page: '+page['title'],'boot_menu')
            for label in page['items']:
                check(normalize(label)in text,f'{lang} item: '+page['title']+' / '+label,'boot_menu')
        for cmd in inventory['boot_commands']:
            # Require literal command tokens; aliases and multi-word commands
            # are enumerated independently, not inferred from HELP alone.
            check(bool(re.search(r'(?<![a-z0-9_])'+re.escape(normalize(cmd))+r'(?![a-z0-9_])',text)),f'{lang} BOOT command: '+cmd,'boot_commands')
        for region in inventory['dump_regions']:
            check(bool(re.search(r'(?<![a-z0-9_])'+re.escape(normalize(region))+r'(?![a-z0-9_])',text)),f'{lang} DUMP region: '+region,'dump_regions')
        for label in inventory['installer_items']:
            check(normalize(label)in text,f'{lang} intermediary item: '+label,'installer_menu')
        for cmd in inventory['installer_commands']:
            check(normalize(cmd)in text,f'{lang} intermediary command: '+cmd,'installer_commands')
        install=normalize((root/f'docs/{lang}/v{version}/installation.md').read_text())
        for screen in ['Complete - click Back','Board and SD verified','Backup x2 verified','Verified; click Back']:
            check(normalize(screen)in install,f'{lang} actual OLED result: '+screen,'oled_installation')
    if version=='1.4.1':
        render_path=root/inventory['renderer_manifest']
        raw=render_path.read_bytes();render=json.loads(raw)
        check(hashlib.sha256(raw).hexdigest()==inventory['renderer_manifest_sha256'],'Matching current renderer manifest','renderer')
        check(render['version']==version and render['hardware_test'] is False and render['private_device_data'] is False,'Render version and truthful evidence scope','renderer')
        check(inventory['native_menu_api_executed'] is True,'Native current menu inventory executed','renderer')
        for name in ('source/src/menu.c','source/include/ib.h','firmware/src/main.c','firmware/include/ib.h'):
            check(render['source_sha256'][name]==inventory['source_sha256'][name],'Same menu/dispatcher source: '+name,'renderer')
        for screen in render['screens']:
            if screen['renderer']=='ib_oled_render_menu' and screen['variant']=='BOOT':
                page=inventory['boot_pages'][screen['page']]
                check(screen['title']==page['title'] and screen['items']==page['items'],'Rendered current menu agrees with complete inventory: '+screen['name'],'renderer')
    notes=(root/f'RELEASE_NOTES_v{version}.md').read_text()
    targets=re.findall(r'\[[^\]]+\]\(([^)]+)\)',notes)
    check(bool(targets),'Release notes have documentation links','release_links')
    for target in targets:
        base='https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/'
        if version=='1.4':
            check(target.startswith(base+'blob/main/'),'Archived release guide opens preserved instructions: '+target,'release_links')
            rel=target.split('/blob/main/',1)[1]
        elif target.startswith(base+'blob/main/'):
            rel=target.split('/blob/main/',1)[1]
        elif target.startswith(base+f'releases/download/v{version}/'):
            rel=f'firmware/v{version}/'+target.rsplit('/',1)[1]
        elif target.startswith(base+f'raw/refs/tags/v{version}/'):
            rel=target.split(f'/raw/refs/tags/v{version}/',1)[1]
        else:
            parsed=urlsplit(target)
            check(not parsed.scheme and not parsed.netloc,'Release link points to a current local guide or exact tagged asset: '+target,'release_links')
            rel=unquote(parsed.path) or f'RELEASE_NOTES_v{version}.md'
        rel=rel.split('#',1)[0].split('?',1)[0]
        path=(root/rel).resolve()
        check(path.is_file() and root.resolve() in path.parents,'Release target exists inside the repository: '+rel,'release_links')
    report={'result':'PASS','version':version+'-options-and-procedures','checks':count,'groups':groups,'boot_pages':13,'boot_positions':50,'boot_command_forms':27,'dump_regions':8,'installer_menu_items':7,'installer_command_forms':9,'languages':['en','pl'],'device_access_performed':False,'firmware_modified':False}
    print(json.dumps(report,indent=2)if a.json else f'PASS_OPTION_COVERAGE {count} checks');return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError)as e:print('FAIL_OPTION_COVERAGE:',e);raise SystemExit(1)
