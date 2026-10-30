# ST-Link: instalacja v1.1 i awaryjny powrót do OEM

[English](../../en/v1.1/stlink-and-recovery.md) · [Polski](../../pl/v1.1/stlink-and-recovery.md) · [Indeks](README.md)

**Archiwalny zapis v1.1 z 29 października 2026.** Poniższe ustalenia zachowują historyczny zakres. [Bieżąca v1.3.1](../v1.3.1/README.md).

**Droga ostateczna lub świadomie wybrana instalacja serwisowa. Nie używaj jej do „sprawdzenia” działającej drukarki.** Opis dotyczy tylko klasycznej M300 Rev.5.3/HW05, 256 KiB oraz profilu akceptowanego przez wydanie. Nie jest to instrukcja dla Inventure, Plus ani Dual. Testy pakietu ST-Link są komputerowe; osobnego sprzętowego zapisu tą metodą nie potwierdzono.

## 1. Najpierw własny, zweryfikowany backup

Wymagane są **dwa zgodne pełne obrazy** oraz pary UID, SIZE i OPTIONS lub cztery poprawne pliki backupu SD. Zabezpiecz oryginalne 32 KiB BOOT i końcowe 8 KiB, zgodnie z [procedurą backupu](original-backup.md). Zachowaj kopie na drugim nośniku. Bez kopii oryginalnego BOOT nie obiecujemy powrotu do OEM.

Nie publikujemy pełnego wsadu zawierającego dane autora. ZIP STLINK zawiera:

| Plik | Zakres |
|---|---|
| `M300Boot_v1.1_FULL_STAGE2_0x08001000.bin` | 28672 B od `0x08001000` |
| `M300Boot_v1.1_FULL_ASSETS_0x0803A000.bin` | 12288 B od `0x0803A000` |
| `M300Boot_v1.1_FULL_SPARSE.hex` | Wyłącznie powyższe dwa zakresy; bez prefixu OEM i danych |
| `RESTORE.BIN` | Pakiet M3B oryginalnej aplikacji 1.3.1, nie plik bezpośrednio do SWD |
| `prepare_stlink.py` i zależne narzędzia hosta | Lokalny generator osobistego obrazu; brak dostępu do urządzeń |

**Sparse HEX i dwa BIN-y nie wystarczą po masowym kasowaniu.** Nie zawierają pierwszych 4 KiB oryginalnego rozruchu ani Twojej tożsamości/NVM. Nie programuj `Update.bin`, `RESTORE.BIN` ani `M300APP.M3B` surowo przez SWD.

## 2. Złóż obraz lokalnie, jeszcze przed ingerencją w urządzenie

Rozpakuj ZIP STLINK i otwórz Terminal w tym katalogu. Python 3.9+; generator nie wymaga pyserial, kluczy OEM ani internetu.

Instalacja własnego boota + stock 1.3.1:

```sh
python3 prepare_stlink.py --backup "/sciezka/do/wlasnej/kopii" --mode m300 --out "$HOME/Desktop/M300_PERSONAL_V11"
```

Odtworzenie OEM v3 + stock 1.3.1, wyłącznie z kopii zawierającej oryginalny OEM:

```sh
python3 prepare_stlink.py --backup "/sciezka/do/wlasnej/kopii_OEM" --mode oem --out "$HOME/Desktop/M300_PERSONAL_OEM"
```

Wynik: `PASS_PERSONAL_IMAGE_OFFLINE`, osobisty BIN **262144 B**, równoważny HEX, manifest i SHA256SUMS. Istniejący katalog wyjściowy powoduje odmowę. Generator zachowuje prefix OEM i końcowe 8 KiB. Dla v1.1 ustawia metadane zatwierdzające stock; istniejący dziennik UART pozostaje zachowany. Nie wykonuje programowania ani zmiany RDP. Obraz jest **zrekonstruowany**, nie dawnym nienaruszonym zrzutem. Licznik i ustawienia będą odpowiadały dacie wybranej kopii.

`BACKUP_VALID_BUT_INSTALL_PROFILE_MISMATCH` lub inna odmowa oznacza STOP. Nie edytuj hashy i nie kopiuj tożsamości z cudzej drukarki.

## 3. Fizyczne połączenie SWD

