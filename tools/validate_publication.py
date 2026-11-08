#!/usr/bin/env python3
"""Validate current 1.4 and preserved 1.3.1/1.1 releases, offline, without a printer."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true');a=p.parse_args()
    reports=[]
    for name in ('validate_publication_v11.py','validate_publication_v131.py','validate_publication_v14.py','validate_documentation.py','validate_option_coverage.py'):
        result=subprocess.run([sys.executable,str(Path(__file__).with_name(name)),'--json'],capture_output=True,text=True)
        if result.returncode:
            print(result.stdout+result.stderr,file=sys.stderr)
            return result.returncode
        reports.append(json.loads(result.stdout))
    report={'result':'PASS','current_version':'1.4','device_access_performed':False,'checks':sum(x['checks'] for x in reports),'releases':reports}
    print(json.dumps(report,indent=2) if a.json else 'PASS_PUBLICATION_AUDIT '+str(report['checks'])+' checks; 1.4 + archived 1.3.1 + 1.1')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
