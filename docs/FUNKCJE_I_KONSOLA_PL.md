# Funkcje, Hardware i konsola — M300 boot v1.1

Nagłówek: **M300 boot v1.1 © Marcin Kowalik**. © jest znakiem bitmapowym. Menu nie zapętla się; wskaźnik dochodzi do krawędzi, a lista przesuwa się o jeden wiersz. Back jest dostępny na górze podmenu. Sterowanie enkoderem jest bezpośrednie, a OLED aktualizuje tylko zmieniony prostokąt.

## Hardware

`Diagnostics → Hardware` pokazuje po angielsku:

```text
Model: Zortrax M300
Hardware version: 05
Serial number: ZXXXXXXXX
Total operating time: <hours>h <minutes>m
```

Serial w przykładzie jest zastępczy. Hardware, serial i czas są odczytywane przy każdym wejściu z rzeczywistych rekordów urządzenia; model oznacza profil docelowy. Błędne/dostępne tylko częściowo dane dają `Unavailable`, nie fikcyjny wynik. Ekran czeka na kolejny klik i nie zapisuje NVM. Odpowiednik jest w instalatorze i4. Oznaczenie HW05 z menu nie jest tym samym co napis PCB Rev.5.3.

## Menu i operacje

Start application: ręczne sprawdzenie/uruchomienie aplikacji. Firmware on SD: wybór do 16 zgodnych plików, sprawdzenie i instalacja po potwierdzeniu. Diagnostics: sprawdzenie Flash, informacje sprzętu, wejścia/panel, ekran, UART i karta. Backup Flash: pełna kopia oraz tożsamość. Service history: historia 24 zdarzeń i zapis na kartę. Restart: powrót do rozruchu.

Pierścień pokazuje procent **bieżącej fazy** z bajtów/stron/czasu przytrzymania. Faza weryfikacji po zapisie może zaczynać się od 0%. Nieznany zakres ma `--`, błąd nie udaje 100%. Oryginalny OEM podczas uruchamiania pośrednika zachowuje własny ekran.

Autostart po 5 sekundach można przerwać ruchem/klikiem lub znakiem UART. Przytrzymanie enkodera przy starcie wymusza wejście serwisowe z 250000. UART ma 19200, 57600, 115200, 250000 i 500000, **8N1 bez flow control**. Zapisane ustawienie jest poza NVM producenta. Instalator używa tymczasowo 250000; zachowuje dziennik boota.

## Połączenie UART

PA9/USART1_TX → RX adaptera, PA10/USART1_RX ← TX, wspólna masa, logika 3,3 V. Zweryfikuj fizyczne piny DEBUG. STLINK-V3SET VCP działa jako adapter; CubeProgrammer w trybie UART jest klientem innego protokołu i nie jest terminalem tekstowym. Zamknij aktywny SWD i inne programy używające portu. Nie podłączaj 5 V.

```sh
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203
```

Wymaga Python3 i pyserial. Port jest przykładem. Oczekiwany `PASS_CONSOLE_V11` sprawdza konsolę, nie cały sprzęt. Skrypt tworzy prywatne logi na Pulpicie.

Dwa odczyty wszystkich obsługiwanych zakresów:

```sh
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203 --dump-all
```

Alternatywnie pojedynczy odczyt, bez poleceń kasowania:

```sh
python3 tools/m300_service.py dump --port /dev/cu.usbmodem14203 --baud 250000 FLASH --out ./private/M300_FLASH.bin
```

Najpierw utwórz prywatny katalog. Dostępne regiony: FLASH, BOOT, NVM (końcowe 8 KiB), FACTORY, SYSROM, SIZE, UID, OPTIONS. Odbiornik wymaga kolejności ramek, CRC i końcowego SHA. Nie nadpisuje pliku. Nie uruchamiaj go na zwykłej aplikacji stock; pozostań w menu M300Boot.

Sprawdzanie kopii SD i historii:

```sh
python3 tools/m300_service.py verify-backup M3FLASH.BIN M3INFO.BIN
python3 tools/m300_service.py decode-log M3LOG.BIN
```

M3LOG powstaje dopiero po osobnym zapisie historii. Do kopii z instalatora (cztery pliki) użyj SPRAWDZ_M300_SD_I4.command --backups.

## Aktualizacja aplikacji przez UART — nie aktualizacja BOOT

Publiczny `ibtool.py` pakuje surową aplikację pod 0x08008000 do M3B, sprawdza pakiet i obsługuje żądania UART bootloadera. Nie odszyfrowuje OEM ani nie tworzy jego HMAC. Dokładne opcje: `python3 tools/ibtool.py --help` oraz `serial --help`. Zmiana BOOT wymaga osobnego pośrednika; nigdy nie pakuj stage2 jako aplikacji. Oryginalne 1.3.1 odtwarza dołączony RESTORE.BIN przez menu SD.

**Nie używaj starych skryptów rc3 `--install` do i4/v1.1.** Nie ma FORCE. Kody błędów należy zachować wraz z OP/PHASE/REASON. Logi mogą zawierać prywatne dane — nie dodawaj surowych zrzutów do publicznych issues.
