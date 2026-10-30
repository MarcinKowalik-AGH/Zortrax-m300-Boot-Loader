# Public host tools — M300Boot v1.3.1

[English](README.md) · [Polski](README_PL.md)

Python **3.9+**; pySerial is needed only for UART. These are operational host tools, not firmware sources. Keep generated backups, logs and plans private.

| File | Purpose | MCU write? |
|---|---|---|
| `KONSOLA_M300_v1.3.1.command`, `m300_console.py` | Version/board/PING and optional paired fixed-region dumps. | No |
| `m300_service.py` | UART region dumps, SD backup verification and history decoding. | No |
| `ibtool.py` | M3B APP pack/inspect; UART check or explicit application update. | Only `serial --update`, with physical confirmation |
| `verify_sd_i2.py` | Current six-file card or completed A/B backup check. | No |
| `stlink_preflight.py` | Offline two-segment plan and complete 256-KiB readback verification; `--images` selects exact extracted components. | No device access; private local plan only |
| `verify_package.py` | Verify the extracted STLINK package manifest. | No |
| `read_flash_m300_055.py`, `audit_reference.py` | Receiver for diagnostic 0.5.5, using its archived procedure. | Host reads only; diagnostic installation replaces APP |
| `prepare_service_sd.py` | Prepare SD service templates without overwrite. | Local SD files only |
| `validate_publication.py` | Audit current/archived packages and documentation. | No |
| `KONSOLA_M300_v1.1.command`, `SPRAWDZ_M300_SD_I4.command`, `prepare_stlink.py`, `check_backup_profile.py` | Archived v1.1/i4 tools. The old image builder produces v1.1, not v1.3.1. | Follow v1.1 instructions |

```sh
python3 tools/validate_publication.py --json
python3 tools/verify_sd_i2.py --help
python3 tools/stlink_preflight.py --help
python3 tools/ibtool.py --help
```

Run these examples from the repository root. Rates: **115200 / 250000 / 500000 / 750000 / 1000000 / 1500000**. Match the active baud and close other serial clients. Bootwait OFF requires local menu entry; ON admits complete allowed diagnostic lines. The SD intermediary temporarily uses 250000.

No RDP removal, identity bypass or OEM signing/decryption. M3B provides SHA integrity, not signature authentication. [Manuals](../docs/en/README.md) · [UART procedure](../docs/en/v1.3.1/uart-examples.md).
