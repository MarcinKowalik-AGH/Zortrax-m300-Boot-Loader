# Public host tools / Narzędzia PC — M300Boot v1.3.1

Python **3.9+**, pySerial for UART only. Public Python/Mac tools are operational tools, not firmware sources. Backups/logs/plans stay private. [Manuals EN/PL](../docs/v1.3.1/README.md).

| File / Plik | Purpose / Działanie | Printer write / Zapis MCU |
|---|---|---|
| `KONSOLA_M300_v1.3.1.command`, `m300_console.py` | Current version/board/PING; optional paired fixed-region dumps. / Konsola i podwójne odczyty. | No |
| `m300_service.py` | Fixed-region UART dump, SD backup validation and history decoding. / Odczyty, kontrola kopii i historii. | No |
| `ibtool.py` | M3B APP pack/inspect; serial check or explicit APP update. | Only `serial --update`, with physical consent |
| `verify_sd_i2.py` | Current six-file card check or completed A/B backups. / Karta lub wykonane kopie. | No |
| `stlink_preflight.py` | Current two-segment offline plan and complete 256-KiB readback verification. `--images` selects extracted v1.3.1 segments. | No device access; writes a private local plan only |
| `verify_package.py` | Check the extracted STLINK archive's own manifest. | No |
| `read_flash_m300_055.py`, `audit_reference.py` | Original diagnostic **0.5.5** receiver; use that diagnostic's instructions. | Host reads only; installing diagnostic replaces APP |
| `prepare_service_sd.py` | Prepare standalone SD service templates without overwrite. | Local SD files only |
| `validate_publication.py` | Current and archived public release validation. / Kontrola bieżącego i archiwalnego wydania. | No |
| `KONSOLA_M300_v1.1.command`, `SPRAWDZ_M300_SD_I4.command`, `prepare_stlink.py`, `check_backup_profile.py` | **Legacy v1.1/i4 tools**, retained for that archive. The old builder produces v1.1, not v1.3.1. | See archived manual; never use as the current installer |

```sh
python3 tools/validate_publication.py --json
python3 tools/verify_sd_i2.py --help
python3 tools/stlink_preflight.py --help
python3 tools/ibtool.py --help
```

Menu rates: **115200 / 250000 / 500000 / 750000 / 1000000 / 1500000**. Match active baud and close other clients. Bootwait OFF requires local service entry; ON permits complete allowed diagnostic lines. The SD intermediary temporarily uses 250000.

Narzędzia nie zdejmują RDP, nie usuwają blokad tożsamości i nie podpisują/odszyfrowują OEM. / No RDP removal, identity bypass or vendor-key tooling. M3B provides SHA integrity, not signature authentication.
