# Public host tools — M300Boot 1.4

[English](README.md) · [Polski](README_PL.md)

Python **3.9+**. pySerial is required only for UART. Match the active rate and close other clients. Exactly five rates: **115200,250000,500000,750000,1500000**; default 250000. The SD intermediary temporarily uses 250000.

| File | Purpose |
|---|---|
| `KONSOLA_M300_v1.4.command`, `m300_console.py` | Read-only1.4 identity, board, PING and paired dumps |
| `m300_service.py` | UART dumps, backup/history decoding |
| `ibtool.py` | M3B inspect/pack; serial check, explicit update with --update |
| `verify_sd_i2.py` | Current six-file cards and completed backups |
| `stlink_preflight.py`, `verify_package.py` | Offline plan, protected ranges, full readback and package checks |
| `validate_publication.py` | Current and historical release audit |
| `read_flash_m300_055.py` | Independent diagnostic 0.5.5 receiver |

```sh
python3 tools/validate_publication.py --json
python3 tools/stlink_preflight.py --help
python3 tools/ibtool.py --help
```

Archived 1.1/1.3.1 launchers and image builders retain their original version. In particular prepare_stlink.py builds 1.1, not 1.4. Do not use historical builders to prepare the current BOOT. Current console tools expect1.4. Local backup files, UID/options, plans and logs remain private.

[UART](../docs/en/v1.4/uart-examples.md) · [ST-Link](../docs/en/v1.4/stlink-and-recovery.md) · [All manuals](../docs/en/README.md).
