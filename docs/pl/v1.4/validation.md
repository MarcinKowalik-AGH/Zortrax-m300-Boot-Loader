# Walidacja — M300Boot 1.4

[English](../../en/v1.4/validation.md) · [Polski](../../pl/v1.4/validation.md) · [Index](README.md)

## Zakres

Audyt wydania obejmuje skompilowane BOOT i instalator, identyfikatory wersji w plikach wykonywalnych, dokładnie pięć prędkości, domyślne 250000, prędkość odzyskiwania, zgodność dziennika, zastępowanie usuniętych prędkości, źródła aktualizacji, chronione obszary, dwie niezależne kopie SD, gesty potwierdzenia, plan/odczyt ST-Link, integralność M3B, narzędzia w paczkach, sumy, odsyłacze i wyrenderowane ekrany OLED.

Raport rozróżnia kontrole programowe od fizycznej pracy. Dane zawierają rzeczywiście wykonane kontrole; archiwalnych liczb testów i wcześniejszych potwierdzeń sprzętowych nie przeniesiono jako wyników 1.4.

## Powtórzenie kontroli publicznych

W katalogu głównym publicznego repozytorium, Python 3.9 lub nowszy:

```sh
sha256sum -c SHA256SUMS.txt
python3 tools/validate_publication.py --json
```

[Manifest](../../../firmware/v1.4/RELEASE_MANIFEST.json) zapisuje tożsamości składników; [lista SHA-256](../../../firmware/v1.4/SHA256SUMS.txt) identyfikuje pliki pobierania. [Bieżący raport](../../reports/v1.4/PUBLICATION_VALIDATION.json) zawiera wyniki i ograniczenia. Kontrole publiczne niezależnie sprawdzają archiwa, adresy segmentów, dokładne skróty, zachowanie narzędzi i instrukcje. Prywatne testy firmware oraz źródła renderowania nie są częścią publicznego drzewa.

## Ograniczenia

Kontrole programowe publikacji nie otwierają sondy ani drukarki. Właściciel potwierdził wszystkie trzy metody instalacji przebudowanej 1.4; zakres opisuje [tabela sprzętu](tested-hardware.md). Nie ma automatycznego cofania zapisu BOOT po utracie zasilania. Zachowano kontrole tożsamości i zabezpieczeń. PASS programu nie oznacza zgodności każdej płyty M300 ani rezerwy podczas druku.

Końcowa walidacja komputerowa: **2784 testy PASS, 0 błędów, 0 pominięć**; zaliczono **51 kontroli binariów BOOT** oraz **59 kontroli instalatora i czystej przebudowy**. Trzy warianty BOOT i instalator odtwarzają się bajt w bajt przy Clang/LLD 19.1.1. Późniejsze [zgłoszenie odbioru przez właściciela](../../reports/v1.4/HARDWARE_ACCEPTANCE.json), zapisane 09.11.2026, potwierdza na drukarce FACTORY, UPGRADE i ST-Link. Niezmieniony manifest wydania opisuje stan z chwili pierwotnej publikacji. Narzędzia programowe nie wykonywały tych prób fizycznych.

## Przegląd kompletności instrukcji — 09.11.2026

Ponowny przegląd kodu obejmuje wszystkie 13 stron BOOT / 50 początkowych pozycji menu, 27 form komend BOOT, osiem obszarów DUMP, siedem opcji i dziewięć form komend instalatora. Publiczny spis zawiera skróty odpowiadających mu źródeł. Dodana kontrola wykrywa pominięcie opcji lub przyjmowanej komendy w obu językach; poprawność znaczenia i kolejności procedur porównano dodatkowo z implementacją. Paczki firmware nie były zmieniane.

[Inventory](../../reports/v1.4/DOCUMENTED_OPTIONS.json) · [Review report](../../reports/v1.4/DOCUMENTATION_REVIEW.json)

```sh
python3 tools/validate_option_coverage.py --json
```
