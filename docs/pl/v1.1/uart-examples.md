# M300 boot v1.1 — przykłady konsoli UART i aktualizacji APP

[English](../../en/v1.1/uart-examples.md) · [Polski](../../pl/v1.1/uart-examples.md) · [Indeks](README.md)

**Archiwalny zapis v1.1 z 29 października 2026.** Poniższe ustalenia zachowują historyczny zakres. [Bieżąca v1.3.1](../v1.3.1/README.md).

**Zakres:** działający M300Boot FULL v1.1, klasyczna M300 Rev.5.3/HW05/256 KiB, profil zgodny. **Nie** są to komendy fabrycznego firmware Zortrax 1.3.1 ani instalatora SD. Przed testem przerwij pięciosekundowy autostart, pozostając w menu bootloadera. Nazwa `/dev/cu.usbmodem14203` jest przykładem.

## Połączenie

UART logika **3,3 V**: potwierdzone sygnały PA9/USART1_TX → RX adaptera, PA10/USART1_RX ← TX adaptera, wspólna GND. **Nigdy 5 V.** STLINK-V3SET VCP jest adapterem szeregowym; SWD oraz UART CubeProgrammer nie są tą konsolą. Zamknij inne procesy korzystające z portu. Domyślne **250000 8N1**; jeżeli zapisano inną prędkość, wybierz ją albo przytrzymaj enkoder podczas startu, aby wejść w tryb serwisowy 250000.

```sh
python3 -m pip install pyserial
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203
```

Powyższy skrypt sprawdza `INFO`, `PING`, `BOARD_CHECK OK` oraz odpowiedzi `DONE`/`READY`, ale nie programuje Flash. Do dwóch odczytów użyj `--dump-all`:

```sh
bash tools/KONSOLA_M300_v1.1.command --port /dev/cu.usbmodem14203 --dump-all
```

Weryfikacja pojedynczego obszaru z osobnym zapisem (odczyt, bez programowania):

```sh
mkdir -p private
python3 tools/m300_service.py dump --port /dev/cu.usbmodem14203 --baud 250000 BOOT --out private/BOOT_NEW.bin
```

## Kontrola/utworzenie M3B — aplikacja, nie BOOT

Weryfikacja pakietu obecnej aplikacji po rozpakowaniu ZIP UPGRADE:

```sh
python3 tools/ibtool.py inspect /sciezka/do/M300APP.M3B
```

Weryfikacja oryginalnej aplikacji opakowanej jako M3B w zestawie SD:

```sh
python3 tools/ibtool.py inspect /sciezka/do/RESTORE.BIN
```

Opakowanie **własnej, już skompilowanej** aplikacji z wektorami dla `0x08008000`:

```sh
python3 tools/ibtool.py pack /sciezka/do/wlasnej_app.bin /sciezka/do/nowej_app.M3B
python3 tools/ibtool.py inspect /sciezka/do/nowej_app.M3B
```

Narzędzie nie odszyfrowuje `Update.bin`, nie posiada kluczy producenta i **nie tworzy bootloadera**. Pole `sha256` w M3B zapewnia integralność, nie uwierzytelnienie.

Próba sprawdzenia pakietu przez UART (bez zapisu MCU):

```sh
python3 tools/ibtool.py serial /sciezka/do/nowej_app.M3B --port /dev/cu.usbmodem14203 --baud 250000
```

**Programowanie APP** jest osobną operacją, dopuszczaną dopiero po kontroli, pełnym backupie i fizycznym potwierdzeniu. Gdy operator świadomie wybiera ten wariant, `serial --update` uruchamia operację programującą aplikację, **nie bootloadera**. Nie używaj go do pierwszej diagnostyki i nie mieszaj go ze starym skryptem instalatora rc3 `--install`.

## Kopie i historia

Kopia wygenerowana przez instalator i4 ma dwa obrazy po 256 KiB i dwie strony informacyjne. Sprawdzenie (bez zapisu do drukarki):

```sh
python3 tools/check_backup_profile.py /sciezka/do/prywatnej/kopii
python3 tools/m300_service.py verify-backup /sciezka/do/M3FLASH.BIN /sciezka/do/M3INFO.BIN
python3 tools/m300_service.py decode-log /sciezka/do/M3LOG.BIN
```

`decode-log` wymaga rzeczywiście zapisanej historii, a nie pustego szablonu. **Nie zamieszczaj kopii, logów ani pełnego wyjścia z numerem seryjnym/UID w publicznym issue.**

[Przed zmianami: kopia oryginału](original-backup.md) · [Instalacja PL](installation.md) · [Funkcje i Hardware](features-and-console.md) · [Index](README.md)
