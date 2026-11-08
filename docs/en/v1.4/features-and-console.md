# Features, complete menu and console — M300Boot 1.4

[English](../../en/v1.4/features-and-console.md) · [Polski](../../pl/v1.4/features-and-console.md) · [Index](README.md)

The permanent bootloader and SD intermediary identify as **1.4**. This guide describes the published FULL bootloader. The original stock application in `RESTORE.BIN`, the separate backup diagnostic and the Klipper MCU/host have their own versions. The technical OEM container version is also separate. See [installation](installation.md) before programming and [validation](validation.md) for the distinction between computer checks and printer acceptance.

## Encoder, screens and startup

Turn the knob to move the selection and click to enter or execute the selected item. Use the visible `Back` item to leave a submenu; a long press is not a universal Back command. The menu does not wrap at its ends. Four item rows are visible: submenus pin `Back` in the first row, leaving three scrolling rows. A reversal first moves the selection within the visible window. Fast queued detents are applied before one redraw; turns made while holding the knob or viewing an operation result are discarded. Identical frames are skipped and changed rectangles alone are transferred.

![BOOT main menu rendered with the native M300 font](../../assets/v1.4/BOOT_MAIN_MENU.png)

The five-second countdown starts after board/OLED initialization, not at power-on. A click or a completed encoder detent enters service. An action already detected during initialization also cancels countdown. Normal timed launch verifies the application and its environment, but needs no confirmation hold. A recovery latch blocks automatic launch. Invalid firmware/environment keeps the controller in service and does not install anything from SD automatically.

Hold the knob during power-on for temporary **250000** service access; this does not replace the stored rate. With `UART on bootwait: OFF`, received host bytes cannot cancel countdown. With `UART on bootwait: ON`, only complete `MENU`, `HOME`, `BACK`, `HELP`, `INFO`, `PING`, `VERIFY`, `ECHO ON` or `ECHO OFF` lines enter service. Binary, incomplete, unrecognized and overlong input cannot extend the deadline. The UART boot banner may still be transmitted with OFF.

Most BOOT action results return to the menu after about **3 seconds**. The Hardware screen stays until the knob has been released and a new click is made. The intermediary's result screens instead require a new click; they do not dismiss automatically. Progress percentages describe the named phase, not a predicted total installation time. Indeterminate progress displays `--`.

## Every BOOT menu and option

The English labels below are the actual OLED labels. The table includes all 13 menu pages; the selected filename replaces the heading on the selected-file screen.

| Screen / menu | Items | Behavior |
|---|---|---|
| `Main menu` | `Start application`; `Firmware on SD`; `Diagnostics`; `About`; `Restart`; `Backup Flash`; `Service history` | Opens the corresponding page; entering a page alone does not program Flash. |
| `Start application` | `Back`; `Launch application` | Checks the installed APP and environment, requests release then a fresh continuous 2-second hold, checks the environment again and launches. It does not install firmware. |
| `Firmware on SD` | `Back`; `Check SD package`; `Install firmware`; `Choose firmware file` | Check verifies without writing; install verifies and, if different from the installed image, asks for the 2-second hold before an APP write. Choose refreshes the file catalog. |
| `Diagnostics` | `Back`; `Verify Flash`; `Hardware`; `Reset / Recovery`; `Clear recovery lock`; `Encoder / raw inputs`; `Display test`; `UART`; `SD card info` | Individual functions are described below. History is a separate main-menu page. |
| `About` | `Back`; `© Marcin Kowalik`; `mkowalik@agh.edu.pl`; `Version v1.4` | Read-only author/version information. Clicking an information row also sends INFO to UART and shows the author/contact status. |
| `Restart` | `Back`; `Restart controller` | Explicit software reset; there is no additional 2-second confirmation after this menu selection. |
| `Backup to SD` | `Back`; `Backup Flash + identity` | Writes one verified Flash/information pair to prepared SD files, after a fresh 2-second hold. This is not the installer's two-copy backup. |
| `Service history` | `Back`; `View history on UART`; `Save history to SD` | LOG displays the retained history on UART. LOGSAVE writes a prepared log file after the 2-second hold. |
| `Files - select, then verify` | `Back`; eligible filenames | Selection identifies a file only; it is explicitly reported as not yet verified. It opens the next page. |
| `Selected firmware` | `Back to files`; `Check selected file`; `Install selected file` | Acts on the exact chosen filename. Changing the card cannot silently substitute an automatic alternative. |
| `UART` | `Back`; `UART test`; `UART baud rate`; `UART on bootwait: OFF` / `UART on bootwait: ON` | Test displays active baud/8N1 and sends PONG. The other entries open the two setting pages. |
| `UART baud rate` | `Back`; `115200`; `250000`; `500000`; `750000`; `1500000` | Selecting a value saves it with readback and applies it after old-speed TX has completed. No additional 2-second hold is used for this setting. |
| `UART on bootwait` | `Back`; `OFF`; `ON` | Saves whether recognized diagnostic lines may enter service during countdown. No additional confirmation hold. |

