# Diagnostyka — v1.3.1

[English](TROUBLESHOOTING_EN.md) · [Indeks](README.md)

| Objaw | Kontrola/działanie |
|---|---|
| Orange Pi przerywa odliczanie | Sprawdź `M300 boot v1.3.1`; ustaw `Diagnostics → UART → UART on bootwait → OFF`. OFF odrzuca odbiór hosta w odliczaniu. Niezależnie menu mogą zatrzymać recovery lub fizyczny sygnał pokrętła. |
| Potrzebna konsola od początku | Zapisz bootwait ON. Wyślij pełną dozwoloną linię, np. `INFO` i nową linię. Pojedynczy bajt i binarna próba Klippera nie otwierają menu. |
| `busy` / `Operation rejected` przy baud | Sprawdź nowy boot, puść pokrętło, wejdź do ustawienia bez aktywnej operacji. Ekrany ustawień odrzucają próby hosta. Prawdziwy timeout UART, niezgodne warunki lub pełny dziennik nadal uzasadniają odmowę; nie kasuj ustawień na siłę. |
| Zapisane 1500000, aktywne 250000 | Przytrzymanie przy włączeniu wymusza 250000 tylko w tej sesji. Uruchom normalnie. `INFO` rozróżnia aktywne `UART_BAUD` i `SAVED`. Instalator SD także używa tymczasowo 250000. |
| MCU Klippera nadal czeka na 250000 | Sprawdź APP z odczytem dziennika i UART8; sam BOOT nie aktualizuje sterownika szeregowego aplikacji. Dopasuj istniejące `[mcu] baud` hosta. |
| `Waiting for Klipper` dopiero po hoście | To ekran aplikacji MCU. Potrzebny jest zgodny firmware z samodzielnym startem OLED; nie ma go w tej publikacji samego BOOT. |
| Nowy boot znów uruchamia instalator SD | Migracja SD pozostawia pośrednik jako APP. Wejdź do BOOT i przywróć `RESTORE.BIN` lub właściwy sprawdzony MCU M3B. Nie wymieniaj ponownie BOOT w pętli. |
| Odmowa profilu/źródła/karty | Zachowaj konkretny błąd i kopie. Sprawdź sześć plików, listę źródeł, oryginalny profil i nowe szablony A5. Nie usuwaj blokad i nie przenoś danych innej drukarki. |
| `Settings full` | Dziennik dopisywany jest pełny; ponowny wybór bieżącej wartości nie zużywa rekordu. Nie ma automatycznego kasowania. Przed osobno zaplanowanym serwisem zachowaj pełny zweryfikowany zrzut. |
| MCU pozostał w shutdown po zatrzymaniu hosta | Przed resetem zachowaj pierwszą przyczynę z logu Klippera. Utrata komunikacji i błąd transportu OLED to różne sytuacje; ostatni ogólny komunikat nie dowodzi błędu baud. |
| ST-Link nie odczytuje przy RDP | Wybierz SD i zachowanie oryginału. Read Unprotect kasuje Flash; dwa segmenty nie są obrazem całego skasowanego układu. |
| Różny readback po SWD | Pozostaw rdzeń zatrzymany; zachowaj prywatnie before/after/UID/options. Nie uruchamiaj, nie resetuj i nie kasuj całego układu automatycznie. |

Normalnie UART ma jednego właściciela. Liczą się wersja firmware, zgodne baud i świeży status; samo `active` usługi tego nie potwierdza. Ready i działający OLED nie kwalifikują ruchu, grzania ani druku.
