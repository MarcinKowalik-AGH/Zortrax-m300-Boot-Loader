# Publication audit — M300Boot v1.1

[English](../../en/v1.1/publication-audit.md) · [Polski](../../pl/v1.1/publication-audit.md) · [Index](README.md)

**Archived v1.1 record, 29 October 2026.** Hardware statements below retain their historical scope. [Current v1.3.1](../v1.3.1/README.md).

**Date: 29 October 2026.** This historical audit compared the then-current Inventure v1.5-HW2 documentation structure with M300 v1.1. Scope: documentation and publication checks, without firmware compilation or replacement.

## Findings and corrections

| Finding | Correction at that time |
|---|---|
| Full EN/PL manuals were mixed in flat docs | Versioned documentation was established under docs/v1.1, with a version index and compatible old links; no invented v1.0 archive. |
| Features and UART examples were combined | Separate English and Polish UART examples were added, checked against the real CLI arguments. |
| No automatic public-release check | Publication audit and GitHub workflow were added: four archives, paired card files, RESTORE, stage2/assets/HEX, M3B, privacy, links, Python 3.9 syntax and negative CRC/SHA cases. |
| Compatibility might be read as universal | Repeated the individual profile gate and independent qualification requirement for another M300/HW05. |
| Release-tag state was mixed with current documentation | Distinguished immutable original release binaries from documentation maintained on main. |

## Historical hardware scope

The owner confirmed UPGRADE through installer 1.1-i4 and restoration/startup of original Zortrax 1.3.1 on one characterized classic M300, Rev.5.3/HW05, ID 0x414, measured SIZE 256 KiB. Serial and counter evidence remained private. At the time of this audit, a separate FACTORY transaction, physical ST-Link programming, continuous printing, other boards and power interruption were not established. A later dated owner feedback record described FACTORY on unit B; [that record](hardware-feedback.md) retains its separate timing.

## Offline private-image test

Using an earlier verified private snapshot pair, `check_backup_profile.py` returned `PASS_I4_PROFILE_MATCH`. The local builder generated both m300 and oem variants, each 262144 B, preserving the prefix and final 8 KiB. No probe was connected, RDP changed or generated image physically booted. Private fixtures were not published.

## Distribution and validation

All four public ZIPs matched the v1.1 release assets byte for byte; no MCU BIN was rebuilt. Manufacturer application/assets retained their rights. Firmware source, ELF/maps, raw identity/NVM/dumps and OEM-key tools were excluded. Technical validation did not establish manufacturer redistribution permissions.

```sh
python3 tools/validate_publication.py --json
```

Run from the repository root. The current command validates both preserved releases and the current documentation layout; the [dated audit results](../../reports/v1.1/AUDIT_CHECKS.json) remain a historical snapshot. The audit does not open UART, SWD or GitHub and does not republish firmware.
