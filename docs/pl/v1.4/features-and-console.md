# Funkcje, kompletne menu i konsola — M300Boot 1.4

[English](../../en/v1.4/features-and-console.md) · [Polski](../../pl/v1.4/features-and-console.md) · [Index](README.md)

Stały bootloader i instalator pośredni mają numer **1.4**. Ta instrukcja opisuje opublikowany bootloader FULL. Oryginalna aplikacja w `RESTORE.BIN`, niezależna diagnostyka kopii i MCU/host Klippera zachowują własne numery wersji. Osobny jest także techniczny numer kontenera OEM. Przed programowaniem przeczytaj [instalację](installation.md); [walidacja](validation.md) rozróżnia kontrole komputerowe i odbiór na drukarce.

## Pokrętło, ekrany i uruchamianie

Obrót przesuwa zaznaczenie, klik otwiera lub wykonuje wybraną pozycję. Z podmenu wraca się przez widoczne `Back`; długie przytrzymanie nie jest ogólnym poleceniem powrotu. Lista nie zawija na końcach. Widoczne są cztery wiersze pozycji: w podmenu `Back` pozostaje w pierwszym wierszu, a trzy pozostałe przewijają się. Po zmianie kierunku najpierw przesuwa się zaznaczenie w widocznym oknie. Kilka oczekujących kroków wykonywanych jest przed jednym odrysowaniem; obroty podczas trzymania przycisku i wyświetlania wyniku operacji są odrzucane. Niezmienione klatki pomija się, przesyłając wyłącznie zmienione prostokąty.

![Główne menu BOOT wyrenderowane natywną czcionką M300](../../assets/v1.4/BOOT_MAIN_MENU.png)

Odliczanie pięciu sekund zaczyna się po inicjalizacji płyty/OLED, nie z chwilą włączenia zasilania. Klik lub pełny krok enkodera otwiera serwis. Czynność wykryta już podczas inicjalizacji także przerywa odliczanie. Zwykły start po czasie sprawdza APP i środowisko, ale nie wymaga przytrzymania potwierdzającego. Blokada recovery zatrzymuje start automatyczny. Błędna aplikacja/środowisko pozostawia kontroler w serwisie; nie następuje samoczynna instalacja z SD.

Przytrzymaj pokrętło przy włączaniu, aby uzyskać tymczasowy dostęp serwisowy przy **250000** bez zmiany zapisanej prędkości. Przy `UART on bootwait: OFF` bajty od hosta nie przerywają odliczania. Przy `UART on bootwait: ON` wejście do serwisu dopuszczają wyłącznie kompletne linie `MENU`, `HOME`, `BACK`, `HELP`, `INFO`, `PING`, `VERIFY`, `ECHO ON` lub `ECHO OFF`. Dane binarne, fragmenty, polecenia nierozpoznane i zbyt długie linie nie wydłużają terminu. Przy OFF nadal może być nadawany baner startowy UART.

Większość wyników operacji BOOT wraca do menu po około **3 sekundach**. Hardware pozostaje do zwolnienia pokrętła i nowego kliku. Wyniki instalatora pośredniego wymagają nowego kliku i nie znikają automatycznie. Procent odnosi się do aktualnie nazwanej fazy, a nie przewidywanego czasu całej instalacji. Nieokreślony postęp pokazuje `--`.

## Wszystkie podmenu i pozycje BOOT

Poniżej zachowano dokładne angielskie etykiety OLED. Tabela obejmuje wszystkie 13 stron menu; na ekranie wybranego pliku nagłówek zastępuje jego rzeczywista nazwa.

