# M300Boot v1.1 — instalator SD 1.1-i4

[English](../../en/v1.1/release-notes.md) · [Polski](../../pl/v1.1/release-notes.md) · [Indeks](README.md)

**Archiwalny zapis v1.1 z 29 października 2026.** Poniższe ustalenia zachowują historyczny zakres. [Bieżąca v1.3.1](../v1.3.1/README.md).

Niezależny bootloader serwisowy dla klasycznej Zortrax M300. Egzemplarz A scharakteryzowano jako Rev.5.3/HW05, STM32F1 high-density ze zmierzonymi 256 KiB, OEM v3 i oryginalnym 1.3.1. Właściciel potwierdził UPGRADE i4 oraz start odtworzonego 1.3.1. Później zgłosił działające FACTORY na B, bez charakterystyki drugiej płyty i szczegółowych etapów. Było to zgłoszenie drogi, nie ogólna kwalifikacja M300. Fizyczny ST-Link nie był wtedy osobno potwierdzony. [Datowany raport](hardware-feedback.md).

## Paczki tego wydania

- **SD_UPGRADE_i4:** dla rozpoznanego własnego M300Boot FULL.
- **SD_FACTORY_OEMV3_i4:** wejście przez rozpoznany oryginalny OEM v3.
- **STLINK_LOCAL_BUILDER:** dokładne segmenty i generator kompletnego prywatnego obrazu z własnej zgodnej kopii. Bez publikacji osobistego zrzutu Flash.
- **BACKUP_0.5.5_UART:** diagnostyka i odbiornik tylko do odczytu BOOT/NVM/UID/SIZE/opcji. Wgranie diagnostyki najpierw zastępuje APP, więc pełna kopia jest stanem po aktualizacji.

Wszystkie drogi zachowują blokady profilu zakwalifikowanego egzemplarza. Samo HW05 nie wystarcza; inna drukarka wymaga własnej kwalifikacji. Zachowaj kopie przed zapisem. Zdjęcie aktywnego RDP STM32F1 kasuje główną Flash; nie służy do uzyskania backupu. Brak automatycznego rollbacku po zaniku zasilania.

Publikacja binarna, bez źródeł firmware, ELF/map, prywatnych UID/NVM/Flash ani narzędzi kluczy OEM. RESTORE.BIN zawiera oryginalny 1.3.1 z prawami producenta. [Manifest](release-manifest.md) · [Instrukcje](README.md).
