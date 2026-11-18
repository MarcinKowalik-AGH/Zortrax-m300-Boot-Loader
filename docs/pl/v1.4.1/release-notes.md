# Zmiany wydania — M300Boot 1.4.1

[English](../../en/v1.4.1/release-notes.md) · [Polski](../../pl/v1.4.1/release-notes.md) · [Indeks](README.md)

## Poprawka po audycie 18.11.2026

Po przerwaniu końcowego zapisu metadanych APP bazowa 1.4 mogła pozostawić stan `NO_COMMIT`, który prawidłowo blokował start, ale blokował także ponowną instalację przez SD/UART. W 1.4.1 dodano ograniczoną ścieżkę ponowienia: ten sam zweryfikowany kandydat musi pasować do przerwanego rekordu oraz całej już zapisanej APP, a zapis wymaga świeżego fizycznego potwierdzenia. Obce lub niezgodne metadane nadal powodują odmowę. [Warunki i procedura](installation.md#ponowna-instalacja-app-po-przerwanym-zapisie-metadanych).

Stały BOOT i instalator pośredni identyfikują się jako **1.4.1**. Zestaw UART pozostaje dokładnie **115200, 250000, 500000, 750000, 1500000**; domyślnie 250000 i bootwait OFF. **1000000 zostało usunięte już w 1.4**, a 10000000 także nie jest opcją. Zachowano kody obsługiwanych zapisów i jawną migrację starszej APP z dawnych prędkości.

Zachowano dwa segmenty BOOT, prefiks OEM, NVM, kwalifikację źródła/urządzenia, dwa backupy SD, odrębną zgodę na BOOT i kolejność przywracania APP. Pełne instrukcje i narzędzia dotyczą trzech wariantów **FACTORY, UPGRADE i STLINK**. Nowa wersja nie rozszerza profilu na inne modele ani nie daje automatycznego rollbacku.

## Zakres testów

Właściciel zgłosił około **dwóch tygodni użytkowania bazowej 1.4**; wcześniej potwierdził jej wszystkie trzy drogi instalacji. **Nowa poprawka 1.4.1 ma osobne wyniki audytu programowego.** Nie przypisujemy jej historycznego czasu testów. [Status sprzętowy](tested-hardware.md) · [Walidacja](validation.md) · [Raport z 18.11.2026](../../reports/v1.4.1/AUDIT_2026-11-18.json).

W przypadku drukarki już zatrzymanej przez stary BOOT 1.4 w `NO_COMMIT` standardowa aktualizacja SD może być nadal odrzucona przez stary kod. Zwykły plan ST-Link także wymaga poprawnej APP. Taki stan wymaga osobnej oceny kopii i planu odzyskania; nie usuwaj kontroli, aby wymusić instalację. Poprawka nie aktualizuje starego BOOT zdalnie ani automatycznie.

`RESTORE.BIN` pozostaje oryginalną aplikacją **Zortrax M300 1.3.1**; niezależna diagnostyka kopii pozostaje **0.5.5**. Klipper MCU/host jest osobnym projektem. Archiwalne paczki 1.4, 1.3.1 i 1.1 zachowują swoje tożsamości. Instrukcje zawierają [29 nowych renderów C wersji 1.4.1](../../assets/v1.4.1/README.md) z udokumentowanymi danymi przykładowymi i skrótami źródeł oraz obrazów; są to ilustracje, a nie zapisy testów sprzętowych.
