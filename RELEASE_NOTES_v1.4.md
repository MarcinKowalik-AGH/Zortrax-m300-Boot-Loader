# M300Boot 1.4

Permanent BOOT and the SD intermediary consistently identify as 1.4. Exactly five UART rates: 115200,250000,500000,750000,1500000; default 250000, bootwait OFF. Supported saved codes are preserved. Removed saved rates fall back to 250000 without automatic journal rewriting; explicitly save 250000 before launching an older APP that may decode the old record.

All three installation routes are packaged with matching host tools, manifests and checksums. SD requires launching the intermediary, two verified Flash backups, separate BOOT confirmation and explicit APP restoration. ST-Link preserves APP and programs only the two addressed target slots. Stock RESTORE.BIN remains Zortrax 1.3.1; independent diagnostic remains 0.5.5.

Complete EN/PL manuals illustrate the installation order, menus, UART and progress using actual OLED-rendered cyan screenshots. Rebuilt 1.4 is validated offline; physical acceptance is pending. Prior hardware evidence remains associated with archived 1.3.1.

[English guide](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/en/v1.4/README.md) · [Polskie instrukcje](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/pl/v1.4/README.md) · [Validation](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/en/v1.4/validation.md).

The links above open the current, corrected 1.4 instructions on `main`. The release tag and downloadable firmware packages retain their originally validated bytes. The complete [menu and command reference](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/en/v1.4/features-and-console.md) covers all OLED options, console commands and intermediary actions.
