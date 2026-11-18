# Historia zmian

[English](../../CHANGELOG.md) · [Polski](changelog.md)

## 1.4.1 — 18.11.2026

- Usunięto blokadę ponowienia APP po przerwanym zapisie metadanych: wymagane są ta sama zweryfikowana paczka, rozpoznany przerwany rekord, zgodność całej APP we Flash i nowe fizyczne potwierdzenie. Niepełny commit nadal blokuje start; obce rekordy i uszkodzona APP powodują odmowę.
- Przebudowano BOOT i instalator jako 1.4.1. Kontrole ponowienia wykorzystują istniejącą lukę pomiędzy wektorami a punktem wejścia OEM; jego stały adres, początek APP, granice obszarów programowania, prefiks OEM, NVM i dzienniki ustawień pozostają chronione.
- Przygotowanie karty serwisowej odrzuca niepoprawne istniejące pliki docelowe przed tworzeniem brakujących szablonów. Poprawiono zamykanie portu i logów po błędach połączenia oraz dokładną kontrolę linii wersji i stanu płyty. Bieżące narzędzia pasują do wydania; narzędzia 1.4 zachowano w archiwum.
- Zachowano dokładnie 115200/250000/500000/750000/1500000, domyślnie 250000 / bootwait OFF. 1000000 usunięto już w 1.4; 10000000 nie jest obsługiwane. Zachowano obsługiwane kody ustawień i jawną migrację przed starszą APP.
- Zaktualizowano trzy warianty: FACTORY, UPGRADE i STLINK, wraz z kompletem instrukcji EN/PL, instrukcjami w paczkach, bezpośrednimi linkami, manifestami, sumami kontrolnymi i aktualnymi renderami OLED z kodu C.
- Rozdzielono dowody: właściciel zgłasza około dwóch tygodni używania bazowej 1.4, której drogi instalacji wcześniej zaakceptowano; nowa poprawka 1.4.1 ma walidację offline z 18.11.2026, bez przypisywania jej dwóch tygodni testów sprzętowych. [Status sprzętowy](../reports/v1.4.1/HARDWARE_STATUS.json) · [Audyt](../reports/v1.4.1/AUDIT_2026-11-18.json).
- Ponowienie wymaga działającego BOOT 1.4.1. Starszy BOOT już zatrzymany w `NO_COMMIT` wymaga osobnej oceny odzyskiwania; zwykły ST-Link preflight wciąż wymaga poprawnej APP. Nie dodano automatycznego powrotu po zaniku zasilania. [Dwujęzyczny opis i pobieranie](../../RELEASE_NOTES_v1.4.1.md).

## 1.4 — 08.11.2026

- Odbiór właściciela zapisany 09.11.2026: FACTORY, UPGRADE i ST-Link zwalidowane na drukarce. Opublikowano niezmieniony oryginalny Zortrax Bootloader v3 z pochodzeniem i SHA-256. Paczki instalacyjne i tag wydania pozostają niezmienione.

- Przegląd instrukcji 09.11.2026: pełny wykaz menu i komend, instalacja oraz odzyskiwanie z obsługą samym OLED-em i pokrętłem, kontrola pokrycia opcji i odsyłacze do bieżących instrukcji w opisie wydania. Paczki firmware zachowują pierwotną tożsamość.

- Spójne 1.4 stałego BOOT i instalatora pośredniego, bez dopisków rozwojowych.
- Dokładnie pięć prędkości 115200/250000/500000/750000/1500000; domyślnie 250000 / bootwait OFF.
- Nieobsługiwane stare zapisy dają aktywne 250000 bez samoczynnego przepisania Flash; opisano jawną migrację przed uruchomieniem starszej APP, z zachowaniem obsługiwanych kodów.
- Przebudowane paczki, zgodne narzędzia i walidacja programowa; późniejszy odbiór sprzętowy właściciela zapisano osobno.
- Pełne instrukcje EN/PL i rendery cyan z czcionką OLED. [Zmiany](v1.4/release-notes.md).

## Porządek dokumentacji — 30.10.2026

- Pełne instrukcje w `docs/en/<wersja>` i `docs/pl/<wersja>`, z identycznymi nazwami plików i przełącznikiem języka.
- Oddzielne EN/PL indeksy projektu, narzędzi i firmware oraz historie zmian, opisy wydań, sprzętu i manifestów.
- Wspólne ilustracje w `docs/assets`, historyczne raporty maszynowe w `docs/reports`; stare adresy zachowane jako odsyłacze.
- Wyraźnie rozdzielone bieżące v1.3.1 i archiwalne v1.1. Bez zmiany firmware, publicznych ZIP-ów, tagów i zakresu potwierdzeń sprzętowych.

## v1.3.1 — 30.10.2026

- Menu UART od 115200 do 1500000, zgodność dawnych indeksów zapisu.
- Trwałe UART on bootwait OFF/ON; binarny host nie przerywa autostartu, poprawione fałszywe busy lokalnej zmiany baud.
- Zachowane częściowe OLED, bezpośrednie kroki enkodera i chronione dzienniki.
- Paczki UPGRADE, FACTORY i ST-Link z dwoma segmentami, instrukcje EN/PL i aktualne narzędzia PC.
- Właściciel potwierdził wszystkie trzy drogi instalacji, UART8 przy 1500000 i samodzielne działanie OLED.
- Przy publikacji 2941 testów BOOT/instalatora i 94 kontrole narzędzi PC PASS. [Zmiany wydania](v1.3.1/release-notes.md).

## Uzupełnienie dokumentacji v1.1 — 29.10.2026

- Właściciel zgłosił działające FACTORY na drugiej drukarce; pozostało potwierdzenie UPGRADE/startu oryginalnego 1.3.1 na scharakteryzowanym egzemplarzu.
- Rozróżniono zgłoszenie od logów poszczególnych etapów stałego BOOT. W tym historycznym zapisie ST-Link nie był jeszcze osobno potwierdzony. Bez zmiany binariów i blokad profilu.

## Publikacja v1.1 — 29.10.2026

- Wersja M300 boot v1.1 i odczyt danych sprzętowych z urządzenia.
- Postęp faz, responsywny enkoder i ograniczone menu wywodzące się z rc3.
- Potwierdzenia instalatora 1.1-i4, ograniczanie częstotliwości odrysowania i szczegóły odmowy.
- FACTORY, UPGRADE, ST-Link z generowaniem prywatnego obrazu offline i procedury zachowania oryginału.
- Binarna publikacja firmware, publiczne adaptacje narzędzi i osobna walidacja offline; zachowane oryginalne załączniki. [Historyczny opis](v1.1/release-notes.md).
