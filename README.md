# M300Boot v1.3.1 — classic Zortrax M300

**Independent service bootloader / Niezależny bootloader serwisowy**
**Autor / Author:** Marcin Kowalik · mkowalik@agh.edu.pl
**Target / Sprzęt:** classic M300, PCB Rev.5.3 / HW05 / STM32F103-family / measured 256 KiB Flash.

**Current / Bieżące: BOOT 1.3.1 · SD installer 1.3.1 · 2026-10-30.**
**UPGRADE, FACTORY i ST-Link potwierdzone na sprzęcie przez właściciela / all three installation routes owner-confirmed on hardware.** UART8 at **1500000 baud** and the standalone MCU waiting/display stage were also confirmed.

## Pobierz / Download

| Stan urządzenia / Device state | Pakiet / Package |
|---|---|
| Rozpoznany własny M300Boot / recognized custom boot | [SD_UPGRADE v1.3.1](firmware/v1.3.1/M300Boot_v1.3.1_SD_UPGRADE.zip) |
| Oryginalny OEM v3, zgodny profil / original OEM v3, matching profile | [SD_FACTORY_OEMV3 v1.3.1](firmware/v1.3.1/M300Boot_v1.3.1_SD_FACTORY_OEMV3.zip) |
| SWD, RDP już wyłączone / SWD, RDP already off | [STLINK v1.3.1 — dwa segmenty / two segments](firmware/v1.3.1/M300Boot_v1.3.1_STLINK.zip) |
| Zachowanie OEM BOOT/NVM przy RDP / preserve original BOOT/NVM under RDP | [Diagnostyka UART 0.5.5 / unchanged backup diagnostic](firmware/v1.3.1/M300_BACKUP_0.5.5_UART.zip) |

**[Instrukcje PL](docs/v1.3.1/INSTALACJA_PL.md) · [English installation](docs/v1.3.1/INSTALLATION_EN.md) · [Wszystkie instrukcje / Complete documentation](docs/v1.3.1/README.md)**
[GitHub Release v1.3.1](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.3.1) · [SHA-256](firmware/v1.3.1/SHA256SUMS.txt) · [Manifest](docs/v1.3.1/RELEASE_MANIFEST.md)

**Najpierw kopia / Backup first:** zachowaj własne BOOT/NVM/UID/SIZE/Option Bytes i zgodne niezależne kopie Flash. Zdjęcie aktywnego RDP w STM32F1 kasuje główną Flash. Publiczne instalatory zachowują blokady profilu konkretnego egzemplarza; samo M300/HW05 nie wystarcza. / Preserve your own verified backups; do not remove RDP to obtain a read or bypass installer identity checks. [PL](docs/v1.3.1/KOPIA_ORYGINALU_PL.md) · [EN](docs/v1.3.1/ORIGINAL_BACKUP_EN.md).

## Nowe funkcje / Current features

| Funkcja / Feature | Działanie / Behavior |
|---|---|
| UART **115200 / 250000 / 500000 / 750000 / 1000000 / 1500000** | W tej kolejności w menu; zapis Flash z kontrolą odczytu. / Ordered menu, persistent selection with readback. Legacy 19200/57600 records remain readable. |
| **UART on bootwait OFF / ON** | OFF: ruch Orange Pi nie przerywa autostartu. ON: pełne dozwolone linie otwierają diagnostykę. / Host binary traffic does not interrupt the countdown; ON allows complete diagnostic lines. Default 250000/OFF. |
| Zmiana baud / Baud selection | Poprawione fałszywe busy i porzucanie części linii hosta; lokalne ekrany ustawień odrzucają RX. / Corrected local busy handling and isolated settings screens. |
| OLED i enkoder / OLED and encoder | Częściowa aktualizacja, pomijanie identycznych klatek, bezpośrednie kroki, Back w podmenu, brak zawijania. / Dirty rectangles, identical-frame skip, direct detents, pinned Back and bounded scrolling. |
| Rozruch / Startup | Pięć sekund po inicjalizacji; pokrętło otwiera serwis; przytrzymanie przy włączeniu wymusza 250000 tylko na tę sesję. / Five-second countdown and temporary 250000 recovery entry. |
| Instalacja / Installation | SD: profil, kontrola karty, dwie kopie i świeże potwierdzenie 5 s. ST-Link: dwa zakresy i pełny readback 256 KiB. / Guarded SD transaction or two-segment SWD with full readback. |
| Diagnostyka / Diagnostics | Odczytywane Hardware/serial/czas, kontrola Flash, kopie, historia i postęp bieżącej fazy. / Live hardware records, verification, backup, history and phase progress. |

