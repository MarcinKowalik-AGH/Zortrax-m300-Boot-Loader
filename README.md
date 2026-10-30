# M300Boot v1.3.1 — classic Zortrax M300

[English](README.md) · [Polski](README_PL.md)

Independent service bootloader by **Marcin Kowalik** · mkowalik@agh.edu.pl.
Target: **classic M300, PCB Rev.5.3 / HW05 / STM32F103-family / measured 256 KiB Flash**.
Current release: **BOOT 1.3.1, SD installer 1.3.1**, 30 October 2026.

**UPGRADE, FACTORY and ST-Link are owner-confirmed on hardware.** UART8 at **1500000 baud** and standalone/display operation were also confirmed. Installer checks remain tied to the qualified device profile.

## Download and install

| Current device state | Package |
|---|---|
| Recognized existing M300Boot | [SD_UPGRADE v1.3.1](firmware/v1.3.1/M300Boot_v1.3.1_SD_UPGRADE.zip) |
| Original OEM v3, matching profile | [SD_FACTORY_OEMV3 v1.3.1](firmware/v1.3.1/M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip) |
| SWD access, RDP already off | [STLINK v1.3.1 — two addressed segments](firmware/v1.3.1/M300Boot_v1.3.1_STLINK.zip) |
| Preserve original BOOT/NVM under RDP | [UART backup diagnostic 0.5.5](firmware/v1.3.1/M300_BACKUP_0.5.5_UART.zip) |

[Release v1.3.1](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.3.1) · [Installation](docs/en/v1.3.1/installation.md) · [Backup first](docs/en/v1.3.1/original-backup.md) · [SHA-256](firmware/v1.3.1/SHA256SUMS.txt).

Preserve your own verified BOOT/NVM/UID/SIZE/options and independent Flash backups before writes. Removing active STM32F1 RDP erases main Flash; do not use it to obtain a backup. Matching M300/HW05 alone does not satisfy the retained identity checks.

## Features

| Feature | Behavior |
|---|---|
| UART | Ordered menu: **115200, 250000, 500000, 750000, 1000000, 1500000**, 8N1. Saved in Flash with readback; legacy 19200/57600 records remain readable. |
| UART on bootwait | Persistent **OFF/ON**. OFF ignores host RX during countdown; ON admits complete allowed diagnostic lines. Binary Klipper traffic does not interrupt autostart. |
| Settings | Corrected local baud busy handling; host probes and incomplete serial lines cannot take over the local settings screen. Defaults: 250000/OFF. |
| OLED and encoder | Changed-rectangle transfer, identical-frame skip, direct detents, pinned Back and bounded scrolling. |
| Startup | Five-second countdown after initialization; local service entry; holding the knob at power-on temporarily forces 250000. |
| Installation | Guarded SD transaction with two backups and fresh 5-s confirmation; two-segment ST-Link with complete 256-KiB readback. |
| Diagnostics | Device-derived hardware/serial/operating-time records, Flash verification, backups, history and current-phase progress. |

[Full feature description](docs/en/v1.3.1/features-and-console.md) · [UART examples](docs/en/v1.3.1/uart-examples.md) · [ST-Link](docs/en/v1.3.1/stlink-and-recovery.md) · [Troubleshooting](docs/en/v1.3.1/troubleshooting.md).

![M300Boot v1.3.1 menu, rendered by the actual OLED code](docs/assets/v1.3.1/BOOT_MAIN_MENU.png)

The preview is renderer output, not a hardware-test photograph. SD migration leaves the intermediary in APP: restore `RESTORE.BIN` or your intended compatible MCU M3B afterwards. ST-Link preserves APP. BOOT, stock APP and Klipper MCU have separate versions. The separate UART8 MCU/host package supplies the standalone `Waiting for Klipper` screen and is not included in this bootloader repository.

## Documentation

| Location | Contents |
|---|---|
| **[docs/en](docs/en/README.md)** | Complete English manuals, current and archived versions |
| **[docs/pl](docs/pl/README.md)** | Complete Polish manuals, current and archived versions |
| `docs/assets/<version>` | Shared native OLED previews |
| `docs/reports/<version>` | Machine-readable validation evidence |
| [firmware](firmware/README.md) | Versioned downloadable packages and checksums |
| [tools](tools/README.md) | Public host utilities and their scope |

Old documentation URLs remain short compatibility links. New manuals use matching filenames in the two language directories. [Changelog](CHANGELOG.md) · [Hardware evidence](docs/en/v1.3.1/tested-hardware.md) · [Release manifest](docs/en/v1.3.1/release-manifest.md).

## Memory and validation

| Range | Purpose |
|---|---|
| `0x08000000–0x08000FFF` | Preserved OEM prefix, 4 KiB |
| `0x08001000–0x08007FFF` | BOOT stage2, 28 KiB |
| `0x08008000–0x08039FFF` | One APP slot, 200 KiB |
| `0x0803A000–0x0803CFFF` | Assets, 12 KiB |
| `0x0803D000–0x0803D7FF` | APP metadata |
| `0x0803D800–0x0803DBFF` | Separate baud and bootwait journals |
| `0x0803E000–0x0803FFFF` | Manufacturer NVM/data outside normal writes |

The v1.3.1 publication re-ran **2941 BOOT/installer tests** and **94 public-host checks**. This documentation reorganization does not rebuild firmware. [Publication evidence](docs/reports/v1.3.1/PUBLICATION_VALIDATION.json). No automatic power-loss rollback, complete personal Flash image or general print qualification is claimed.

## Previous release and publication scope

[v1.1 manuals](docs/en/v1.1/README.md) · [v1.1 original assets](firmware/v1.1). No synthetic releases are created for private 1.2/1.3 stages. Release tags and original assets retain their published identities.

Binary firmware, operational host tools and documentation are public. Firmware C/ASM, ELF/maps, OEM-key tools and private Flash/NVM/UID/serial data are excluded. `RESTORE.BIN` and manufacturer assets retain their original rights. [Third-party notices](THIRD_PARTY_NOTICES.md) · [License](LICENSE).

Independent project, not endorsed by Zortrax or STMicroelectronics. **Classic M300 only; not M300 Plus, Dual or Inventure.**
