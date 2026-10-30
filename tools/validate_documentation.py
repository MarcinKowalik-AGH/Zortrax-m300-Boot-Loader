#!/usr/bin/env python3
"""Validate EN/PL documentation, old URLs and shared evidence; no device access."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import posixpath
import re

ROOT=Path(__file__).resolve().parents[1]
BASE='https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/'
LINK=re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')

def links(path):
    result=[]
    for url in LINK.findall(path.read_text()):
        if url.startswith(BASE):
            target=url[len(BASE):].split('#',1)[0].split('?',1)[0]
        elif url.startswith(('http://','https://','mailto:','#')):
            continue
        else:
            target=posixpath.normpath(posixpath.join(path.relative_to(ROOT).parent.as_posix(),url.split('#',1)[0].split('?',1)[0]))
        if target:
            result.append(target)
    return result

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--json',action='store_true');args=parser.parse_args(argv)
    layout=json.loads((ROOT/'docs/DOCUMENTATION_MAP.json').read_text())
    count=0;groups={}
    def check(value,message,group):
        nonlocal count
        count+=1;groups[group]=groups.get(group,0)+1
        if not value:
            raise ValueError(group+': '+message)
    check(layout['current_version']=='v1.3.1' and layout['languages']==['en','pl'],'Current version and locales','layout')
    for path in ('README.md','README_PL.md','tools/README.md','tools/README_PL.md','firmware/README.md','firmware/README_PL.md','docs/en/README.md','docs/pl/README.md'):
        text=(ROOT/path).read_text()
        check('[English]' in text and '[Polski]' in text,'Language switch in '+path,'navigation')
    for version,indexes in layout['version_indexes'].items():
        for lang,path in indexes.items():
            check(path==f'docs/{lang}/{version}/README.md' and (ROOT/path).is_file(),'Version index '+path,'layout')
            check(('Archive' in (ROOT/path).read_text() or 'Archiw' in (ROOT/path).read_text()) if version=='v1.1' else ('Current' in (ROOT/path).read_text() or 'Bieżąc' in (ROOT/path).read_text()),'Explicit current/archive status '+path,'navigation')
    pairs=layout['paired_manuals']
    check(len(pairs)==19,'Expected complete manual pairs','layout')
    check(len({p['en'] for p in pairs})==len(pairs) and len({p['pl'] for p in pairs})==len(pairs),'No duplicate canonical manuals','layout')
    for pair in pairs:
        en,pl=ROOT/pair['en'],ROOT/pair['pl']
        check(en.name==pl.name,'Matching EN/PL filenames','layout')
        for lang,p,other in [('en',en,pl),('pl',pl,en)]:
            text=p.read_text()
            check(len(text)>800 and text.startswith('# '),'Complete manual '+str(p.relative_to(ROOT)),'content')
            check(other.relative_to(ROOT).as_posix() in links(p),'Reciprocal language switch '+p.name,'navigation')
            check(not re.search(r'^## (English|Polski)\s*$',text,re.M),'Mixed language sections '+p.name,'content')
            check(not re.search(r'_(EN|PL)\.md$',p.name),'Locale suffix is redundant inside locale directory','layout')
    for item in layout['legacy_redirects']:
        p=ROOT/item['old'];text=p.read_text()
        check(len(text)<800 and text.startswith('# Documentation link'),'Compatibility page '+item['old'],'compatibility')
        actual=links(p)
        for target in item['targets'].values():
            check(target in actual and (ROOT/target).is_file(),'Legacy target '+item['old']+' -> '+target,'compatibility')
            check(not (ROOT/target).read_text().startswith('# Documentation link'),'No redirect chains','compatibility')
    for item in layout['shared_compatibility_copies']:
        a,b=ROOT/item['old'],ROOT/item['canonical']
        check(a.read_bytes()==b.read_bytes(),'Unchanged report/image '+item['old'],'shared_evidence')
    all_md=[p for p in ROOT.rglob('*.md') if '.git' not in p.relative_to(ROOT).parts]
    number=0
    for p in all_md:
        for target in links(p):
            check(not target.startswith('../') and (ROOT/target).exists(),'Broken link '+str(p.relative_to(ROOT))+' -> '+target,'links')
            number+=1
    # Release assets are immutable; the dated manifests remain the authority.
    assets=0
    for version in ('v1.1','v1.3.1'):
        folder=ROOT/'firmware'/version
        manifest=json.loads((folder/'RELEASE_MANIFEST.json').read_text())
        for item in manifest['assets']:
            data=(folder/item['name']).read_bytes()
            check(len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256'],'Release asset changed during docs cleanup','firmware')
            assets+=1
    report={'result':'PASS','version':'documentation-en-pl','checks':count,'groups':groups,'manual_pairs':len(pairs),'legacy_redirect_pages':len(layout['legacy_redirects']),'markdown_links_verified':number,'immutable_zip_assets_verified':assets,'device_access_performed':False,'firmware_changed':False}
    print(json.dumps(report,indent=2) if args.json else f'PASS_DOCUMENTATION_EN_PL {count} checks; {number} links')
    return 0

if __name__=='__main__':
    try:
        raise SystemExit(main())
    except (OSError,ValueError,KeyError) as e:
        print('FAIL_DOCUMENTATION_EN_PL:',e)
        raise SystemExit(1)
