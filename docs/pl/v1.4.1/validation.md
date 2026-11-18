# Walidacja — M300Boot 1.4.1

[English](../../en/v1.4.1/validation.md) · [Polski](../../pl/v1.4.1/validation.md) · [Indeks](README.md)

## Bieżący zakres i dowody

Audyt z 18.11.2026 obejmuje źródła i binaria BOOT/instalatora, ponowienie zapisu APP po przerwanym zatwierdzaniu metadanych, zachowanie odmów obcych danych, pięć prędkości UART i migrację kodów dziennika, chronione zakresy, dwie kopie SD, fizyczne gesty, plan i pełny odczyt ST-Link, format M3B, narzędzia hosta, zgodność trzech paczek, sumy oraz instrukcje EN/PL.

[AUDIT_2026-11-18.json](../../reports/v1.4.1/AUDIT_2026-11-18.json) zawiera rzeczywiście wykonane kontrole i ich wyniki. [HARDWARE_STATUS.json](../../reports/v1.4.1/HARDWARE_STATUS.json) oddziela historię sprzętową bazowej 1.4 od nowej poprawki. Dokładne skróty i rozmiary pobrań określa [manifest 1.4.1](../../../firmware/v1.4.1/RELEASE_MANIFEST.json).

Właściciel zgłosił około dwóch tygodni użytkowania **1.4**. Kod poprawki **1.4.1** powstał w bieżącym audycie i podlega osobnej walidacji programowej. Historyczne liczby 2784 testów oraz 51/59 kontroli z publikacji 1.4 pozostają dowodami tamtej publikacji; nie są nowym wynikiem uzyskanym przez samą zmianę numeru.

## Wyniki offline — 18.11.2026

| Kontrola | Wynik | Zakres |
|---|---|---|
| Prywatny zestaw regresji BOOT/instalatora | **2992 zaliczone, 34 pominięte, 0 błędów** | 34 pominięte przypadki dotyczą faz zapisu w trybie READONLY; nie są wliczane do zaliczonych. |
| Niezależna czysta kompilacja | **59 kontroli zaliczonych** | BOOT w trybach FULL, READONLY i PREVIEW oraz instalator dały identyczne bajtowo wyniki przebudowy. |
| Skompilowany warunek metadanych ARM | **105 przypadków zaliczonych** | Rzeczywisty skompilowany kod decyzji płyty/metadanych wykonano w Unicorn. To izolowana kontrola tego warunku, nie pełny start BOOT ani test fizycznej drukarki. |
| Publiczne testy jednostkowe narzędzi hosta | **13 zaliczonych** | Obejmują kontrole karty serwisowej, dokładną akceptację INFO, sprzątanie częściowo otwartych zasobów oraz zachowanie manifestu/archiwum przy błędzie zamykania. |

Są to nowo wykonane kontrole komputerowe 1.4.1. Szczegóły i narzędzia podano w [raporcie audytu](../../reports/v1.4.1/AUDIT_2026-11-18.json). Nie stanowią odbioru sprzętowego ani dwutygodniowej historii testów nowej poprawki.

## Powtórzenie kontroli publicznych

W katalogu głównym repozytorium, Python 3.9 lub nowszy:

```sh
sha256sum -c SHA256SUMS.txt
python3 tools/validate_publication.py --json
```

W macOS odpowiednikiem pierwszej komendy jest `shasum -a 256 -c SHA256SUMS.txt`. Do pojedynczego pobranego ZIP-a w PowerShell użyj `Get-FileHash -Algorithm SHA256 <plik.zip>` i porównaj pełny skrót z [listą wydania](../../../firmware/v1.4.1/SHA256SUMS.txt).

Publiczna walidacja sprawdza dostępne paczki, formaty, adresy, narzędzia i opis. Prywatny kod firmware i testy wymagające tego kodu nie są częścią publicznego repozytorium. Liczby kontroli sum/rekordów HEX obejmują wiele sprawdzeń bajtowych i nie oznaczają takiej samej liczby niezależnych scenariuszy zachowania drukarki.

## Co musi potwierdzać poprawka metadanych

- Brak poprawnego znacznika commit nadal blokuje uruchomienie APP.
- Ponowienie dotyczy wyłącznie zweryfikowanego kandydata zgodnego z przerwanym zapisem i całym obrazem APP w pamięci.
- Niezgodne metadane, obcy obraz, błędny skrót lub uszkodzona zawartość APP nie uzyskują ogólnej zgody na kasowanie.
- Ponowna instalacja nadal wymaga właściwego profilu i świeżego fizycznego potwierdzenia 2 s.
- Prefiks OEM, BOOT, dzienniki ustawień i dane producenta pozostają poza zapisem APP.

Wyniki konkretnych scenariuszy i użyta wersja narzędzi znajdują się w raporcie audytu. Test nie oznacza obietnicy automatycznego odzyskania dowolnego przerwania zapisu ani cofnięcia firmware po utracie zasilania.

## Kompletność instrukcji

Zachowano pełne instrukcje bazowej 1.4: 13 stron BOOT, 50 początkowych pozycji, 27 form komend, osiem obszarów DUMP oraz siedem opcji i dziewięć form komend instalatora. Wersje, nazwy paczek, komenda `INSTALL V141`, wyniki i procedura ponownej instalacji APP są opisane dla 1.4.1. [Pełna referencja](features-and-console.md) i [instalacja](installation.md) są dostępne w obu językach.

[29 aktualnych renderów OLED](../../assets/v1.4.1/README.md) powstało przez wykonanie renderera C wersji 1.4.1 z oryginalną czcionką bitmapową i udokumentowanymi danymi przykładowymi. Natywny obraz ma 256×64 piksele; podglądy to dokładne powiększenia 4× metodą najbliższego sąsiada, w kolorze cyjan na czarnym tle. [Manifest renderów](../../assets/v1.4.1/RENDER_MANIFEST.json) zawiera skróty źródeł i obrazów, a [walidacja renderów](../../assets/v1.4.1/RENDER_VALIDATION.json) zapis wykonania natywnego menu i potwierdzeń oraz kontroli odczytu PNG. Ilustracje nie potwierdzają wykonania operacji na drukarce i nie zastępują testów sprzętowych.
