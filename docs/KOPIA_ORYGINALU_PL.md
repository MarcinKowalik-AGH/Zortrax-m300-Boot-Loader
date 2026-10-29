# Zabezpieczenie oryginalnej M300 — przed instalacją

Zakres: klasyczna M300 Rev.5.3/HW05, rzeczywiście zmierzone 256 KiB. Nie stosować do Plus, Dual ani Inventure. Pakiet i4 jest dodatkowo przypisany do zakwalifikowanego egzemplarza; zgodność samej nazwy płyty nie wystarcza.

## 1. Zapisz stan działającej drukarki

W menu Information/Informacje zapisz lokalnie zdjęcia Firmware version oraz Printer information: model, hardware, numer seryjny, całkowity czas pracy. Zachowaj ustawienia użytkownika, stan kalibracji, zdjęcie PCB/revizji i czytelnego oznaczenia MCU. Zachowaj oryginalny Update.bin właściwego modelu, archiwum i SHA-256. Referencją projektu jest M300 1.3.1. Zdjęcie numeru nie zastępuje bajtowej kopii danych.

## 2. Zachowaj wszystkie obszary

| Obszar | Adres i rozmiar |
|---|---|
| Cała główna Flash — dwa odczyty | 0x08000000, 0x40000 = 262144 B |
| OEM BOOT — osobno i w obu pełnych kopiach | 0x08000000–0x08007FFF, 32768 B |
| Końcowe dane — dwa odczyty | 0x0803E000–0x0803FFFF, 8192 B |
| Bank NVM A | 0x0803E800, 2048 B |
| Bank NVM B | 0x0803F000, 2048 B |
| Strona fabryczna | 0x0803F800, 2048 B |
| Option Bytes — dwa odczyty | 0x1FFFF800, 16 B |
| UID — dwa odczyty | 0x1FFFF7E8, 12 B |
| SIZE — dwa odczyty | 0x1FFFF7E0, 2 B |

Zachowaj także SYSROM, rejestry BKP i diagnostyczne, jeżeli dostępne. Nie są zwykłymi obrazami do programowania.

W rozpoznanym stock ostatni kompletny rekord ID0 aktywnego NVM zawiera czas w minutach. HW05 jest dekodowane z E5; numer drukarki jest formatowany z rekordów binarnych, nie musi istnieć jako pełny ASCII. Nie odtwarzaj ręcznie tylko tych pól: zachowaj oba całe banki i całą stronę fabryczną, także dane o nierozpoznanym znaczeniu. Model w naszym Hardware jest nazwą profilu docelowego.

## 3. Odczyt SWD, gdy jest dostępny

Sprawdź opcje bez Apply. Odczytaj dwa razy zakres 0x08000000/0x40000 i zapisz FLASH_A.bin oraz FLASH_B.bin. Odczytaj również pary UID/SIZE/OPTIONS. Porównaj bajtowo i SHA-256:

```sh
cmp FLASH_A.bin FLASH_B.bin
shasum -a 256 FLASH_A.bin FLASH_B.bin
```

Nie opieraj pojemności wyłącznie na GUI. W testowanym egzemplarzu CubeProgrammer pokazywał 512 KB, ale dwa wewnętrzne odczyty SIZE dały `00 01`, czyli little-endian 0x0100 = 256 KiB. Nie odczytuj niepotwierdzonej górnej połowy.

## 4. Gdy aktywne RDP blokuje SWD

**Nie używaj Read Unprotect, Mass Erase ani zmiany RDP, aby zrobić backup.** Usunięcie aktywnego RDP STM32F1 kasuje główną Flash. Kod wykonywany z wewnętrznej Flash przy nieaktywnym debugowaniu może ją odczytywać.

W projekcie użyto tymczasowej diagnostyki UART 0.5.5, uruchamianej przez OEM v3. Publiczny pakiet zawiera niezmienione firmware i read-only host. Instalacja tej aplikacji już zastępuje stock — późniejszy pełny zrzut jest PO aktualizacji, nie nienaruszonym obrazem sprzed niej. Oryginalny Update.bin trzeba zachować osobno.

Na niezależnie rozpoznanej zgodnej płycie: osobna karta FAT32 z diagnostycznym Update.bin; standardowa aktualizacja OEM; po jej rzeczywistym zakończeniu wyłączenie, wyjęcie karty i uruchomienie bez aktywnej sesji SWD. UART 3,3 V: PA9/TX do RX adaptera, PA10/RX z TX adaptera, wspólna masa. Nie podłączaj 5 V i nie kopiuj numeracji P4 z Inventure. STLINK-V3SET VCP jest adapterem szeregowym, a tryb UART CubeProgrammer nie jest tą konsolą.

Z katalogu rozpakowanego pakietu backupu:

```sh
python3 -m pip install --user pyserial  # tylko gdy brakuje
python3 read_flash_m300_055.py --port /dev/cu.usbmodem14203
```

Port jest przykładem. Po otwarciu portu uruchom drukarkę bez karty. Oczekiwany wynik to PASS_FULL_AUDIT_256K_X2. Program wymaga CRC ramek, końcowego SHA, równości par i nakładających się zakresów. Tworzy nowy prywatny katalog/ZIP; nie programuje MCU. Publiczny host sprawdza nowe odczyty, ale nie udaje porównania z nieistniejącym historycznym obrazem danej drukarki.

## 5. Przed użyciem instalatora i4

Lokalny check_backup_profile.py sprawdza kopie oraz zgodność z niezmienioną blokadą i4. PASS_I4_PROFILE_MATCH jest warunkiem koniecznym, nie gwarancją bezawaryjnej instalacji. BACKUP_VALID_BUT_INSTALL_PROFILE_MISMATCH oznacza STOP: inny egzemplarz wymaga osobnej kwalifikacji i kompilacji. Nie zmieniaj hashy, nie kopiuj cudzej tożsamości i nie zeruj danych.

## 6. Archiwizacja

Zachowaj oryginalne BIN-y, manifest, SHA-256, surowy/tekstowy UART, zdjęcia menu/PCB, oryginalny firmware oraz datę/metodę odczytu. Przechowuj drugą kopię na osobnym nośniku. Nie publikuj surowych zrzutów w GitHub issues. Dwa pliki na tej samej karcie nie są dwoma niezależnymi nośnikami. Przywrócenie starego obrazu odtwarza też stary licznik i ustawienia.

Źródło właściwości MCU: [ST PM0075 §§2.3–2.4](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf). Mapę rekordów Zortraxa ustalono w prywatnym audycie projektu, nie w dokumentacji ST.