### UART settings and their storage

The five selectable rates are **115200, 250000, 500000, 750000, 1500000**; an empty configuration defaults to **250000** and bootwait **OFF**. Each setting has its own append-only journal of **256 logical slots**. Torn/invalid occupied slots still consume space. Re-selecting an already stored value does not consume a new slot; recovering temporarily at 250000 is independent of what is stored. No automatic erase reclaims a full journal.

Old stored 19200, 57600 or 1000000 records yield active 250000 in BOOT 1.4 without rewriting Flash. An older Klipper APP may still decode the old value itself: explicitly choose/save 250000 before starting it, and match the host baud. A full journal can prevent that save and requires a separate service procedure. The two local setting pages discard host input; no console command sets arbitrary baud. See [UART migration and host configuration](uart-examples.md).

### File selection and application validation

Only eligible `.BIN` and `.M3B` files in the FAT16/FAT32 root directory are listed. Names are matched without case sensitivity; supported long names are ASCII and at most **26 characters**. Directories, reserved backup/log names and files outside the accepted size range are excluded. The list supports **16 eligible files**; a seventeenth causes `LIST_FULL`, rather than silently truncating the catalog. Listing and selecting never validate the executable contents.

`LIST` refreshes the catalog; `SELECT n` uses the **zero-based** index printed by LIST. The selection remains active until another selection, `SELECT AUTO` or a restart. If the selected file disappears, the operation fails instead of falling back to another file. In automatic mode the three candidates are `M300APP.M3B`, `Update.bin` and `RESTORE.BIN`. **Any two or three present together are ambiguous**. Thus the six-file installation cards require an explicit file choice when both the installer and RESTORE are present.

Every check/install normalizes the supported package, checks target/base/length and vectors, and verifies the payload hash before erase. Native M3B provides SHA-256 integrity, not a cryptographic signature. OEM/stock compatibility uses the retained exact-image rules. Installed custom APP validation requires committed metadata, valid vectors and matching Flash hash; an erased manifest is accepted only for an exact allowlisted stock image. A partly written or invalid manifest is not accepted as arbitrary stock firmware.

`Verify Flash` checks the installed application, not a newly selected SD file. A verified identical image is reported as `ALREADY_INSTALLED` and skipped without asking for a write hold. A real APP write erases application metadata first, withholds vectors until incoming payload verification and writes the commit last. There is one APP slot; none of this provides automatic rollback after power loss. BOOT replacement uses the separate intermediary, not the ordinary APP installation action.

### Diagnostics, reset guard and Hardware

| Option / command | What it does and how to leave it |
|---|---|
| `Verify Flash` / `VERIFY` | Validates the currently installed APP and reports its length and stock identity or `CUSTOM_MANIFEST`; no Flash write. |
| `Hardware` | Reads model/profile, hardware version, factory serial and accumulated operating time each time the page opens. Missing/invalid records show `Unavailable`. These are decoded device records, not live print measurements. Release the knob, then click again to return. |
| `Reset / Recovery` / `RESETINFO` | Prints raw reset flags, cause, BOOT_COUNT, WDG_LOOP_COUNT, recovery latch and `RETENTION WARM_RESET_ONLY`. It does not erase or clear the latch. |
| `Clear recovery lock` / `RECOVERY CLEAR` | Immediately clears the pending-handoff marker, watchdog-loop count and recovery latch in the service SRAM state. There is no confirmation hold, APP repair or Flash/NVM erase. |
| `Encoder / raw inputs` / `DIAG` | Displays virtual UP/OK/DOWN input changes and sends raw GPIO input values to UART. Hold OK for 1 second to exit, or wait for the approximately 20-second timeout. No motor, heater or thermistor test is performed. |
| `Display test` / `DISPLAY` | Displays two built-in test patterns. Turn the knob to switch pattern; click OK to exit. It also ends after approximately 20 seconds. |
| `UART test` / `PING` | Shows the active baud and 8N1, and sends `PONG`; it does not change baud or perform a loopback/cable certification. |
| `SD card info` / `CARDINFO` | Initializes/reads the card and prints sector count and calculated MiB. The OLED shows 512-byte sector count. It neither formats nor writes the card. |

