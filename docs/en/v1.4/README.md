# M300Boot 1.4 — documentation

[English](../../en/v1.4/README.md) · [Polski](../../pl/v1.4/README.md) · [Index](README.md)

**Current release: 1.4.**

M300Boot **1.4** is for the qualified classic M300 HW05 / PCB Rev.5.3 / measured 256-KiB profile. BOOT, the SD installer, stock application and Klipper MCU application have separate roles. The 1.4 release is validated offline, and the owner confirmed FACTORY, UPGRADE and ST-Link installation on the printer, recorded on 2026-11-09. [Owner acceptance](../../reports/v1.4/HARDWARE_ACCEPTANCE.json) is separate from earlier archived 1.3.1 reports.

- [SD installation and update order](installation.md)
- [Original memory and independent backups](original-backup.md)
- [Complete menu, options and console reference](features-and-console.md)
- [UART settings and application handoff](uart-examples.md)
- [ST-Link installation and recovery](stlink-and-recovery.md)
- [Troubleshooting](troubleshooting.md)
- [Hardware scope and acceptance](tested-hardware.md)
- [Validation and release evidence](validation.md)
- [Release files and checksums](release-manifest.md)
- [Release changes](release-notes.md)

Exactly five UART rates: **115200, 250000, 500000, 750000, 1500000**. Default **250000 / bootwait OFF**. Start with backups, select the installation route, complete BOOT installation and then explicitly restore the intended APP. Keep the old releases for historical reference.

[All versions](../README.md) · [Project](../../../README.md)
