# Publiczne narzędzia hosta — M300Boot 1.4.1

[English](README.md) · [Polski](README_PL.md)

Python **3.9+**. pySerial jest wymagany tylko dla UART. Dopasuj aktywną prędkość i zamknij pozostałe programy UART. Dokładnie pięć prędkości: **115200,250000,500000,750000,1500000**; domyślnie 250000. Instalator SD chwilowo korzysta z 250000.

| File | Zastosowanie |
|---|---|
| `KONSOLA_M300_v1.4.1.command`, `m300_console.py` | Odczyt wersji 1.4.1, płyty, PING i par zrzutów |
| `m300_service.py` | Zrzuty UART, kontrola kopii i historii |
| `ibtool.py` | Kontrola/pakowanie M3B; sprawdzenie UART, jawna aktualizacja --update |
| `verify_sd_i2.py` | Bieżące sześcioplikowe karty i gotowe kopie |
| `stlink_preflight.py`, `verify_package.py` | Programowy plan, chronione obszary, pełny odczyt i kontrola paczki |
| `validate_publication.py` | Audyt bieżącego i archiwalnych wydań |
| `validate_original_boot.py` | Tożsamość oryginalnego BOOT OEM i późniejszy odbiór właściciela |
| `read_flash_m300_055.py` | Odbiornik niezależnej diagnostyki 0.5.5 |

```sh
python3 tools/validate_publication.py --json
python3 tools/stlink_preflight.py --help
python3 tools/ibtool.py --help
```

Archiwalne launchery i generatory 1.1/1.3.1/1.4 zachowują pierwotny numer. W szczególności prepare_stlink.py buduje 1.1, nie 1.4.1. Nie przygotowuj bieżącego BOOT historycznym generatorem. Aktualna konsola oczekuje 1.4.1. Własne kopie, UID/opcje, plany i logi pozostają prywatne.

[UART](../docs/pl/v1.4.1/uart-examples.md) · [ST-Link](../docs/pl/v1.4.1/stlink-and-recovery.md) · [Wszystkie instrukcje](../docs/pl/README.md).

Pomocnik karty serwisowej sprawdza rozmiary i typy plików przed tworzeniem czegokolwiek; zachowuje istniejące pliki i nie potwierdza ich zawartości. Integralność gotowych kopii sprawdź odpowiednim weryfikatorem. Błąd połączenia UART zamyka częściowo otwarte logi i nie nadpisuje wcześniejszych dzienników.
