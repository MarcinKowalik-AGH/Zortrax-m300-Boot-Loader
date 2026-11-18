# M300Boot 1.4.1 — dokumentacja

[English](../../en/v1.4.1/README.md) · [Polski](../../pl/v1.4.1/README.md) · [Indeks](README.md)

**Bieżące wydanie: 1.4.1.** Bootloader serwisowy dla zakwalifikowanego profilu klasycznej Zortrax M300: HW05 / PCB Rev.5.3 / zmierzone 256 KiB Flash.

Właściciel zgłosił 18.11.2026 około **dwóch tygodni użytkowania bazowej wersji 1.4**; wcześniejszy odbiór tej wersji obejmował FACTORY, UPGRADE i ST-Link. **1.4.1 zawiera nową poprawkę i ma osobną walidację programową z bieżącego audytu. Nie przypisujemy jej dwóch tygodni testów sprzętowych.** [Zakres dowodów](tested-hardware.md) · [Wyniki audytu](validation.md).

W 1.4.1 poprawiono możliwość kontrolowanej ponownej instalacji tego samego obrazu APP po przerwanym końcowym zapisie metadanych. Zachowano kwalifikację urządzenia, kontrolę całego obrazu, chronione zakresy i fizyczne potwierdzenie. Przed użyciem przeczytaj [dokładny zakres ponownej instalacji](installation.md#ponowna-instalacja-app-po-przerwanym-zapisie-metadanych).

## Trzy warianty instalacji

| Stan drukarki | Pobieranie | Instrukcja |
|---|---|---|
| Oryginalny, zakwalifikowany OEM v3 | [SD_FACTORY_OEMV3](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_SD_FACTORY_OEMV3.zip) | [Instalacja SD](installation.md) |
| Rozpoznany, działający własny M300Boot | [SD_UPGRADE](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_SD_UPGRADE.zip) | [Instalacja SD](installation.md) |
| Działający odczyt SWD, RDP już wyłączone, poprawna APP i zgodny profil | [STLINK](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.4.1/M300Boot_v1.4.1_STLINK.zip) | [Dwa segmenty i pełna weryfikacja](stlink-and-recovery.md) |

[Wydanie na GitHub](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.4.1) · [SHA-256](../../../firmware/v1.4.1/SHA256SUMS.txt) · [Manifest](release-manifest.md).

## Pełne instrukcje

- [Instalacja FACTORY i UPGRADE krok po kroku](installation.md)
- [Kopie oryginału, kopia BOOT i dwie kopie instalatora](original-backup.md)
- [Wszystkie menu, funkcje i komendy](features-and-console.md)
- [UART, zapis ustawień i migracja starszej APP](uart-examples.md)
- [ST-Link, adresy i pełny odczyt kontrolny](stlink-and-recovery.md)
- [Rozwiązywanie problemów](troubleshooting.md)
- [Sprzęt i zakres potwierdzeń](tested-hardware.md)
- [Walidacja oraz kompletność opisu](validation.md)
- [Zmiany wydania](release-notes.md)

Dokładnie pięć prędkości UART: **115200, 250000, 500000, 750000, 1500000**, 8N1. **1000000 i 10000000 nie są obsługiwanymi pozycjami.** Wartość 1000000 usunięto już w 1.4; 1.4.1 zachowuje tę decyzję. Domyślnie **250000 / bootwait OFF**. Zgłoszenie problemu z dzielnikami Orange Pi jest przyczyną pozostawienia 1000000 poza listą; dobierz jedną z obsługiwanych wartości zgodnie z konfiguracją danego hosta.

Instalacja SD zastępuje APP pośrednikiem: po zapisie BOOT jawnie przywróć stock lub zgodną aplikację Klippera. ST-Link zapisuje dwa segmenty BOOT i zachowuje APP. Oryginalna APP w `RESTORE.BIN` pozostaje **Zortrax 1.3.1**, a dodatkowa diagnostyka kopii **0.5.5** jest osobnym narzędziem, nie czwartym wariantem instalacji. [Archiwum bazowej 1.4](../v1.4/README.md).
