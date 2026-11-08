# Kopie bezpieczeństwa — M300Boot 1.4

[English](../../en/v1.4/original-backup.md) · [Polski](../../pl/v1.4/original-backup.md) · [Index](README.md)

Zachowaj oryginalny BOOT 32 KiB, końcowe 8 KiB danych producenta/NVM, pełny Flash 256 KiB, gdy jest dostępny, oraz UID, zmierzone SIZE i Option Bytes. Uzyskaj dwa niezależne zgodne odczyty, zamiast powielać jeden plik. Przechowuj kopie na dwóch nośnikach. Nie publikuj ekranów z numerem seryjnym, logów ani zrzutów urządzenia.

## Przed zmianą oryginalnej drukarki

Przy aktywnym RDP postępuj według niezmienionej [instrukcji diagnostyki 0.5.5](../v1.1/original-backup.md). Diagnostyka najpierw zastępuje APP. Pełny zrzut Flash wykonany później zawiera APP diagnostyczną; nie jest nienaruszonym obrazem fabrycznym sprzed aktualizacji. Oryginalne BOOT/NVM pozostają zachowane, a aplikację oryginalną 1.3.1 dostarcza osobno `RESTORE.BIN`. Dla diagnostyki 0.5.5 używaj `read_flash_m300_055.py`, a dla instalacji BOOT instrukcji 1.4. Nie usuwaj RDP STM32F1 w celu odczytu: Read Unprotect kasuje główny Flash.

## Z BOOT 1.4

Zatrzymaj Klippera i inne programy UART. Wejdź do lokalnego menu i uruchom:

```sh
bash tools/KONSOLA_M300_v1.4.command --port /dev/cu.usbmodem14203 --baud 250000 --dump-all
```

Port jest przykładowy. Dopasuj aktywny baud; przytrzymanie pokrętła przy włączaniu wymusza chwilowo 250000. Narzędzie tylko odczytuje, wykonuje pary eksportów stałych obszarów i sprawdza ich zgodność z pełnym Flash. Zachowaj wyniki oraz manifest prywatnie.

## Kopie instalatora

| Kopia | Plik Flash | Plik informacyjny |
|---|---|---|
| A | `M3FLASH.BIN` — 262144 B | `M3INFO.BIN` — 1024 B |
| B | `ZBACK2.BIN` — 262144 B | `ZINFO2.DAT` — 1024 B |

Instalator wypełnia cztery szablony A5 podczas `Backup Flash x2`, sprawdza oba zrzuty i zachowuje kwalifikację sesji. Kopie opisują stan po wgraniu pośredniej APP, przed zmianą BOOT. Sprawdź gotowe pliki: `python3 tools/verify_sd_i2.py --backups "/private/completed-backups"`. Nigdy nie zastępuj ich świeżymi szablonami.

Gdy RDP jest już wyłączone, użyj [kontroli ST-Link](stlink-and-recovery.md): dwóch rzeczywistych odczytów Flash, UID i opcji. Paczka dwóch segmentów nie odtwarza całkowicie skasowanego układu.
