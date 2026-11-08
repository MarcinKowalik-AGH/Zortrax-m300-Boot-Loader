# Historia zmian

[English](../../CHANGELOG.md) · [Polski](changelog.md)

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
