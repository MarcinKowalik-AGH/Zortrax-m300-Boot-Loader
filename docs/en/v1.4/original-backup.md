# Backups — M300Boot 1.4

[English](../../en/v1.4/original-backup.md) · [Polski](../../pl/v1.4/original-backup.md) · [Index](README.md)

Preserve original 32-KiB BOOT, final 8-KiB manufacturer NVM/data, full 256-KiB Flash where available, UID, measured SIZE and Option Bytes. Obtain two independent matching reads, rather than duplicating one file, and store copies on two media. Do not publish serial-bearing screens, logs or device dumps.

## Before changing an original printer

With active RDP, follow the unchanged [diagnostic 0.5.5 instructions](../v1.1/original-backup.md). That diagnostic replaces APP first. A full Flash dump obtained afterwards contains diagnostic APP; it is not a pristine pre-update factory image. Original BOOT/NVM are preserved, and stock application 1.3.1 is separately supplied in `RESTORE.BIN`. Use `read_flash_m300_055.py` for diagnostic 0.5.5 and the 1.4 instructions for installing BOOT. Do not remove STM32F1 RDP to read memory: Read Unprotect erases main Flash.

## Before upgrading an existing custom BOOT

Before replacing an older custom BOOT, obtain the independent pre-update reads with the tools matching that running release. For example, the archived 1.3.1 console requires the 1.3.1 banner; the current 1.4 console intentionally requires 1.4 and is not a substitute for it. Use the corresponding [archived instructions](../v1.3.1/original-backup.md) when starting from 1.3.1. The extra installer copies described below supplement these pre-update reads; they do not replace them.

## From BOOT 1.4

Stop Klipper and other UART clients. Enter the local menu and run:

```sh
bash tools/KONSOLA_M300_v1.4.command --port /dev/cu.usbmodem14203 --baud 250000 --dump-all
```

The port is an example. Match the active baud; holding the knob at power-on temporarily selects 250000. The read-only tool obtains paired fixed-region exports and checks overlapping regions against full Flash. Keep its output and manifest private.


## Ordinary BOOT backup to a service card: one pair

`Backup Flash → Backup Flash + identity` in ordinary BOOT produces **one** 256-KiB snapshot and one 1024-byte identity file. It is a different operation from the intermediary's mandatory `Backup Flash x2` and does not qualify an installer session.

1. On a computer, use a separate checked FAT16/FAT32 service card. From the repository root run:

```sh
python3 tools/prepare_service_sd.py "/Volumes/M300_SERVICE"
```

This creates A5-filled `M3FLASH.BIN` (262144 B), `M3INFO.BIN` (1024 B) and optional history storage `M3LOG.BIN` (4096 B). It does not format the card or replace existing files. `KEPT EXISTING` is not proof that an old file is a blank template. Do not use this three-file service preparation as the six-file FACTORY/UPGRADE card preparation.
2. Safely eject the card, insert it in the printer, enter BOOT's local menu, select `Backup Flash → Backup Flash + identity`, release the knob and make a fresh **2-second hold**. Rotation cancels. This writes SD only, not the controller Flash.
3. Wait for completion and the automatic return to the BOOT menu. An error is shown as `Operation rejected`; an optional UART console confirms success with `BACKUP VERIFIED: M3FLASH.BIN + M3INFO.BIN` followed by `DONE OK`. BOOT result/menu timing differs from the intermediary's click-to-close result screens.
4. After the operation finishes and BOOT is in a stable menu, power off, move the card to a computer and copy the pair elsewhere. Verify the copied files:

```sh
python3 tools/m300_service.py verify-backup "/private/backup/M3FLASH.BIN" "/private/backup/M3INFO.BIN"
```

Require exit code 0 and `"verified": true`. The output includes the MCU identity and Option Bytes; keep it private. This verifies this single pair, not two independent reads. The storage layer accepts blank A5 sectors or exactly matching already-copied contents and refuses an incompatible existing snapshot. Never delete the only retained backup to bypass a refusal.

## Installer backups

| Copy | Flash file | Information file |
|---|---|---|
| A | `M3FLASH.BIN` — 262144 B | `M3INFO.BIN` — 1024 B |
| B | `ZBACK2.BIN` — 262144 B | `ZINFO2.DAT` — 1024 B |

The installer fills the four A5 templates during `Backup Flash x2`, verifies both snapshots and retains the session qualification. These copies describe the state after the intermediary APP was installed, before BOOT replacement. Check completed copies with `python3 tools/verify_sd_i2.py --backups "/private/completed-backups"`. Never replace them with fresh templates. The two complete reads and their identity records are made and compared by the installer itself. A reset clears its in-RAM backup qualification even if the files remain on the card; another install attempt requires a new successful `Backup Flash x2` in that session. Do not use `--card` on completed backups: it checks the original A5-template package and will reject changed files by design. Use `--backups` for the completed two-pair set, retaining all four original filenames.

With RDP already off, use the [ST-Link preflight](stlink-and-recovery.md) for two genuine Flash reads, UID and options. The two-segment package does not reconstruct a fully erased chip.

## Published original BOOT

The [original Zortrax Bootloader v3](../../../firmware/original/README.md) retained by the project is available as an unmodified 32-KiB reference image with SHA-256 and provenance. It contains only BOOT and does not replace the full, independent backups of your own printer. The published image is separate from stock application `RESTORE.BIN` and the 1.4 installation packages.
