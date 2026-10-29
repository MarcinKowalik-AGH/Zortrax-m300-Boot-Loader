# Release manifest — M300 boot v1.1 / SD installer 1.1-i4

Published machine code is unchanged from the supplied i4 build and the owner's successful UPGRADE/stock 1.3.1 report. This is a **binary-only firmware release** with public operational host tools. Public availability is not permission to bypass the single-device compatibility gates.

## Assets

| Asset | Bytes | SHA-256 |
|---|---:|---|
| M300Boot_v1.1_SD_FACTORY_OEMV3_i4.zip | 185648 | `56573f61992e1dc8a011f1b591008de2c3cc9fefc3f323f15c64998dd53c6d38` |
| M300Boot_v1.1_SD_UPGRADE_i4.zip | 145976 | `30460fe766771a4d5e10f5552fe69d5685146a1c4f8afd756e1ed633765afb15` |
| M300Boot_v1.1_STLINK_LOCAL_BUILDER.zip | 165843 | `13e776a729a5cac102a72a7e786acad51efbc07a258ad2b60e7be203d6b85494` |
| M300_BACKUP_0.5.5_UART.zip | 30476 | `61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149` |

## Validation and evidence

- Publication checks this session: **31 passed**. Includes independent complete BIN/HEX reconstruction, original/private data preservation, old/new boot detection, negative profile/pair/size checks, public audit of the real .055 session and recursive privacy/package scan.
- The earlier retained build report records **1687 bootloader tests, 655 installer tests, 59 installer/static/rebuild checks**. These historic totals were not re-run or counted as new hardware evidence during publication.
- SD_FACTORY and SD_UPGRADE archives are byte-for-byte unchanged. The ST-Link ZIP is newly assembled from exact stage2/assets and a new offline personal-image builder. The backup diagnostic firmware is exact 0.5.5; its public host is a separately tested privacy-only derivative.
- Physical confirmation: **unit A**, classic M300, Rev.5.3/HW05, 256 KiB, OEM v3, firmware 1.3.1: owner verified custom-boot **UPGRADE** to v1.1 through i4 and startup of original 1.3.1.
- Additional owner report: **unit B — FACTORY works on a second printer**. Its board revision, original firmware and exact install/boot success checkpoints are not yet documented. With fixed profile gates, do not interpret this report as proof of general compatibility. [Test report](HARDWARE_FEEDBACK_2026-10-29.md).
- Not asserted: independent second-device log verification of the full FACTORY write transaction, physical SWD recovery, power-loss safety, every baud/menu branch or full printing performance.

No private full Flash, NVM, raw UID, original OEM recovery image, serial-bearing photograph, firmware source/ELF/map or key-generating tool is included. Embedded identity hashes are retained. The local ST-Link builder produces a private reconstructed image that must never be committed.

See [tested hardware](TESTED_HARDWARE.md), [original backup](ORIGINAL_BACKUP_EN.md), [instalacja PL](INSTALACJA_PL.md), [installation EN](INSTALLATION_EN.md) and [publication checks](PUBLICATION_VALIDATION.json).
