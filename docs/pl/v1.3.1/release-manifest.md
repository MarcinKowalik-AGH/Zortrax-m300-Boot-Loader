# Manifest wydania — M300Boot v1.3.1

[English](../../en/v1.3.1/release-manifest.md) · [Polski](../../pl/v1.3.1/release-manifest.md) · [Indeks](README.md)

[Pliki wydania](../../../firmware/v1.3.1) · [SHA-256](../../../firmware/v1.3.1/SHA256SUMS.txt) · [Manifest JSON](../../../firmware/v1.3.1/RELEASE_MANIFEST.json).

| Plik | Bajty | SHA-256 |
|---|---:|---|
| M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip | 186363 | `6c400ea5bbe4a6711bb5242d1e617914e27542cd85ab8448ee97ed17a71b9466` |
| M300Boot_v1.3.1_SD_UPGRADE.zip | 147954 | `128862d76bfd954ec6ab2fd52eb08ab418b1c33339d6bca5245cdd7c8463e56c` |
| M300Boot_v1.3.1_STLINK.zip | 86409 | `509df96c2550fda4710a3d2f2e35aa79db1ffab104df63d89bbe4e261ceb3c2d` |
| M300_BACKUP_0.5.5_UART.zip | 30476 | `61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149` |

Paczki publiczne zawierają identyczne bajty wykonawcze v1.3.1. Nie kompilowano firmware ponownie przy publikacji ani porządkowaniu dokumentacji. Archiwa SD mają sześć plików w katalogu głównym. STLINK zawiera dwa segmenty BIN, odpowiadający HEX, kontrolery offline i instrukcje EN/PL. Diagnostyka 0.5.5 pozostała identyczna z v1.1.

Publiczne ZIP-y różnią się od prywatnego pakietu rozwojowego: bez C/ASM firmware, ELF/map, SDK MCU, materiałów analizy, kluczy OEM i zrzutów urządzenia. Powyższe hashe dotyczą archiwów publicznych, nie prywatnych ZIP-ów o innych nazwach.

Właściciel potwierdził UPGRADE, FACTORY, ST-Link, UART8 przy 1500000 i samodzielne działanie OLED. [Macierz sprzętu](tested-hardware.md). Walidacja programowa: **2116 BOOT + 825 instalatora/ST-Link/migracji = 2941 PASS** i 94 kontrole narzędzi PC. [Raport publikacji](../../reports/v1.3.1/PUBLICATION_VALIDATION.json) · [Raport narzędzi](../../reports/v1.3.1/HOST_TOOL_VALIDATION.json).

Migracja SD zastępuje tymczasowo APP i wymaga jej przywrócenia. ST-Link zachowuje APP. Blokady profilu i chronione zakresy pozostają; nie rozszerza to kwalifikacji na wszystkie płyty, druk ani utratę zasilania.
