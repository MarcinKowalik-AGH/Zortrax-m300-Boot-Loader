# M300 boot v1.1 — SD FACTORY and UPGRADE

Read [Original backup](ORIGINAL_BACKUP_EN.md) and [Tested hardware](TESTED_HARDWARE.md) first. The unchanged i4 installer is single-device-profile locked, not universal HW05 firmware.

Use FACTORY with recognized original OEM v3 (Update.bin), or UPGRADE with recognized custom M300Boot FULL (M300APP.M3B). A fresh FAT32 root must contain that one entry file, RESTORE.BIN, M3FLASH.BIN, M3INFO.BIN, ZBACK2.BIN and ZINFO2.DAT. The four backup files initially contain A5 placeholders. Never overwrite actual earlier backups with placeholders.

## Factory entry

With power off insert FACTORY. Allow OEM update to complete without interrupting power. After completion power off, remove SD and start the intermediary without it. Once the stable i4 menu appears, insert the same card. This initial step replaces the application, not yet the bootloader.

## Existing custom bootloader entry

Insert UPGRADE with power off. Start and cancel the five-second autoboot using the encoder. Select Firmware on SD → Choose firmware file → M300APP.M3B. Check selected file, then Install selected file; release and hold for two seconds only when prompted. After success choose Diagnostics → Verify Flash, then Start application → Launch application with a separate confirmation. Keep the SD card inserted in i4.

## Shared i4 sequence

1. Check board + SD; require CHECK_SOURCE_CARD_RESTORE_OK.
2. Backup Flash x2; require PASS_SD_FULL_FLASH_X2. These are two full 256-KiB reads with SD readback and SHA validation. Do not reset between backup and installation: session authorization would expire.
3. Install / upgrade boot. Wait until checking is finished. An identical target is skipped; rc3 → v1.1 really writes pages. Follow: release; click once; release; press again and hold five seconds. Rotation cancels. The knob is not held during earlier checking.
4. After CONFIRM_OK the copies/protected regions are checked again. Do not reset/remove SD/power during WRITING_FIXED_BOOT_PAGES except for an actual hazard. Require INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED.
5. Restart to boot. Hold the encoder during restart to stay in the service menu, then release.

## Restore original 1.3.1

Select RESTORE.BIN, not M300APP.M3B. Check selected file → Install selected file; confirm the prompted two-second hold. Then Diagnostics → Verify Flash and Start application → Launch application with separate consent. Check original firmware, your own hardware/serial/counter before motion or heating.

After completion and power-off copy the four real SD backup files to another medium and verify them using the supplied host tool. RESTORE preserves current NVM rather than replacing it with an old snapshot.

No automatic power-loss rollback exists. Recover saved boot is conditional on a still-running intermediary and valid same-session backups. The old OEM SD recovery behavior is not guaranteed after replacing its second stage. Do not bypass errors with RDP/WRP edits or changed hashes. Preserve complete OP/PHASE/REASON diagnostics privately.
