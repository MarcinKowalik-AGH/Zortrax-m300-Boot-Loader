# Release notes — M300Boot 1.4

[English](../../en/v1.4/release-notes.md) · [Polski](../../pl/v1.4/release-notes.md) · [Index](README.md)

BOOT and SD intermediary now consistently identify as **1.4**, with no development suffixes. The active UART/menu set is exactly **115200,250000,500000,750000,1500000**; default 250000 and bootwait OFF. Supported saved records retain their original codes. Removed stored rates fall back to 250000 without implicit journal writes; explicitly save 250000 before using an older APP that reads the old record.

The update preserves original-prefiks/NVM protection, source/device gates, verified double backups, independent BOOT consent, APP restoration order and two-segment ST-Link addresses. Host tools, embedded launcher code, package validators and manifests are updated together. See [installation](installation.md) and [UART migration](uart-examples.md).

Documentation is organized as paired complete EN/PL manuals with step-by-step SD and ST-Link procedures. Native OLED renders illustrate BOOT, installer, UART and progress using cyan pixels. They are generated screenshots, not photographs or new physical acceptance evidence.

The 1.4 firmware is rebuilt and checked offline. [Validation evidence](validation.md) records the checks; physical1.4 acceptance is pending. Previous1.3.1 hardware observations and immutable downloads remain in the [archive](../v1.3.1/README.md). RESTORE.BIN remains stock Zortrax 1.3.1, and diagnostic 0.5.5 keeps its independent version.
