# Original Zortrax Bootloader v3 — classic M300

[English](README.md) · [Polski](README_PL.md)

[Download OEM_BOOT_V3.bin](OEM_BOOT_V3.bin) · [Manifest](MANIFEST.json) · [SHA-256](SHA256SUMS.txt)

This is the unmodified **32-KiB original Zortrax Bootloader v3** retained in the M300 project archive. It is published separately from M300Boot 1.4.

| Property | Value |
|---|---|
| File | `OEM_BOOT_V3.bin` |
| Format | Raw binary, 32768 bytes |
| Original Flash range | `0x08000000–0x08007FFF` |
| Embedded identification | `Zortrax Bootloader v3` |
| Initial stack pointer | `0x20003FF0` |
| Reset vector, Thumb | `0x08000165` |
| Recorded target | Classic M300, HW05 / PCB Rev.5.3 / STM32F103-family / measured 256-KiB Flash |

SHA-256:

```text
dcc69ce6ad7d4ca46ba9363239f1f39863559e286fa3e53abfeb5eb47c82de3a
```

## Provenance and verification

The file is preserved from `04_OEM_ROLLBACK/OEM_BOOT_V3.bin` in the retained `M300Boot_v1.3.1_KOMPLET_2026-10-30.zip` project archive. It matches both the private reference copy and the first 32768 bytes of the retained original Flash image, byte for byte. These are consistency checks of retained project material, not three new independent device reads. No bytes were patched or reconstructed.

From the repository root, verify the published file with Python 3.9 or later:

```sh
python3 tools/validate_original_boot.py --json
```

For a standalone download, compare its SHA-256 with the value above. Within this directory, `sha256sum -c SHA256SUMS.txt` also checks the manifest and both descriptions.

## File scope

The stated address describes where this original BOOT resides. This raw image is not an SD update package, a complete printer image, or the stock application `RESTORE.BIN` (Zortrax M300 1.3.1). It contains only the BOOT range, without APP, the final manufacturer NVM/data region, UID or Option Bytes. It does not replace the printer's own independent backups or establish compatibility with other boards, Plus, Dual or Inventure.

The owner's [three-method acceptance of M300Boot 1.4](../../docs/en/v1.4/tested-hardware.md) concerns FACTORY, UPGRADE and ST-Link installation of the custom bootloader. Restoration of this OEM image has not been separately reported as tested. For the existing installation and recovery procedures, use the [current manual](../../docs/en/v1.4/README.md).

Manufacturer firmware retains its original rights; the project's MIT notice does not relicense this binary. See [third-party notices](../../THIRD_PARTY_NOTICES.md).
