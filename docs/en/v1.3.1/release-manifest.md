# Release manifest — M300Boot v1.3.1

[English](../../en/v1.3.1/release-manifest.md) · [Polski](../../pl/v1.3.1/release-manifest.md) · [Index](README.md)

[Release files](../../../firmware/v1.3.1) · [SHA-256](../../../firmware/v1.3.1/SHA256SUMS.txt) · [JSON manifest](../../../firmware/v1.3.1/RELEASE_MANIFEST.json).

| Asset | Bytes | SHA-256 |
|---|---:|---|
| M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip | 186363 | `6c400ea5bbe4a6711bb5242d1e617914e27542cd85ab8448ee97ed17a71b9466` |
| M300Boot_v1.3.1_SD_UPGRADE.zip | 147954 | `128862d76bfd954ec6ab2fd52eb08ab418b1c33339d6bca5245cdd7c8463e56c` |
| M300Boot_v1.3.1_STLINK.zip | 86409 | `509df96c2550fda4710a3d2f2e35aa79db1ffab104df63d89bbe4e261ceb3c2d` |
| M300_BACKUP_0.5.5_UART.zip | 30476 | `61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149` |

The public packages contain byte-identical v1.3.1 executable components. No firmware was rebuilt for publication or documentation reorganization. SD archives contain six flat card files. STLINK contains two BIN segments, their sparse HEX, offline checkers and EN/PL instructions. Diagnostic 0.5.5 is unchanged from v1.1.

These public ZIPs differ from the private full-development package: no firmware C/ASM, ELF/maps, MCU SDK, analysis material, OEM keys or device dumps. The hashes above identify the public archives, not privately distributed ZIPs with different names.

The owner confirmed UPGRADE, FACTORY, ST-Link, UART8 at 1500000 and standalone/display operation. [Hardware matrix](tested-hardware.md). Software validation: **2116 BOOT + 825 installer/ST-Link/migration = 2941 PASS**, plus 94 public-host checks. [Publication report](../../reports/v1.3.1/PUBLICATION_VALIDATION.json) · [Host report](../../reports/v1.3.1/HOST_TOOL_VALIDATION.json).

SD migration temporarily replaces APP and requires application restoration. ST-Link preserves APP. Profile gates and protected ranges remain; no universal-board, printing or power-loss guarantee is inferred.