| Ekran / menu | Pozycje | Działanie |
|---|---|---|
| `Main menu` | `Start application`; `Firmware on SD`; `Diagnostics`; `About`; `Restart`; `Backup Flash`; `Service history` | Otwiera odpowiednią stronę; samo wejście do podmenu nie programuje Flash. |
| `Start application` | `Back`; `Launch application` | Sprawdza zainstalowaną APP i środowisko, żąda zwolnienia oraz nowego ciągłego przytrzymania 2 s, ponownie sprawdza środowisko i uruchamia APP. Nie instaluje firmware. |
| `Firmware on SD` | `Back`; `Check SD package`; `Install firmware`; `Choose firmware file` | Sprawdzenie nie zapisuje; instalacja sprawdza i dla innego obrazu żąda przytrzymania 2 s przed zapisem APP. Wybór odświeża katalog plików. |
| `Diagnostics` | `Back`; `Verify Flash`; `Hardware`; `Reset / Recovery`; `Clear recovery lock`; `Encoder / raw inputs`; `Display test`; `UART`; `SD card info` | Poszczególne funkcje opisano poniżej. Historia jest osobną pozycją menu głównego. |
| `About` | `Back`; `© Marcin Kowalik`; `mkowalik@agh.edu.pl`; `Version v1.4` | Informacje o autorze i wersji tylko do odczytu. Klik wiersza informacji wysyła też INFO na UART i pokazuje autora/kontakt. |
| `Restart` | `Back`; `Restart controller` | Jawny reset programowy; po wybraniu tej pozycji nie ma dodatkowego przytrzymania 2 s. |
| `Backup to SD` | `Back`; `Backup Flash + identity` | Zapisuje jedną zweryfikowaną parę Flash/informacje do przygotowanych plików SD po świeżym przytrzymaniu 2 s. To nie są dwie kopie wymagane przez instalator. |
| `Service history` | `Back`; `View history on UART`; `Save history to SD` | LOG wyświetla zachowaną historię przez UART. LOGSAVE zapisuje przygotowany plik dziennika po przytrzymaniu 2 s. |
| `Files - select, then verify` | `Back`; nazwy dopuszczonych plików | Wybór tylko wskazuje plik, zgłaszany jako jeszcze niesprawdzony; otwiera następną stronę. |
| `Selected firmware` | `Back to files`; `Check selected file`; `Install selected file` | Działa na dokładnie wskazanej nazwie. Zmiana karty nie może po cichu zastąpić pliku kandydatem automatycznym. |
| `UART` | `Back`; `UART test`; `UART baud rate`; `UART on bootwait: OFF` / `UART on bootwait: ON` | Test pokazuje aktywne baud/8N1 i wysyła PONG. Pozostałe pozycje otwierają strony ustawień. |
| `UART baud rate` | `Back`; `115200`; `250000`; `500000`; `750000`; `1500000` | Wybór zapisuje ustawienie z odczytem kontrolnym i stosuje je po zakończeniu nadawania ze starą prędkością. Nie ma dodatkowego przytrzymania 2 s. |
| `UART on bootwait` | `Back`; `OFF`; `ON` | Zapisuje, czy rozpoznane linie diagnostyczne mogą otworzyć serwis w czasie odliczania. Bez dodatkowego przytrzymania. |

### Ustawienia UART i ich zapis

Pięć pozycji wyboru to **115200, 250000, 500000, 750000, 1500000**; pusta konfiguracja daje **250000** i bootwait **OFF**. Każde ustawienie ma osobny dopisywany dziennik o **256 logicznych slotach**. Zajęty slot częściowego/błędnego zapisu też zużywa miejsce. Ponowne wybranie już zapisanej wartości nie zużywa nowego slotu; tymczasowy dostęp przy 250000 jest niezależny od wartości zapisanej. Zapełnionego dziennika nie odzyskuje automatyczne kasowanie.

Dawne rekordy 19200, 57600 lub 1000000 dają aktywne 250000 w BOOT 1.4 bez przepisywania Flash. Starsza APP Klippera może nadal samodzielnie odczytać dawną wartość: przed jej startem jawnie wybierz/zapisz 250000 i uzgodnij baud hosta. Pełny dziennik może uniemożliwić zapis, wymagając osobnej procedury serwisowej. Obie lokalne strony ustawień odrzucają dane hosta; nie ma komendy konsoli ustawiającej dowolne baud. Zobacz [migrację UART i konfigurację hosta](uart-examples.md).

### Wybór pliku i sprawdzenie aplikacji

Lista obejmuje dopuszczone pliki `.BIN` i `.M3B` z katalogu głównego FAT16/FAT32. Nazwy porównuje się bez rozróżniania wielkości liter; obsługiwane długie nazwy są ASCII i mają najwyżej **26 znaków**. Katalogi, zastrzeżone nazwy kopii/dziennika oraz pliki poza dopuszczalnym zakresem wielkości są pomijane. Limit wynosi **16 dopuszczonych plików**; siedemnasty powoduje `LIST_FULL`, a nie ciche obcięcie listy. Wyświetlenie i wybranie nazwy nigdy nie potwierdza poprawności zawartości.

