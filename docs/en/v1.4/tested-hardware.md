# Hardware and acceptance — M300Boot 1.4

[English](../../en/v1.4/tested-hardware.md) · [Polski](../../pl/v1.4/tested-hardware.md) · [Index](README.md)

M300Boot **1.4** is for the qualified classic M300 HW05 / PCB Rev.5.3 / measured 256-KiB profile. BOOT, the SD installer, stock application and Klipper MCU application have separate roles. The 1.4 release is validated offline; its rebuilt firmware still requires physical acceptance on the printer. Earlier hardware reports belong to the archived 1.3.1 build.

## Target and protected memory

| Item | Scope |
|---|---|
| Printer | Classic M300 HW05 / PCB Rev.5.3 |
| MCU / memory | STM32F103-family; measured 256 KiB Flash, 2-KiB pages |
| Display | Native 256×64 OLED and pushbutton rotary encoder |
| Installation profile | Existing device/UID/options/factory checks retained |
| Preserved regions | OEM prefiks 0x08000000–0x08000FFF; APP for ST-Link; settings and manufacturer NVM outside the two target slots |

## Evidence and physical acceptance

1.4 rebuild and package checks are offline. [Validation](validation.md) links the current machine-readable report. Physical FACTORY/UPGRADE/ST-Link and UART1500000 reports for 1.3.1 remain in the [archive](../v1.3.1/tested-hardware.md); they are not re-labelled as 1.4 hardware results.

On the qualified printer, separately confirm each installation route used, boot and installer identity 1.4, the five UART entries, default 250000/bootwait OFF, supported saved-rate persistence, explicit migration of removed rates, restart and correct APP restoration. Compare the expected physical displays with the cyan illustrations, which are generated renders rather than photographs. UART tests must check both directions and status after restart. A successful boot does not qualify a different PCB, unreported MCU, or all motion/heater/printing behavior.

Keep raw identity data, logs and personal Flash snapshots private. Publish only the acceptance result and non-identifying observations.
