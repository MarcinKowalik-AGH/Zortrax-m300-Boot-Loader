# M300 boot v1.1 — FACTORY oraz UPGRADE

Najpierw [kopia oryginału](KOPIA_ORYGINALU_PL.md), zgodność prywatnego profilu i4 oraz [zakres testów](TESTED_HARDWARE.md). Wydanie nie jest uniwersalne dla wszystkich HW05.

## Wybór zestawu

- Oryginalny rozpoznany OEM v3: SD_FACTORY_OEMV3_i4, start z Update.bin.
- Rozpoznany M300Boot FULL rc1/rc2/rc3/v1.1: SD_UPGRADE_i4, ręczny wybór M300APP.M3B.
- SWD: osobna procedura ST-Link, nie przemianowanie pliku SD.

Każda świeża karta FAT32 zawiera sześć plików w katalogu głównym: Update.bin ALBO M300APP.M3B, RESTORE.BIN, M3FLASH.BIN, M3INFO.BIN, ZBACK2.BIN, ZINFO2.DAT. Cztery ostatnie są szablonami A5, nie backupem. Nie nadpisuj nimi istniejących realnych kopii. Na kartę nie kopiuj całego projektu ani obu wariantów naraz. RESTORE zawiera oryginalne M300 1.3.1.

## FACTORY

Przy wyłączonej drukarce włóż kartę FACTORY i uruchom aktualizację OEM; może rozpocząć się automatycznie. Nie przerywaj zapisu. Po faktycznym końcu wyłącz, wyjmij kartę i uruchom bez niej. Gdy pojawi się stabilne menu SD installer 1.1-i4, włóż tę samą kartę. Sam ten etap zastąpił aplikację, jeszcze nie bootloader.

## UPGRADE

Włóż kartę przy wyłączonym urządzeniu. Uruchom i przerwij pięciosekundowy autostart pokrętłem. Wybierz Firmware on SD → Choose firmware file → M300APP.M3B. Wykonaj Check selected file, następnie Install selected file. Dopiero na prośbę puść pokrętło i przytrzymaj 2 sekundy. Po zapisie: Diagnostics → Verify Flash, potem Start application → Launch application z osobnym potwierdzeniem. Uruchomi się i4; kartę pozostaw w czytniku.

## Wspólna procedura i4

1. Check board + SD: sprawdza tożsamość, rozpoznany kod, RESTORE i rozdzielne łańcuchy FAT. Oczekiwane CHECK_SOURCE_CARD_RESTORE_OK. Błąd oznacza STOP.
2. Backup Flash x2: dwa niezależne odczyty po 256 KiB, readback SD, SHA-256 i porównanie kopii. Oczekiwane PASS_SD_FULL_FLASH_X2. Nie resetuj pomiędzy Backup i Install; po restarcie trzeba ponownie wykonać/zweryfikować backup.
3. Install / upgrade boot: najpierw kontrole. Identyczne v1.1 jest pomijane, a rc3 → v1.1 wymaga zapisu. Poczekaj na ekran zgody — nie wciskaj przycisku podczas Checking/Verifying.

Gest zgody:

| Ekran | Czynność |
|---|---|
| 1 Release knob | Niczego nie naciskaj |
| 2 Click knob once | Naciśnij |
| 3 Release after click | Puść |
| 4 Press and hold 5s | Naciśnij ponownie |
| 5 Keep holding knob | Trzymaj do końca gestu; obrót anuluje |

Po CONFIRM_OK CONFIRMED_5S ponownie sprawdzane są kopie i chronione zakresy. Od WRITING_FIXED_BOOT_PAGES nie resetuj, nie wyjmuj SD i nie odłączaj zasilania, chyba że występuje zagrożenie. Dopuszczalne strony: 2–15 i 116–121. Oczekiwany koniec INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED.

4. Restart to boot: po powodzeniu lub pominięciu identycznego celu. Przy starcie przytrzymaj pokrętło, aby pozostać w menu, potem puść. Nie pozwól autostartowi ponownie wejść do pośrednika.

## Odtworzenie 1.3.1

W nowym bootloaderze ręcznie wybierz Firmware on SD → Choose firmware file → RESTORE.BIN, nie M300APP.M3B. Check selected file → Install selected file; na prośbę 2-sekundowe przytrzymanie. Następnie Diagnostics → Verify Flash oraz Start application → Launch application, z osobną zgodą. Sprawdź stock 1.3.1, własny serial, hardware i bieżący licznik. To jeszcze nie pełny test ruchu/grzałek/druku.

Po zakończeniu i wyłączeniu skopiuj cztery rzeczywiste pliki backupu na inny nośnik. Skrypt SPRAWDZ_M300_SD_I4.command --backups sprawdza ich strukturę, CRC/SHA i zgodność. Zachowaj logi prywatnie.

## Ograniczenia

Przerwa podczas podmiany może zablokować rozruch; brak automatycznego rollbacku. Recover saved boot działa jedynie przy nadal pracującym instalatorze i poprawnych kopiach tej sesji. Zachowane 4 KiB nie są niezależnym recovery. Stara automatyczna karta OEM po podmianie nie jest gwarantowanym ratunkiem. Nie zmieniaj RDP/WRP ani hashy w celu obejścia odmowy. Zapisz pełne ERROR INSTALL / OP / PHASE / REASON.