History, BOOT_COUNT and recovery state use two checksummed snapshots in the last 1 KiB of ordinary SRAM. Retention is expected only across warm resets and requires the APP to leave that region reserved. They are not persistent lifetime counters in Flash and need not survive power loss. Factory operating time shown by Hardware is a separate NVM-derived value.

The reset-loop guard increments only after a recorded application handoff followed by a watchdog reset. Power-on, NRST and an intentional software reset are not proof of APP failure. After three such watchdog strikes the recovery latch blocks **automatic** launch. Manual launch still has its normal validation and physical confirmation. Clearing the latch does not diagnose the cause of the resets.

### BOOT backup and SD history files

Prepare a separate service card, or preserve existing backups elsewhere before making new templates:

```sh
python3 tools/prepare_service_sd.py "/Volumes/M300_SERVICE"
```

This creates missing preallocated `M3FLASH.BIN` (**262144 B**), `M3INFO.BIN` (**1024 B**) and `M3LOG.BIN` (**4096 B**) files filled with A5. It does not format the card or overwrite existing files; an existing wrong-sized file is not repaired automatically. Firmware writes file contents, not new FAT directory entries or allocation chains.

`Backup Flash + identity` / `BACKUP` asks for release then a fresh 2-second hold. It writes and reads back one full Flash snapshot plus identity/size/options/hash metadata. Only blank templates or exact already-copied contents of the current image are accepted. An older backup of a different state/device causes refusal (`BACKUP_EXISTS`); keep it and use fresh templates on a service card. This command does not qualify the installer's required x2 backup session.

`View history on UART` / `LOG` shows up to **24 retained events**, oldest first, with boot number, boot-relative milliseconds, event name and argument. Supported events include reset, check, install begin/end, error, boot, backup, dump, log save, recovery clear, user reset and an identical-image skip. `Save history to SD` / `LOGSAVE` asks for the 2-second hold and writes `M3LOG.BIN`, including a history snapshot and integrity information. Blank templates or logs bearing this same printer identity can be replaced; foreign/unknown files are rejected. Neither operation programs controller Flash. Backups and logs contain private device identifiers; keep them private.

## Complete BOOT console reference

Commands are case-sensitive ASCII. Use the exact spelling, send a line terminator and wait for the resulting `DONE` / `ERROR` and `READY`; reset/launch naturally stop the old console. `MENU`, `HOME` and `BACK` all go directly to the main menu — console BACK is not one-level-up navigation. During the local baud and bootwait setting screens, received host commands are discarded so they cannot replace the operator's page. Stop Klipper and other serial clients before using the console.

| Command / syntax | Action, prerequisites and side effects |
|---|---|
| `INFO` | Version/profile, mode, APP bounds, OLED/UART/bootwait status and board/environment diagnostics; read-only. |
| `HELP` | Prints supported command forms; read-only. |
| `PING` | PONG at the active UART baud, plus OLED status; read-only. |
| `MENU`, `HOME`, `BACK` | Return to Main menu; no programming or restart. |
| `ECHO ON`, `ECHO OFF` | Enable/disable typed-character echo in the BOOT console; no persistent setting. |
| `VERIFY` | Check the currently installed APP; no programming. |
| `LIST` | Refresh/list eligible SD files and zero-based indices; no validation/write. |
| `SELECT n` | Select catalog index n from the last successful LIST; no validation/write. |
| `SELECT AUTO` | Clear explicit selection and use the ambiguity-checked three-name automatic mode. |
| `SDCHECK` | Check the selected/automatic package; no programming or hold. |
| `SDUPDATE` | Verify selected/automatic package; skip if identical; otherwise require physical 2-second hold before an APP write. |
| `UARTCHECK N`, `UARTUPDATE N` | Bounded file-server protocol for a package of N bytes. N is decimal, 72–204864 inclusive. Use `ibtool.py serial`; never type binary frames manually. CHECK only verifies; UPDATE still needs the local hold and all image checks. |
| `BACKUP` | One SD Flash/identity pair; prepared files and 2-second hold required. |
| `DUMP FLASH`, `DUMP BOOT`, `DUMP NVM`, `DUMP FACTORY`, `DUMP SYSROM`, `DUMP SIZE`, `DUMP UID`, `DUMP OPTIONS` | Export only the fixed regions below with per-block CRC and final SHA-256; no controller/SD write. Use the read-only host tool to retain and verify paired exports. |
| `RESETINFO` | Reset cause, counters and recovery state; no clearing. |
| `RECOVERY CLEAR` | Clear the SRAM service recovery state immediately; no hold or firmware repair. |
| `DIAG` | Blocking input diagnostic; OK hold 1 second / timeout about 20 seconds. |
| `DISPLAY` | Blocking display patterns; rotation switches, OK exits / timeout about 20 seconds. |
| `CARDINFO` | Card capacity readout; no format/write. |
| `LOG` | Print retained history to UART; no SD write. |
| `LOGSAVE` | Save the retained log to prepared `M3LOG.BIN`; 2-second hold. |
| `BOOT` | Validate and launch installed APP after a fresh 2-second hold. |
| `REBOOT` | Record an intentional reset and reset the controller; no extra hold. |

