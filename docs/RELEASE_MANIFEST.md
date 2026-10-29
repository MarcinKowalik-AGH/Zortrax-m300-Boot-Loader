# v1.1 release preparation manifest

Status: documentation committed; GitHub Release assets await the explicit CLI authorization/publication step. The final checked public bundle contains 40 files and these four archives:

| Package | Bytes | SHA-256 |
|---|---:|---|
| M300Boot_v1.1_SD_FACTORY_OEMV3_i4.zip | 185648 | 56573f61992e1dc8a011f1b591008de2c3cc9fefc3f323f15c64998dd53c6d38 |
| M300Boot_v1.1_SD_UPGRADE_i4.zip | 145976 | 30460fe766771a4d5e10f5552fe69d5685146a1c4f8afd756e1ed633765afb15 |
| M300Boot_v1.1_STLINK_LOCAL_BUILDER.zip | 165843 | 13e776a729a5cac102a72a7e786acad51efbc07a258ad2b60e7be203d6b85494 |
| M300_BACKUP_0.5.5_UART.zip | 30476 | 61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149 |

Machine-code v1.1 stage2 SHA-256: f475e62a3941a8e4d0f0f78b376b2f55c5dd3196033fb5f1e40089bd9b3dd74e. Assets SHA-256: c12148a90fc69a3dc2dae133962dbd9abca0f23547adada53a685ef4339917c1. SD archives and firmware remain byte-for-byte unchanged from the supplied i4 build.

Publication checks this session: 31 passed, including complete personal BIN/HEX reconstruction, preservation of original prefix/data, refusal of mismatched backups/profiles/capacity, public read-only audit of the retained .055 data, and recursive scans excluding private raw identity and firmware sources. Earlier retained build totals (1687 bootloader tests, 655 installer tests, 59 static/rebuild checks) were not re-run as new hardware tests.

Physical evidence: one owner's confirmed custom-boot upgrade through i4 to v1.1 and stock 1.3.1 startup. FACTORY i4, SWD programming, power-loss recovery, other boards and printing qualification are not independently confirmed.

No complete personal Flash/NVM/UID dump, firmware C/ASM, ELF/map, serial-bearing photo, OEM crypto-key tool or universal clone image is included. Fixed compatibility hashes are intentionally retained. RESTORE.BIN contains original manufacturer firmware with separate rights.
