# Zachowanie oryginalnej pamięci — M300Boot v1.3.1

[English](ORIGINAL_BACKUP_EN.md) · [Instalacja](INSTALACJA_PL.md)

Przed zmianami zachowaj dwa niezależnie odczytane, zgodne zestawy: oryginalny BOOT 32 KiB, końcowe 8 KiB NVM/danych fabrycznych, pełne 256 KiB Flash, jeśli dostępne, UID, zmierzony SIZE i Option Bytes. Przechowuj kopie na dwóch fizycznych nośnikach. Te pliki, ekrany z numerem seryjnym i logi UART pozostają prywatne.

## Oryginalna drukarka z aktywnym RDP

Użyj dotychczasowej [procedury diagnostyki UART 0.5.5](../v1.1/KOPIA_ORYGINALU_PL.md) i niezmienionego `M300_BACKUP_0.5.5_UART.zip`, dołączonego również do tego wydania. Wgranie diagnostyki najpierw zastępuje APP. Późniejszy pełny odczyt Flash jest zatem **po aktualizacji**: zachowuje oryginalne BOOT/NVM, lecz ma aplikację diagnostyczną. Nie jest dziewiczym zrzutem sprzed zmiany. Dokładny oryginał aplikacji 1.3.1 jest osobno w `RESTORE.BIN`.

Diagnostyka ma własny odbiornik `read_flash_m300_055.py`; nie służy do niej konsola boota v1.3.1. Ze starej instrukcji wykonaj część dotyczącą backupu; instalację v1.3.1 prowadź według nowej instrukcji. Nie wyłączaj ochrony STM32F1, aby uzyskać odczyt: **Read Unprotect kasuje główną Flash**. Nieudany odczyt SWD nie jest poleceniem zdjęcia RDP.

## Działający M300Boot v1.3.1

Wejdź pokrętłem do menu serwisowego. Zamknij Klippera i inne procesy używające tego UART. Konsola tylko do odczytu:

```sh
bash tools/KONSOLA_M300_v1.3.1.command --port /dev/cu.usbmodem14203 --baud 250000 --dump-all
```

Port jest przykładem. Dopasuj baud lub przytrzymaj pokrętło przy włączeniu, aby tymczasowo użyć 250000. Polecenie wykonuje po dwa niezależne odczyty każdego stałego obszaru, porównuje A/B i kontroluje części względem pełnej Flash. Nie programuje MCU. Wygenerowany katalog/ZIP i `MANIFEST.json` są prywatne.

## Kopie SD instalatora

Zestawy SD mają cztery **szablony A5**, nie gotowe kopie. `Backup Flash x2` wypełnia je i sprawdza tożsamość, SHA-256, CRC oraz zgodność. Zachowaj razem:

| Zestaw | Flash | Informacja |
|---|---|---|
| A | `M3FLASH.BIN` — 262144 B | `M3INFO.BIN` — 1024 B |
| B | `ZBACK2.BIN` — 262144 B | `ZINFO2.DAT` — 1024 B |

```sh
python3 tools/verify_sd_i2.py --backups "/sciezka/do/wykonanych-kopii"
```

Oczekiwane `PASS_SD_V131_BACKUPS_X2`. Ten kontroler stosuje zachowany profil instalacyjny i opcje z aktywnym RDP; kopię SWD przy RDP0 sprawdza preflight ST-Link. Nie nadpisuj wykonanych kopii świeżymi szablonami. Kopie instalatora pokazują stan **po** wgraniu APP pośrednika i **przed** wymianą BOOT.

## SWD, jeśli RDP jest już wyłączone

Użyj [instrukcji ST-Link](STLINK_I_ODZYSKIWANIE_PL.md): dwa rzeczywiste odczyty po 256 KiB, UID, opcje i kontrola SIZE 256 KiB. Skopiowanie pliku nie jest drugim odczytem. Nowa paczka STLINK ma wyłącznie dwa adresowane segmenty i nie odtworzy skasowanego całego układu. Odbudowa z pełnej prywatnej kopii wymaga zachowania prefixu, NVM i danych tej samej drukarki; to osobno planowana procedura.