`LIST` odświeża katalog; `SELECT n` używa indeksu **liczonego od zera**, wydrukowanego przez LIST. Wybór obowiązuje do następnego wyboru, `SELECT AUTO` lub restartu. Brak wybranego pliku powoduje odmowę zamiast wyboru zastępczego. W trybie automatycznym kandydatami są `M300APP.M3B`, `Update.bin` i `RESTORE.BIN`. **Każda para lub trzy jednocześnie oznaczają niejednoznaczność.** Dlatego na sześcioplikowej karcie instalacyjnej trzeba jawnie wybrać plik, gdy obok instalatora znajduje się RESTORE.

Każde sprawdzenie/instalacja normalizuje dopuszczony kontener, kontroluje cel/adres/długość/wektory i sprawdza skrót zawartości przed kasowaniem. Natywne M3B zapewnia integralność SHA-256, nie podpis kryptograficzny. Zgodność OEM/stock korzysta z zachowanych reguł dokładnych obrazów. Zainstalowana własna APP wymaga zatwierdzonych metadanych, poprawnych wektorów i zgodnego skrótu Flash; wymazane metadane dopuszczają wyłącznie dokładny obraz stock z listy. Częściowego lub błędnego zapisu metadanych nie traktuje się jako dowolnej aplikacji stock.

`Verify Flash` kontroluje zainstalowaną APP, nie nowo wybrany plik SD. Zweryfikowany identyczny obraz zwraca `ALREADY_INSTALLED` i jest pomijany bez żądania zgody na zapis. Faktyczna instalacja APP najpierw kasuje metadane aplikacji, zachowuje wektory do zakończenia kontroli przychodzącej zawartości i zapisuje znacznik commit na końcu. Jest jeden slot APP; nie zapewnia to automatycznego cofnięcia po utracie zasilania. BOOT zastępuje osobny instalator, a nie zwykła operacja instalacji APP.

### Diagnostyka, blokada resetów i Hardware

| Opcja / komenda | Działanie i wyjście |
|---|---|
| `Verify Flash` / `VERIFY` | Sprawdza aktualnie zainstalowaną APP i zgłasza jej długość oraz nazwę stock albo `CUSTOM_MANIFEST`; bez zapisu Flash. |
| `Hardware` | Przy każdym otwarciu odczytuje profil/model, wersję sprzętu, numer fabryczny i zgromadzony czas pracy. Brak/błędny rekord daje `Unavailable`. To dekodowane dane urządzenia, nie bieżący pomiar drukowania. Zwolnij pokrętło i kliknij ponownie, aby wrócić. |
| `Reset / Recovery` / `RESETINFO` | Wypisuje flagi resetu, przyczynę, BOOT_COUNT, WDG_LOOP_COUNT, blokadę recovery i `RETENTION WARM_RESET_ONLY`. Nie kasuje ani nie zwalnia blokady. |
| `Clear recovery lock` / `RECOVERY CLEAR` | Natychmiast zeruje znacznik oczekiwanego przekazania do APP, licznik pętli watchdog i blokadę recovery w stanie serwisowym SRAM. Bez przytrzymania, naprawy APP i kasowania Flash/NVM. |
| `Encoder / raw inputs` / `DIAG` | Pokazuje zmiany wirtualnych UP/OK/DOWN i wysyła surowe wejścia GPIO przez UART. Przytrzymaj OK przez 1 s albo zaczekaj około 20 s na zakończenie. Nie jest to test silników, grzałek ani termistorów. |
| `Display test` / `DISPLAY` | Pokazuje dwa wbudowane wzory. Obrót przełącza wzór, klik OK kończy; jest też limit około 20 s. |
| `UART test` / `PING` | Pokazuje aktywne baud i 8N1 oraz wysyła `PONG`; nie zmienia prędkości i nie certyfikuje przewodu ani sprzętowej pętli zwrotnej. |
| `SD card info` / `CARDINFO` | Inicjalizuje/odczytuje kartę, wypisuje liczbę sektorów i obliczoną pojemność MiB. OLED pokazuje liczbę sektorów po 512 B. Nie formatuje i nie zapisuje karty. |

