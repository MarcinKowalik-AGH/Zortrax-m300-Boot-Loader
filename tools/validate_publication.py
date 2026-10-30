#!/usr/bin/env python3
"""Validate current v1.3.1 and preserved v1.1 releases, offline, without a printer."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true');a=p.parse_args()
    reports=[]
    for name in ('validate_publication_v11.py','validate_publication_v131.py','validate_documentation.py'):
        result=subprocess.run([sys.executable,str(Path(__file__).with_name(name)),'--json'],capture_output=True,text=True)
        if result.returncode:
            print(result.stdout+result.stderr,file=sys.stderr)
            return result.returncode
        reports.append(json.loads(result.stdout))
    report={'result':'PASS','current_version':'1.3.1','device_access_performed':False,'checks':sum(x['checks'] for x in reports),'releases':reports}
    print(json.dumps(report,indent=2) if a.json else 'PASS_PUBLICATION_AUDIT '+str(report['checks'])+' checks; v1.3.1 + v1.1')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
