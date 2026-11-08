# Kopie bezpieczeństwa — M300Boot 1.4

[English](../../en/v1.4/original-backup.md) · [Polski](../../pl/v1.4/original-backup.md) · [Index](README.md)

Zachowaj oryginalny BOOT 32 KiB, końcowe 8 KiB danych producenta/NVM, pełny Flash 256 KiB, gdy jest dostępny, oraz UID, zmierzone SIZE i Option Bytes. Uzyskaj dwa niezależne zgodne odczyty, zamiast powielać jeden plik. Przechowuj kopie na dwóch nośnikach. Nie publikuj ekranów z numerem seryjnym, logów ani zrzutów urządzenia.

## Przed zmianą oryginalnej drukarki

Przy aktywnym RDP postępuj według niezmienionej [instrukcji diagnostyki 0.5.5](../v1.1/original-backup.md). Diagnostyka najpierw zastępuje APP. Pełny zrzut Flash wykonany później zawiera APP diagnostyczną; nie jest nienaruszonym obrazem fabrycznym sprzed aktualizacji. Oryginalne BOOT/NVM pozostają zachowane, a aplikację oryginalną 1.3.1 dostarcza osobno `RESTORE.BIN`. Dla diagnostyki 0.5.5 używaj `read_flash_m300_055.py`, a dla instalacji BOOT instrukcji 1.4. Nie usuwaj RDP STM32F1 w celu odczytu: Read Unprotect kasuje główny Flash.

## Przed aktualizacją istniejącego własnego BOOT

Przed zastąpieniem starszego własnego BOOT wykonaj niezależne odczyty sprzed aktualizacji narzędziami dopasowanymi do działającej wersji. Przykładowo archiwalna konsola 1.3.1 wymaga bannera 1.3.1, a bieżąca konsola 1.4 celowo wymaga 1.4 i jej nie zastępuje. Przy przejściu z 1.3.1 użyj [odpowiedniej instrukcji archiwalnej](../v1.3.1/original-backup.md). Dodatkowe kopie instalatora opisane niżej uzupełniają te odczyty sprzed aktualizacji; nie zastępują ich.

## Z BOOT 1.4

Zatrzymaj Klippera i inne programy UART. Wejdź do lokalnego menu i uruchom:

```sh
bash tools/KONSOLA_M300_v1.4.command --port /dev/cu.usbmodem14203 --baud 250000 --dump-all
```

Port jest przykładowy. Dopasuj aktywny baud; przytrzymanie pokrętła przy włączaniu wymusza chwilowo 250000. Narzędzie tylko odczytuje, wykonuje pary eksportów stałych obszarów i sprawdza ich zgodność z pełnym Flash. Zachowaj wyniki oraz manifest prywatnie.


## Zwykła kopia BOOT na karcie serwisowej: jedna para

`Backup Flash → Backup Flash + identity` w zwykłym BOOT wykonuje **jeden** zrzut 256 KiB i jeden plik tożsamości 1024 B. To inna czynność niż obowiązkowe `Backup Flash x2` pośrednika; nie nadaje kwalifikacji sesji instalatora.

1. Przygotuj na komputerze osobną sprawdzoną kartę serwisową FAT16/FAT32. Z głównego katalogu repozytorium uruchom:

```sh
python3 tools/prepare_service_sd.py "/Volumes/M300_SERVICE"
```

Powstaną szablony A5: `M3FLASH.BIN` (262144 B), `M3INFO.BIN` (1024 B) i opcjonalny plik historii `M3LOG.BIN` (4096 B). Skrypt nie formatuje karty ani nie zastępuje istniejących plików. `KEPT EXISTING` nie oznacza, że starszy plik jest pustym szablonem. Nie zastępuj tym trzyelementowym przygotowaniem karty serwisowej sześciu plików instalacyjnych FACTORY/UPGRADE.
2. Bezpiecznie odłącz kartę, włóż ją do drukarki, wejdź do lokalnego menu BOOT i wybierz `Backup Flash → Backup Flash + identity`. Zwolnij pokrętło, a następnie wykonaj nowe **przytrzymanie 2 s**. Obrót anuluje. Zapisywana jest wyłącznie karta SD, nie Flash kontrolera.
3. Poczekaj na zakończenie i automatyczny powrót do menu BOOT. Błąd jest sygnalizowany jako `Operation rejected`; opcjonalna konsola UART potwierdza sukces przez `BACKUP VERIFIED: M3FLASH.BIN + M3INFO.BIN`, następnie `DONE OK`. Czas wyświetlania wyniku i powrót do menu BOOT działają inaczej niż zamykane kliknięciem wyniki instalatora pośredniego.
4. Gdy operacja się zakończy i BOOT pokazuje stabilne menu, wyłącz drukarkę, przenieś kartę do komputera i skopiuj parę na inny nośnik. Sprawdź skopiowane pliki:

```sh
python3 tools/m300_service.py verify-backup "/private/backup/M3FLASH.BIN" "/private/backup/M3INFO.BIN"
```

Wymagaj kodu zakończenia 0 i `"verified": true`. Wynik zawiera tożsamość MCU i Option Bytes; zachowaj go prywatnie. Sprawdzana jest ta jedna para, nie dwa niezależne odczyty. Warstwa zapisu dopuszcza puste sektory A5 lub identyczną zawartość już skopiowaną i odmawia nadpisania niezgodnej istniejącej kopii. Nie usuwaj jedynej zachowanej kopii, aby ominąć odmowę.

## Kopie instalatora

| Kopia | Plik Flash | Plik informacyjny |
|---|---|---|
| A | `M3FLASH.BIN` — 262144 B | `M3INFO.BIN` — 1024 B |
| B | `ZBACK2.BIN` — 262144 B | `ZINFO2.DAT` — 1024 B |

Instalator wypełnia cztery szablony A5 podczas `Backup Flash x2`, sprawdza oba zrzuty i zachowuje kwalifikację sesji. Kopie opisują stan po wgraniu pośredniej APP, przed zmianą BOOT. Sprawdź gotowe pliki: `python3 tools/verify_sd_i2.py --backups "/private/completed-backups"`. Nigdy nie zastępuj ich świeżymi szablonami. Instalator sam wykonuje i porównuje oba pełne odczyty oraz rekordy tożsamości. Reset usuwa kwalifikację kopii zapamiętaną w RAM, nawet gdy pliki pozostały na karcie; kolejna próba instalacji wymaga ponownego poprawnego `Backup Flash x2` w tej sesji. Nie używaj `--card` do gotowych kopii: ta opcja sprawdza początkowy zestaw z szablonami A5 i celowo odrzuci zmienione pliki. Do gotowego kompletu dwóch par używaj `--backups`, zachowując wszystkie cztery oryginalne nazwy.

Gdy RDP jest już wyłączone, użyj [kontroli ST-Link](stlink-and-recovery.md): dwóch rzeczywistych odczytów Flash, UID i opcji. Paczka dwóch segmentów nie odtwarza całkowicie skasowanego układu.

## Udostępniony oryginalny BOOT

Zachowany w projekcie [oryginalny Zortrax Bootloader v3](../../../firmware/original/README_PL.md) jest dostępny jako niezmieniony obraz referencyjny 32 KiB z SHA-256 i opisem pochodzenia. Zawiera wyłącznie BOOT i nie zastępuje pełnych, niezależnych kopii własnej drukarki. Jest osobny od aplikacji oryginalnej `RESTORE.BIN` i paczek instalacyjnych 1.4.
