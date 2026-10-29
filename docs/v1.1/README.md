# M300 boot v1.1 — dokumentacja / documentation

**Wersja bieżąca / Current:** **v1.1, instalator SD 1.1-i4**, 29 October 2026. [Repozytorium](../../README.md) · [Wszystkie wersje](../README.md).

| Zakres / Area | Polski | English |
|---|---|---|
| Instalacja z fabrycznego OEM v3 i aktualizacja M300Boot | [Instalacja](INSTALACJA_PL.md) | [Installation](INSTALLATION_EN.md) |
| Zachowanie fabrycznego BOOT/NVM/serialu/licznika przed zmianami | [Kopia oryginału](KOPIA_ORYGINALU_PL.md) | [Original backup](ORIGINAL_BACKUP_EN.md) |
| ST-Link i odbudowa osobistego obrazu | [ST-Link i odzyskiwanie](STLINK_I_ODZYSKIWANIE_PL.md) | [ST-Link and recovery](STLINK_AND_RECOVERY_EN.md) |
| Funkcje, Hardware, menu i UART | [Funkcje i konsola](FUNKCJE_I_KONSOLA_PL.md) | [Features and console](FEATURES_AND_CONSOLE_EN.md) |
| Przykłady poleceń UART, M3B i diagnostyki | [Przykłady UART](KONSOLA_UART_PRZYKLADY_PL.md) | [UART examples](UART_EXAMPLES_EN.md) |
| Sprawdzony sprzęt i ograniczenia | [Tested hardware](TESTED_HARDWARE.md) | [Tested hardware](TESTED_HARDWARE.md) |
| Sumy, binaria i status testów | [Manifest](RELEASE_MANIFEST.md) | [Manifest](RELEASE_MANIFEST.md) |

[Oficjalne Release v1.1](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.1) · [Pliki firmware](../../firmware/v1.1) · [SHA-256](../../firmware/v1.1/SHA256SUMS.txt) · [Wyniki audytu](AUDYT_REPOZYTORIUM_PL.md)

**Potwierdzone sprzętowo:** właściciel wykonał upgrade własnego bootloadera do v1.1 przez pośrednik **1.1-i4** i uruchomił oryginalne Zortrax **1.3.1**. **Jedna klasyczna M300, PCB Rev. 5.3 / HW05, SIZE 256 KiB.** Osobnych prób FACTORY i ST-Link nie potwierdzono. Firmwarowe pliki binarne nie zostały przebudowane w tej reorganizacji.

**Publiczne archiwa są powiązane hashami z jednym rozpoznanym egzemplarzem.** Inne drukarki M300/HW05 wymagają własnej kwalifikacji; nie wyłączaj ochrony, nie modyfikuj hashy i nie przenoś obcych NVM/UID. Nie publikuj kopii konkretnej drukarki.

**Uwaga dotycząca taga:** `v1.1` zachowuje opublikowane binaria/załączniki i pierwotny stan dokumentacji wydania; aktualna wersjonowana dokumentacja i raport audytu znajdują się na `main`, jak w projekcie Inventure.
