# M300Boot v1.3.1 — klasyczna Zortrax M300

[English](README.md) · [Polski](README_PL.md)

Niezależny bootloader serwisowy. **Autor: Marcin Kowalik** · mkowalik@agh.edu.pl.
Sprzęt: **klasyczna M300, PCB Rev.5.3 / HW05 / rodzina STM32F103 / zmierzone 256 KiB Flash**.
Bieżące wydanie: **BOOT 1.3.1, instalator SD 1.3.1**, 30 października 2026.

**Właściciel potwierdził sprzętowo UPGRADE, FACTORY i ST-Link.** Potwierdzone są też UART8 przy **1500000 baud** oraz samodzielne działanie i transmisja OLED. Instalator zachowuje kontrole profilu zakwalifikowanego egzemplarza.

## Pobieranie i instalacja

| Stan urządzenia | Paczka |
|---|---|
| Rozpoznany własny M300Boot | [SD_UPGRADE v1.3.1](firmware/v1.3.1/M300Boot_v1.3.1_SD_UPGRADE.zip) |
| Oryginalny OEM v3, zgodny profil | [SD_FACTORY_OEMV3 v1.3.1](firmware/v1.3.1/M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip) |
| Dostęp SWD, RDP już wyłączone | [STLINK v1.3.1 — dwa adresowane segmenty](firmware/v1.3.1/M300Boot_v1.3.1_STLINK.zip) |
| Zachowanie oryginalnego BOOT/NVM przy RDP | [Diagnostyka UART 0.5.5](firmware/v1.3.1/M300_BACKUP_0.5.5_UART.zip) |

[Wydanie v1.3.1](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.3.1) · [Instalacja](docs/pl/v1.3.1/installation.md) · [Najpierw kopia](docs/pl/v1.3.1/original-backup.md) · [SHA-256](firmware/v1.3.1/SHA256SUMS.txt).

Przed zapisem zachowaj własne BOOT/NVM/UID/SIZE/opcje i niezależne zgodne kopie Flash. Zdjęcie aktywnego RDP STM32F1 kasuje główną Flash; nie służy do uzyskania backupu. Samo M300/HW05 nie oznacza zgodności z zachowanymi kontrolami tożsamości.

## Funkcje

| Funkcja | Działanie |
|---|---|
| UART | Menu kolejno **115200, 250000, 500000, 750000, 1000000, 1500000**, 8N1. Zapis Flash z kontrolą odczytu; dawne 19200/57600 nadal są czytelne. |
| UART on bootwait | Trwałe **OFF/ON**. OFF odrzuca odbiór hosta w odliczaniu, ON dopuszcza pełne dozwolone linie diagnostyczne. Binarny Klipper nie przerywa autostartu. |
| Ustawienia | Poprawione fałszywe busy zmiany baud; ruch hosta i niepełne linie nie przejmują lokalnego menu. Domyślne 250000/OFF. |
| OLED i enkoder | Przesyłanie zmienionego prostokąta, pomijanie identycznych klatek, bezpośrednie kroki, przypięty Back i ograniczone przewijanie. |
| Rozruch | Odliczanie 5 s po inicjalizacji, lokalne wejście do serwisu; trzymanie pokrętła przy włączeniu chwilowo wymusza 250000. |
| Instalacja | Kontrolowana transakcja SD, dwie kopie i świeże potwierdzenie 5 s; dwa segmenty ST-Link z pełnym readback 256 KiB. |
| Diagnostyka | Odczyt sprzętu/numeru/czasu pracy, kontrola Flash, kopie, historia i postęp bieżącej fazy. |

[Pełny opis funkcji](docs/pl/v1.3.1/features-and-console.md) · [Przykłady UART](docs/pl/v1.3.1/uart-examples.md) · [ST-Link](docs/pl/v1.3.1/stlink-and-recovery.md) · [Diagnostyka](docs/pl/v1.3.1/troubleshooting.md).

![Menu M300Boot v1.3.1, render rzeczywistego kodu OLED](docs/assets/v1.3.1/BOOT_MAIN_MENU.png)

Podgląd pochodzi z renderera, nie ze zdjęcia próby sprzętowej. Migracja SD pozostawia pośrednik w APP: potem przywróć `RESTORE.BIN` lub właściwy zgodny MCU M3B. ST-Link zachowuje APP. BOOT, oryginalna aplikacja i MCU Klippera mają osobne wersje. Samodzielny `Waiting for Klipper` dostarcza osobna paczka MCU/host UART8, niedołączona do repozytorium bootloadera.

## Dokumentacja

| Lokalizacja | Zawartość |
|---|---|
| **[docs/pl](docs/pl/README.md)** | Pełne polskie instrukcje, wersja bieżąca i archiwum |
| **[docs/en](docs/en/README.md)** | Pełne angielskie instrukcje, wersja bieżąca i archiwum |
| `docs/assets/<wersja>` | Wspólne podglądy OLED |
| `docs/reports/<wersja>` | Maszynowe raporty walidacji |
| [firmware](firmware/README_PL.md) | Wersjonowane paczki i sumy kontrolne |
| [tools](tools/README_PL.md) | Narzędzia PC i opis zakresu działania |

Stare adresy dokumentów pozostają krótkimi odsyłaczami. Pełne instrukcje mają takie same nazwy plików w osobnych katalogach językowych. [Historia zmian](docs/pl/changelog.md) · [Potwierdzenia sprzętowe](docs/pl/v1.3.1/tested-hardware.md) · [Manifest wydania](docs/pl/v1.3.1/release-manifest.md).

## Pamięć i walidacja

| Zakres | Przeznaczenie |
|---|---|
| `0x08000000–0x08000FFF` | Zachowany prefix OEM, 4 KiB |
| `0x08001000–0x08007FFF` | BOOT stage2, 28 KiB |
| `0x08008000–0x08039FFF` | Jeden slot APP, 200 KiB |
| `0x0803A000–0x0803CFFF` | Zasoby, 12 KiB |
| `0x0803D000–0x0803D7FF` | Metadane APP |
| `0x0803D800–0x0803DBFF` | Osobne dzienniki baud i bootwait |
| `0x0803E000–0x0803FFFF` | NVM/dane producenta poza normalnym zapisem |

Przy publikacji v1.3.1 ponownie wykonano **2941 testów BOOT/instalatora** i **94 kontrole narzędzi PC**. Porządkowanie dokumentacji nie kompiluje firmware. [Raport publikacji](docs/reports/v1.3.1/PUBLICATION_VALIDATION.json). Nie deklarujemy automatycznego rollbacku po utracie zasilania, publicznego osobistego zrzutu Flash ani ogólnej kwalifikacji druku.

## Archiwum i zakres publikacji

[Instrukcje v1.1](docs/pl/v1.1/README.md) · [Pierwotne paczki v1.1](firmware/v1.1). Nie tworzymy fikcyjnych publicznych wydań dla prywatnych etapów 1.2/1.3. Tagi i oryginalne załączniki zachowują tożsamość wydania.

Publiczne są binaria, narzędzia operacyjne i instrukcje. Bez C/ASM firmware, ELF/map, kluczy OEM i prywatnych Flash/NVM/UID/numerów seryjnych. `RESTORE.BIN` i zasoby producenta zachowują jego prawa. [Opis praw do materiałów](docs/pl/third-party-notices.md) · [Licencja](LICENSE).

Projekt niezależny, niezatwierdzony przez Zortrax ani STMicroelectronics. **Wyłącznie klasyczna M300; bez M300 Plus, Dual i Inventure.**
