# SD installation — M300Boot 1.4

[English](../../en/v1.4/installation.md) · [Polski](../../pl/v1.4/installation.md) · [Index](README.md)

## Choose the route

Use **UPGRADE** from a recognized custom M300Boot, or **FACTORY** from the qualified original OEM v3. Use the corresponding archive from [firmware/v1.4](../../../firmware/v1.4). Existing UID/options/factory/profile and source checks remain mandatory. Stop Klipper and other UART clients before servicing.

## Prepare and verify the card

1. First complete [independent backups](original-backup.md) and copy them to another medium.
2. Verify the downloaded ZIP with [this release's SHA-256 list](../../../firmware/v1.4/SHA256SUMS.txt). Extract into a new folder.
3. Copy exactly six files to a fresh FAT32 card:

| Route | Files at card root |
|---|---|
| UPGRADE | `M300APP.M3B`, `RESTORE.BIN`, `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT` |
| FACTORY | `Update.bin`, `RESTORE.BIN`, `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT` |

The four A5-filled template files are not backups: Flash files are 262144 B each, information files 1024 B each. Never overwrite completed backups with templates. Do not put the FACTORY `Update.bin` and the intermediary M3B on the same card.

```sh
python3 tools/verify_sd_i2.py --card "/Volumes/M300_CARD" --route upgrade
# Use --route factory for the FACTORY card.
```

Require a successful 1.4 card check. The printer installer separately checks FAT cluster separation before writes.

## Install and launch the intermediary

For ordinary BOOT APP writes and manual APP launch, the OLED asks `Release, then hold 2s`: release the selection click, then press again and hold continuously for 2 s. There is no extra short click between that release and hold. Rotation cancels. The separate 5-second BOOT-installer gesture below has its own additional click/release step.

**UPGRADE:** interrupt countdown with the knob; release it. Select `Firmware on SD → Choose firmware file → M300APP.M3B`, check and install it with the fresh 2-second hold. Verify Flash. Select `Start application → Launch application` and confirm. APP now contains **SD installer 1.4**; permanent BOOT has not yet been updated.

**FACTORY:** power off and insert the FACTORY card. OEM may program `Update.bin` immediately at power-on. Wait for completion, switch off, remove the card and boot without it. Require **SD installer 1.4**. The container's technical OEM wrapper version is independent of the running installer's 1.4 identity. Reinsert the same card in the stable installer menu.

![SD installer 1.4 rendered with the native OLED font](../../assets/v1.4/INSTALLER_MAIN_MENU.png)

## Complete the BOOT transaction

The printer-side procedure needs only the OLED and knob; a connected UART console is optional. Rotate to select and press briefly to execute. After a result appears, **release the knob, then make a new short click** to return to the installer menu. The result does not disappear automatically. Turning the knob cannot dismiss a result screen.

| Step | Local action | Successful OLED display | Optional UART confirmation |
|---|---|---|---|
| 1 | `Check board + SD` | `Complete - click Back` / `Board and SD verified` | `CHECK_SOURCE_CARD_RESTORE_OK` |
| 2 | Return with a new click, then `Backup Flash x2` | `Complete - click Back` / `Backup x2 verified` | `PASS_SD_FULL_FLASH_X2` |
| 3 | Return with a new click, then `Install / upgrade boot` | The five confirmation prompts, then `Writing boot pages` | `CONFIRM RELEASE_THEN_PRESS_RELEASE_THEN_HOLD_5S_ROTATE_CANCELS` |
| 4 | Wait for verification to finish | `Complete - click Back` / `Verified; click Back` | `INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED` |
| 5 | New click, then `Restart to boot`; interrupt countdown | The BOOT header contains `M300 boot v1.4` | BOOT `INFO` identifies `M300BOOT v1.4` |

The third step requires **release → fresh click → release → fresh press and hold 5 s**. Follow `1 Release knob`, `2 Click knob once`, `3 Release after click`, `4 Press and hold 5s`, `5 Keep holding knob`. Rotation cancels; releasing during the continuous hold cancels; the entire confirmation sequence times out after 45 s. A successful double backup in this same powered installer session is mandatory. A power cycle loses the session qualification; repeat `Check board + SD` and `Backup Flash x2` before another attempt.

If current Flash differs from the retained backups after a restart, the old files do not qualify the new state: preserve them elsewhere and prepare fresh templates on a separate card. Never replace the recovery files of a still-running session after a failed write for this purpose.

If the target was already identical, the local result is `Already v1.4 - no write` and optional UART reports `ALREADY_TARGET_V14_NO_BOOT_WRITES`; no BOOT pages were rewritten. Preserve any error screen and error number. Do not remove a guard or change identity hashes.

After the verified transaction, enter the stable BOOT menu, power off, and remove the card to copy **all four** completed backup files to another medium. Verify them with `python3 tools/verify_sd_i2.py --backups "/private/completed-backups"`. Keep both pairs together, with their original filenames. Do not copy the original A5 templates over them. Reinsert the card, power on and interrupt the countdown again before restoring APP.

![Installer progress, rendered example](../../assets/v1.4/INSTALLER_WRITE_PROGRESS.png)

### Physical BOOT confirmation and completion

The following are renders of the actual release screens: backup progress, the independent confirmation hold and verified completion. Read the five-step gesture above before performing it.

![Backup Flash x2](../../assets/v1.4/INSTALLER_BACKUP_PROGRESS.png)

![BOOT confirmation hold](../../assets/v1.4/INSTALLER_CONFIRM_HOLD.png)

![Verified completion](../../assets/v1.4/INSTALLER_COMPLETE.png)

## Restore APP before normal use

**SD installation leaves the intermediary in APP.** To restore stock printing, explicitly choose `Firmware on SD → Choose firmware file → RESTORE.BIN`, then `Check selected file` and `Install selected file`. Complete the separate fresh 2-second confirmation, then use `Diagnostics → Verify Flash`. Finally choose `Start application → Launch application` and complete its own fresh 2-second confirmation. Do not rely on automatic file selection while the intermediary M3B is still on the card. This file remains original **Zortrax M300 1.3.1**, independently of BOOT 1.4.

For Klipper, first replace the intermediary `M300APP.M3B` on the card with the application M3B from the matching Klipper MCU package. Check/install/verify that APP. Before launching it, configure and save a supported UART rate as described below. Then launch the application. The bootloader packages do not contain the Klipper MCU/host bundle.

Before starting an older Klipper APP after migration from saved 1000000, 19200 or 57600, explicitly select **250000** in BOOT and confirm the save. Match the host `[mcu] baud: 250000`. See [UART migration](uart-examples.md). Bootwait OFF is the normal host setting.

Keep power stable during writes. BOOT has no automatic power-loss rollback. Recovery through a still-running intermediary requires its valid session backups; [ST-Link](stlink-and-recovery.md) is a separate route.

## Live recovery after an interrupted BOOT write

Use this path only while the same intermediary remains powered and responsive after its BOOT write attempt. If the screen says `KEEP POWER - see UART`, **keep power on and keep the same SD card inserted**. Do not restart, remove the card or prepare fresh templates.

1. Record the visible error number. Release the knob and make a new short click to return to the installer menu.
2. Select `Recover saved boot`. The installer checks both completed copies and the retained session identity; it asks for the same release/click/release/continuous-5-second confirmation, and checks the copies again before writes.
3. Wait for `Complete - click Back` / `Verified; click Back`. Optional UART reports `SAVED_SOURCE_RESTORED_VERIFIED`. A recovery refusal is not permission to force a reset or erase; retain its error and the powered state while diagnosing.
4. After successful recovery, the previous **BOOT** is restored. APP is still the intermediary; this is not a restore of the stock printing application. Return with a new click. A verified source can be restarted using `Restart to boot`. If the source was OEM, do not leave `Update.bin` on a card that the OEM will read at its next start; after the verified recovery is complete and no write is active, power off and remove that update card before a new start.

`Recover saved boot` is refused before any write attempt (`NO_LIVE_WRITE_TO_RECOVER`) and cannot recover the previous powered session after a reset. It is not an automatic fallback following a power failure. If BOOT no longer starts or the intermediary is no longer running, use complete personal recovery material and the separately reviewed [ST-Link route](stlink-and-recovery.md).
