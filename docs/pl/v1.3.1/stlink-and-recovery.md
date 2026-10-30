# ST-Link i kontrola odczytu — M300Boot v1.3.1

[English](../../en/v1.3.1/stlink-and-recovery.md) · [Polski](../../pl/v1.3.1/stlink-and-recovery.md) · [Indeks](README.md)

Droga STLINK tej wersji zapisuje **dwa segmenty, zachowując APP i dane drukarki**. To bieżąca procedura SWD 1.3.1 zamiast dawnej rekonstrukcji pełnego obrazu. Właściciel potwierdził działanie ST-Link na sprzęcie, tak samo jak FACTORY i UPGRADE, 30 października 2026. Preflight/readback sprawdzono również programowo.

| Plik w `03_TARGET_FULL` | Adres | Dokładna długość | Kasuj tylko te strony 2 KiB |
|---|---|---:|---|
| `M300Boot_v1.3.1_FULL_ASSETS_0x0803A000.bin` | `0x0803A000` | 12288 B | 116–121 |
| `M300Boot_v1.3.1_FULL_STAGE2_0x08001000.bin` | `0x08001000` | 28672 B | 2–15 |
| `M300Boot_v1.3.1_FULL_SPARSE.hex` | W rekordach HEX | 40960 B pamięci | Te same dwa zakresy |

**STAGE2 nie jest BIN-em pod 0x08000000.** HEX ma pełne końcówki FF i nie zawiera APP, prefixu OEM, dzienników ani NVM. Nie odtworzy całego skasowanego układu. `Update.bin`, `RESTORE.BIN` i M3B są kontenerami, nie bezpośrednimi obrazami SWD.

## Warunki i połączenie

RDP musi być **już wyłączone**, odczyt SWD działać, WRP zezwalać na wymagane cele, profil sprzętu/UID/prefixu/strony fabrycznej być zgodny, a APP poprawna. Przy aktywnym RDP wybierz SD. Nie wykonuj Read Unprotect, Mass Erase, zmiany RDP ani Apply Option Bytes, żeby kontynuować. Zdjęcie aktywnego RDP STM32F1 kasuje Flash, której nie odtworzą te segmenty.

Przy wyłączonym zasilaniu podłącz niezależnie rozpoznane **SWDIO, SWCLK, GND, VTref 3,3 V i NRST**. UART TX/RX to nie SWD. Nie podajemy niezweryfikowanych numerów złącza M300. W CubeProgrammer wybierz ST-LINK/SWD, Under reset, Hardware reset, początkowo 400 kHz; wymagany NRST. Sprawdź napięcie, Cortex-M3/F103 i **zmierzone 256 KiB**. Zatrzymaj rdzeń; nie uruchamiaj pomiędzy odczytami i zapisami.

Zapisz dwa rzeczywiste niezależne odczyty `FLASH_A.bin` i `FLASH_B.bin` od `0x08000000`, długość `0x40000`. Odczytaj `UID.bin` z `0x1FFFF7E8` (12 B), `OPTIONS.bin` z `0x1FFFF800` (16 B). Sprawdź 16-bitowy SIZE `0x1FFFF7E0` = 256. Nie programuj tych adresów systemowych ani pliku opcji.

## Prywatny plan offline

Rozpakuj archiwum STLINK i przejdź do jego głównego katalogu:

```sh
python3 tools/verify_package.py
python3 tools/stlink_preflight.py plan   --backup-a "/private/FLASH_A.bin" --backup-b "/private/FLASH_B.bin"   --uid "/private/UID.bin" --options "/private/OPTIONS.bin"   --out-dir "/private/NOWY_PLAN_M300_V131"
```

Oczekiwane `PASS_OFFLINE_STLINK_PLAN`. Powstaje wyłącznie prywatny plan na komputerze; skrypt nie otwiera programatora i odmawia nadpisania katalogu. Przy `changed: false` nie programuj identycznego obrazu. Kontrole UID/profilu i już wyłączonego RDP są celowe. Odmowa nie pozwala na ich usunięcie. Używając narzędzi z repozytorium zamiast paczki, dodaj do plan i verify `--images "/sciezka/STLINK/03_TARGET_FULL"`.

## Zapis, weryfikacja, dopiero start

1. Pozostaw rdzeń zatrzymany. Włącz Verify after programming; wyłącz automatyczne Run i kasowanie całego układu.
2. Zapisz **ASSETS pod 0x0803A000**, kasując tylko strony 116–121; zweryfikuj.
3. Zapisz **STAGE2 pod 0x08001000**, kasując tylko strony 2–15; zweryfikuj. Zachowaj początkowe 4 KiB.
4. Nadal bez startu odczytaj całe 256 KiB do `FLASH_AFTER.bin` oraz `UID_AFTER.bin` i `OPTIONS_AFTER.bin`.
5. Sprawdź cały obraz i każdy bajt poza segmentami:

```sh
python3 tools/stlink_preflight.py verify   --plan "/private/NOWY_PLAN_M300_V131/PRIVATE_STLINK_PLAN.json"   --before "/private/FLASH_A.bin" --after "/private/FLASH_AFTER.bin"   --uid-after "/private/UID_AFTER.bin" --options-after "/private/OPTIONS_AFTER.bin"
```

Oczekiwane `PASS_STLINK_READBACK_ALL_256K`. Przy różnicy zachowaj odczyty i pozostaw rdzeń zatrzymany; nie resetuj ani nie kasuj automatycznie. Po zgodnym odczycie zakończ debug, wyłącz zasilanie, odłącz programator i uruchom bez karty aktualizacji. Sprawdź **M300 boot v1.3.1**, zapisane baud/bootwait i dotychczasową aplikację. Ta droga nie zastępuje APP i nie wymaga wgrywania jej ponownie tylko z powodu zmiany BOOT.

Utrata zasilania podczas programowania BOOT może uniemożliwić rozruch. Odzyskanie po pełnym kasowaniu wymaga własnych kompletnych kopii i osobno sprawdzonego planu. Dawny `prepare_stlink.py` tworzy **v1.1**, nie v1.3.1; nie używaj go do tego wydania.

Dokumentacja producenta: [ST PM0075](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf), Flash/RDP/WRP; [ST UM2237](https://www.st.com/resource/en/user_manual/dm00403500-stm32cubeprogrammer-stmicroelectronics.pdf), programowanie i odczyt zwrotny.