Historia, BOOT_COUNT i stan recovery korzystają z dwóch migawek z sumą kontrolną w ostatnim 1 KiB zwykłej SRAM. Zachowanie jest zakładane wyłącznie podczas ciepłych resetów i wymaga pozostawienia tego obszaru przez APP. To nie są trwałe liczniki życia urządzenia w Flash; mogą zniknąć po odłączeniu zasilania. Fabryczny czas z Hardware jest odrębną wartością odczytywaną z NVM.

Blokada pętli resetów zwiększa licznik tylko wtedy, gdy po zapisanym przekazaniu do APP nastąpi reset watchdog. Włączenie zasilania, NRST i celowy reset programowy nie są dowodem awarii APP. Po trzech takich przypadkach watchdog blokada zatrzymuje **automatyczny** start. Uruchomienie ręczne zachowuje zwykłą kontrolę i fizyczne potwierdzenie. Skasowanie blokady nie wyjaśnia przyczyny resetów.

### Kopia BOOT i plik historii na SD

Przygotuj osobną kartę serwisową albo zachowaj stare kopie poza kartą przed tworzeniem nowych szablonów:

```sh
python3 tools/prepare_service_sd.py "/Volumes/M300_SERVICE"
```

Polecenie tworzy brakujące, wstępnie przydzielone pliki `M3FLASH.BIN` (**262144 B**), `M3INFO.BIN` (**1024 B**) i `M3LOG.BIN` (**4096 B**) wypełnione A5. Nie formatuje karty i nie nadpisuje istniejących plików; nie poprawia automatycznie istniejącego pliku o złym rozmiarze. Firmware zapisuje zawartość plików, nie tworzy wpisów katalogu FAT ani łańcuchów przydziału.

`Backup Flash + identity` / `BACKUP` żąda zwolnienia i świeżego przytrzymania 2 s. Zapisuje i odczytuje kontrolnie jedną pełną kopię Flash z metadanymi tożsamości/rozmiaru/opcji/skrótu. Dopuszczone są puste szablony albo dokładna już skopiowana zawartość aktualnego obrazu. Starsza kopia innego stanu/urządzenia powoduje odmowę (`BACKUP_EXISTS`); zachowaj ją i użyj nowych szablonów na karcie serwisowej. Ta komenda nie spełnia wymagania dwóch kopii w sesji instalatora.

`View history on UART` / `LOG` pokazuje do **24 zachowanych zdarzeń**, od najstarszego, z numerem startu, czasem w milisekundach od danego startu, nazwą zdarzenia i argumentem. Zdarzenia obejmują reset, sprawdzenie, początek/koniec instalacji, błąd, start APP, kopię, eksport, zapis logu, zwolnienie recovery, celowy reset i pominięcie identycznego obrazu. `Save history to SD` / `LOGSAVE` żąda przytrzymania 2 s i zapisuje `M3LOG.BIN` z migawką historii i kontrolą integralności. Można zastąpić pusty szablon lub dziennik z tożsamością tej samej drukarki; plik obcy/nieznany jest odrzucany. Żadna z tych operacji nie programuje Flash kontrolera. Kopie i dzienniki zawierają prywatne identyfikatory urządzenia.

## Pełna lista komend konsoli BOOT

Komendy są ASCII i rozróżniają wielkość liter. Użyj dokładnej pisowni, zakończ linię i zaczekaj na `DONE` / `ERROR` oraz `READY`; restart/start APP naturalnie kończy starą konsolę. `MENU`, `HOME` i `BACK` kierują bezpośrednio do menu głównego — konsolowe BACK nie cofa o jeden poziom. Podczas lokalnych stron baud i bootwait polecenia hosta są odrzucane, aby nie zastąpiły strony operatora. Zatrzymaj Klippera i inne programy używające portu.

