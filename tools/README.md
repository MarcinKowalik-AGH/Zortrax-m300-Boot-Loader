# M300 boot v1.1 — public host tools / narzędzia PC

**Version:** M300 boot v1.1, SD installer **1.1-i4**. Public scripts are Python tools and Mac launchers, not firmware C/ASM sources. They cannot remove RDP or make the single-device i4 installer accept a different printer. Always start with the [original-device backup procedure](../docs/v1.1/KOPIA_ORYGINALU_PL.md).

| File | Purpose | MCU writes? |
|---|---|---|
| `KONSOLA_M300_v1.1.command` / `m300_console.py` | Version/board/PING and read-only UART dump; private logs | No |
| `m300_service.py` | Read-only UART dump, local SD-backup verification, saved history decoding | No |
| `read_flash_m300_055.py` + `audit_reference.py` | Receive fixed-range backup from **already installed diagnostic 0.5.5**, pairing and SHA/CRC | No host write; installing diagnostic changes APP |
| `SPRAWDZ_M300_SD_I4.command` | Check six SD-card files or completed i4 A/B backups | No |
| `check_backup_profile.py` | Verify paired full-Flash backups and this release's locked identity profile **locally** | No |
| `prepare_stlink.py` | Offline generation of a **private, complete 256-KiB recovery image** from *your own* verified backup plus pinned v1.1 components | No; generated output is a programming input, not an automatic flash |
| `ibtool.py` | Offline M3B APP pack/inspect, opt-in UART APP check or update | `serial --update` writes APP **only after explicit user/physical approval** |
| `prepare_service_sd.py` | Make three standalone service templates without overwriting existing files | SD files only |
| `validate_publication.py` | Validate public archives, HEX/BIN, checksums, Markdown links and host files | No (read-only) |

**Important:** `ibtool.py` does **not** sign/decrypt vendor `Update.bin`, create vendor HMAC, or flash the second-stage bootloader. M3B integrity uses SHA-256 but **is not authenticated by a cryptographic signature**. Do not use legacy rc3 installation scripts with v1.1/i4.

## Checked examples / sprawdzone składnie

```sh
python3 tools/ibtool.py --help
python3 tools/ibtool.py inspect /path/to/M300APP.M3B
python3 tools/m300_service.py --help
python3 tools/check_backup_profile.py /path/to/private_backup_directory
python3 tools/validate_publication.py --json
```

See [Polish UART examples](../docs/v1.1/KONSOLA_UART_PRZYKLADY_PL.md) or [English UART examples](../docs/v1.1/UART_EXAMPLES_EN.md).

The **tested hardware** was one classic M300 PCB Rev.5.3/HW05/256 KiB unit. Reported UPGRADE→v1.1 and stock 1.3.1 startup do not qualify FACTORY i4, ST-Link, power-loss recovery or other boards. **Never publish logs, private Flash, UID, serial, calibration or raw NVM.**
