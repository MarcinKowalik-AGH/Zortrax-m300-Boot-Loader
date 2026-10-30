# Manifest wydania — M300Boot v1.1

[English](../../en/v1.1/release-manifest.md) · [Polski](../../pl/v1.1/release-manifest.md) · [Indeks](README.md)

**Archiwalny zapis v1.1 z 29 października 2026.** Poniższe ustalenia zachowują historyczny zakres. [Bieżąca v1.3.1](../v1.3.1/README.md).

[Pliki wydania](../../../firmware/v1.1) · [SHA-256](../../../firmware/v1.1/SHA256SUMS.txt) · [Manifest JSON](../../../firmware/v1.1/RELEASE_MANIFEST.json).

| Plik | Bajty | SHA-256 |
|---|---:|---|
| M300Boot_v1.1_SD_FACTORY_OEMV3_i4.zip | 185648 | `56573f61992e1dc8a011f1b591008de2c3cc9fefc3f323f15c64998dd53c6d38` |
| M300Boot_v1.1_SD_UPGRADE_i4.zip | 145976 | `30460fe766771a4d5e10f5552fe69d5685146a1c4f8afd756e1ed633765afb15` |
| M300Boot_v1.1_STLINK_LOCAL_BUILDER.zip | 165843 | `13e776a729a5cac102a72a7e786acad51efbc07a258ad2b60e7be203d6b85494` |
| M300_BACKUP_0.5.5_UART.zip | 30476 | `61a72b7e296c2b3066324aa0352bea2c86c760673cb0b5c4536e7b065cf02149` |

Cztery pierwotne ZIP-y i ich elementy wykonawcze pozostały bez zmian. Była to publikacja binarna firmware z narzędziami PC i blokadami indywidualnego profilu.

Datowany raport odnotował 31 poprawnych kontroli publikacji. Zachowany wcześniejszy raport kompilacji miał 1687 testów BOOT, 655 instalatora i 59 kontroli statycznych/ponownego buildu; te liczby nie oznaczały nowej próby sprzętowej. Archiwa SD FACTORY i UPGRADE pozostały identyczne. ST-Link złożono z dokładnych segmentów i generatora prywatnego obrazu offline. Diagnostyka 0.5.5 była niezmieniona, z osobno sprawdzoną adaptacją hosta.

Wtedy właściciel potwierdził UPGRADE i start oryginalnego 1.3.1 na egzemplarzu A oraz zgłosił FACTORY na egzemplarzu B bez szczegółowych etapów. ST-Link nie był jeszcze potwierdzony. [Datowany raport sprzętowy](hardware-feedback.md). Bieżące potwierdzenie dla v1.3.1 jest zapisane osobno, bez zmiany daty historycznych ustaleń.

Nie dołączono prywatnych Flash/NVM/UID, zdjęć z numerem seryjnym, źródeł firmware, ELF/map ani narzędzi kluczy. Materiały producenta zachowują jego prawa. [Raport publikacji](../../reports/v1.1/PUBLICATION_VALIDATION.json) · [Kopia oryginału](original-backup.md).
