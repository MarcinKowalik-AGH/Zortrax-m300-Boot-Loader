# Features, Hardware and UART — M300 boot v1.1

[English](../../en/v1.1/features-and-console.md) · [Polski](../../pl/v1.1/features-and-console.md) · [Index](README.md)

**Archived v1.1 record, 29 October 2026.** Hardware statements below retain their historical scope. [Current v1.3.1](../v1.3.1/README.md).

Header: **M300 boot v1.1 © Marcin Kowalik**. Non-wrapping menus, pinned Back, one-row viewport scrolling, direct encoder detents and dirty-rectangle OLED transfer preserve the responsive rc3 behavior.

`Diagnostics → Hardware` displays **Model, Hardware version, Serial number and Total operating time**. Hardware/serial/time are read from the device on each entry; Model denotes the configured target profile. Invalid records display `Unavailable`. The screen stays until another click and never writes NVM. Installer i4 has the same view. Menu HW05 and PCB Rev.5.3 are distinct identifiers.

The progress ring uses bytes/pages/hold time for the **current phase**. Separate write and verification phases may each start at zero. Indeterminate waits show `--`, and errors never masquerade as 100%. Original OEM screens remain unchanged before the intermediary starts.

Main functions: manual verified application launch; cancellable 5-second autoboot; FAT16/FAT32 SD application selection/check/install; identical-image skip; full Flash/identity backup; diagnostics; UART; persistent baud selection; 24-event history and explicit log save; watchdog-loop recovery state. This is one application slot, not simultaneous dual boot or a ready-made Klipper configuration.

## UART connection

3.3-V logic, PA9/USART1_TX to adapter RX, PA10/USART1_RX from adapter TX, common ground. Verify physical header pins independently of Inventure. STLINK-V3SET VCP is a serial adapter; CubeProgrammer's UART protocol is not this console. Close active SWD/debugging and other serial clients. Do not attach 5 V.

Baud rates: **19200, 57600, 115200, 250000, 500000; 8N1, no flow control**. Hold the encoder during boot for service entry at 250000. Saved settings are separate from manufacturer NVM. Installer UART is temporarily 250000 and preserves the bootloader journal.

```sh
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203 --dump-all
```

Python3/pyserial are required; replace the example port. The console-only status is not a hardware qualification. Logs/backups are private. Stay in M300Boot service mode, not stock.

A single read-only dump:

```sh
mkdir -p private
python3 tools/m300_service.py dump --port /dev/cu.usbmodem14203 --baud 250000 FLASH --out private/M300_FLASH.bin
```

Regions: FLASH, BOOT, NVM (final 8 KiB), FACTORY, SYSROM, SIZE, UID, OPTIONS. The receiver validates sequence, CRC and final SHA and refuses overwrites.

```sh
python3 tools/m300_service.py verify-backup M3FLASH.BIN M3INFO.BIN
python3 tools/m300_service.py decode-log M3LOG.BIN
```

M3LOG exists only after explicit history save. Use the i4 card tool to validate the installer's four backup files.

Public `ibtool.py` packs/checks a raw application linked at **0x08008000** and serves an M3B package to the loader. It has no OEM decryption/signing keys. Consult `--help` and `serial --help`. A stage2 boot binary is **not** an application; BOOT updates use the separate intermediary. RESTORE.BIN restores the original 1.3.1 through the SD menu. Do not use obsolete rc3 installation host scripts for i4/v1.1 or bypass any refusal.
