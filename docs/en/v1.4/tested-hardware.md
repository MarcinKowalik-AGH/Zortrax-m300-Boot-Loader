# Hardware and acceptance — M300Boot 1.4

[English](../../en/v1.4/tested-hardware.md) · [Polski](../../pl/v1.4/tested-hardware.md) · [Index](README.md)

M300Boot **1.4** is for the qualified classic M300 HW05 / PCB Rev.5.3 / measured 256-KiB profile. BOOT, the SD installer, stock application and Klipper MCU application have separate roles. The 1.4 release is validated offline, and the owner confirmed FACTORY, UPGRADE and ST-Link installation on the printer, recorded on 2026-11-09. [Owner acceptance](../../reports/v1.4/HARDWARE_ACCEPTANCE.json) is separate from earlier archived 1.3.1 reports.

The distributed installers retain a device-specific UID / OEM-prefix / factory-data qualification. Matching the M300 model, HW05 or PCB Rev.5.3 alone does not qualify another printer; a profile refusal must be resolved from its own verified backup rather than bypassed.

## Target and protected memory

| Item | Scope |
|---|---|
| Printer | Classic M300 HW05 / PCB Rev.5.3 |
| MCU / memory | STM32F103-family; measured 256 KiB Flash, 2-KiB pages |
| Display | Native 256×64 OLED and pushbutton rotary encoder |
| Installation profile | Existing device/UID/options/factory checks retained |
| Preserved regions | OEM prefiks 0x08000000–0x08000FFF; APP for ST-Link; settings and manufacturer NVM outside the two target slots |

## Evidence and physical acceptance

1.4 rebuild and package checks are offline. The owner separately reported on-printer validation of all three installation methods; this is recorded in [HARDWARE_ACCEPTANCE.json](../../reports/v1.4/HARDWARE_ACCEPTANCE.json).

| 1.4 installation method | Hardware result | Evidence |
|---|---|---|
| FACTORY OEMv3 | Confirmed by owner | Statement recorded 2026-11-09 |
| UPGRADE | Confirmed by owner | Statement recorded 2026-11-09 |
| ST-Link | Confirmed by owner | Statement recorded 2026-11-09 |

This report confirms the three installation routes. Individual tests of every UART rate, motion, heating, printing and restoration of the original OEM BOOT were not separately reported. The immutable release manifest and initial offline reports retain their publication-time status; the later owner report adds the hardware result. Earlier 1.3.1 evidence remains in the [archive](../v1.3.1/tested-hardware.md).

For any additional hardware acceptance, record each installation route used, boot and installer identity 1.4, the five UART entries, default 250000/bootwait OFF, supported saved-rate persistence, explicit migration of removed rates, restart and correct APP restoration. Compare the expected physical displays with the cyan illustrations, which are generated renders rather than photographs. UART tests must check both directions and status after restart. A successful boot does not qualify a different PCB, unreported MCU, or all motion/heater/printing behavior.

Keep raw identity data, logs and personal Flash snapshots private. Publish only the acceptance result and non-identifying observations.
