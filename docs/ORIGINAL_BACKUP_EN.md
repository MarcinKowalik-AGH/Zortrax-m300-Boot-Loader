# Preserve the original printer before migration

Target: separately identified classic M300 Rev.5.3/HW05, measured 256 KiB. This is not for Plus/Dual/Inventure. The unchanged i4 installer additionally checks one qualified device profile.

Record stock Firmware version and Printer information: model, HW, serial, accumulated time, preferences and calibration state. Photograph PCB revision and readable MCU marking. Preserve the correct original Update.bin, its archive and SHA-256. A serial-number photo is not a substitute for factory-record bytes.

Preserve twice: complete main Flash at 0x08000000, 262144 B; BOOT at 0x08000000, 32768 B; final DATA at 0x0803E000, 8192 B; OPTIONS at 0x1FFFF800, 16 B; UID at 0x1FFFF7E8, 12 B; SIZE at 0x1FFFF7E0, 2 B. Keep both NVM pages (0x0803E800 and 0x0803F000, 2048 B each), the factory page (0x0803F800, 2048 B) and unknown records. UID is not the printer serial.

The reverse-engineered stock minute counter is the last complete ID0 entry in the active NVM bank; HW05 is decoded from E5. Store whole pages, not hand-recreated values. The model line in our Hardware view denotes its target profile.

When SWD reads are available, inspect options without Apply, save two complete images and identity/options pairs, and compare with cmp and shasum -a 256. The test unit's GUI originally displayed 512 KB, but matching SIZE bytes `00 01` establish 256 KiB. Do not probe an unconfirmed upper half.

**If RDP blocks access, do not remove RDP or use mass erase to obtain a backup. STM32F1 read-unprotect erases main Flash.** The project used an unchanged temporary UART diagnostic 0.5.5 running internally through OEM v3, with SWD debugging inactive. Installing it replaces stock first, so the resulting full snapshot is post-update, not a pristine pre-installation image.

The backup package is separate from the boot installer. On independently identified compatible hardware, install its Update.bin using OEM, power off after actual completion, remove the update card and use 3.3-V USART1 UART: PA9/TX to adapter RX, PA10/RX from adapter TX and ground. Verify physical header pins; never infer Inventure P4 numbering or connect 5 V. Close CubeProgrammer and other clients.

From the extracted backup directory:

```sh
python3 -m pip install --user pyserial  # only when missing
python3 read_flash_m300_055.py --port /dev/cu.usbmodem14203
```

The port is an example. Open the receiver first, then start without the card. Require PASS_FULL_AUDIT_256K_X2. The host verifies frame CRC, final SHA, paired reads and overlap; it never programs the chip. The public host does not pretend to compare with an unavailable historical private snapshot.

Run check_backup_profile.py locally on the completed backup before using i4. A profile mismatch means STOP, not permission to patch identity gates. Preserve raw files/logs, menu/PCB photos, original firmware and date/method on a second medium. Never post raw UID/NVM/Flash to public issues. OPTIONS/SYSROM/UID/SIZE are evidence, not files to blindly replay. Restoring an old snapshot also restores its old counter/preferences.

Source: [ST PM0075](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf). Zortrax-specific layout comes from the project's private audit.
