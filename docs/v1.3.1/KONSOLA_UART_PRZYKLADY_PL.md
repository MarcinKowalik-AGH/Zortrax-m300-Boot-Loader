# UART, zapis ustawień i start MCU — v1.3.1

[English](UART_EXAMPLES_EN.md) · [Funkcje](FUNKCJE_I_KONSOLA_PL.md)

## Konsola boota

Logika **TTL 3,3 V**: PA9/USART1_TX → RX adaptera, PA10/USART1_RX ← TX adaptera, wspólna GND. To nazwy sygnałów MCU, **nie numery pinów fizycznego złącza**. Użyj niezależnie potwierdzonego podłączenia M300. Nie podawaj 5 V. VCP TX/RX to nie SWDIO/SWCLK. Przed otwarciem konsoli zatrzymaj inne procesy UART, także hosta Orange Pi.

Przy bootwait OFF wejdź najpierw pokrętłem do menu serwisowego. Do diagnostyki w odliczaniu wcześniej zapisz ON; pełna dozwolona komenda, np. `INFO`, otworzy wtedy konsolę. Przy nieznanej prędkości przytrzymaj pokrętło przy włączeniu — tymczasowo 250000. Pośrednik SD używa 250000 niezależnie od zapisu.

```sh
python3 -m pip install -r tools/requirements.txt
bash tools/KONSOLA_M300_v1.3.1.command --port /dev/cu.usbmodem14203 --baud 250000
bash tools/KONSOLA_M300_v1.3.1.command --port /dev/cu.usbmodem14203 --baud 1500000 --dump-all
```

Przykłady zakładają różne aktywne prędkości; wykonaj pasujący. Kontrola wymaga `M300BOOT v1.3.1`, `BOARD_CHECK OK`, PONG i końcowego READY. Wyniki są prywatne. Launcher tylko odczytuje; `ibtool.py serial --update` to osobna, jawna operacja zapisu APP.

| Komenda | Działanie |
|---|---|
| `INFO`, `PING`, `HELP` | Wersja/sprzęt/UART/OLED, test łącza, lista poleceń. |
| `MENU`, `HOME`, `BACK` | Powrót do głównego menu boota. |
| `VERIFY` | Kontrola zainstalowanej Flash. |
| `LIST`, `SELECT n`, `SELECT AUTO` | Katalog SD, wybór indeksu od zera lub automatyczny. |
| `SDCHECK`, `SDUPDATE` | Kontrola/instalacja wybranej APP; zapis wymaga fizycznego potwierdzenia. |
| `UARTCHECK N`, `UARTUPDATE N` | Protokół serwera plików M3B; obsługuj przez `ibtool.py`. |
| `DUMP FLASH`, `DUMP BOOT`, `DUMP NVM`, `DUMP FACTORY`, `DUMP SYSROM`, `DUMP SIZE`, `DUMP UID`, `DUMP OPTIONS` | Odczyt stałych zakresów z kontrolą kolejności, CRC i pełnego SHA-256. |
| `BACKUP`, `LOGSAVE` | Jawny zapis kopii/historii SD; wymagane przygotowane pliki. |
| `RESETINFO`, `RECOVERY CLEAR`, `DIAG`, `DISPLAY`, `CARDINFO`, `LOG` | Diagnostyka; skasowanie blokady recovery celowo zmienia stan. |
| `BOOT`, `REBOOT` | Jawne uruchomienie APP/restart sterownika. |

```sh
python3 tools/ibtool.py inspect "/sciezka/M300APP.M3B"
python3 tools/ibtool.py pack "/sciezka/wlasna-app.bin" "/sciezka/NOWA.M3B"
python3 tools/ibtool.py serial "/sciezka/NOWA.M3B" --port /dev/cu.usbmodem14203 --baud 250000
```

`pack` wymaga gotowej APP pod 0x08008000, nie stage2. `serial` bez `--update` jedynie sprawdza. M3B ma integralność SHA-256, nie podpis. Narzędzie nie ma kluczy OEM ani funkcji odszyfrowania.

## Dopasowanie Klippera do zapisu

Ta publikacja BOOT nie instaluje modułów Klippera. Do 1500000 wymagane są zgodne MCU **UART8** i walidator hosta; nie wymuszaj obsługi na UART7. Samodzielny ekran `Waiting for Klipper` rysuje aplikacja MCU przed połączeniem Orange Pi, odczytując zapisany baud. Bootloader 1.3.1 nie doda tego ekranu dowolnej aplikacji.

Zatrzymaj Klippera na Orange Pi. W boocie wybierz `Diagnostics → UART → UART baud rate → 1500000` i sprawdź potwierdzenie zapisu Flash. Do normalnego startu ustaw `UART on bootwait → OFF`. W istniejącej sekcji hosta zmień tylko baud:

```ini
[mcu]
serial = /dev/ttyS1
baud = 1500000
restart_method = command
```

Ścieżka to sprawdzona konfiguracja UART1 Orange Pi, nie uniwersalne mapowanie Linuksa. Uruchom drukarkę **bez trzymania pokrętła**, zaczekaj na ekran zgodnej aplikacji MCU, potem uruchom Klippera. W konsoli Fluidd:

```gcode
STATUS
ZORTRAX_MCU_STATUS
ZORTRAX_OLED_STATUS
```

Oczekiwane Ready, `uart.baud = host_baud = 1500000`, `index = 7`, `match = true`, brak zgłoszonego fault. Właściciel potwierdził takie połączenie UART8, również z późniejszym OLED-R3.2. Nie oznacza to kwalifikacji ruchu/grzania ani zapasu podczas druku. Przy zmianie baud nie zmieniaj SPI ani blokad wykonawczych.

Przy braku połączenia zatrzymaj hosta i przywróć **po obu stronach** sprawdzony baud, uruchom MCU, potem hosta. Sama zmiana `[mcu] baud` nie zmienia zapisu MCU. [Diagnostyka](DIAGNOSTYKA_PL.md).
