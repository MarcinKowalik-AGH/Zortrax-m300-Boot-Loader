# Release manifest — M300Boot 1.4.1

[English](../../en/v1.4.1/release-manifest.md) · [Polski](../../pl/v1.4.1/release-manifest.md) · [Index](README.md)

The [machine-readable manifest](../../../firmware/v1.4.1/RELEASE_MANIFEST.json) and [SHA-256 list](../../../firmware/v1.4.1/SHA256SUMS.txt) identify exact component sizes and bytes. Compare the full downloaded ZIP digest before extraction. The intermediary, target segments and tools must come from the same release.

| Variant | Download | Contents and purpose |
|---|---|---|
| FACTORY | [M300Boot_v1.4.1_SD_FACTORY_OEMV3.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_SD_FACTORY_OEMV3.zip) | Qualified original OEM v3; six files in the SD root |
| UPGRADE | [M300Boot_v1.4.1_SD_UPGRADE.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_SD_UPGRADE.zip) | Recognized custom BOOT; six files in the SD root |
| STLINK | [M300Boot_v1.4.1_STLINK.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_STLINK.zip) | Two addressed segments, sparse HEX, guides and validation tools |

The separate, unchanged `M300_BACKUP_0.5.5_UART.zip` diagnostic obtains backups and has its own instructions. It is not a fourth BOOT installation route.

Permanent BOOT and the SD intermediary are **1.4.1**. Original APP in `RESTORE.BIN` remains **1.3.1**, diagnostic **0.5.5**, and the technical OEM envelope version is independent. Those different programs do not need matching version numbers.

Public material consists of binary firmware, host tools and full EN/PL manuals. Private firmware sources, ELF/maps, OEM-key tools and device data are excluded. Do not publish your Flash backups, UID, options or ST-Link plans. Archived 1.4, 1.3.1 and 1.1 packages retain their original identities.

[HARDWARE_STATUS.json](../../reports/v1.4.1/HARDWARE_STATUS.json) distinguishes owner-reported approximately two-week baseline 1.4 use from the new 1.4.1 patch. The [audit report](../../reports/v1.4.1/AUDIT_2026-11-18.json) records current checks. [Original Zortrax Bootloader v3](../../../firmware/original/README.md) remains a separate, unmodified 32-KiB reference image outside the three installation packages.
