#!/usr/bin/env python3
"""Read-only integrity check of extracted release files. No printer access."""
import argparse,hashlib,json,sys
from pathlib import Path,PurePosixPath
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args(argv)
    try:
        root=a.root.resolve();mf=root/'MANIFEST_SHA256.json'
        if mf.is_symlink():raise ValueError('Symlink manifest')
        manifest=json.loads(mf.read_text());files=manifest['files']
        if manifest['version']!='1.3.1' or not files:raise ValueError('Invalid release manifest')
        for name,item in files.items():
            rel=PurePosixPath(name)
            if rel.is_absolute() or '..' in rel.parts or '\\' in name:raise ValueError('Unsafe path: '+name)
            f=root.joinpath(*rel.parts)
            if any(q.is_symlink() for q in [f,*list(f.parents)[:len(rel.parts)-1]]):raise ValueError('Symlink path: '+name)
            if not f.is_file() or f.stat().st_size!=item['bytes'] or hashlib.sha256(f.read_bytes()).hexdigest()!=item['sha256']:raise ValueError('Missing or modified: '+name)
        print('PASS_M300BOOT_V131_PACKAGE',len(files),'files');return 0
    except (OSError,ValueError,KeyError,TypeError) as e:print('FAIL:',e,file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
