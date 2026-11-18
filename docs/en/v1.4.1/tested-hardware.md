# Hardware and evidence scope — M300Boot 1.4.1

[English](../../en/v1.4.1/tested-hardware.md) · [Polski](../../pl/v1.4.1/tested-hardware.md) · [Index](README.md)

This release targets **classic Zortrax M300** with the qualified HW05 / PCB Rev.5.3 / measured 256-KiB profile. Matching the model or board label does not replace UID, option-byte, OEM-prefix and factory-data checks. Resolve a profile refusal from the printer's own verified backups; do not remove identity checks.

## Hardware and preserved regions

| Item | Scope |
|---|---|
| Printer | Classic M300; Plus, Dual and Inventure are separate targets |
| MCU / memory | STM32F103 family; measured 256 KiB Flash, 2-KiB pages |
| Local interface | Native 256×64 OLED and rotary encoder with button |
| Installation qualification | Device, UID, options and factory-data checks remain |
| First 4 KiB | OEM prefix 0x08000000–0x08000FFF is preserved |
| BOOT writes | Stage2 0x08001000–0x08007FFF; assets 0x0803A000–0x0803CFFF |
| Other memory | ST-Link preserves APP; setting journals and manufacturer NVM remain outside the BOOT segments |

## Hardware history and the new patch

| Version / evidence | Confirmed scope | Meaning for 1.4.1 |
|---|---|---|
| 1.4 — owner acceptance recorded 2026-11-09 | FACTORY, UPGRADE and ST-Link completed on the printer | Evidence for baseline 1.4 |
| 1.4 — owner report on 2026-11-18 | About two weeks of use/testing | Owner-reported duration, without an inferred exact start date or continuous operating hours |
| 1.4.1 — current audit | New patch code, tools and packages covered by the offline checks in the report | Separate validation of the new release; historical two-week duration is not assigned to it |

[Current hardware status](../../reports/v1.4.1/HARDWARE_STATUS.json) · [Historical 1.4 acceptance](../../reports/v1.4/HARDWARE_ACCEPTANCE.json) · [1.4.1 audit report](../../reports/v1.4.1/AUDIT_2026-11-18.json).

The new patch addresses APP reinstallation after an interrupted final metadata write. Computer checks can reproduce interruptions and reject mismatching images; they are not physical power-cut tests on the printer. When later recording 1.4.1 hardware acceptance, preserve the BOOT/installer version, route, APP restoration result and baud used. Keep the printer's raw logs and backups private.

Existing reports do not automatically qualify all boards, every UART rate, motion/heating/printing or restoration of original OEM BOOT. No automatic BOOT rollback after power loss is provided. [APP repair eligibility](installation.md#reinstalling-app-after-an-interrupted-metadata-write) is separate from [BOOT recovery](stlink-and-recovery.md).
