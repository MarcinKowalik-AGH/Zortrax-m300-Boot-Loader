# M300Boot 1.4.1 — documentation

[English](../../en/v1.4.1/README.md) · [Polski](../../pl/v1.4.1/README.md) · [Index](README.md)

**Archived release: 1.4.1.** Service bootloader for the qualified classic Zortrax M300 profile: HW05 / PCB Rev.5.3 / measured 256 KiB Flash.

On 2026-11-18 the owner reported about **two weeks of using baseline 1.4**; earlier acceptance of that version covered FACTORY, UPGRADE and ST-Link. **1.4.1 contains a new fix and has separate offline validation in this audit. It is not described as having two weeks of hardware testing.** [Evidence scope](tested-hardware.md) · [Audit results](validation.md).

Version 1.4.1 corrects controlled reinstallation of the same APP image after an interrupted final metadata write. Device qualification, complete image checks, protected ranges and physical confirmation remain. Read the [precise retry scope](installation.md#reinstalling-app-after-an-interrupted-metadata-write) before use.

## Three installation variants

| Printer state | Download | Instructions |
|---|---|---|
| Qualified original OEM v3 | [SD_FACTORY_OEMV3](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_SD_FACTORY_OEMV3.zip) | [SD installation](installation.md) |
| Recognized, working custom M300Boot | [SD_UPGRADE](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_SD_UPGRADE.zip) | [SD installation](installation.md) |
| SWD reads work, RDP is already off, APP and profile are valid | [STLINK](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_STLINK.zip) | [Two segments and full readback](stlink-and-recovery.md) |

[GitHub release](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.4.1) · [SHA-256](../../../firmware/v1.4.1/SHA256SUMS.txt) · [Manifest](release-manifest.md).

## Complete manuals

- [FACTORY and UPGRADE step by step](installation.md)
- [Original backups, BOOT backup and two installer backups](original-backup.md)
- [All menus, functions and commands](features-and-console.md)
- [UART, saved settings and older-APP migration](uart-examples.md)
- [ST-Link, addresses and full readback](stlink-and-recovery.md)
- [Troubleshooting](troubleshooting.md)
- [Hardware and acceptance scope](tested-hardware.md)
- [Validation and documentation completeness](validation.md)
- [Release changes](release-notes.md)

Exactly five UART rates: **115200, 250000, 500000, 750000, 1500000**, 8N1. **1000000 and 10000000 are not supported choices.** The 1000000 option was already removed in 1.4; 1.4.1 retains that decision. Default **250000 / bootwait OFF**. The owner's Orange Pi divisor incompatibility report is the reason to keep 1000000 off the list; choose a supported value that matches the particular host configuration.

SD installation replaces APP with the intermediary: explicitly restore stock or a matching Klipper application after installing BOOT. ST-Link writes two BOOT segments and preserves APP. The original APP in `RESTORE.BIN` remains **Zortrax 1.3.1**; extra backup diagnostic **0.5.5** is a separate tool, not a fourth installation route. [Baseline 1.4 archive](../v1.4/README.md).

[Current 1.5 documentation](../v1.5/README.md). The 1.4.1 tag and download bytes retain their published identities.