| DUMP region | Base address | Bytes |
|---|---:|---:|
| `FLASH` | `0x08000000` | 262144 |
| `BOOT` | `0x08000000` | 32768 |
| `NVM` | `0x0803E000` | 8192 |
| `FACTORY` | `0x0803F800` | 2048 |
| `SYSROM` | `0x1FFFF000` | 2048 |
| `SIZE` | `0x1FFFF7E0` | 2 |
| `UID` | `0x1FFFF7E8` | 12 |
| `OPTIONS` | `0x1FFFF800` | 16 |

The full-dump tool and examples are in [backups](original-backup.md) and [UART](uart-examples.md). A DUMP exports bytes; it does not by itself certify a pristine factory APP, remove read protection or create a restore procedure for an erased device.

## SD intermediary: all seven options and its own console

The intermediary runs in APP at `0x08008000`, uses temporary **250000 8N1**, has no automatic BOOT write and does not rewrite the saved baud journal. Its result/Hardware screens wait for release and a new click. Its service console is separate from BOOT's console: use LF/newline; CR alone is ignored.

| Installer menu item | Actual behavior and conditions |
|---|---|
| `Check board + SD` | On-demand source preparation and qualification of the board, source BOOT, six-file card/RESTORE and protected ranges; no BOOT write. |
| `Backup Flash x2` | Takes, writes and verifies two full Flash/identity pairs on the same card. This qualifies backups for this running session only. |
| `Install / upgrade boot` | Requires that session's verified backups, revalidates card/source before and after the operator gesture, then writes and checks fixed BOOT/asset pages. An already-identical target is skipped. |
| `Recover saved boot` | Available only after a BOOT-write attempt in this still-powered session. Revalidates saved backups and requires the same physical gesture, then restores the saved source BOOT pages. It is not APP restoration and cannot recover after loss of the live session automatically. |
| `Restart to boot` | Rechecks invariants/source identity and resets to BOOT. The intended stock/Klipper APP must still be restored separately after SD installation. |
| `Hardware` | Read-only decoded device information; click again after releasing to return. |
| `About` | Sends intermediary/target/source/backup-session diagnostics and displays the result; no write. |

The BOOT replacement/recovery gesture is **release → fresh click → release → fresh press and continuous 5-second hold**. Rotation cancels; release before five seconds cancels. The entire confirmation times out after **45 seconds**. The prompts distinguish the state that timed out. Hash/source/card checks run again after confirmation; a delay or external change cannot authorize stale data. After a failed write keep power and the same card in place and use the live recovery procedure described in [installation](installation.md) / [ST-Link and recovery](stlink-and-recovery.md). There is no automatic power-loss rollback.

| Intermediary command | Effect |
|---|---|
| `INFO` | Version 1.4, target/source identity, backup-session status and temporary UART mode; read-only. |
| `PING` | `PONG M300INSTALL 1.4`; read-only. |
| `HELP` | Lists the intermediary's commands. |
| `ECHO OFF` | Acknowledged for host compatibility; the intermediary does not implement BOOT's interactive character-echo switch. |
| `CHECK` | Same guarded checks as Check board + SD. |
| `BACKUP SD` | Same two-copy operation as Backup Flash x2. |
| `INSTALL V14` | Same guarded BOOT installation; verified SD backups and the physical gesture remain mandatory. |
| `RECOVER SOURCE` | Same live-session restoration of saved BOOT; backups and the physical gesture remain mandatory. |
| `REBOOT` | Same guarded restart as Restart to boot. |

These UART commands never bypass the board/source/SD qualification or physical BOOT-write confirmation. They do not accept arbitrary raw addresses. The complete FAT/card preparation, installation order, removal of the OEM update file when appropriate and final stock/Klipper APP restoration are in [installation](installation.md).

The firmware HELP banners are abbreviated: BOOT also accepts `HOME`, and the intermediary also acknowledges `ECHO OFF`, although those forms are not listed by their HELP text. The tables here were checked against accepted command dispatch, not inferred from HELP alone.
