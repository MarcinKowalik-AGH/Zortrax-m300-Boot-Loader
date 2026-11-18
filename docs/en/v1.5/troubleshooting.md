# Troubleshooting — M300Boot 1.5

[English](../../en/v1.5/troubleshooting.md) · [Polski](../../pl/v1.5/troubleshooting.md) · [Index](README.md)

| Symptom | Action |
|---|---|
| `NO_COMMIT` after final APP metadata write was interrupted, BOOT 1.5 is running | Preserve backups and retry the exact same valid package. Eligibility requires a matching interrupted record, the full APP digest and a fresh 2-second hold. Do not launch before successful VERIFY. [Procedure](installation.md#reinstalling-app-after-an-interrupted-metadata-write). |
| `NO_COMMIT` under old BOOT 1.4 | The fix is not in the old binary. SD and ordinary ST-Link preflight may still refuse. Preserve backups and prepare a separately reviewed recovery plan; do not manually erase metadata or bypass guards. |
| Host appears to stop countdown | Confirm BOOT 1.5 and bootwait OFF. Physical encoder events and a recovery lock independently keep service open. |
| UART 250000 displayed after migration | Removed stored rates 1000000/19200/57600 fall back to 250000 in BOOT without rewriting the record. Explicitly select/save 250000 before launching an older APP; set host to 250000. |
| Saved 1500000 but temporarily active 250000 | Holding the knob at power-on forces recovery speed. Restart without holding it. The SD intermediary also uses 250000 independently. |
| Klipper cannot connect | Check active BOOT rate, stored journal, APP support and host baud separately. BOOT installation cannot update an unrelated APP. Stop other clients. |
| SD installer starts again | APP still contains the intermediary. Restore/check/install/verify the intended stock or Klipper APP through BOOT. |
| Wrong source/profile/card refusal | Preserve the exact error. Check the matching six-file route, qualified profile, verified copies and FAT card. Do not bypass identity or protection checks. |
| Settings full | Preserve a full verified snapshot. Journals are append-only; this release does not auto-erase them. A separate service procedure is required. |
| Busy or UART timeout during save | Release the knob, ensure no operation is running and retry the local menu after the cause is resolved. Do not force Flash erase. |
| ST-Link cannot read active RDP | Use the SD/diagnostic backup route. Read Unprotect erases main Flash; this sparse package cannot restore the entire erased device. |
| SWD readback differs | Preserve before/after/UID/options and keep the core halted. Do not automatically run, reset or mass-erase. |

The controller's 1.5 identity must agree across permanent BOOT, SD intermediary and current tools. The OEM stock application remains 1.3.1, and independent backup diagnostic remains 0.5.5. Those are expected different version numbers, not stale bootloader labels.

For missing standalone waiting screens, inspect the installed Klipper MCU APP; the bootloader package does not contain that application. For a shutdown, retain the first Klipper error and UART/OLED status, rather than inferring the cause from a later generic message. Software validation and readable screens do not establish motion/heater or print-load acceptance. See [validation](validation.md), [UART](uart-examples.md) and [installation](installation.md).
