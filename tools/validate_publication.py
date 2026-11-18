#!/usr/bin/env python3
"""Validate current 1.4.1 and preserved 1.4/1.3.1/1.1 releases, offline."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true');a=p.parse_args()
    reports=[]
    checks=(
        ('validate_publication_v11.py',()),
        ('validate_publication_v131.py',()),
        ('validate_publication_v14.py',()),
        ('validate_publication_v141.py',()),
        ('validate_documentation.py',()),
        ('validate_option_coverage.py',('--version','1.4')),
        ('validate_option_coverage.py',('--version','1.4.1')),
        ('validate_original_boot.py',()),
    )
    for name,arguments in checks:
        result=subprocess.run([sys.executable,str(Path(__file__).with_name(name)),*arguments,'--json'],capture_output=True,text=True)
        if result.returncode:
            print(result.stdout+result.stderr,file=sys.stderr)
            return result.returncode
        reports.append(json.loads(result.stdout))
    report={'result':'PASS','current_version':'1.4.1','device_access_performed':False,'checks':sum(x['checks'] for x in reports),'counting_note':'Aggregate includes historical byte-level HEX assertions; it is not a count of independent functional or hardware tests. The 1.4.1 validator counts file/invariant checks separately.','releases':reports}
    print(json.dumps(report,indent=2) if a.json else 'PASS_PUBLICATION_AUDIT '+str(report['checks'])+' assertions; 1.4.1 + archived 1.4 + 1.3.1 + 1.1')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
