# Narzędzia PC — M300Boot v1.3.1

[English](README.md) · [Polski](README_PL.md)

Python **3.9+**; pySerial wymagany tylko do UART. To operacyjne narzędzia PC, nie źródła firmware. Utworzone kopie, logi i plany pozostają prywatne.

| Plik | Działanie | Zapis MCU? |
|---|---|---|
| `KONSOLA_M300_v1.3.1.command`, `m300_console.py` | Wersja/sprzęt/PING i opcjonalne podwójne odczyty stałych zakresów. | Nie |
| `m300_service.py` | Odczyt zakresów UART, kontrola kopii SD i dekodowanie historii. | Nie |
| `ibtool.py` | Pakowanie/sprawdzanie APP M3B; kontrola UART lub jawna aktualizacja aplikacji. | Tylko `serial --update`, z fizycznym potwierdzeniem |
| `verify_sd_i2.py` | Kontrola bieżącej karty z sześcioma plikami lub wykonanych kopii A/B. | Nie |
| `stlink_preflight.py` | Plan dwóch segmentów i pełny readback 256 KiB offline; `--images` wskazuje dokładne rozpakowane segmenty. | Bez dostępu do urządzenia; tylko prywatny plan na dysku |
| `verify_package.py` | Kontrola manifestu rozpakowanej paczki STLINK. | Nie |
| `read_flash_m300_055.py`, `audit_reference.py` | Odbiornik diagnostyki 0.5.5 według jej archiwalnej procedury. | Host tylko odczytuje; instalacja diagnostyki zastępuje APP |
| `prepare_service_sd.py` | Przygotowanie szablonów serwisowych SD bez nadpisywania. | Wyłącznie lokalne pliki SD |
| `validate_publication.py` | Kontrola bieżących/archiwalnych paczek i dokumentacji. | Nie |
| `KONSOLA_M300_v1.1.command`, `SPRAWDZ_M300_SD_I4.command`, `prepare_stlink.py`, `check_backup_profile.py` | Archiwalne narzędzia v1.1/i4. Stary generator buduje v1.1, nie v1.3.1. | Według instrukcji v1.1 |

```sh
python3 tools/validate_publication.py --json
python3 tools/verify_sd_i2.py --help
python3 tools/stlink_preflight.py --help
python3 tools/ibtool.py --help
```

Przykłady uruchamiaj z głównego katalogu repozytorium. Prędkości: **115200 / 250000 / 500000 / 750000 / 1000000 / 1500000**. Dopasuj aktywne baud i zamknij inne procesy UART. Bootwait OFF wymaga lokalnego wejścia do menu; ON dopuszcza pełne dozwolone linie diagnostyczne. Instalator SD chwilowo używa 250000.

Bez zdejmowania RDP, obchodzenia tożsamości i podpisywania/odszyfrowania OEM. M3B zapewnia integralność SHA, nie podpis kryptograficzny. [Instrukcje](../docs/pl/README.md) · [Procedura UART](../docs/pl/v1.3.1/uart-examples.md).
