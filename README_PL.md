# M300Boot 1.4 — klasyczna Zortrax M300

[English](README.md) · [Polski](README_PL.md)

Niezależny bootloader serwisowy: **Marcin Kowalik** · mkowalik@agh.edu.pl. Cel: **klasyczna M300, HW05 / PCB Rev.5.3 / rodzina STM32F103 / zmierzone 256 KiB Flash**. Stały BOOT i instalator SD mają numer **1.4**.

Dokładnie pięć prędkości UART: **115200, 250000, 500000, 750000, 1500000**, 8N1. Domyślnie **250000**, UART on bootwait **OFF**. Obsługiwane zapisy pozostają po aktualizacji. Dawne niedozwolone rekordy dają w BOOT 250000; przed starszą APP samodzielnie odczytującą te rekordy jawnie zapisz 250000.

## Pobieranie i kolejność instalacji

| Stan urządzenia | Paczka |
|---|---|
| Rozpoznany własny M300Boot | [SD_UPGRADE](firmware/v1.4/M300Boot_v1.4_SD_UPGRADE.zip) |
| Zakwalifikowany oryginalny OEMv3 | [SD_FACTORY_OEMV3](firmware/v1.4/M300Boot_v1.4_SD_FACTORY_OEMV3.zip) |
| Działający odczyt SWD, RDP już wyłączone | [STLINK — dwa adresowane segmenty](firmware/v1.4/M300Boot_v1.4_STLINK.zip) |

[Wydanie 1.4](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.4) · [SHA-256](firmware/v1.4/SHA256SUMS.txt) · [Pełne instrukcje po polsku](docs/pl/v1.4/README.md).

**Kolejność SD:** zachowaj niezależne kopie → wgraj i uruchom instalator pośredni → sprawdź płytę/kartę → wykonaj i zweryfikuj dwie kopie Flash → osobno potwierdź zastąpienie BOOT → uruchom BOOT 1.4 → jawnie przywróć docelową APP stock lub Klipper. [Instrukcja krok po kroku](docs/pl/v1.4/installation.md).

![BOOT 1.4 — render z kodu OLED, piksele cyan](docs/assets/v1.4/BOOT_MAIN_MENU.png)
![Instalator SD 1.4 — render natywnej czcionki](docs/assets/v1.4/INSTALLER_MAIN_MENU.png)

Ilustracje są renderami, a nie fotografiami. Kompilacja 1.4 jest sprawdzana programowo; odbiór fizyczny na drukarce pozostaje do wykonania. Wcześniejsze próby sprzętowe dotyczą 1.3.1. [Walidacja i ograniczenia](docs/pl/v1.4/validation.md) · [Zakres sprzętowy](docs/pl/v1.4/tested-hardware.md).

## Obsługa i odzyskiwanie

- [Zachowanie oryginalnej pamięci](docs/pl/v1.4/original-backup.md)
- [Menu i konsola](docs/pl/v1.4/features-and-console.md)
- [Ustawienia i migracja UART](docs/pl/v1.4/uart-examples.md)
- [Adresy ST-Link i pełny odczyt kontrolny](docs/pl/v1.4/stlink-and-recovery.md)
- [Rozwiązywanie problemów](docs/pl/v1.4/troubleshooting.md)
- [Narzędzia hosta](tools/README_PL.md) · [Pobieranie](firmware/README_PL.md) · [Historia zmian](docs/pl/changelog.md)

Stage2 BOOT zajmuje **0x08001000–0x08007FFF**; zasoby **0x0803A000–0x0803CFFF**. ST-Link zachowuje APP. Instalacja SD chwilowo zastępuje APP i wymaga jej przywrócenia. Oryginalne pierwsze 4 KiB, NVM producenta, kontrole urządzenia i chronione ustawienia pozostają zachowane. Nie ma automatycznego cofania BOOT po zaniku zasilania. Nie usuwaj aktywnego RDP w celu wykonania kopii.

`RESTORE.BIN` nadal zawiera oryginalny **Zortrax M300 1.3.1**. Niezależna diagnostyka kopii zachowuje **0.5.5**. MCU/host Klippera to osobna paczka. Różne numery tych składników są celowe.

[Cała dokumentacja i archiwum](docs/pl/README.md) · [Archiwalne 1.3.1](docs/pl/v1.3.1/README.md) · [Archiwalne 1.1](docs/pl/v1.1/README.md). Publiczne są binaria, narzędzia hosta i instrukcje; prywatne źródła firmware, narzędzia kluczy OEM i dane Flash/tożsamości pozostają wyłączone. [Zasady dystrybucji](THIRD_PARTY_NOTICES.md). Klasyczna M300; Plus, Dual i Inventure są osobnymi celami.
