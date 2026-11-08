# Backups — M300Boot 1.4

[English](../../en/v1.4/original-backup.md) · [Polski](../../pl/v1.4/original-backup.md) · [Index](README.md)

Preserve original 32-KiB BOOT, final 8-KiB manufacturer NVM/data, full 256-KiB Flash where available, UID, measured SIZE and Option Bytes. Obtain two independent matching reads, rather than duplicating one file, and store copies on two media. Do not publish serial-bearing screens, logs or device dumps.

## Before changing an original printer

With active RDP, follow the unchanged [diagnostic 0.5.5 instructions](../v1.1/original-backup.md). That diagnostic replaces APP first. A full Flash dump obtained afterwards contains diagnostic APP; it is not a pristine pre-update factory image. Original BOOT/NVM are preserved, and stock application 1.3.1 is separately supplied in `RESTORE.BIN`. Use `read_flash_m300_055.py` for diagnostic 0.5.5 and the 1.4 instructions for installing BOOT. Do not remove STM32F1 RDP to read memory: Read Unprotect erases main Flash.

## From BOOT 1.4

Stop Klipper and other UART clients. Enter the local menu and run:

```sh
bash tools/KONSOLA_M300_v1.4.command --port /dev/cu.usbmodem14203 --baud 250000 --dump-all
```

The port is an example. Match the active baud; holding the knob at power-on temporarily selects 250000. The read-only tool obtains paired fixed-region exports and checks overlapping regions against full Flash. Keep its output and manifest private.

## Installer backups

| Copy | Flash file | Information file |
|---|---|---|
| A | `M3FLASH.BIN` — 262144 B | `M3INFO.BIN` — 1024 B |
| B | `ZBACK2.BIN` — 262144 B | `ZINFO2.DAT` — 1024 B |

The installer fills the four A5 templates during `Backup Flash x2`, verifies both snapshots and retains the session qualification. These copies describe the state after the intermediary APP was installed, before BOOT replacement. Check completed copies with `python3 tools/verify_sd_i2.py --backups "/private/completed-backups"`. Never replace them with fresh templates.

With RDP already off, use the [ST-Link preflight](stlink-and-recovery.md) for two genuine Flash reads, UID and options. The two-segment package does not reconstruct a fully erased chip.