| Komenda / składnia | Działanie, wymagania i skutki |
|---|---|
| `INFO` | Wersja/profil, tryb, obszar APP, stan OLED/UART/bootwait i diagnostyka płyty/środowiska; tylko odczyt. |
| `HELP` | Drukuje obsługiwane formy komend; tylko odczyt. |
| `PING` | PONG przy aktywnym baud i stan OLED; tylko odczyt. |
| `MENU`, `HOME`, `BACK` | Powrót do Main menu; bez programowania i restartu. |
| `ECHO ON`, `ECHO OFF` | Włącza/wyłącza echo wpisywanych znaków w konsoli BOOT; bez zapisu trwałego ustawienia. |
| `VERIFY` | Sprawdzenie zainstalowanej APP; bez zapisu. |
| `LIST` | Odświeża/wypisuje dopuszczone pliki SD i indeksy od zera; bez weryfikacji/zapisu. |
| `SELECT n` | Wybiera indeks n z ostatniego poprawnego LIST; bez weryfikacji/zapisu. |
| `SELECT AUTO` | Usuwa jawny wybór i włącza automatyczny wybór trzech nazw z kontrolą niejednoznaczności. |
| `SDCHECK` | Sprawdza wskazany/automatyczny pakiet; bez zapisu i przytrzymania. |
| `SDUPDATE` | Weryfikuje wskazany/automatyczny pakiet; identyczny pomija, inny wymaga fizycznego przytrzymania 2 s przed zapisem APP. |
| `UARTCHECK N`, `UARTUPDATE N` | Protokół serwera plikowego dla pakietu N bajtów. N jest dziesiętne, 72–204864 włącznie. Używaj `ibtool.py serial`, nie wpisuj ręcznie ramek binarnych. CHECK tylko sprawdza, UPDATE nadal wymaga lokalnego przytrzymania i wszystkich kontroli obrazu. |
| `BACKUP` | Jedna para Flash/informacje na SD; wymagane przygotowane pliki i przytrzymanie 2 s. |
| `DUMP FLASH`, `DUMP BOOT`, `DUMP NVM`, `DUMP FACTORY`, `DUMP SYSROM`, `DUMP SIZE`, `DUMP UID`, `DUMP OPTIONS` | Eksportuje wyłącznie stałe obszary poniżej z CRC bloków i końcowym SHA-256; bez zapisu kontrolera/SD. Narzędzie hosta zachowuje i weryfikuje pary eksportów. |
| `RESETINFO` | Przyczyna resetu, liczniki i recovery; bez zerowania. |
| `RECOVERY CLEAR` | Natychmiast zeruje serwisowy stan recovery w SRAM; bez przytrzymania i naprawy firmware. |
| `DIAG` | Blokująca diagnostyka wejść; wyjście po przytrzymaniu OK 1 s albo około 20 s. |
| `DISPLAY` | Blokujący pokaz wzorów; obrót przełącza, OK kończy albo limit około 20 s. |
| `CARDINFO` | Odczyt pojemności SD; bez formatowania/zapisu. |
| `LOG` | Wypisuje zachowaną historię na UART; bez zapisu SD. |
| `LOGSAVE` | Zapisuje historię do przygotowanego `M3LOG.BIN`; przytrzymanie 2 s. |
| `BOOT` | Sprawdza i uruchamia zainstalowaną APP po nowym przytrzymaniu 2 s. |
| `REBOOT` | Zapisuje zdarzenie celowego resetu i restartuje kontroler; bez dodatkowego przytrzymania. |

| Obszar DUMP | Adres bazowy | Bajty |
|---|---:|---:|
| `FLASH` | `0x08000000` | 262144 |
| `BOOT` | `0x08000000` | 32768 |
| `NVM` | `0x0803E000` | 8192 |
| `FACTORY` | `0x0803F800` | 2048 |
| `SYSROM` | `0x1FFFF000` | 2048 |
| `SIZE` | `0x1FFFF7E0` | 2 |
| `UID` | `0x1FFFF7E8` | 12 |
| `OPTIONS` | `0x1FFFF800` | 16 |

Narzędzie pełnego eksportu i przykłady znajdują się w [kopii oryginału](original-backup.md) oraz [UART](uart-examples.md). Sam DUMP nie potwierdza dziewiczej fabrycznej APP, nie usuwa ochrony odczytu i nie stanowi kompletnej procedury odtworzenia wymazanego urządzenia.

## Instalator SD: wszystkie siedem opcji i odrębna konsola

Instalator pośredni działa w APP pod `0x08008000`, używa tymczasowego **250000 8N1**, nie zapisuje BOOT samoczynnie i nie zmienia dziennika baud. Ekrany wyniku/Hardware wymagają zwolnienia i nowego kliku. Jego konsola jest odrębna: używaj LF/nowej linii; samo CR jest ignorowane.

