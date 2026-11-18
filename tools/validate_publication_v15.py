#!/usr/bin/env python3
"""Offline M300Boot 1.5 release audit, using only the Python 3.9 stdlib.

Component pins are independently obtained from the reviewed build. They are
not taken from the release's own manifest. Checks are counted per invariant,
file, or archive; individual HEX bytes do not inflate the assertion count.
This validator neither rebuilds firmware nor accesses a printer or GitHub.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FW = ROOT / 'firmware/v1.5'
HOST = ROOT / 'tools'
VERSION = '1.5'
RATES = (115200, 250000, 500000, 750000, 1500000)
DEFAULT_BAUD = 250000

# Replace these placeholders only with identities from the independently
# reviewed build, never by copying the publication manifest under test.
# Missing pins intentionally fail closed.
PINNED = {
    'stage2': (28672, '2dd2b0c101b2b2aa6860d965d2c667a7e086fb1a2f31a693bd28916ac2dfb2b5'),
    'assets': (12288, 'bf9936ff0575c3bbad0f555f356a201cf5cc2b825db80fc0a6d26a724ca5eec8'),
    'Update.bin': (102485, '10a7414968e747f6544bde5d871ff7b9710deb3f7c8f41a7f78fd0a861155e05'),
    'M300APP.M3B': (102492, 'a87f3ac0968d7b3e1bee684501ae852a11b10ee3d18ce1ce59e7e202b67fdaec'),
    'RESTORE.BIN': (146496, '350d7f9235dedc813ea3d005d51a24f5b0e56a74465a6e14d728e5e4e3d15916'),
}
DIAGNOSTIC = 'M300_BACKUP_0.5.5_UART.zip'
DIAGNOSTIC_PIN = (30476, '61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149')
INSTALL_ZIPS = {
    'FACTORY': 'M300Boot_v1.5_SD_FACTORY_OEMV3.zip',
    'UPGRADE': 'M300Boot_v1.5_SD_UPGRADE.zip',
    'STLINK': 'M300Boot_v1.5_STLINK.zip',
}
# The reported two-week hardware experience belongs to these unchanged 1.4
# assets, not to the newly built patch. Keep their immutable release intact.
LEGACY_V14_PINS = {
    'M300Boot_v1.4_SD_FACTORY_OEMV3.zip': (186427, 'd0f6a157aff470d510fb28c0f400b1f64b3b5c53a5750e1d1caf92e5bf1e831f'),
    'M300Boot_v1.4_SD_UPGRADE.zip': (148076, '002e313a7ead97cebdc0a4da0c897a6a788a5ebc43491a6fbc11af13531b8b20'),
    'M300Boot_v1.4_STLINK.zip': (83763, '8409a1871fb167ca3b91ddc640007b8db1123102f17256678bb6e6ee6d0403c5'),
    DIAGNOSTIC: DIAGNOSTIC_PIN,
}
LEGACY_V141_PINS = {
    'M300Boot_v1.4.1_SD_FACTORY_OEMV3.zip': (186480, 'c744294cd726242268422b3f37cf31384d8859f1e3bd0d34e0d0b4dd37df8c08'),
    'M300Boot_v1.4.1_SD_UPGRADE.zip': (148340, 'ed711a6ec8fad4a266a0cf24851fbea63b75996375e7227fe7144bdcad7f24b7'),
    'M300Boot_v1.4.1_STLINK.zip': (88710, '0071a7d0217822219b3cffef6cdd399d433187260f67dba6e41860d664fb31a9'),
    DIAGNOSTIC: DIAGNOSTIC_PIN,
}
FORBIDDEN = {'.c', '.h', '.s', '.asm', '.elf', '.map', '.mfd', '.so', '.o', '.a', '.key'}
TEXT = {'.md', '.txt', '.py', '.command', '.json', '.cff', '.yml', '.yaml'}
IGNORED_PARTS = {'.git', '__pycache__', '.pytest_cache', '.mypy_cache'}
PRINTER_SERIAL = re.compile(r'\bZ[0-9A-F]{8}\b')
DIGEST = re.compile(r'[0-9a-f]{64}\Z')
MANUALS = (
    'README.md', 'installation.md', 'original-backup.md',
    'features-and-console.md', 'uart-examples.md', 'stlink-and-recovery.md',
    'troubleshooting.md', 'tested-hardware.md', 'validation.md',
    'release-manifest.md', 'release-notes.md',
)


class Checks:
    def __init__(self):
        self.count = 0
        self.groups = {}

    def ok(self, condition, message, group):
        self.count += 1
        self.groups[group] = self.groups.get(group, 0) + 1
        if not condition:
            raise AssertionError(f'{group}: {message}')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(data, pin):
    return len(data) == pin[0] and sha(data) == pin[1]


def safe_relative(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or '\\' in name:
        raise ValueError('Unsafe relative path: ' + name)
    return path


def read_json(data):
    # Duplicate names can otherwise hide a changed field or checksum entry.
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique)


def check_component(c, data, name):
    c.ok(identity(data, PINNED[name]), 'Independent component identity: ' + name, 'firmware')


def read_archive(c, path, allowed=None):
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        c.ok(len(names) == len(set(names)), path.name + ': no duplicate entries', 'archives')
        if allowed is not None:
            c.ok(set(names) == allowed, path.name + ': exact file set', 'archives')
        c.ok(archive.testzip() is None, path.name + ': CRCs', 'archives')
        files = {}
        for entry in archive.infolist():
            relative = safe_relative(entry.filename)
            mode = entry.external_attr >> 16
            if entry.is_dir() or stat.S_ISLNK(mode) or (stat.S_IFMT(mode) and not stat.S_ISREG(mode)):
                raise ValueError('Archive entry is not an ordinary file: ' + entry.filename)
            if relative.suffix.lower() in FORBIDDEN:
                raise ValueError('Private build/source material in archive: ' + entry.filename)
            if relative.name.startswith(('UID_', 'DATA_', 'BOOT_A', 'BOOT_B', 'FLASH_A', 'FLASH_B')):
                raise ValueError('Private device file in archive: ' + entry.filename)
            data = archive.read(entry)
            if relative.suffix.lower() in TEXT and PRINTER_SERIAL.search(data.decode('utf-8')):
                raise ValueError('Raw printer serial in archive: ' + entry.filename)
            files[entry.filename] = data
        c.ok(True, path.name + ': safe paths, ordinary files and public content', 'privacy')
        return files


def parse_hex(data):
    """Check every record and address, but report one integrity invariant."""
    memory = {}
    upper = 0
    ended = False
    records = 0
    for line in data.decode('ascii').splitlines():
        if ended or not line.startswith(':'):
            raise ValueError('Invalid HEX prefix or data after EOF')
        row = bytes.fromhex(line[1:])
        if len(row) < 5:
            raise ValueError('Truncated HEX record')
        length, kind = row[0], row[3]
        address = int.from_bytes(row[1:3], 'big')
        if len(row) != length + 5 or sum(row) & 255:
            raise ValueError('HEX length/checksum mismatch')
        records += 1
        if kind == 4:
            if length != 2 or address:
                raise ValueError('Invalid HEX extended address')
            upper = int.from_bytes(row[4:-1], 'big') << 16
        elif kind == 0:
            if address + length > 0x10000:
                raise ValueError('HEX record crosses a 64-KiB window')
            for offset, byte in enumerate(row[4:-1]):
                absolute = upper + address + offset
                if absolute in memory:
                    raise ValueError('Duplicate HEX address')
                memory[absolute] = byte
        elif kind == 1:
            if length or address:
                raise ValueError('Invalid HEX EOF')
            ended = True
        else:
            raise ValueError('Unexpected HEX record type')
    if not ended:
        raise ValueError('Missing HEX EOF')
    return memory, records


def public_files():
    return sorted(path for path in ROOT.rglob('*')
                  if (path.is_file() or path.is_symlink()) and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts))


def check_checksums(c, root, filename, expected, group):
    entries = {}
    for line in (root / filename).read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  (.+)', line)
        if not match:
            raise ValueError('Invalid checksum line in ' + str(root / filename))
        digest, name = match.groups()
        safe_relative(name)
        if name in entries:
            raise ValueError('Duplicate checksum path: ' + name)
        entries[name] = digest
    c.ok(set(entries) == set(expected), filename + ': complete exact checksum coverage', group)
    for name, digest in entries.items():
        path = root / name
        if path.is_symlink() or not path.is_file() or sha(path.read_bytes()) != digest:
            raise ValueError('Missing, symlinked or modified checksum entry: ' + str(path))
    c.ok(True, filename + ': all listed bytes match', group)
    return len(entries)


def markdown_body(text):
    """Remove fenced code before considering headings or documentation links."""
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return '\n'.join(lines)


def heading_anchors(text):
    body = markdown_body(text)
    anchors = set(re.findall(r'<a\s+[^>]*(?:id|name)=["\']([^"\']+)["\']', body, re.I))
    lines = body.splitlines()
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r'^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
        if match:
            headings.append(match.group(1))
        elif index and re.fullmatch(r'\s{0,3}(?:=+|-+)\s*', line) and lines[index - 1].strip():
            headings.append(lines[index - 1].strip())
    for heading in headings:
        heading = re.sub(r'!?(\[([^]]+)\])\([^)]+\)', r'\2', heading)
        heading = html.unescape(re.sub(r'<[^>]+>', '', heading)).lower()
        # GitHub-style slugs for the plain Unicode headings used by these
        # manuals: punctuation/formatting removed, spaces become hyphens.
        base = ''.join(ch for ch in heading
                       if ch in '-_' or ch.isspace() or unicodedata.category(ch)[0] in 'LNM')
        base = re.sub(r'\s', '-', base)
        anchor = base
        number = 0
        while anchor in anchors:
            number += 1
            anchor = base + '-' + str(number)
        anchors.add(anchor)
    return anchors


def check_current_links(c, paths):
    links = anchors = 0
    cache = {}
    for path in paths:
        body = markdown_body(path.read_text())
        destinations = re.findall(r'!?\[[^\]]*\]\((<[^>]+>|[^\s)]+)(?:\s+["\'][^)]*["\'])?\)', body)
        destinations += re.findall(r'^\s{0,3}\[[^\]]+\]:\s*(\S+)', body, re.M)
        for destination in destinations:
            destination = destination.strip('<>')
            parsed = urlsplit(destination)
            if parsed.scheme or parsed.netloc:
                continue  # Remote network validation belongs to publication verification.
            relative = unquote(parsed.path)
            target = (path.parent / relative).resolve() if relative else path.resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                raise ValueError('Markdown link escapes repository: ' + str(path) + ': ' + destination)
            if not target.exists():
                raise ValueError('Broken Markdown destination: ' + str(path.relative_to(ROOT)) + ': ' + destination)
            links += 1
            if parsed.fragment:
                if target.is_dir():
                    target = target / 'README.md'
                if target.suffix.lower() == '.md':
                    if target not in cache:
                        cache[target] = heading_anchors(target.read_text())
                    fragment = unquote(parsed.fragment)
                    if fragment not in cache[target]:
                        raise ValueError('Broken Markdown anchor: ' + str(path.relative_to(ROOT)) + ': ' + destination)
                    anchors += 1
        c.ok(True, 'Current manual links and anchors: ' + str(path.relative_to(ROOT)), 'docs')
    return links, anchors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    c = Checks()
    for name, (size, digest) in PINNED.items():
        c.ok(size > 0 and DIGEST.fullmatch(digest), 'Independent build pin populated: ' + name, 'firmware')

    manifest = read_json((FW / 'RELEASE_MANIFEST.json').read_text())
    c.ok(manifest['version'] == manifest['installer'] == VERSION, 'Release and installer version', 'release')
    c.ok(manifest['scope'].startswith('single qualified device'), 'Retained device qualification scope', 'release')
    c.ok(tuple(manifest['baud_menu']) == RATES, 'Exactly five supported rates', 'release')
    c.ok(manifest['unsupported_legacy_saved_baud'] == [19200, 57600, 1000000], 'Legacy migration list', 'release')
    c.ok(manifest['default_baud'] == DEFAULT_BAUD and manifest['default_uart_on_bootwait'] is False, 'Safe existing defaults retained', 'release')
    c.ok(manifest['hardware_tested'] is False, 'New patch does not inherit base hardware qualification', 'evidence')
    if 'owner_confirmed_hardware' in manifest:
        c.ok(manifest['owner_confirmed_hardware'] == dict.fromkeys(INSTALL_ZIPS, False), 'New patch routes not falsely marked hardware-tested', 'evidence')
    c.ok(manifest['firmware_binaries_rebuilt_for_publication'] is True, 'New build disclosed', 'evidence')
    hardware_status = read_json((ROOT / 'docs/reports/v1.5/HARDWARE_STATUS.json').read_text())
    c.ok(hardware_status['version'] == VERSION and hardware_status['new_firmware_hardware_tested'] is False,
         'Current evidence identifies the new patch as not hardware-tested', 'evidence')
    c.ok(hardware_status['baseline_version'] == '1.4'
         and hardware_status['baseline_owner_reported_duration'] == 'approximately two weeks'
         and hardware_status['baseline_report_date'] == '2026-11-18'
         and hardware_status['exact_start_date_reported'] is False,
         'Two-week owner statement belongs to the base without an invented start date', 'evidence')
    render = read_json((ROOT / 'docs/assets/v1.5/RENDER_MANIFEST.json').read_text())
    inventory = read_json((ROOT / 'docs/reports/v1.5/DOCUMENTED_OPTIONS.json').read_text())
    c.ok(render['version'] == VERSION and render['hardware_test'] is False
         and render['private_device_data'] is False, 'Current native renderer has the correct version and evidence scope', 'evidence')
    c.ok(render['screen_headers'] == dict.fromkeys(('BOOT', 'INSTALLER'), 'M300 boot v1.5 © Marcin Kowalik'),
         'Both native OLED headers identify the new release', 'firmware')
    c.ok(inventory['build_versions'] == dict.fromkeys(('BOOT', 'INSTALLER'), VERSION),
         'Current source IB_VERSION values were extracted for both builds', 'firmware')
    for name in ('source/src/menu.c', 'source/include/ib.h', 'source/src/oled_render.c',
                 'firmware/src/main.c', 'firmware/include/ib.h', 'firmware/src/oled_render.c'):
        c.ok(render['source_sha256'][name] == inventory['source_sha256'][name],
             'Rendered OLED and extracted inventory share reviewed source: ' + name, 'firmware')
    c.ok(manifest['target_stage2_sha256'] == PINNED['stage2'][1] and manifest['target_assets_sha256'] == PINNED['assets'][1], 'Manifest agrees with independent target pins', 'firmware')
    expected_zips = set(INSTALL_ZIPS.values()) | {DIAGNOSTIC}
    entries = manifest['assets']
    c.ok(len(entries) == len(expected_zips) and {entry['name'] for entry in entries} == expected_zips, 'Three installation variants plus separate diagnostic', 'release')
    for entry in entries:
        c.ok(identity((FW / entry['name']).read_bytes(), (entry['bytes'], entry['sha256'])), 'Asset catalog: ' + entry['name'], 'release')
    check_checksums(c, FW, 'SHA256SUMS.txt', expected_zips | {'RELEASE_MANIFEST.json'}, 'release')
    c.ok(identity((FW / DIAGNOSTIC).read_bytes(), DIAGNOSTIC_PIN), 'Diagnostic 0.5.5 remains original', 'firmware')
    for name, pin in LEGACY_V14_PINS.items():
        c.ok(identity((ROOT / 'firmware/v1.4' / name).read_bytes(), pin), 'Historical 1.4 asset unchanged: ' + name, 'history')

    for name, pin in LEGACY_V141_PINS.items():
        c.ok(identity((ROOT / 'firmware/v1.4.1' / name).read_bytes(), pin), 'Historical 1.4.1 asset unchanged: ' + name, 'history')

    shared = {'RESTORE.BIN', 'M3FLASH.BIN', 'M3INFO.BIN', 'ZBACK2.BIN', 'ZINFO2.DAT'}
    factory = read_archive(c, FW / INSTALL_ZIPS['FACTORY'], shared | {'Update.bin'})
    upgrade = read_archive(c, FW / INSTALL_ZIPS['UPGRADE'], shared | {'M300APP.M3B'})
    for name in shared:
        c.ok(factory[name] == upgrade[name], 'Identical shared SD component: ' + name, 'archives')
        if name != 'RESTORE.BIN':
            size = 262144 if name in ('M3FLASH.BIN', 'ZBACK2.BIN') else 1024
            c.ok(factory[name] == b'\xa5' * size, 'Empty preallocated template, not a private snapshot: ' + name, 'privacy')
    for name, data in (('Update.bin', factory['Update.bin']), ('M300APP.M3B', upgrade['M300APP.M3B']), ('RESTORE.BIN', upgrade['RESTORE.BIN'])):
        check_component(c, data, name)

    stage_name = '03_TARGET_FULL/M300Boot_v1.5_FULL_STAGE2_0x08001000.bin'
    assets_name = '03_TARGET_FULL/M300Boot_v1.5_FULL_ASSETS_0x0803A000.bin'
    hex_name = '03_TARGET_FULL/M300Boot_v1.5_FULL_SPARSE.hex'
    packaged_tools = ('stlink_preflight.py', 'verify_sd_i2.py', 'verify_package.py')
    stlink_names = {stage_name, assets_name, hex_name, '00_START_HERE_EN.md', '00_START_TUTAJ_PL.md', 'LICENSE', 'MANIFEST_SHA256.json'}
    stlink_names.update('tools/' + name for name in packaged_tools)
    stlink = read_archive(c, FW / INSTALL_ZIPS['STLINK'], stlink_names)
    check_component(c, stlink[stage_name], 'stage2')
    check_component(c, stlink[assets_name], 'assets')
    memory, hex_records = parse_hex(stlink[hex_name])
    c.ok(True, 'All HEX records: syntax, checksums, sequence and unique addresses', 'hex')
    ranges = ((0x08001000, 0x08008000, stage_name), (0x0803A000, 0x0803D000, assets_name))
    addresses = set().union(*(set(range(lo, hi)) for lo, hi, _ in ranges))
    c.ok(set(memory) == addresses, 'HEX covers exactly the two complete slots; OEM prefix/APP/settings/NVM excluded', 'hex')
    for lo, hi, name in ranges:
        c.ok(bytes(memory[address] for address in range(lo, hi)) == stlink[name], 'HEX equals pinned BIN: ' + name, 'hex')
    inner = read_json(stlink['MANIFEST_SHA256.json'])
    c.ok(inner['version'] == VERSION and set(inner['files']) == stlink_names - {'MANIFEST_SHA256.json'}, 'Complete STLINK inner manifest', 'archives')
    for name, entry in inner['files'].items():
        c.ok(identity(stlink[name], (entry['bytes'], entry['sha256'])), 'STLINK inner identity: ' + name, 'archives')
    for name in packaged_tools:
        c.ok(stlink['tools/' + name] == (HOST / name).read_bytes(), 'Canonical and packaged tool match: ' + name, 'host')

    boot = stlink[stage_name] + stlink[assets_name]
    intermediary = upgrade['M300APP.M3B'][64:]
    c.ok(b'M300BOOT v1.5 START ' in boot, 'Exact BOOT startup version marker', 'firmware')
    c.ok(b'Version v1.5\0' in boot and b'M300 boot v1.5' in boot, 'Exact BOOT About and OLED header versions', 'firmware')
    c.ok(b'M300INSTALL 1.5' in intermediary and b'SD installer 1.5\0' in intermediary, 'Exact intermediary console/OLED markers', 'firmware')
    previous_labels = (b'Version v1.4.1\0', b'M300 boot v1.4.1', b'SD installer 1.4.1\0')
    c.ok(not any(label in boot or label in intermediary for label in previous_labels), 'No stale 1.4.1 OLED version labels; historical compatibility strings may remain', 'firmware')
    c.ok(intermediary.count(stlink[stage_name]) == 1 and intermediary.count(stlink[assets_name]) == 1, 'SD intermediary embeds exactly the same pinned target segments as STLINK', 'firmware')
    c.ok(factory['Update.bin'][:13] == b'ZRTXUPD39.8.7' and upgrade['M300APP.M3B'][:8] == b'M3BOOT1\0', 'FACTORY and UPGRADE envelopes retain their distinct formats', 'protocol')
    for rate in RATES:
        c.ok(str(rate).encode() + b'\0' in boot, 'BOOT rate label: ' + str(rate), 'firmware')
    c.ok(all(str(rate).encode() + b'\0' not in boot and str(rate).encode() + b'\0' not in intermediary for rate in (1000000, 10000000)), 'No selectable 1M or 10M label', 'firmware')
    table = struct.pack('<8I', 0, 0, 115200, 250000, 500000, 750000, 0, 1500000)
    c.ok(table in boot, 'Persisted baud table retains historical index holes', 'firmware')

    sys.path.insert(0, str(HOST))
    import ibtool
    import m300_console
    import m300_service
    import verify_sd_i2
    for name in ('M300APP.M3B', 'RESTORE.BIN'):
        package = upgrade[name]
        info = ibtool.inspect(package)
        c.ok(info['application_base'] == '0x8008000' and ibtool.pack(package[64:]) == package, 'Native M3B validation and exact reconstruction: ' + name, 'protocol')
        damaged = bytearray(package)
        damaged[-1] ^= 1
        try:
            ibtool.inspect(damaged)
        except ValueError:
            c.ok(True, 'Corrupted M3B rejected: ' + name, 'protocol')
        else:
            raise AssertionError('Corrupted M3B accepted: ' + name)
    c.ok(tuple(m300_console.RATES) == tuple(m300_service.BAUDRATES) == RATES, 'Active host baud constants', 'host')
    commands = {
        'm300_console.py': ['--port', '/dev/__m300_audit_no_port__'],
        'm300_service.py': ['dump', '--port', '/dev/__m300_audit_no_port__', 'SIZE', '--out', '/__m300_audit_no_output__'],
        'ibtool.py': ['serial', '/__m300_audit_no_package__.M3B', '--port', '/dev/__m300_audit_no_port__'],
    }
    invalid_rates = (19200, 57600, 1000000, 10000000, 2000000, 0, -1, 2147483647)
    for name, arguments in commands.items():
        tree = ast.parse((HOST / name).read_text())
        constants = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                try:
                    constants[node.targets[0].id] = ast.literal_eval(node.value)
                except (ValueError, TypeError):
                    pass
        baud_options = [node for node in ast.walk(tree)
                        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                        and node.func.attr == 'add_argument' and node.args
                        and isinstance(node.args[0], ast.Constant) and node.args[0].value == '--baud']
        c.ok(len(baud_options) == 1, 'One unambiguous baud option: ' + name, 'host')
        keywords = {keyword.arg: keyword.value for keyword in baud_options[0].keywords}
        choice = keywords['choices']
        choices = constants[choice.id] if isinstance(choice, ast.Name) else ast.literal_eval(choice)
        c.ok(tuple(choices) == RATES and ast.literal_eval(keywords['default']) == DEFAULT_BAUD,
             'CLI has exactly five supported rates and the correct default: ' + name, 'host')
        for rate in invalid_rates:
            result = subprocess.run([sys.executable, str(HOST / name), *arguments, '--baud', str(rate)], capture_output=True, text=True)
            c.ok(result.returncode == 2 and 'invalid choice' in result.stderr, f'{name}: reject {rate} before I/O', 'cli_negative_baud')
    launcher = HOST / 'KONSOLA_M300_v1.5.command'
    c.ok((HOST / 'm300_console.py').read_text() in launcher.read_text(), 'Standalone launcher embeds canonical console', 'host')
    c.ok(subprocess.run(['bash', '-n', str(launcher)], capture_output=True).returncode == 0, 'Standalone launcher shell syntax', 'host')
    for route, files in (('factory', factory), ('upgrade', upgrade)):
        key = {'factory': '01_SD_FACTORY_OEMV3', 'upgrade': '02_SD_UPGRADE_M300BOOT'}[route]
        catalog = verify_sd_i2.CARD_MANIFEST[key]
        c.ok(set(catalog) == set(files), 'Exact current card checker file set: ' + route, 'host')
        c.ok(all(identity(files[name], (entry['bytes'], entry['sha256'])) for name, entry in catalog.items()), 'Current card checker identities: ' + route, 'host')

    manuals = []
    for name in MANUALS:
        pair = [ROOT / 'docs' / language / ('v' + VERSION) / name for language in ('en', 'pl')]
        c.ok(all(path.is_file() and path.stat().st_size > 500 for path in pair), 'Substantive EN/PL manual pair: ' + name, 'docs')
        c.ok('/pl/' in pair[0].read_text() and '/en/' in pair[1].read_text(), 'Manual language navigation: ' + name, 'docs')
        manuals.extend(pair)
    roots = [ROOT / name for name in ('README.md', 'README_PL.md', 'RELEASE_NOTES_v1.5.md')]
    c.ok(all(path.is_file() for path in roots), 'Current release entry pages', 'docs')
    for path in roots:
        text = path.read_text()
        c.ok('1.5' in text and all(name in text for name in INSTALL_ZIPS.values()), 'Version and three direct package links: ' + path.name, 'docs')
    links, anchors = check_current_links(c, manuals + roots)

    files = public_files()
    for path in files:
        if path.is_symlink() or path.suffix.lower() in FORBIDDEN:
            raise ValueError('Private source/build file or symlink in public tree: ' + str(path.relative_to(ROOT)))
        if path.suffix.lower() in TEXT and PRINTER_SERIAL.search(path.read_text()):
            raise ValueError('Raw printer serial in public tree: ' + str(path.relative_to(ROOT)))
        if path.suffix == '.py':
            ast.parse(path.read_text(), filename=str(path), feature_version=(3, 9))
    c.ok(True, 'Public tree excludes private source/build/device identifiers and symlinks', 'privacy')
    c.ok(True, 'All public Python files parse as Python 3.9', 'host')
    root_coverage = {str(path.relative_to(ROOT)) for path in files if path != ROOT / 'SHA256SUMS.txt'}
    checksum_files = check_checksums(c, ROOT, 'SHA256SUMS.txt', root_coverage, 'repository')
    report = {
        'result': 'PASS', 'version': VERSION, 'checks': c.count, 'groups': c.groups,
        'counting': 'One assertion per invariant, file or archive; HEX bytes are not individual checks.',
        'installation_variants': list(INSTALL_ZIPS), 'supported_uart_baud': list(RATES),
        'hex_records_validated': hex_records, 'hex_target_bytes_compared': len(memory),
        'root_checksum_files_verified': checksum_files, 'manual_pairs': len(MANUALS),
        'relative_markdown_links_verified': links, 'markdown_anchors_verified': anchors,
        'device_access_performed': False, 'firmware_rebuild_performed_by_this_validator': False,
        'release_contains_new_firmware_build': True, 'hardware_tested': False,
        'hardware_evidence': {
            'base_version': hardware_status['baseline_version'],
            'base_owner_reported_duration': hardware_status['baseline_owner_reported_duration'],
            'owner_report_date': hardware_status['baseline_report_date'], 'evidence_type': 'owner_statement',
            'exact_start_date_reported': hardware_status['exact_start_date_reported'],
            'patch_version': VERSION, 'patch_hardware_tested': False,
            'base_testing_is_not_patch_hardware_qualification': True,
        },
        'scope': 'Offline artifact, protocol, host and documentation audit; owner testing applies to the preceding 1.4 base, not the new patch.',
    }
    print(json.dumps(report, indent=2) if args.json else f'PASS_PUBLICATION_V15 {c.count} assertions; {links} links; {anchors} anchors')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (AssertionError, ValueError, OSError, KeyError, TypeError, struct.error, zipfile.BadZipFile) as error:
        print('FAIL_PUBLICATION_V15:', error, file=sys.stderr)
        raise SystemExit(1)
