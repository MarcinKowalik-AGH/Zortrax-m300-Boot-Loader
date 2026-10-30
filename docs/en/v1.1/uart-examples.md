# M300 boot v1.1 — UART and application update examples

[English](../../en/v1.1/uart-examples.md) · [Polski](../../pl/v1.1/uart-examples.md) · [Index](README.md)

**Archived v1.1 record, 29 October 2026.** Hardware statements below retain their historical scope. [Current v1.3.1](../v1.3.1/README.md).

**Target:** permanent M300Boot FULL v1.1 on a recognized classic M300 Rev.5.3/HW05/256 KiB. This UART service console is **not** the original Zortrax 1.3.1 application's console. Stop five-second autoboot to remain in the bootloader. The port name is only an example.

Use 3.3-V logic PA9/USART1_TX → adapter RX, PA10/USART1_RX ← adapter TX, and common ground. Never connect 5 V. STLINK-V3SET VCP can act as the serial adapter; CubeProgrammer's UART protocol is a different interface. Close other serial clients. The service default is 250000 8N1; hold the encoder at startup to enter the recovery service at 250000 if a different baud rate was saved.

```sh
python3 -m pip install pyserial
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203 --dump-all
```

Read-only single region:

```sh
mkdir -p private
python3 tools/m300_service.py dump --port /dev/cu.usbmodem14203 --baud 250000 BOOT --out private/BOOT_NEW.bin
```

Check a supplied M3B application package offline (extract it from the relevant SD ZIP):

```sh
python3 tools/ibtool.py inspect /path/to/M300APP.M3B
python3 tools/ibtool.py inspect /path/to/RESTORE.BIN
```

Pack **your own compiled** application linked for `0x08008000`, not a stage2 bootloader:

```sh
python3 tools/ibtool.py pack /path/to/my_application.bin /path/to/new_application.M3B
python3 tools/ibtool.py inspect /path/to/new_application.M3B
```

Serve/check it via UART, without an MCU write:

```sh
python3 tools/ibtool.py serial /path/to/new_application.M3B --port /dev/cu.usbmodem14203 --baud 250000
```

`ibtool.py serial --update` is an **explicit write request for the APP slot** and requires physical confirmation; it is neither a bootloader updater nor a diagnostic read. The M3B SHA-256 checks integrity; it is not a cryptographic signature. No OEM decryption/signing/tail20 key material is included.

Check SD installer backup and optional saved history locally:

```sh
python3 tools/check_backup_profile.py /path/to/private_backup_folder
python3 tools/m300_service.py verify-backup /path/to/M3FLASH.BIN /path/to/M3INFO.BIN
python3 tools/m300_service.py decode-log /path/to/M3LOG.BIN
```

A saved history file is not the blank template. Never publish raw UID, serial-bearing console logs or private Flash/NVM images. See [Original backup](original-backup.md), [Installation](installation.md), [Features](features-and-console.md), and [Docs index](README.md).