**[Pełny opis PL](docs/v1.3.1/FUNKCJE_I_KONSOLA_PL.md) · [Features EN](docs/v1.3.1/FEATURES_AND_CONSOLE_EN.md) · [UART PL](docs/v1.3.1/KONSOLA_UART_PRZYKLADY_PL.md) · [UART EN](docs/v1.3.1/UART_EXAMPLES_EN.md)**

![M300Boot v1.3.1 — native renderer preview](docs/v1.3.1/images/BOOT_MAIN_MENU.png)

*Render z rzeczywistego kodu OLED, nie zdjęcie testu / Actual OLED renderer output, not a hardware-test photograph.*

## Po aktualizacji / After installation

**SD pozostawia instalator jako APP** — przywróć `RESTORE.BIN` (oryginalny Zortrax M300 1.3.1) albo zgodny MCU M3B. **ST-Link zachowuje APP.** BOOT, stock APP i MCU Klipper mają osobne wersje. Ekran `Waiting for Klipper` i obsługa zapisanego baud po stronie MCU należą do osobnej aplikacji UART8; ta publikacja jej nie dołącza.

**SD leaves the intermediary in APP**: restore stock or the intended MCU application after BOOT replacement. Matching UART8 MCU/host support is required at 1500000. A working display/Ready state is not motion/heater or print-load qualification. [Diagnostyka PL](docs/v1.3.1/DIAGNOSTYKA_PL.md) · [Troubleshooting EN](docs/v1.3.1/TROUBLESHOOTING_EN.md).

## Mapa pamięci / Memory layout

| Zakres / Range | Przeznaczenie / Purpose |
|---|---|
| `0x08000000–0x08000FFF` | Zachowany prefix OEM / preserved first 4 KiB |
| `0x08001000–0x08007FFF` | BOOT stage2 — 28 KiB |
| `0x08008000–0x08039FFF` | Jeden slot APP / one application slot — 200 KiB |
| `0x0803A000–0x0803CFFF` | Zasoby / assets — 12 KiB |
| `0x0803D000–0x0803D7FF` | Metadane APP / application metadata |
| `0x0803D800–0x0803DBFF` | Osobne dzienniki baud i bootwait / separate journals |
| `0x0803E000–0x0803FFFF` | Dane producenta/NVM poza normalnym zapisem / protected manufacturer data |

Nie ma publicznego pełnego BIN-a pod 0x08000000 ani automatycznego rollbacku po utracie zasilania. / No complete personal Flash image or automatic power-loss rollback is published. [ST-Link PL](docs/v1.3.1/STLINK_I_ODZYSKIWANIE_PL.md) · [ST-Link EN](docs/v1.3.1/STLINK_AND_RECOVERY_EN.md).

## Wersje / Versions

| Wersja / Version | Status | Dokumentacja / Docs | Pliki / Files |
|---|---|---|---|
| **v1.3.1** | **Bieżąca / Current** | [docs/v1.3.1](docs/v1.3.1/README.md) | [firmware/v1.3.1](firmware/v1.3.1) |
| v1.1 / i4 | Archiwalna / Archived, immutable original assets | [docs/v1.1](docs/v1.1/README.md) | [firmware/v1.1](firmware/v1.1) |

[Indeks dokumentacji](docs/README.md) · [Zmiany / Changelog](CHANGELOG.md) · [Potwierdzenia sprzętowe / Hardware evidence](docs/v1.3.1/TESTED_HARDWARE.md) · [Narzędzia / Tools](tools/README.md).

Układ jak dotąd: `docs/v<version>` — pełne instrukcje EN/PL, `firmware/v<version>` — publiczne binaria i manifest, `docs/*.md` — zgodne odsyłacze. Nie tworzymy fikcyjnych publicznych wydań dla prywatnych etapów 1.2/1.3. / Versioned docs and binaries retain the established layout; no synthetic historical releases.

## Zakres publikacji / Publication scope

2941 testów BOOT/instalatora ponownie PASS; archiwa, protokoły, HEX, linki i prywatność kontrolowane osobno. / 2941 boot/installer tests re-run successfully, with separate public-package validation. Owner-confirmed UPGRADE, FACTORY, ST-Link and 1.5-Mb/s link; no universal board/power-loss/printing qualification inferred.

Publiczne są binaria, narzędzia operacyjne, instrukcje PL/EN, sumy i podglądy. Bez C/ASM firmware, ELF/map, kluczy OEM, prywatnych pełnych Flash/NVM/UID, numerów seryjnych i gotowych osobistych obrazów odtworzeniowych. / Binary firmware publication; no private device dumps, firmware sources or vendor-key tools.

`RESTORE.BIN` zachowuje prawa producenta. MIT dotyczy nowo napisanych elementów, nie firmware/zasobów producenta. / Manufacturer material retains its rights. [Notices](THIRD_PARTY_NOTICES.md). Independent project, not endorsed by Zortrax or STMicroelectronics. **Classic M300 only — not M300 Plus, Dual or Inventure.**
