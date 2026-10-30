# Audyt i uporządkowanie repozytorium M300 boot v1.1

[English](../../en/v1.1/publication-audit.md) · [Polski](../../pl/v1.1/publication-audit.md) · [Indeks](README.md)

**Archiwalny zapis v1.1 z 29 października 2026.** Poniższe ustalenia zachowują historyczny zakres. [Bieżąca v1.3.1](../v1.3.1/README.md).

**Data:** 29.10.2026. **Punkt odniesienia:** publiczna publikacja Inventure boot **v1.5-HW2**, po reorganizacji `docs/v1.5`, `docs/v1.4` i indeksu `docs/README.md` (nie historyczna v1.4). **Zakres:** aktualizacja dokumentacji i kontrola publikacji; bez kompilacji, podmiany lub modyfikowania firmware M300 i4.

## Wykryte rozbieżności i zastosowana naprawa

| Ustalenie | Naprawa |
|---|---|
| M300 v1.1 miał szczegółowe PL/EN instrukcje w płaskim `docs/`, w odróżnieniu od bieżącego Inventure v1.5 | Pełna dokumentacja obecnej wersji została skopiowana bez zmian merytorycznych do `docs/v1.1`; `docs/README.md` prowadzi do właściwej wersji. Stare `docs/*.md` są kompatybilnymi odsyłaczami. Nie tworzono fikcyjnej historii v1.0. |
| Funkcje i konsola były omówione razem, bez oddzielnych przykładów jak Inventure `P4` | Dodano `KONSOLA_UART_PRZYKLADY_PL.md` i `UART_EXAMPLES_EN.md`: PING/INFO, read-only DUMP, M3B inspect/pack/check, SD backup. Przykłady korzystają z rzeczywistych argumentów `--help`. |
| Brak automatycznego testu publikacji uruchamianego przy zmianach plików | Dodano `tools/validate_publication.py` i workflow `publication-audit.yml`: suma i zawartość 4 archiwów, parzystość dwóch kart, RESTORE, stage2/zasoby i sparse HEX, M3B, prywatność, linki Markdown, składnia Python 3.9, CLI i negatywne CRC/SHA. |
| Instrukcje mogły być odczytane jako deklaracja uniwersalnej zgodności | Powtórzono w indeksie, że obrazy i4 są blokowane hashami konkretnego rozpoznanego egzemplarza. Brak automatycznego włączenia obsługi innej M300/HW05. |
| Wcześniejsza publikacja mieszała bieżącą wersję dokumentacji z historycznym stanem taga | README jawnie odróżnia binaria GitHub Release v1.1 (bez zmian) od dokumentacji na `main`, na wzór Inventure v1.5. |

## Zakres potwierdzenia sprzętowego

Właściciel potwierdził **UPGRADE** do M300 boot v1.1 przy użyciu SD installer **1.1-i4**, następnie przywrócenie i uruchomienie oryginalnego **Zortrax 1.3.1** na **jednym** egzemplarzu klasycznej M300, **PCB Rev. 5.3 / menu HW05 / STM32F1 0x414 / wewnętrzny SIZE 256 KiB**. Ostatni pomiar licznika i numer seryjny są zachowane w prywatnym archiwum; nie opublikowano ich bajtów.

Nie wykazano oddzielnego testu FACTORY i4 od OEM v3, nowego fizycznego programowania przez ST-Link, nieprzerwanego drukowania, innych płyt ani zachowania przy zaniku zasilania. Pośrednik i4 pozostaje zgodny **tylko z jednoznacznie rozpoznanym profilem**. RDP/Option Bytes nie wolno zmieniać w celu obejścia odmowy.

## Oddzielny test odzyskiwania ST-Link na kopii prywatnej

Przeprowadzono **wyłącznie lokalny test offline** z wcześniejszą, zweryfikowaną parą zrzutów. `check_backup_profile.py` zwrócił `PASS_I4_PROFILE_MATCH`, a generator `prepare_stlink.py` utworzył oba warianty (`m300` oraz `oem`) po 262144 bajty z zachowanym chronionym prefiksem i końcowym 8 KiB. Nie podłączano programatora, nie wyłączano RDP ani nie testowano fizycznego uruchomienia tych obrazów. Dane testowe pozostają poza publicznym repozytorium.

## Prawa i integralność dystrybucji

Wszystkie cztery publiczne ZIP-y są **bajtowo identyczne** z opublikowanymi załącznikami v1.1; nie przebudowywano żadnego MCU BIN. Plik RESTORE zawiera aplikację producenta Zortrax 1.3.1 z zachowaniem praw producenta; licencja MIT nie przenosi tych praw na projekt. Nie ma C/ASM firmware, ELF/map, prywatnego UID, NVM, zrzutów ani narzędzi OEM-key. Dystrybucja oryginalnej aplikacji może wymagać osobnego uprawnienia od producenta; techniczna walidacja nie zastępuje weryfikacji prawnej.

## Audyt powtarzalny

Z katalogu głównego repozytorium uruchom:

```sh
python3 tools/validate_publication.py --json
```

Wynik i szczegółowy podział kontroli przedstawia [AUDIT_CHECKS.json](../../reports/v1.1/AUDIT_CHECKS.json). Test nie otwiera UART, SWD ani GitHub; automatyczny workflow wykonuje go na zmianach repozytorium i **nie publikuje ponownie firmwaru**.

**Załączniki istniejącego GitHub Release i tag v1.1 pozostają bez zmian.** Dokumentacja i nowe testy są dostępne na `main`.

[Pełna dokumentacja v1.1](README.md) · [Indeks wersji](../README.md) · [Wydanie v1.1](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/tag/v1.1)
