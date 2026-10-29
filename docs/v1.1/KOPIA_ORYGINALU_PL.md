# Najpierw zabezpiecz oryginalną drukarkę

**Nie zaczynaj od podmiany bootloadera ani od wyłączenia RDP.** Celem pierwszego etapu jest zachowanie rzeczywistych bajtów konkretnego urządzenia. Zdjęcie numeru seryjnego nie zastępuje kopii rekordów fabrycznych.

## 1. Dokumentacja przed zmianami

Na działającym stock wybierz `Information / Informacje → Firmware version` oraz `Printer information`. Zapisz lokalnie zdjęcia modelu, wersji firmware, hardware, numeru seryjnego i całkowitego czasu pracy. Zanotuj ustawienia użytkownika i stan kalibracji. Sfotografuj rewizję PCB i oznaczenie MCU, jeżeli jest czytelne. Nie zgaduj pełnego symbolu MCU z samego ID rodziny.

Zachowaj **oryginalne Update.bin właściwego modelu**, jego archiwum i SHA-256. W tym projekcie referencją jest M300 1.3.1. Nie używaj M300 Plus/Dual/Inventure. Osobną sprawdzoną kartę przywracania OEM trzymaj poza kartą testową. Po trwałej zmianie bootloadera stara automatyczna aktualizacja OEM może już nie działać.

## 2. Co zachować

| Obszar | Adres / długość | Dlaczego |
|---|---|---|
| Cała główna Flash | `0x08000000`, **0x40000 = 262144 B**, dwa odczyty | Obejmuje boot, aplikację, ustawienia, pozostałości i nieznane obszary |
| Oryginalny bootloader | `0x08000000–0x08007FFF`, **32768 B**, osobno i w pełnej Flash | Przyszła analiza i odbudowa OEM |
| Końcowe dane | `0x0803E000–0x0803FFFF`, **8192 B**, dwa odczyty | Nie wolno ograniczyć kopii do widocznego serialu |
| Bank ustawień A | `0x0803E800`, **2048 B** | Zachować nawet pusty lub nieaktywny |
| Bank ustawień B | `0x0803F000`, **2048 B** | Bieżące preferencje, parametry i licznik |
| Strona fabryczna | `0x0803F800`, **2048 B** | M.in. serial, hardware i inne rekordy fabryczne |
| Option Bytes | `0x1FFFF800`, **16 B**, dwa odczyty | Konfiguracja zabezpieczeń i startu; materiał dowodowy, nie automatyczny wsad |
| UID | `0x1FFFF7E8`, **12 B**, dwa odczyty | Powiązanie kopii z właściwym MCU; nie mylić z numerem drukarki |
| SIZE | `0x1FFFF7E0`, **2 B**, dwa odczyty | Faktyczny zakres odczytu; `00 01` w little-endian = 256 KiB |
| SYSROM / BKP / rejestry | Dodatkowe, jeżeli dostępne przez diagnostykę | Identyfikacja i kontekst; nie obrazy do zwykłego flashowania |

W rozpoznanym stock M300 licznik jest ostatnim kompletnym rekordem **ID0** aktywnej strony NVM, w minutach. Godziny to dzielenie przez 60. Wersja HW05 jest dekodowana z `E5`, a numer seryjny nie musi być zapisany jako pełny tekst ASCII. **Przechowuj oba całe banki i całą stronę fabryczną; nie odbudowuj ich ręcznie z kilku pól.** `Model: Zortrax M300` w naszym Hardware jest nazwą profilu, nie osobnym dowodem identyfikacji modelu przez MCU.

## 3. Gdy SWD pozwala czytać

Podłącz ST-Link przez SWD, odczytaj opcje **bez Apply**, a następnie dwa razy zapisz całe potwierdzone 256 KiB jako `FLASH_A.bin` i `FLASH_B.bin`. Zapisz osobno UID, SIZE i Option Bytes jako pary `_A.bin`, `_B.bin`. Do odczytu używaj Memory/File editing → Read/Save, nie panelu kasowania. Przykładowe pole głównej Flash: Address `0x08000000`, Size `0x40000`.

Nie opieraj wielkości wyłącznie na nagłówku GUI. W testowanym egzemplarzu GUI mówiło 512 KB, a rzeczywisty SIZE jednoznacznie 256 KiB. Gdy RDP blokuje SIZE/Flash, nie wykonuj odblokowania tylko po to, aby „sprawdzić”.

Porównaj pliki na Macu:

```sh
cmp FLASH_A.bin FLASH_B.bin
shasum -a 256 FLASH_A.bin FLASH_B.bin
```

Dwa pliki o tym samym rozmiarze nie wystarczą; wymagane są identyczne bajty. Kopie przechowuj także na innym nośniku, nie tylko w dwóch plikach tej samej karty.

## 4. Gdy RDP blokuje zewnętrzny odczyt

**Nie używaj Read Unprotect, Mass Erase ani zmiany RDP jako metody backupu.** W tej rodzinie STM32F1 przejście na stan niezabezpieczony kasuje główną Flash. Program wykonywany z wewnętrznej Flash może odczytać ją bez zdejmowania RDP przy nieaktywnym debugowaniu [ST PM0075].

Projekt wykorzystał tymczasową aplikację **UART Full Audit 0.5.5**, uruchamianą przez zachowany OEM v3. Jej kod maszynowy w publicznym ZIP-ie jest niezmieniony. Sam diagnostyczny program nie programuje Flash ani Option Bytes, **ale jego instalacja przez OEM zastępuje poprzednią aplikację drukującą**. Zrzut wykonany później nie jest pełnym obrazem sprzed tej aktualizacji. Oryginalne 1.3.1 trzeba zachować oddzielnie.

