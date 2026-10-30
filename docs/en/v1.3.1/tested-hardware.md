# Hardware and evidence — M300Boot v1.3.1

[English](../../en/v1.3.1/tested-hardware.md) · [Polski](../../pl/v1.3.1/tested-hardware.md) · [Index](README.md)

**Report date: 30 October 2026.**

| Parameter | Established value |
|---|---|
| Printer | Classic Zortrax M300, PCB Rev.5.3 / HW05 |
| MCU | STM32F103-family Cortex-M3 high-density; exact ordering code not established |
| Silicon / CPUID | Device ID 0x414 / Rev X; CPUID 0x411FC231 |
| Flash | Measured 256 KiB / 262144 B, 128 × 2048-B pages; an old GUI label of 512 KB was not the accepted measurement |
| Original BOOT / APP | OEM v3 / Zortrax M300 1.3.1; independent version numbers |
| Display / input | Native 256×64 OLED and rotary encoder with pushbutton |
| Confirmed host link | Orange Pi Zero UART1, observed 24-MHz UART clock; `/dev/ttyS1` in the owner's setup |
| Compatible application reported | UART8, later `0.13.3-TEST01-OLED-R32-UART8`; host OLED-R3.2 |
| Installation gate | Retained per-device UID/options/factory-page hashes; HW05 alone is insufficient |

## Test matrix

| Route or function | Status | Evidence |
|---|---|---|
| UPGRADE to v1.3.1 | **Hardware confirmed** | Owner's installed-boot and operating-MCU reports |
| FACTORY | **Hardware confirmed** | Explicit owner confirmation on 30 October 2026 |
| ST-Link | **Hardware confirmed** | Explicit owner confirmation on 30 October 2026 |
| UART 1500000, saved index 7 | **Confirmed** | MCU and host 1500000, match true, saved 1, index 7, fault 0 |
| Standalone waiting OLED and display link | **Accepted** | Owner closed this stage after UART8/OLED-R3.2 tests |
| BOOT / installer software | **2941 tests PASS** | 2116 BOOT + 825 installer/ST-Link/migration tests re-run for the publication |

FACTORY and ST-Link confirmation comes from the owner's hardware reports. It supersedes the previous unconfirmed status for the current release. [Historical v1.1 evidence](../v1.1/tested-hardware.md) retains its original date and scope.

No raw serial, UID, private log or unreported second-board parameters are inferred or published. These confirmations do not establish all M300 boards, power-loss recovery, all baud/reboot combinations, motion/heating qualification or printing headroom. Installation identity gates remain intact.
