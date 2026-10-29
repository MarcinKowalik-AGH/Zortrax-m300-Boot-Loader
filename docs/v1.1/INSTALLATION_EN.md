# M300 boot v1.1 — factory and upgrade installation

Target: **classic M300, Rev.5.3/HW05, measured 256 KiB, matching i4 device profile**. Read [original backup](ORIGINAL_BACKUP_EN.md) and [hardware scope](TESTED_HARDWARE.md) first. Not for Plus, Dual or Inventure. Matching model text alone is insufficient: this unchanged installer is identity-locked.

## Select and prepare the route

Use **FACTORY OEMV3 i4** only with recognized original Zortrax Bootloader v3. Use **UPGRADE i4** with recognized custom M300Boot FULL rc1/rc2/rc3/v1.1. Use the separate [ST-Link procedure](STLINK_AND_RECOVERY_EN.md) for deliberate SWD installation/recovery.

Extract one SD ZIP to fresh FAT32 root (FAT16 also supported; not exFAT). Keep previous real backups elsewhere. There are six files: **Update.bin OR M300APP.M3B**, RESTORE.BIN, M3FLASH.BIN, M3INFO.BIN, ZBACK2.BIN, ZINFO2.DAT. Never mix both route packages. Four backup files start as A5 templates; they are not real backups. Both Flash files are **256 KiB**, not Inventure's 32-KiB boot-only files.

```sh
bash tools/SPRAWDZ_M300_SD_I4.command --card "/Volumes/M300" --route upgrade
# use --route factory for the factory set
```

`PASS_SD_I4_CARD_FILES` checks files, not physical FAT chains or the board. Run `tools/check_backup_profile.py` against your private verified backups **before installing the intermediary**. A mismatch is a stop condition, not permission to patch the checks.

## A. Enter from original OEM v3

1. Insert the FACTORY card with power off; allow the normal OEM update to complete. It may start automatically, so inserting the card is not a harmless recognition test.
2. After actual completion, switch off, remove the card, and power on without it. **M300 SD installer 1.1-i4** should start.
3. When its menu is idle, reinsert the same FACTORY card. Continue with the common procedure below.

The OEM bootloader remains until the separate replacement step. Installing the intermediary already replaces the stock printing application; later backups are not pristine pre-update full images. **Owner feedback:** FACTORY reportedly worked on a second printer; without the second unit’s hardware details and completion log this is not independent verification of each stage or universal compatibility. See [hardware feedback](HARDWARE_FEEDBACK_2026-10-29.md).

## B. Enter through an existing custom M300Boot

1. Insert UPGRADE card with power off; boot and cancel the five-second countdown using the encoder.
2. Select `Firmware on SD → Choose firmware file → M300APP.M3B`.
3. Run `Check selected file`, then `Install selected file` after success. When prompted, release the encoder and hold it for **2 seconds**. Do not hold throughout verification.
4. After writing: `Diagnostics → Verify Flash`, then `Start application → Launch application`, with a separate prompted two-second hold.
5. The intermediary i4 starts. **Leave the UPGRADE card inserted.** Its v1.1 heading does not mean the permanent bootloader has already changed.

## Common i4 procedure

### Check board + SD

Select and click. Require successful completion (`CHECK_SOURCE_CARD_RESTORE_OK`). It verifies current code, identity, all six files, RESTORE and disjoint FAT chains. Stop on failure; do not alter protection settings.

### Backup Flash x2

Wait for two independent full reads, SD writes, readback and SHA-256. Expected result: `PASS_SD_FULL_FLASH_X2`. Return to the menu with a new click. **Do not restart between Backup and Install.** Session authorization expires on restart; Check alone does not re-establish it.

### Install / upgrade boot

Wait for prechecks to finish before performing the gesture. An identical v1.1 target is skipped without rewriting boot pages. A recognized older source is migrated only after confirmation:

| Prompt | Action |
|---|---|
| `1 Release knob` | Do not press; if already released, wait |
| `2 Click knob once` | Press once |
| `3 Release after click` | Release |
| `4 Press and hold 5s` | Press again |
| `5 Keep holding knob` | Keep holding until completion; rotation cancels |

After `CONFIRM_OK CONFIRMED_5S`, backup and protected-region checks run again. From `WRITING_FIXED_BOOT_PAGES`, **do not reset/remove the card/power**, unless electrical or thermal safety requires it. Only pages 2–15 and 116–121 can be changed. The OEM first 4 KiB, intermediary application, own metadata/journal and final 8-KiB NVM/factory region are outside this transaction. Expected completion: `INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED`.

There is **no automatic recovery from arbitrary power loss**. Preserving the OEM prefix is not equivalent to a complete independent recovery loader. `Recover saved boot` is limited to a still-running installer session with verified copies.

### Restart to boot

After success/identical-target skip, select `Restart to boot`. Hold the encoder during restart to remain in service mode; release once the menu appears. Do not allow autoboot to launch the intermediary again.

## Restore stock 1.3.1

Select **RESTORE.BIN**, not M300APP.M3B:

`Firmware on SD → Choose firmware file → RESTORE.BIN → Check selected file → Install selected file`.

Confirm with the prompted **2-second hold**. After verification, select `Diagnostics → Verify Flash`, then `Start application → Launch application` with a separate confirmation. Check stock firmware 1.3.1, HW, your serial and operating time. A successful UI startup is not full print/heater/motor qualification.

RESTORE contains the original application, not a historical NVM snapshot. Installer preservation does not prevent the stock application from normally updating its counter/preferences after launch.

## Archive the new copies

With power off after completion, copy M3FLASH.BIN, M3INFO.BIN, ZBACK2.BIN and ZINFO2.DAT into a new private folder:

```sh
bash tools/SPRAWDZ_M300_SD_I4.command --backups "$HOME/Desktop/M300_SD_BACKUPS"
```

Require `PASS_SD_I4_BACKUPS_X2`, preserve originals and another physical medium. Never replace completed copies with A5 templates. On failure keep the complete `ERROR INSTALL ... OP ... PHASE ... REASON ...` text; do not use obsolete rc3 host installation commands on i4 or force compatibility. After boot replacement, the old automatic OEM recovery-card behavior is not guaranteed.