### Procedura dla wcześniej rozpoznanej, zgodnej płyty

1. Zachowaj dokumentację, poprawny oryginalny firmware i kartę ratunkową; potwierdź model/revizję. Nie uruchamiaj tego kodu na nieznanej elektronice.
2. Rozpakuj `M300_BACKUP_0.5.5_UART.zip`. Na osobną FAT32 kopiuj **tylko Update.bin z tej paczki diagnostycznej**, nie instalator v1.1. Wydanie diagnostyki ma wersję kontenera 9.9.4.
3. Standardową metodą OEM zainstaluj diagnostykę. Po rzeczywistym zakończeniu wyłącz drukarkę, wyjmij kartę i nie podłączaj aktywnej sesji SWD.
4. Połącz **PA9/USART1_TX → RX adaptera**, **PA10/USART1_RX ← TX adaptera**, wspólne GND, poziomy 3,3 V. Zweryfikuj fizyczne piny konkretnej PCB. Nie przenoś automatycznie kolejności P4 z Inventure; nie podawaj 5 V i nie zasilaj płyty z VCP.
5. STLINK-V3SET może pracować jako VCP. **Tryb UART w CubeProgrammer nie jest zwykłym terminalem tej konsoli.** Zamknij CubeProgrammer. Port Maca znajdziesz przez `ls /dev/cu.usbmodem*`.
6. W rozpakowanym katalogu na Macu: `python3 -m pip install --user pyserial` (tylko gdy brak), potem:

```sh
python3 read_flash_m300_055.py --port /dev/cu.usbmodem14203
```

Nazwa portu jest przykładem, nie stałą właściwością urządzenia. Uruchom drukarkę bez karty po `PORT OTWARTY`. Parametry są stałe **250000 8N1**, bez rekonfiguracji timeout w pętli.

7. Host wymaga pełnych odpowiedzi PONG/INFO, sprawdza każdą ramkę CRC32, końcowy SHA-256, dwa odczyty SIZE oraz równość kopii. Dla 256 KiB kończy `PASS_FULL_AUDIT_256K_X2`. Zapisuje ZIP na Pulpicie. Przy błędzie zachowaj `.partial` i log; nie certyfikuj niepełnej kopii.

**Publiczny odbiornik nie zawiera prywatnego wzorca danych NVM autora.** Potwierdza spójność dwóch nowych odczytów i znanego payloadu diagnostyki, nie identyczność z nieistniejącą wcześniejszą kopią konkretnej drukarki. To publikacyjny wariant hosta, sprawdzany offline; field-tested transport i niezmienione firmware nie oznaczają nowego testu tego hosta na każdej płycie.

Po backupie możesz powrócić do oryginalnego firmware przez zachowany OEM, zanim podejmiesz dalszą decyzję. Nie testuj druku na diagnostyce.

## 5. Kontrola przed instalatorem v1.1

```sh
python3 tools/check_backup_profile.py /sciezka/do/prywatnego/audytu
```

Akceptowane są pary `FLASH256_POST_UPDATE_A/B.bin` lub `FLASH_A/B.bin` + UID/SIZE/OPTIONS A/B albo cztery ukończone kopie SD: `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT`.

- `PASS_I4_PROFILE_MATCH`: kopie są spójne i pasują do **wbudowanego profilu wydania**. To nie certyfikat bezpieczeństwa całej instalacji.
- `BACKUP_VALID_BUT_INSTALL_PROFILE_MISMATCH`: zachowaj kopie; **nie używaj tych pakietów i4** na tym urządzeniu. Nie kopiuj cudzych danych ani nie zmieniaj hashy.

## 6. Archiwum osobiste

Zachowaj: niezmienione BIN-y, manifest, SHA256SUMS, UART.log/raw, zdjęcia menu i PCB, oryginalny Update.bin z wersją i SHA oraz zapis daty i procedury. Udostępniaj publicznie co najwyżej zanonimizowany wynik. Zrzuty zawierają numer/UID, kalibrację i dane producenta. Wgranie cudzej kopii może sklonować obcą tożsamość i ustawienia.

Backup wykonany przez instalator SD jest **przed podmianą bootloadera, ale po zastąpieniu aplikacji pośrednikiem**. Nie opisuj go jako oryginalnej nienaruszonej drukarki. Przy odtwarzaniu może cofnąć licznik do daty kopii. UID/SYSROM/SIZE nie są plikami do programowania, a OPTIONS wymagają świadomego osobnego postępowania.

## Źródła / Sources

Dane o zachowaniu M300 pochodzą z kodu wydania v1.1/i4, audytów plików z projektu i relacji właściciela. Nie są deklaracją producenta. Publiczny zestaw nie zawiera prywatnych zrzutów ani logów.

- [ST PM0075, Rev. 2, §2.4, s. 17–20](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf): RDP/WRP i Option Bytes STM32F1.
- [STM32CubeProgrammer 2.23 — programming and erasing](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_UserManual/Memory_programming_and_erasing.html): adres dla BIN, zapis i weryfikacja.
- [STM32CubeProgrammer 2.23 — connection settings](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_UserManual/Main_window.html): SWD, Under Reset i NRST.
- [Projekt odniesienia — Inventure Boot Loader](https://github.com/MarcinKowalik-AGH/Zortrax-Inventure-Boot-Loader). Binaria obu drukarek NIE są zamienne.