| Pozycja instalatora | Rzeczywiste działanie i warunki |
|---|---|
| `Check board + SD` | Przygotowanie źródła na żądanie i sprawdzenie płyty, źródłowego BOOT, sześcioplikowej karty/RESTORE oraz zakresów chronionych; bez zapisu BOOT. |
| `Backup Flash x2` | Wykonuje, zapisuje i weryfikuje dwie pełne pary Flash/tożsamość na tej samej karcie. Kwalifikuje kopie tylko w tej działającej sesji. |
| `Install / upgrade boot` | Wymaga zweryfikowanych kopii sesji, ponawia kontrolę karty/źródła przed gestem operatora i po nim, potem zapisuje/sprawdza stałe strony BOOT/zasobów. Identyczny cel pomija. |
| `Recover saved boot` | Dostępne wyłącznie po próbie zapisu BOOT w tej samej sesji przy zachowanym zasilaniu. Sprawdza kopie i wymaga tego samego gestu, następnie przywraca zapisany źródłowy BOOT. Nie odtwarza APP i nie odzyskuje automatycznie po utracie sesji. |
| `Restart to boot` | Ponownie sprawdza niezmienniki/tożsamość źródła i restartuje do BOOT. Po instalacji SD docelową stock/Klipper APP trzeba jeszcze odtworzyć osobno. |
| `Hardware` | Odczyt zdekodowanych informacji urządzenia; zwolnij i kliknij ponownie, aby wrócić. |
| `About` | Wypisuje diagnostykę instalatora/celu/źródła/sesji kopii i wyświetla wynik; bez zapisu. |

Gest zastąpienia/odtworzenia BOOT: **zwolnij → nowy klik → zwolnij → ponownie naciśnij i trzymaj nieprzerwanie 5 s**. Obrót anuluje; zwolnienie przed pięcioma sekundami anuluje. Całe potwierdzenie ma limit **45 s**, a komunikaty rozróżniają etap oczekiwania. Po potwierdzeniu ponownie sprawdzane są skróty, źródło i karta; opóźnienie ani zmiana danych nie może zatwierdzić nieaktualnego stanu. Po błędzie zapisu zachowaj zasilanie i tę samą kartę, korzystając z procedury działającego instalatora opisanej w [instalacji](installation.md) / [ST-Link i odzyskiwaniu](stlink-and-recovery.md). Nie ma automatycznego cofania po zaniku zasilania.

| Komenda instalatora | Skutek |
|---|---|
| `INFO` | Wersja 1.4, tożsamość celu/źródła, stan kopii sesji i tymczasowy UART; tylko odczyt. |
| `PING` | `PONG M300INSTALL 1.4`; tylko odczyt. |
| `HELP` | Lista komend instalatora. |
| `ECHO OFF` | Potwierdzenie dla zgodności hosta; instalator nie ma interaktywnego przełącznika echa znaków jak BOOT. |
| `CHECK` | Te same kontrolowane sprawdzenia co Check board + SD. |
| `BACKUP SD` | Ta sama operacja dwóch kopii co Backup Flash x2. |
| `INSTALL V14` | Ta sama kontrolowana instalacja BOOT; kopie SD i fizyczny gest nadal obowiązkowe. |
| `RECOVER SOURCE` | To samo odtworzenie zapisanego BOOT w żywej sesji; kopie i fizyczny gest nadal obowiązkowe. |
| `REBOOT` | Ten sam kontrolowany restart co Restart to boot. |

Komendy UART nie omijają kwalifikacji płyty/źródła/SD ani fizycznego potwierdzenia zapisu BOOT. Nie przyjmują dowolnych surowych adresów. Przygotowanie FAT/karty, kolejność instalacji, właściwe usunięcie pliku OEM update i końcowe odtworzenie stock/Klipper APP opisuje [instalacja](installation.md).

Teksty HELP w firmware są skrócone: BOOT przyjmuje również `HOME`, a instalator potwierdza także `ECHO OFF`, mimo że tych form nie wypisuje ich HELP. Poniższe tabele porównano z faktycznie przyjmowanymi komendami, a nie wyłącznie z tekstem HELP.
