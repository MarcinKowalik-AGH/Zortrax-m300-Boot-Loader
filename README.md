# M300Boot 1.5 — classic Zortrax M300

[English](README.md) · [Polski](README_PL.md)

Independent service bootloader by **Marcin Kowalik** · mkowalik@agh.edu.pl. Target: **classic M300, HW05 / PCB Rev.5.3 / STM32F103-family / measured 256 KiB Flash**. Both permanent BOOT and SD installer identify as **1.5**.

Exactly five UART rates: **115200, 250000, 500000, 750000, 1500000**, 8N1. Default **250000**, UART on bootwait **OFF**. Supported saved choices survive upgrade. Old unsupported records fall back to 250000 in BOOT; explicitly save 250000 before launching an older APP that independently reads those records.

The distributed installers retain a device-specific UID / OEM-prefix / factory-data qualification. Matching the M300 model, HW05 or PCB Rev.5.3 alone does not qualify another printer; a profile refusal must be resolved from its own verified backup rather than bypassed.

## Download and installation order

| Current state | Package |
|---|---|
| Recognized custom M300Boot | [SD_UPGRADE](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_SD_UPGRADE.zip) |
| Qualified original OEMv3 | [SD_FACTORY_OEMV3](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_SD_FACTORY_OEMV3.zip) |
| SWD reads working, RDP already off | [STLINK — two addressed segments](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_STLINK.zip) |

[Release 1.5](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.5) · [SHA-256](firmware/v1.5/SHA256SUMS.txt) · [Full English instructions](docs/en/v1.5/README.md).

**SD order:** preserve independent backups → install and launch the intermediary → check board/card → create and verify two Flash backups → separately confirm BOOT replacement → restart into BOOT 1.5 → explicitly restore the intended stock or Klipper APP. [Step-by-step guide](docs/en/v1.5/installation.md).

![BOOT startup: M300 boot v1.5](docs/assets/v1.5/BOOT_COUNTDOWN.png)
![About: Version v1.5](docs/assets/v1.5/BOOT_ABOUT_MENU.png)
![SD installer 1.5, native-font render](docs/assets/v1.5/INSTALLER_MAIN_MENU.png)

The screenshots are generated from the 1.5 OLED code. **Field history: the owner reports about two weeks of use of baseline 1.4**, with all three installation routes already accepted on 2026-11-09. **The 1.5 binaries carry forward the audited 1.4.1 fixes with a new version identity and their own offline checks. They have not accumulated two weeks of hardware testing.** [Hardware status](docs/reports/v1.5/HARDWARE_STATUS.json) · [Audit and validation](docs/en/v1.5/validation.md).

## What release 1.5 contains

The audited APP/host fixes from 1.4.1 are retained. BOOT startup, About, the SD installer and UART identify as **1.5**; use `INSTALL V15` in the installer. Version 1.4.1 remains available as an archived release.

- Restores a constrained retry after an interrupted APP metadata commit: the same verified candidate, matching complete Flash payload, a recognized torn record and physical consent are required. Ordinary boot still rejects an incomplete commit.
- Uses the existing unused space before the fixed OEM hook for the recovery checks; protected memory boundaries remain unchanged.
- Checks all existing service-card destinations before creating missing templates, and reliably closes UART logs after connection errors.
- Provides matching instructions inside the ST-Link ZIP, direct download links and complete English/Polish manuals.

**UART 1,000,000 and 10,000,000 are not selectable.** Removal of 1,000,000 was already present in 1.4 and is retained. The default remains 250000; keep the host and MCU settings matched.

## Use and recovery

- [Original Zortrax Bootloader v3 — 32-KiB binary, provenance and SHA-256](firmware/original/README.md)
- [Preserve original memory](docs/en/v1.5/original-backup.md)
- [Menus and console](docs/en/v1.5/features-and-console.md)
- [UART settings and migration](docs/en/v1.5/uart-examples.md)
- [ST-Link addresses and complete readback](docs/en/v1.5/stlink-and-recovery.md)
- [Troubleshooting](docs/en/v1.5/troubleshooting.md)
- [Public tools](tools/README.md) · [Downloads](firmware/README.md) · [Changelog](CHANGELOG.md)

BOOT stage2 occupies **0x08001000–0x08007FFF**; assets **0x0803A000–0x0803CFFF**. ST-Link preserves APP. SD migration temporarily replaces APP and requires restoration. Original first 4 KiB, manufacturer NVM, device checks and protected settings remain. No automatic power-loss BOOT rollback is provided. Do not remove active RDP to obtain a backup.

`RESTORE.BIN` remains original **Zortrax M300 1.3.1**. Independent backup diagnostic remains **0.5.5**. Klipper MCU/host is a separate package. Their different version numbers are intentional.

[All documentation and archives](docs/en/README.md) · [Archived 1.4.1](docs/en/v1.4.1/README.md) · [Archived 1.4](docs/en/v1.4/README.md) · [Archived 1.3.1](docs/en/v1.3.1/README.md) · [Archived 1.1](docs/en/v1.1/README.md). Binary firmware, host tools and manuals are public; private firmware sources, OEM-key tools and personal Flash/identity data are excluded. [Distribution notices](THIRD_PARTY_NOTICES.md). Classic M300 only; Plus, Dual and Inventure are separate targets.
