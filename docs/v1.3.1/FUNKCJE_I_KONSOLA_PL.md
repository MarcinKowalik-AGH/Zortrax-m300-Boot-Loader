# Funkcje i konsola — M300Boot v1.3.1

[English](FEATURES_AND_CONSOLE_EN.md) · [Indeks](README.md)

Stały bootloader i instalator SD pokazują **1.3.1**. Kontener FACTORY zgodny z OEM ma techniczną wersję **9.8.7**; nie jest to wersja uruchomionego bootloadera.

## Menu i wyświetlanie

| Pozycja główna | Działanie |
|---|---|
| Start application | Kontrola aplikacji i uruchomienie po lokalnym potwierdzeniu. |
| Firmware on SD | Kontrola/instalacja pakietu; wybór z katalogu do 16 plików. Sam wybór nie sprawdza ani nie instaluje obrazu. |
| Diagnostics | Verify Flash, Hardware, Reset / Recovery, Clear recovery lock, Encoder / raw inputs, Display test, UART, SD card info. |
| About | Autor, e-mail i bieżąca wersja. |
| Restart | Jawnie wybrany restart sterownika. |
| Backup Flash | Kopia Flash i tożsamości do przygotowanych plików SD. |
| Service history | Historia 24 zdarzeń na UART lub jawny zapis historii na SD. |

Angielskie menu OLED zachowuje piksele czcionki oryginału, bezpośrednią obsługę kroków enkodera, przypięty `Back` w podmenu i przewijanie bez zawijania. Zapamiętany jest ostatni skutecznie wysłany obraz; przesyłany jest zmieniony prostokąt, a identyczna klatka jest pomijana. Zakolejkowane kroki zmieniają wybór przed jednym odrysowaniem. To optymalizacja bootloadera, niezależna od transportu DMA/RLE aplikacji Klippera.

`Diagnostics → Hardware` za każdym wejściem odczytuje rewizję sprzętu, numer seryjny i czas pracy z zapisów drukarki. Brak poprawnego rekordu oznacza `Unavailable`. Model oznacza profil M300, nie automatyczne wykrycie wariantu handlowego. Ekran niczego nie zapisuje do NVM. Pierścień postępu pokazuje bajty/strony/czas przytrzymania bieżącej fazy; nieokreślone oczekiwanie ma `--`.

## Autostart i UART podczas odliczania

Pięć sekund odliczania rozpoczyna się po inicjalizacji płyty i OLED. Klik lub pełny krok enkodera przerywa autostart. Przed skokiem sprawdzane są aplikacja, warunki uruchomienia i stan recovery. Reset watchdog/recovery może zatrzymać urządzenie w menu.

`Diagnostics → UART → UART on bootwait → OFF / ON` zapisuje się we Flash niezależnie od prędkości:

| Ustawienie | Podczas odliczania |
|---|---|
| **OFF — domyślne** | Odbierane dane są odrzucane. Binarny ruch z uruchomionego Orange Pi/Klippera nie przerywa autostartu. Wejście pokrętłem nadal działa. |
| **ON — diagnostyka** | Tylko pełna tekstowa linia `MENU`, `HOME`, `BACK`, `HELP`, `INFO`, `PING`, `VERIFY`, `ECHO ON`, `ECHO OFF` otwiera menu serwisowe. Ruch binarny, niepełne lub zbyt długie linie i komendy zapisu nie zatrzymują ani nie odsuwają końca odliczania. |

Opcja steruje **odbiorem poleceń podczas odliczania**. Nie wyłącza UART ani nadawania nagłówka startowego. Po wejściu do menu normalna konsola działa w obu trybach. Na lokalnych ekranach ustawiania baud i bootwait odbiór hosta jest odrzucany, aby nie zastąpił menu błędem ani nie pozostawił części komendy.

## Prędkości i zgodność zapisu

Menu ma kolejno **115200, 250000, 500000, 750000, 1000000, 1500000**, **8N1, bez kontroli przepływu**. Puste dzienniki oznaczają **250000 / bootwait OFF**. Odczyt dawnych 19200/57600 pozostaje, ale nie ma ich na liście wyboru. 2000000 nie jest obsługiwane.

Zmiana czeka na koniec ostatniego bajtu starej prędkości, sprawdza UART, zapisuje rekord z kontrolą odczytu i dopiero ustawia nową prędkość. Poprawiono fałszywe `busy` lokalnej zmiany, zachowując rzeczywiste blokady operacji. Niepełne linie hosta są porzucane. Rzeczywisty timeout, niezgodne warunki lub pełny dziennik nadal mogą odrzucić zmianę; nie ma wymuszenia ani automatycznego kasowania.

Przytrzymanie pokrętła przy włączeniu wymusza **250000 tylko dla tej sesji boota**. Nie zmienia zapisu; puść pokrętło i uruchom normalnie. Aplikacja MCU musi osobno czytać dziennik i obsługiwać wybrany baud. Instalator SD używa tymczasowo **250000**.

| Indeks zapisu | Baud | Obsługa w 1.3.1 |
|---:|---:|---|
| 0 | 19200 | Odczyt starego zapisu |
| 1 | 57600 | Odczyt starego zapisu |
| 2 | 115200 | Menu |
| 3 | 250000 | Domyślna i menu |
| 4 | 500000 | Menu |
| 5 | 750000 | Menu |
| 6 | 1000000 | Menu |
| 7 | 1500000 | Nowa, rekord `0xFF99` |

Dziennik baud zajmuje `0x0803D800–0x0803D9FF`, a bootwait `0x0803DA00–0x0803DBFF`. Każdy ma 256 dopisywanych półsłów. Ponowny wybór tej samej wartości nie zużywa rekordu. Boot nie kasuje dzienników po zapełnieniu; `Settings full` wymaga osobno zaplanowanego serwisu. Zweryfikowana migracja 1.3 → 1.3.1 zachowuje oba dzienniki, metadane APP i NVM producenta. Starszy firmware nie zyskuje obsługi 1500000 przez sam zapis tej wartości.

## Aktualizacja aplikacji i recovery

Menu FAT16/FAT32 i `UARTCHECK` / `UARTUPDATE` obsługują aplikację pod **0x08008000** w jednym slocie 200 KiB. M3B sprawdza cel, długość, wektory i SHA-256; zapewnia integralność, **nie podpis kryptograficzny**. Identyczny obraz jest pomijany. Ręczny start/zapis APP wymaga puszczenia i świeżego przytrzymania pokrętła przez 2 s; obrót anuluje.

Stały BOOT wymienia osobny pośrednik SD: kontrola źródła/profilu/karty, dwa niezależne pełne odczyty Flash, a potem puść → świeży klik → puść → nowe przytrzymanie 5 s. Obrót anuluje. Odzyskiwanie działa z poprawnymi kopiami w tej samej, nadal uruchomionej sesji instalatora; nie jest automatycznym rollbackiem po utracie zasilania ani drugim bankiem firmware.

Końcowe 8 KiB, początkowe 4 KiB OEM i Option Bytes nie są normalnymi celami aktualizacji. Zachowano blokady profilu UID/opcji/strony fabrycznej; dowolna M300/HW05 nie jest automatycznie zgodna. [Instalacja](INSTALACJA_PL.md) · [UART](KONSOLA_UART_PRZYKLADY_PL.md) · [Diagnostyka](DIAGNOSTYKA_PL.md).
