# Manifest wydania / Release manifest — M300Boot v1.3.1

BOOT **1.3.1**, SD installer **1.3.1**, date **2026-10-30**. [Files](../../firmware/v1.3.1) · [SHA-256](../../firmware/v1.3.1/SHA256SUMS.txt) · [Machine-readable manifest](../../firmware/v1.3.1/RELEASE_MANIFEST.json).

| Plik / Asset | Bajty / Bytes | SHA-256 |
|---|---:|---|
| M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip | 186363 | `6c400ea5bbe4a6711bb5242d1e617914e27542cd85ab8448ee97ed17a71b9466` |
| M300Boot_v1.3.1_SD_UPGRADE.zip | 147954 | `128862d76bfd954ec6ab2fd52eb08ab418b1c33339d6bca5245cdd7c8463e56c` |
| M300Boot_v1.3.1_STLINK.zip | 86409 | `509df96c2550fda4710a3d2f2e35aa79db1ffab104df63d89bbe4e261ceb3c2d` |
| M300_BACKUP_0.5.5_UART.zip | 30476 | `61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149` |

All new public archives are assembled from **byte-identical** v1.3.1 firmware components. No bootloader/installer machine code was rebuilt or changed for this publication. SD ZIPs have exactly six flat card files. STLINK has two BIN segments, their sparse HEX, current offline checkers and PL/EN instructions. Diagnostic 0.5.5 is copied unchanged from the first public release.

Paczki publiczne mają inne opakowanie niż prywatny KOMPLET: nie zawierają źródeł C/ASM, ELF/map, SDK MCU, materiałów analizy, kluczy OEM ani zrzutów drukarki. Binaria wykonawcze i szablony SD pozostają identyczne. Manifest i sumy dotyczą **tych publicznych ZIP**, nie prywatnych archiwów o innych nazwach.

Hardware status / Sprzęt: the owner confirmed **UPGRADE, FACTORY, ST-Link**, the **1500000** UART8 link and standalone/display operation. [Evidence matrix](TESTED_HARDWARE.md). Re-run software tests: **2116 BOOT + 825 installer/ST-Link/migration = 2941 PASS**. Package and public-host validation is separately recorded in [PUBLICATION_VALIDATION.json](PUBLICATION_VALIDATION.json). No fresh on-device test was performed by the publishing assistant.

Protected ranges and all qualification checks remain. SD replaces APP with the intermediary and requires restoring APP afterwards; ST-Link preserves APP. No general print, arbitrary-board or power-interruption guarantee follows from these tests. / Zakres potwierdzeń nie rozszerza się na druk ani inne płyty.
