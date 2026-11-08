#!/usr/bin/env python3
"""Check complete 1.4 UI/command documentation against a source-derived inventory.

The inventory was extracted from the matching private C implementation, with
native execution of its actual menu functions. CI does not contain that private
firmware source; this check prevents documented options from disappearing.
Meaning and installation order are also subject to the recorded source review.
"""
import argparse,json,re
from pathlib import Path

def normalize(text):
    return re.sub(r'\s+',' ',text).strip().casefold()

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true');p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args(argv)
    root=a.root;inventory=json.loads((root/'docs/reports/v1.4/DOCUMENTED_OPTIONS.json').read_text());count=0;groups={}
    def check(ok,message,group):
        nonlocal count
        count+=1;groups[group]=groups.get(group,0)+1
        if not ok:raise ValueError(group+': '+message)
    check(inventory['version']=='1.4','Inventory version','inventory')
    check(len(inventory['boot_pages'])==13 and sum(len(x['items'])for x in inventory['boot_pages'])==50,'All 13 native BOOT pages / 50 initial positions','inventory')
    check(len(inventory['boot_commands'])==27 and len(inventory['installer_commands'])==9 and len(inventory['installer_items'])==7,'Complete accepted dispatch forms','inventory')
    for lang in ['en','pl']:
        path=root/f'docs/{lang}/v1.4/features-and-console.md';text=normalize(path.read_text())
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
        install=normalize((root/f'docs/{lang}/v1.4/installation.md').read_text())
        for screen in ['Complete - click Back','Board and SD verified','Backup x2 verified','Verified; click Back']:
            check(normalize(screen)in install,f'{lang} actual OLED result: '+screen,'oled_installation')
    notes=(root/'RELEASE_NOTES_v1.4.md').read_text()
    targets=re.findall(r'\[[^\]]+\]\(([^)]+)\)',notes)
    check(bool(targets),'Release notes have documentation links','release_links')
    for target in targets:
        check(target.startswith('https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/'),'Release guide opens current corrected instructions: '+target,'release_links')
        rel=target.split('/blob/main/',1)[1];check((root/rel).is_file(),'Release guide target exists: '+rel,'release_links')
    report={'result':'PASS','version':'1.4-options-and-procedures','checks':count,'groups':groups,'boot_pages':13,'boot_positions':50,'boot_command_forms':27,'dump_regions':8,'installer_menu_items':7,'installer_command_forms':9,'languages':['en','pl'],'device_access_performed':False,'firmware_modified':False}
    print(json.dumps(report,indent=2)if a.json else f'PASS_OPTION_COVERAGE {count} checks');return 0
if __name__=='__main__':
    try:raise SystemExit(main())
    except (OSError,ValueError,KeyError)as e:print('FAIL_OPTION_COVERAGE:',e);raise SystemExit(1)
