# Preserve the original device — M300Boot v1.3.1

[Polski](KOPIA_ORYGINALU_PL.md) · [Installation](INSTALLATION_EN.md)

Keep two independently read, matching backups before any destructive change. Preserve original 32-KiB BOOT, final 8-KiB NVM/factory data, full 256-KiB Flash where available, UID, measured SIZE and Option Bytes. Store copies on two physical media. These files, serial-bearing screens and UART logs are private.

## Original printer with active RDP

Use the existing [UART backup diagnostic 0.5.5 procedure](../v1.1/ORIGINAL_BACKUP_EN.md) and the unchanged `M300_BACKUP_0.5.5_UART.zip` supplied beside this release. Its diagnostic installation replaces APP first. A later full-Flash export is therefore **post-update**, with original BOOT/NVM retained but diagnostic APP, not a pristine pre-update snapshot. The exact original stock 1.3.1 application is separately supplied in `RESTORE.BIN`.

The diagnostic uses its own `read_flash_m300_055.py` receiver, not the v1.3.1 boot console. Follow that version's backup steps only; use the new installation manual for installing v1.3.1. Do not disable STM32F1 read protection to obtain a backup: **Read Unprotect mass-erases main Flash**. A failed SWD read is not a request to remove RDP.

## Already running M300Boot v1.3.1

Enter the service menu with the knob. Close Klipper and every other UART client on that port. Read-only console backup:

```sh
bash tools/KONSOLA_M300_v1.3.1.command --port /dev/cu.usbmodem14203 --baud 250000 --dump-all
```

The port is an example. Match the active rate, or hold the knob at power-on for temporary 250000. The command makes two independent reads for each fixed region, compares A/B, and checks overlapping regions against the full Flash export. It never programs the MCU. Its generated directory/archive and `MANIFEST.json` are private.

## Installer SD copies

The six-file SD sets include four **A5 templates**, not existing backups. The intermediary fills them through `Backup Flash x2` and verifies identity, SHA-256, CRC and equality. Preserve all four completed files together:

| Snapshot | Flash | Information |
|---|---|---|
| A | `M3FLASH.BIN` — 262144 B | `M3INFO.BIN` — 1024 B |
| B | `ZBACK2.BIN` — 262144 B | `ZINFO2.DAT` — 1024 B |

```sh
python3 tools/verify_sd_i2.py --backups "/path/to/completed-backups"
```

Require `PASS_SD_V131_BACKUPS_X2`. This checker applies the retained installation profile and protected-RDP options; an RDP0 SWD snapshot uses the ST-Link preflight instead. Never overwrite completed backup files by copying fresh release templates over them. Copies made by the intermediary describe the state **after** the intermediary APP was installed and **before** BOOT replacement.

## SWD reads when RDP is already off

Use [ST-Link](STLINK_AND_RECOVERY_EN.md): two actual 256-KiB reads, UID and options, measured SIZE 256 KiB. A duplicated file is not a second read. The new STLINK archive contains only address-specific segments and cannot reconstruct an erased whole chip. Recovery from a complete private snapshot must retain that same printer's original prefix, factory data and NVM; it is a separate planned procedure.
