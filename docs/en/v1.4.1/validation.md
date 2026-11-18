# Validation — M300Boot 1.4.1

[English](../../en/v1.4.1/validation.md) · [Polski](../../pl/v1.4.1/validation.md) · [Index](README.md)

## Current scope and evidence

The 2026-11-18 audit covers BOOT/installer sources and binaries, APP retry after interrupted metadata commit, refusal of unrelated data, five UART rates and saved-code migration, protected ranges, two SD backups, physical gestures, ST-Link planning/full readback, M3B integrity, host tools, three-package consistency, checksums and EN/PL instructions.

[AUDIT_2026-11-18.json](../../reports/v1.4.1/AUDIT_2026-11-18.json) records the checks actually performed and their outcomes. [HARDWARE_STATUS.json](../../reports/v1.4.1/HARDWARE_STATUS.json) separates baseline 1.4 hardware history from the new patch. The [1.4.1 manifest](../../../firmware/v1.4.1/RELEASE_MANIFEST.json) identifies exact download lengths and hashes.

The owner reported about two weeks of using **1.4**. The **1.4.1** fix was written during this audit and has separate offline validation. Historical totals of 2784 tests and 51/59 checks from the 1.4 publication remain evidence for that publication; changing a version number does not make them a newly executed result.

## Offline results — 2026-11-18

| Check | Result | Scope |
|---|---|---|
| Private BOOT/installer regression suite | **2992 passed, 34 skipped, 0 failed** | The 34 skipped cases concern write phases in READONLY mode; they are not counted as passes. |
| Independent clean rebuild | **59 checks passed** | FULL, READONLY and PREVIEW BOOT builds plus the installer reproduced byte-identical output. |
| Compiled ARM metadata predicate | **105 cases passed** | The actual compiled board/metadata decision code was executed in Unicorn. This is an isolated predicate check, not a complete boot or physical-printer test. |
| Public host-tool unit tests | **13 passed** | Includes service-card checks, exact INFO acceptance, partial-resource cleanup and preservation of the manifest/archive on close failure. |

These are newly executed computer checks for 1.4.1. Details and tooling are recorded in the [audit report](../../reports/v1.4.1/AUDIT_2026-11-18.json). They do not establish hardware acceptance or a two-week test history for the new patch.

## Repeating the public checks

From the repository root, with Python 3.9 or later:

```sh
sha256sum -c SHA256SUMS.txt
python3 tools/validate_publication.py --json
```

On macOS use `shasum -a 256 -c SHA256SUMS.txt` for the first command. For one downloaded ZIP in PowerShell, run `Get-FileHash -Algorithm SHA256 <file.zip>` and compare the full digest with the [release list](../../../firmware/v1.4.1/SHA256SUMS.txt).

Public validation checks the distributed packages, formats, addresses, tools and documentation. Private firmware code and tests requiring it are not in the public repository. Check totals for hashes/HEX records include many byte-level assertions; they do not represent the same number of independent printer behavior scenarios.

## What the metadata fix must establish

- A missing valid commit still prevents launching APP.
- Retry is limited to a verified candidate consistent with the interrupted record and the complete APP image in Flash.
- Unrelated metadata, a different image, wrong digest or damaged APP do not obtain general permission to erase.
- Reinstallation still requires the qualified profile and fresh physical 2-second confirmation.
- OEM prefix, BOOT, setting journals and manufacturer data remain outside APP writes.

Actual scenario results and the toolchain used are recorded in the audit report. Passing them does not promise automatic recovery from every interrupted write or firmware rollback after power loss.

## Documentation completeness

The full baseline 1.4 reference is retained: 13 BOOT pages, 50 initial positions, 27 command forms, eight DUMP regions, seven intermediary items and nine intermediary command forms. Versions, package names, `INSTALL V141`, results and APP retry procedure are described for 1.4.1. The [complete reference](features-and-console.md) and [installation procedure](installation.md) are available in both languages.

The [29 current OLED renders](../../assets/v1.4.1/README.md) execute the 1.4.1 C renderer with the original packed font and documented example inputs. Native output is 256×64 pixels; previews are exact 4× nearest-neighbour enlargements in cyan on black. The [render manifest](../../assets/v1.4.1/RENDER_MANIFEST.json) records source and image hashes; [render validation](../../assets/v1.4.1/RENDER_VALIDATION.json) records native menu/confirmation execution and PNG readback checks. These illustrations do not establish a successful printer operation or replace hardware testing.
