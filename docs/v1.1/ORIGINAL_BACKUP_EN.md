# Preserve the original printer before installation

Do not start by replacing the bootloader or clearing read protection. A serial-number photo is not a substitute for the complete factory records.

## Before any change

Photograph the stock `Information → Firmware version` and `Printer information` screens: model, hardware revision, serial and accumulated operating time. Record settings/calibration and photograph the PCB revision and legible MCU marking. Keep the correct **original M300 Update.bin**, its archive and SHA-256; the project reference is stock **1.3.1**. Retain a separate, previously checked OEM recovery SD card. It may cease to be an automatic recovery route after bootloader replacement.

## Required private copies

| Region | Address / size |
|---|---|
| Complete measured main Flash, twice | `0x08000000`, `0x40000` = **262144 bytes** |
| Original bootloader, twice and within both complete images | `0x08000000–0x08007FFF`, **32768 B** |
| Final device-data region, twice | `0x0803E000–0x0803FFFF`, **8192 B** |
| Settings page A / B | `0x0803E800` / `0x0803F000`, 2048 B each; retain both, even inactive/erased |
| Factory page | `0x0803F800`, 2048 B; not just the displayed serial |
| Raw Option Bytes, twice | `0x1FFFF800`, 16 B |
| MCU UID, twice | `0x1FFFF7E8`, 12 B; different from the printer serial |
| Flash size, twice | `0x1FFFF7E0`, 2 B; little-endian `00 01` means 256 KiB |
| Optional diagnostic context | SYSROM, packed BKP data and register snapshots; these are not ordinary flashable images |

The reverse-engineered M300 settings contain a minute counter in the last complete ID0 record of the active NVM page. HW05 is encoded as raw E5; the serial is formatted from binary bytes. Keep the **whole pages**, not reconstructed values. The Hardware screen's model line identifies the target profile rather than independently detecting a marketing model.

## If SWD reads are available

Use ST-Link/SWD to inspect options without applying changes. Read/save two complete images at `0x08000000`, size `0x40000`, and separate pairs of UID, SIZE and OPTIONS. Never rely solely on the GUI size label: this unit initially displayed 512 KB, but internal SIZE reads established 256 KiB. Compare with `cmp` and `shasum -a 256`. Store a second copy on another physical medium.

## If RDP blocks external reads

**Do not click Read Unprotect, Mass Erase or change RDP to obtain a backup.** STM32F1 RDP removal erases main Flash. Code running internally from Flash can read it with debug mode inactive; see ST PM0075.

The project used a temporary **UART Full Audit 0.5.5** application launched by OEM v3. Its released binary is unchanged. The diagnostic code has no Flash/Option Bytes programming feature, but installing it through OEM **replaces the stock application first**. Its resulting full dump is post-update, not a pristine pre-update image. Preserve the original stock package separately.

For an independently identified compatible HW05/Rev.5.3 board:

1. Keep the recorded identity, original firmware, recovery card and stable supervised power. Do not use the application on unidentified hardware.
2. Extract `M300_BACKUP_0.5.5_UART.zip`. Copy **only that diagnostic Update.bin** to a separate FAT32 card. This is not the v1.1 boot installer. Its OEM wrapper version is 9.9.4.
3. Install through OEM. After actual completion, power off, remove the card and do not run an SWD debugging session.
4. Use 3.3-V UART: printer PA9/USART1_TX → adapter RX, PA10/USART1_RX ← adapter TX, common ground. Verify physical header pins; Inventure P4 is not assumed interchangeable. Do not connect 5 V or power the board from VCP.
5. Close CubeProgrammer. Its UART bootloader interface is not this text console. STLINK-V3SET VCP works as a serial adapter. Locate the Mac port, for example with `ls /dev/cu.usbmodem*`.
6. From the extracted backup-tool folder run:

```sh
python3 -m pip install --user pyserial  # only if missing
python3 read_flash_m300_055.py --port /dev/cu.usbmodem14203
```

The port is an example. After `PORT OTWARTY`, power on without the update card. The host uses fixed **250000 8N1**, per-frame CRC32, final SHA-256, two size reads, two full reads and overlap checks. Expected result on this unit: `PASS_FULL_AUDIT_256K_X2`. A new private ZIP is created on the Desktop. Preserve failed-session logs/partial files rather than declaring success.

The **public host** removes the author's private historic NVM reference and checks the integrity of the new pair and the pinned diagnostic payload. It cannot prove equality with a pre-installation snapshot that never existed. Its public packaging was tested offline; no new hardware test of this host derivative is claimed. The exact 0.5.5 firmware and original transport were previously used successfully by the owner.

## Check the release profile before using i4

```sh
python3 tools/check_backup_profile.py /path/to/private/backup
```

Supported layouts: paired FLASH256_POST_UPDATE_A/B or FLASH_A/B plus UID/SIZE/OPTIONS A/B; or the four completed SD files M3FLASH.BIN, M3INFO.BIN, ZBACK2.BIN, ZINFO2.DAT.

`PASS_I4_PROFILE_MATCH` is a necessary compatibility check, not a safety guarantee. `BACKUP_VALID_BUT_INSTALL_PROFILE_MISMATCH` means **do not use this installer**. Another HW05 unit needs independent qualification; never patch gates, clone identity or erase settings to force acceptance.

## Archive and privacy

Keep unmodified BIN files, manifests, hashes, raw/text UART logs, menu/PCB photos, original firmware and the date/procedure. Do not upload them to public issues. Copies include device identity, calibration and manufacturer data. UID/SYSROM/SIZE are evidence, not flashable regions; do not replay OPTIONS blindly. Restoring an old snapshot also restores its old operating-time counter and preferences.

The SD installer's two snapshots are **before boot replacement but after installing the intermediary application**. Two files on the same SD card are not independent storage media. Preserve a second copy elsewhere.

## Źródła / Sources

Dane o zachowaniu M300 pochodzą z kodu wydania v1.1/i4, audytów plików z projektu i relacji właściciela. Nie są deklaracją producenta. Publiczny zestaw nie zawiera prywatnych zrzutów ani logów.

- [ST PM0075, Rev. 2, §2.4, s. 17–20](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf): RDP/WRP i Option Bytes STM32F1.
- [STM32CubeProgrammer 2.23 — programming and erasing](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_UserManual/Memory_programming_and_erasing.html): adres dla BIN, zapis i weryfikacja.
- [STM32CubeProgrammer 2.23 — connection settings](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_UserManual/Main_window.html): SWD, Under Reset i NRST.
- [Projekt odniesienia — Inventure Boot Loader](https://github.com/MarcinKowalik-AGH/Zortrax-Inventure-Boot-Loader). Binaria obu drukarek NIE są zamienne.
