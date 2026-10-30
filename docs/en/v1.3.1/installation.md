# SD installation — M300Boot v1.3.1

[English](../../en/v1.3.1/installation.md) · [Polski](../../pl/v1.3.1/installation.md) · [Index](README.md)

Choose **UPGRADE** for a recognized existing custom M300Boot, or **FACTORY** for the qualified original OEM v3. Retained source hashes cover rc1/rc2/rc3, 1.1, 1.1-u1, 1.2, 1.2.1, 1.3 and 1.3.1. That allowlist does not remove the separate identity/profile checks. Stop Klipper on a connected host before servicing. Keep power stable throughout writes.

## Prepare the card

1. Preserve verified backups on another physical medium. Never replace an existing completed backup with blank templates.
2. Download the matching archive from `firmware/v1.3.1` or the v1.3.1 Release, and check its SHA-256 against that version's manifest. Unzip it into a new folder. The six SD files are at the ZIP root.
3. On a fresh FAT32 card, copy exactly the six files for your route:

| Route | Six files at card root |
|---|---|
| UPGRADE | `M300APP.M3B`, `RESTORE.BIN`, `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT` |
| FACTORY | `Update.bin`, `RESTORE.BIN`, `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT` |

`M3FLASH.BIN` / `ZBACK2.BIN` (262144 B each) and `M3INFO.BIN` / `ZINFO2.DAT` (1024 B each) initially contain **A5 templates, not backups**. The installer checks physical cluster separation before writing. Do not mix `Update.bin` and the boot intermediary's `M300APP.M3B` on one card.

From the repository root, using the current tools:

```sh
python3 tools/verify_sd_i2.py --card "/Volumes/M300_CARD" --route upgrade
# For FACTORY, use --route factory instead.
```

Require `PASS_SD_V131_CARD_FILES`. This is a host file check, not a printer write or FAT-cluster validation.

## UPGRADE: existing custom bootloader

1. Cancel the five-second countdown with the knob and release it.
2. `Firmware on SD → Choose firmware file → M300APP.M3B → Check selected file`.
3. Choose `Install selected file`; release, then hold the knob for 2 s when prompted. This replaces **APP with the intermediary**, not BOOT yet.
4. `Diagnostics → Verify Flash`, then `Start application → Launch application`; confirm the manual launch. The screen must identify **SD installer 1.3.1**.
5. Continue with the common installer transaction below.

## FACTORY: original OEM v3

1. With power off, insert the FACTORY card. OEM may immediately program `Update.bin` at power-on; inserting it is not a read-only detection test.
2. Wait for the stock updater to finish. Power off, remove the card, and start without it. Require **SD installer 1.3.1**. The permanent original boot is still present at this stage. Technical wrapper `9.8.7` is expected and differs from the installer version.
3. In the stable intermediary menu, when no operation is running, reinsert the same card. Continue below without restarting between checks, backup and BOOT replacement.

## Common installer transaction

1. `Check board + SD` → require `CHECK_SOURCE_CARD_RESTORE_OK`.
2. `Backup Flash x2` → require `PASS_SD_FULL_FLASH_X2` in this session. The two independent snapshots include the intermediary already installed as APP; they are not pristine pre-update factory images.
3. `Install / upgrade boot`. For consent: **release → fresh click → release → fresh press and hold 5 s**. Rotation cancels. Do not infer consent from the click that entered the screen.
4. Require `INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED`. An already identical target may take the verified no-write path. Refusal is not permission to edit a hash or remove protection.
5. `Restart to boot`; interrupt the countdown and verify **M300 boot v1.3.1**.
6. Copy the four completed SD backup files to two private storage locations, then check:

```sh
python3 tools/verify_sd_i2.py --backups "/path/to/completed-backups"
```

Require `PASS_SD_V131_BACKUPS_X2`. Keep these files private.

## Restore the printing or Klipper application

SD migration leaves the intermediary in the application slot. Select `RESTORE.BIN` through `Firmware on SD → Choose firmware file`; check it, install it with the 2-s confirmation, verify Flash, then launch. It contains the original stock **Zortrax M300 1.3.1**. Check your hardware information, counter and settings before actuator tests.

For Klipper, replace the card's intermediary `M300APP.M3B` with the **application M3B from your matching MCU package**, then check/install/verify/launch that application. The boot intermediary here is **102280 B**; it is not a Klipper MCU application. This repository intentionally does not bundle the separate MCU/host package.

For 1500000, the MCU and host must support **UART8**. With the host stopped, save the rate under `Diagnostics → UART → UART baud rate`, set the same `[mcu] baud` on the host, restart the printer normally without holding the knob, then start the host. Use bootwait **OFF** for normal Orange Pi autostart. [Detailed UART procedure](uart-examples.md).

There is no power-loss-safe automatic BOOT rollback. `Recover saved boot` requires the still-running intermediary and valid backups from that session. [ST-Link conditions](stlink-and-recovery.md).
