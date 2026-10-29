# M300 boot v1.1 — classic Zortrax M300

**Independent service bootloader · SD installer 1.1-i4**  
**Author / Autor:** Marcin Kowalik · mkowalik@agh.edu.pl

> Publication status: PL/EN documentation is committed. The checked binary packages are prepared, but **the GitHub Release and its attachments have not yet been published**. Final publication uses the supplied local publisher and official GitHub CLI browser authorization. This notice will be replaced by the full download index when publication completes.

## Backup first / Najpierw kopia

**Never remove RDP to obtain a backup. On this STM32F1, removing active read protection erases main Flash.** Preserve two matching images, original BOOT, NVM/factory pages, UID, SIZE and options before migration. Installing a diagnostic intermediary already replaces the printer application; its full dump is post-update, not a pristine factory image.

**[Kopia oryginalnej pamięci — PL](docs/KOPIA_ORYGINALU_PL.md)** · **[Original-memory backup — EN](docs/ORIGINAL_BACKUP_EN.md)**

## Three installation routes

| Existing state | Distribution prepared for v1.1 |
|---|---|
| Recognized original Zortrax Bootloader v3 | SD_FACTORY_OEMV3_i4, starting from Update.bin |
| Recognized existing M300Boot FULL | SD_UPGRADE_i4, starting from M300APP.M3B |
| Deliberate ST-Link installation or recovery | STLINK_LOCAL_BUILDER: exact stage2/assets and a local PERSONAL-image builder using your own backup |

**Important:** the unchanged i4 installers are **locked to one qualified device profile**, including identity/options/factory-page hashes. HW05 alone does not establish compatibility. Do not patch safety gates, copy another printer's identity or erase data to force acceptance.

[Instalacja PL](docs/INSTALACJA_PL.md) · [Installation EN](docs/INSTALLATION_EN.md)  
[ST-Link i odzyskiwanie PL](docs/STLINK_I_ODZYSKIWANIE_PL.md) · [ST-Link and recovery EN](docs/STLINK_AND_RECOVERY_EN.md)  
[Funkcje i Hardware PL](docs/FUNKCJE_I_KONSOLA_PL.md) · [Features EN](docs/FEATURES_AND_CONSOLE_EN.md)  
[Tested hardware / Przetestowany sprzęt](docs/TESTED_HARDWARE.md) · [Release scope](docs/RELEASE_MANIFEST.md)

## Tested configuration

One **classic M300**, mainboard **Rev.5.3**, menu hardware **05**, STM32F1 high-density device ID **0x414 / Rev X**, measured **256 KiB Flash**. Original loader **OEM v3**, printer firmware **1.3.1**. The exact full MCU part marking was not reliably read; no VDT6/VET6 ordering code is asserted.

The owner confirmed successful **UPGRADE through installer 1.1-i4 to M300 boot v1.1**, followed by restoration and startup of original **Zortrax 1.3.1**. The factory-entry i4 and ST-Link routes are separately documented, not separately hardware-qualified. No power-loss, general printing or other-board guarantee is claimed.

## Functions and preservation

OLED header `M300 boot v1.1 © Marcin Kowalik`; responsive non-wrapping encoder menus; Hardware information decoded from current records; progress rings; cancellable 5-second autoboot; checked SD/UART application updates; persistent UART baud; backups, diagnostics and service history.

The original first **4 KiB** remain. Stage2 is at 0x08001000, assets at 0x0803A000; the replaceable application starts at 0x08008000 with **200 KiB capacity**. Final **8 KiB at 0x0803E000** retain manufacturer settings and identity. ST-Link recovery must use a complete personal reconstruction, not a foreign full-Flash image.

Public scope follows Inventure: binary firmware, operational host tools, instructions/checksums and non-identifying UI previews. No firmware C/ASM, ELF/maps, private raw UID/NVM/full-Flash dumps, serial-bearing screenshots or vendor-key tools. Manufacturer firmware in RESTORE.BIN retains its own rights. Independent project; not endorsed by Zortrax or STMicroelectronics.
