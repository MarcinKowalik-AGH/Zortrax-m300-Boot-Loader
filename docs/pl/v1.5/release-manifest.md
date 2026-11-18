# Manifest wydania — M300Boot 1.5

[English](../../en/v1.5/release-manifest.md) · [Polski](../../pl/v1.5/release-manifest.md) · [Indeks](README.md)

[Manifest maszynowy](../../../firmware/v1.5/RELEASE_MANIFEST.json) i [lista SHA-256](../../../firmware/v1.5/SHA256SUMS.txt) określają dokładne rozmiary i tożsamości składników. Przed rozpakowaniem porównaj pełny skrót pobranego ZIP-a. Instalator, segmenty docelowe i narzędzia muszą pochodzić z tego samego wydania.

| Wariant | Pobieranie | Zawartość i przeznaczenie |
|---|---|---|
| FACTORY | [M300Boot_v1.5_SD_FACTORY_OEMV3.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_SD_FACTORY_OEMV3.zip) | Zakwalifikowany oryginalny OEM v3; sześć plików w katalogu głównym SD |
| UPGRADE | [M300Boot_v1.5_SD_UPGRADE.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_SD_UPGRADE.zip) | Rozpoznany własny BOOT; sześć plików w katalogu głównym SD |
| STLINK | [M300Boot_v1.5_STLINK.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_STLINK.zip) | Dwa adresowane segmenty, rzadki HEX, instrukcje i narzędzia kontroli |

Osobna, niezmieniona diagnostyka `M300_BACKUP_0.5.5_UART.zip` służy wykonywaniu kopii i ma własną instrukcję. Nie jest czwartą metodą instalacji BOOT.

Stały BOOT i instalator pośredni mają wersję **1.5**. Oryginalna APP w `RESTORE.BIN` pozostaje **1.3.1**, diagnostyka **0.5.5**, a techniczny numer kontenera OEM jest niezależny. Numery tych różnych programów nie muszą być identyczne.

Publiczne są binaria, narzędzia hosta i pełne instrukcje EN/PL. Prywatne źródła firmware, ELF/mapy, narzędzia kluczy OEM i dane urządzenia pozostają wyłączone. Nie publikuj własnych kopii Flash, UID, opcji ani planów ST-Link. Archiwalne paczki 1.4.1, 1.4, 1.3.1 i 1.1 zachowują pierwotne tożsamości.

[HARDWARE_STATUS.json](../../reports/v1.5/HARDWARE_STATUS.json) rozróżnia około dwutygodniowe użytkowanie bazowej 1.4 zgłoszone przez właściciela i nową poprawkę 1.5. [Raport audytu](../../reports/v1.5/AUDIT_2026-11-18.json) zawiera wyniki bieżących kontroli. [Oryginalny Zortrax Bootloader v3](../../../firmware/original/README_PL.md) jest osobnym, niezmienionym obrazem referencyjnym 32 KiB, poza trzema paczkami instalacyjnymi.