Wyłącz zasilanie przed zmianą przewodów. Połącz zweryfikowane sygnały **SWDIO, SWCLK, GND, napięcie odniesienia 3,3 V oraz NRST**. UART TX/RX nie zastępuje SWD. Nie podłączaj 5 V ani napięcia mocy do portu debug. Płytę zasilaj właściwym stabilnym zasilaniem; napięcie odniesienia nie jest poleceniem zasilania jej z programatora. Nie zgaduj numeracji P4 na podstawie Inventure.

CubeProgrammer: ST-LINK / SWD, **Under reset**, **Hardware reset**, początkowo **400 kHz**. Under reset wymaga fizycznego NRST. Sprawdź napięcie i ID rodziny 0x414. Błąd połączenia nie jest poleceniem kasowania. Zapisz bieżące opcje i log.

## 4. RDP — punkt destrukcyjny

Jeżeli SWD jest zablokowane aktywnym RDP, jego usunięcie powoduje **masowe kasowanie głównej Flash**. Tylko po przygotowaniu i sprawdzeniu całego osobistego obrazu można świadomie użyć Read Unprotect / wyłączyć RDP. To nie jest etap rutynowego upgrade SD. Dla STM32F1 surowe `A5` oznacza brak ochrony; `00` oznacza aktywne RDP. Nie kopiuj wartości `AA` z Inventure/F2. Jeżeli RDP już jest nieaktywne, nie wywołuj ponownie read-unprotect.

Po przeładowaniu opcji połącz się ponownie. Porównaj UID i rzeczywiste SIZE z wybraną kopią. Nie programuj UID, SYSROM ani rejestru SIZE. Pozostałe ustawienia USER/DATA/WRP sprawdź względem własnego zapisu; nie wgrywaj surowych 16 B OPTIONS jako zwykłego BIN. Na czas kontroli pozostaw RDP wyłączone. Jeżeli docelowa ochrona ma zostać później ponownie włączona, jest to osobna, świadoma operacja po poprawnym readback i starcie.

## 5. Programowanie i kontrola

Wybierz osobisty **pełny BIN** utworzony przez generator (nie ogólne komponenty):

```text
Start address:            0x08000000
File size:                262144 B (0x40000)
Verify after programming: enabled
Run after programming:    disabled
Skip erase:               disabled
```

Nie przerywaj zapisu. Po kontroli programu, z zatrzymanym procesorem, odczytaj **dokładnie 0x40000 B od 0x08000000** do nowego `READBACK.bin` i porównaj przed uruchomieniem:

```sh
cmp M300_BOOT_v1.1_STOCK_1.3.1_PERSONAL_256KiB.bin READBACK.bin
shasum -a 256 M300_BOOT_v1.1_STOCK_1.3.1_PERSONAL_256KiB.bin READBACK.bin
```

Dla trybu OEM użyj wygenerowanej nazwy OEM. Wymagane są identyczne bajty. Zakończ sesję debug, wyłącz zasilanie, odłącz programator i uruchom bez karty aktualizacyjnej. Dla v1.1 zatrzymaj autostart pokrętłem, sprawdź Hardware i dopiero potem stock 1.3.1. Dla OEM sprawdź oryginalne menu. Numer, HW i czas muszą odpowiadać Twojemu backupowi. Najpierw test bez ruchu/grzania.

## 6. Co jest chronione, a czego procedura nie gwarantuje

Pełny osobisty obraz pozwala odtworzyć zawartość po skasowaniu, jeśli MCU i interfejs nadal dają się zaprogramować. Nie naprawia uszkodzenia elektroniki ani nie zapewnia odporności na przerwę zasilania. Zachowane pierwsze 4 KiB w drodze SD nie są niezależnym recovery, a stara karta OEM po wymianie drugiego etapu nie jest gwarantowanym ratunkiem.

## Źródła

- STMicroelectronics [PM0075, §§2.3–2.4](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf): STM32F1 Flash, RDP/WRP, first-page protection, option-byte changes.
- ST [STM32CubeProgrammer 2.23 command reference](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_Command_Lines.html): SWD under reset, hardware reset, read/program/verify.
- The device-specific memory map and tested behavior are from the project's retained private audit and operator reports, not an endorsement by ST or Zortrax.
