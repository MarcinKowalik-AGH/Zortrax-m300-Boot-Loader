# M300Boot v1.3.1 — 2026-10-30

[English](../../en/v1.3.1/release-notes.md) · [Polski](../../pl/v1.3.1/release-notes.md) · [Index](README.md)

Independent service bootloader for **classic Zortrax M300, Rev.5.3 / HW05 / measured 256 KiB**. Permanent BOOT and OLED installer version: **1.3.1**. The owner confirmed **UPGRADE, FACTORY and ST-Link** on hardware, and an active **1500000-baud UART8** link. The qualified per-device gates remain.

- New visible rate sequence: **115200 → 250000 → 500000 → 750000 → 1000000 → 1500000**. Legacy 19200/57600 records remain readable; 2000000 is not supported.
- Persistent **UART on bootwait OFF/ON**. OFF ignores host RX during autostart; ON admits complete allowed diagnostic lines. Binary Klipper traffic does not stop the countdown.
- Corrected local baud-change busy handling, partial-line cleanup and settings-screen isolation from host probes. Real operation/refusal guards remain.
- Incremental OLED updates, direct detent navigation, pinned Back and bounded scrolling retained and reviewed; progress reports measured phases.
- 1.3 → 1.3.1 preserves baud and bootwait journals, metadata and NVM. Empty journals default to 250000/OFF. Knob-at-start recovery is temporary 250000.
- Public UPGRADE, FACTORY and **two-segment STLINK** packages, updated public console/checkers, complete paired PL/EN manuals, checksums and native renderer previews. Historical v1.1 assets/tags are unchanged.

**SD migration replaces APP with the intermediary first; restore `RESTORE.BIN` or your matching MCU M3B afterwards. ST-Link preserves APP.** The standalone Klipper waiting screen belongs to the separate MCU APP; this publication is bootloader-only. 2941 boot/installer tests were re-run successfully; public package checks are in the publication validation report. No power-loss rollback or general print qualification is claimed.
