# Release manifest — M300Boot v1.1

[English](../../en/v1.1/release-manifest.md) · [Polski](../../pl/v1.1/release-manifest.md) · [Index](README.md)

**Archived v1.1 record, 29 October 2026.** Hardware statements below retain their historical scope. [Current v1.3.1](../v1.3.1/README.md).

[Release files](../../../firmware/v1.1) · [SHA-256](../../../firmware/v1.1/SHA256SUMS.txt) · [JSON manifest](../../../firmware/v1.1/RELEASE_MANIFEST.json).

| Asset | Bytes | SHA-256 |
|---|---:|---|
| M300Boot_v1.1_SD_FACTORY_OEMV3_i4.zip | 185648 | `56573f61992e1dc8a011f1b591008de2c3cc9fefc3f323f15c64998dd53c6d38` |
| M300Boot_v1.1_SD_UPGRADE_i4.zip | 145976 | `30460fe766771a4d5e10f5552fe69d5685146a1c4f8afd756e1ed633765afb15` |
| M300Boot_v1.1_STLINK_LOCAL_BUILDER.zip | 165843 | `13e776a729a5cac102a72a7e786acad51efbc07a258ad2b60e7be203d6b85494` |
| M300_BACKUP_0.5.5_UART.zip | 30476 | `61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149` |

The four original public ZIPs and executable components are unchanged. This was a binary-only firmware publication with operational host tools and fixed device-profile gates.

The dated publication recorded 31 successful publication checks. The retained earlier build report recorded 1687 BOOT tests, 655 installer tests and 59 installer/static/rebuild checks; these historic totals were not new on-device evidence. FACTORY and UPGRADE SD archives were unchanged; ST-Link was assembled from exact components with an offline private-image builder. Diagnostic 0.5.5 was unchanged, with a separately validated public host adaptation.

At the time, the owner confirmed UPGRADE and stock 1.3.1 startup on unit A, and reported FACTORY working on unit B without detailed second-unit checkpoints. Physical ST-Link was then unconfirmed. [Dated hardware feedback](hardware-feedback.md). Current v1.3.1 owner confirmation is documented separately and is not backdated into this record.

No private full Flash, NVM, raw UID, serial photograph, firmware source, ELF/map or key tools are included. Manufacturer material retains its rights. [Publication report](../../reports/v1.1/PUBLICATION_VALIDATION.json) · [Original backup](original-backup.md).
