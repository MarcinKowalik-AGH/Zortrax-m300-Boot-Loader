# M300Boot 1.4 — downloads

[English](README.md) · [Polski](README_PL.md)

| Route | Package |
|---|---|
| UPGRADE | [M300Boot_v1.4_SD_UPGRADE.zip](v1.4/M300Boot_v1.4_SD_UPGRADE.zip) |
| FACTORY OEMv3 | [M300Boot_v1.4_SD_FACTORY_OEMV3.zip](v1.4/M300Boot_v1.4_SD_FACTORY_OEMV3.zip) |
| ST-Link | [M300Boot_v1.4_STLINK.zip](v1.4/M300Boot_v1.4_STLINK.zip) |

[SHA-256](v1.4/SHA256SUMS.txt) · [Manifest](v1.4/RELEASE_MANIFEST.json) · [Installation](../docs/en/v1.4/installation.md) · [Validation](../docs/en/v1.4/validation.md).

Choose only the route qualified for the existing printer. SD archives have six files and temporarily replace APP with the 1.4 intermediary. Restore the intended stock or Klipper application after BOOT replacement. ST-Link contains two addressed segments, preserving APP. RESTORE.BIN is original Zortrax 1.3.1; backup diagnostic 0.5.5 is independent. The owner confirmed all three 1.4 installation methods on the printer; see the [acceptance record](../docs/reports/v1.4/HARDWARE_ACCEPTANCE.json).

The [original Zortrax Bootloader v3](original/README.md) is also available separately: unmodified 32-KiB raw BOOT with provenance and SHA-256.

Unchanged archives: [1.3.1](v1.3.1), [1.1](v1.1). [0.5.5 diagnostic](v1.3.1/M300_BACKUP_0.5.5_UART.zip).
