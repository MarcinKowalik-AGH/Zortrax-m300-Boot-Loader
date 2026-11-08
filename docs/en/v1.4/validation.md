# Validation — M300Boot 1.4

[English](../../en/v1.4/validation.md) · [Polski](../../pl/v1.4/validation.md) · [Index](README.md)

## Scope

The release audit covers compiled BOOT and intermediary, executable version identifiers, exactly five rates, default 250000, recovery speed, journal compatibility, removed-rate fallback, update sources, protected ranges, two independent SD backups, guarded confirmations, ST-Link plan/readback, M3B integrity, packaged tools, checksums, documentation links and rendered OLED evidence.

The report distinguishes software checks from physical operation. The linked data record the actual checks executed; archived test counts and old hardware confirmations are not reused as new 1.4 results.

## Reproduce the public checks

From the public repository root, with Python 3.9 or later:

```sh
sha256sum -c SHA256SUMS.txt
python3 tools/validate_publication.py --json
```

The release [manifest](../../../firmware/v1.4/RELEASE_MANIFEST.json) records component identities; [SHA-256 list](../../../firmware/v1.4/SHA256SUMS.txt) identifies downloadable files. [Current report](../../reports/v1.4/PUBLICATION_VALIDATION.json) provides results and limitations. Public checks independently verify archive contents, segment addresses, exact hashes, host behavior and instructions. Private firmware tests and rendering source remain excluded from the public tree.

## Limits

No probe or printer is opened by offline publication checks. Physical acceptance of rebuilt 1.4 must follow [the target matrix](tested-hardware.md). There is no automatic rollback after loss of power during BOOT programming. Existing device identity and protection gates remain. A software PASS does not establish compatibility with every M300 board or print-load headroom.

Final offline validation: **2784 tests passed, 0 failed, 0 skipped**; **51 BOOT binary checks** and **59 installer / clean rebuild checks** passed. All three BOOT variants and the intermediary rebuild byte-for-byte with Clang/LLD 19.1.1. Physical acceptance of 1.4 remains pending.

## Documentation completeness review — 2026-11-09

A follow-up source review covers all 13 BOOT pages / 50 initial menu positions, 27 BOOT command forms, eight DUMP regions, seven intermediary options and nine intermediary command forms. The public inventory records the matching source hashes. The added check prevents an option or accepted command from silently disappearing from either language; semantic correctness and procedure order were additionally reviewed against the implementation. Firmware packages were not changed.

[Inventory](../../reports/v1.4/DOCUMENTED_OPTIONS.json) · [Review report](../../reports/v1.4/DOCUMENTATION_REVIEW.json)

```sh
python3 tools/validate_option_coverage.py --json
```
