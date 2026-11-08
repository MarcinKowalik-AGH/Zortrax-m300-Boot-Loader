#!/usr/bin/env python3
"""Verify the original OEM BOOT and the owner's 1.4 acceptance record offline."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
SHA256 = 'dcc69ce6ad7d4ca46ba9363239f1f39863559e286fa3e53abfeb5eb47c82de3a'
RELEASE_MANIFEST_SHA256 = '526b69cffdb6f198db00ec12080cc18c612f51b78e7cf34fcd80589c9cd82aca'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    checks = 0

    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            raise ValueError(message)

    folder = ROOT / 'firmware/original'
    check({p.name for p in folder.iterdir()} == {
        'OEM_BOOT_V3.bin', 'README.md', 'README_PL.md', 'MANIFEST.json', 'SHA256SUMS.txt'
    }, 'Original directory must contain only the documented BOOT and its metadata')
    data = (folder / 'OEM_BOOT_V3.bin').read_bytes()
    check(len(data) == 32768, 'Original BOOT must be exactly 32 KiB')
    check(hashlib.sha256(data).hexdigest() == SHA256, 'Original BOOT exact identity')
    check(struct.unpack_from('<II', data) == (0x20003FF0, 0x08000165), 'Original vector table')
    check(b'Zortrax Bootloader v3\0' in data, 'Original embedded version')

    manifest = json.loads((folder / 'MANIFEST.json').read_text())
    check(manifest['file'] == 'OEM_BOOT_V3.bin' and manifest['bytes'] == len(data)
          and manifest['sha256'] == SHA256, 'Original manifest file identity')
    check(manifest['flash_start'] == '0x08000000' and manifest['flash_end_inclusive'] == '0x08007FFF',
          'Only the original BOOT memory range')
    check(manifest['modified'] is False and manifest['format'] == 'raw_binary', 'Unmodified raw BOOT')
    check(manifest['provenance']['archive'] == 'M300Boot_v1.3.1_KOMPLET_2026-10-30.zip'
          and manifest['provenance']['member'] == '04_OEM_ROLLBACK/OEM_BOOT_V3.bin',
          'Retained archive provenance')
    check(manifest['oem_restore_hardware_test_reported'] is False, 'OEM restoration not overclaimed')

    entries = []
    for line in (folder / 'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ', 1)
        check('/' not in name and name != 'SHA256SUMS.txt', 'Flat original-file checksum name')
        entries.append(name)
        check(hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest,
              'Original metadata checksum: ' + name)
    check(len(entries) == len(set(entries)) == 4 and set(entries) == {
        'OEM_BOOT_V3.bin', 'MANIFEST.json', 'README.md', 'README_PL.md'
    }, 'Complete original-file checksum catalog')
    for name in ('README.md', 'README_PL.md'):
        text = (folder / name).read_text()
        check(SHA256 in text and '0x08000000–0x08007FFF' in text
              and 'RESTORE.BIN' in text and 'M300Boot 1.4' in text, 'Precise original BOOT description: ' + name)

    acceptance = json.loads((ROOT / 'docs/reports/v1.4/HARDWARE_ACCEPTANCE.json').read_text())
    check(acceptance['version'] == '1.4' and acceptance['evidence_type'] == 'owner_statement'
          and acceptance['reported_by'] == 'Marcin Kowalik', 'Owner acceptance identity')
    check(acceptance['owner_confirmed_hardware'] == {'FACTORY': True, 'UPGRADE': True, 'STLINK': True},
          'All three installation methods confirmed by owner')
    check(acceptance['independently_observed_by_automation'] is False, 'Owner report distinguished from automation')
    check(acceptance['firmware_assets_unchanged'] is True, 'Acceptance concerns unchanged released firmware')
    check(acceptance['release_manifest_sha256'] == RELEASE_MANIFEST_SHA256
          and hashlib.sha256((ROOT / 'firmware/v1.4/RELEASE_MANIFEST.json').read_bytes()).hexdigest()
          == RELEASE_MANIFEST_SHA256, 'Acceptance tied to immutable release manifest')

    report = {'result': 'PASS', 'version': 'original-oem-v3-and-owner-acceptance-1.4',
              'checks': checks, 'original_boot_bytes': len(data), 'original_boot_sha256': SHA256,
              'owner_confirmed_methods': ['FACTORY', 'UPGRADE', 'STLINK'],
              'device_access_performed': False, 'oem_restore_hardware_test_reported': False}
    print(json.dumps(report, indent=2) if args.json else f'PASS_ORIGINAL_BOOT {checks} checks')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, struct.error) as error:
        print('FAIL_ORIGINAL_BOOT:', error, file=sys.stderr)
        raise SystemExit(1)
