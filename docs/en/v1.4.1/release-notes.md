# Release changes — M300Boot 1.4.1

[English](../../en/v1.4.1/release-notes.md) · [Polski](../../pl/v1.4.1/release-notes.md) · [Index](README.md)

## Fix following the 2026-11-18 audit

An interruption during the final APP metadata write could leave baseline 1.4 in `NO_COMMIT`: launch was correctly blocked, but SD/UART reinstallation was also refused. Version 1.4.1 adds a constrained retry path: the same verified candidate must match the interrupted record and the complete already-written APP, and the write requires fresh physical confirmation. Unrelated or inconsistent metadata still cause refusal. [Conditions and procedure](installation.md#reinstalling-app-after-an-interrupted-metadata-write).

Permanent BOOT and the SD intermediary identify as **1.4.1**. UART remains exactly **115200, 250000, 500000, 750000, 1500000**; default 250000 and bootwait OFF. **1000000 was already removed in 1.4**; 10000000 is not an option either. Supported stored codes and explicit migration for older APPs are preserved.

The two BOOT slots, OEM prefix, NVM, source/device qualification, two SD backups, separate BOOT confirmation and APP restoration order remain. Complete instructions and matching tools cover **FACTORY, UPGRADE and STLINK**. This release does not expand the qualified profile to other models or provide automatic rollback.

## Test scope

The owner reported about **two weeks of using baseline 1.4**, having previously confirmed all three installation routes. **The new 1.4.1 patch has its own offline audit results.** The historical test duration is not assigned to the new binary. [Hardware status](tested-hardware.md) · [Validation](validation.md) · [2026-11-18 report](../../reports/v1.4.1/AUDIT_2026-11-18.json).

If a printer is already stuck in `NO_COMMIT` under old BOOT 1.4, its old code can still refuse a standard SD upgrade. The ordinary ST-Link plan also requires a valid APP. Such a state needs a separate review of backups and a recovery plan; do not remove guards to force installation. The fix does not remotely or automatically update old BOOT.

`RESTORE.BIN` remains original **Zortrax M300 1.3.1**; the independent backup diagnostic remains **0.5.5**. Klipper MCU/host is a separate project. Archived 1.4, 1.3.1 and 1.1 packages retain their identities. The manuals include [29 newly generated 1.4.1 C renders](../../assets/v1.4.1/README.md) with documented example inputs and source/image hashes; these are illustrations, not hardware test records.
