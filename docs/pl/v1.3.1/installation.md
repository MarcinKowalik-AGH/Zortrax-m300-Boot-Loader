# Instalacja SD — M300Boot v1.3.1

[English](../../en/v1.3.1/installation.md) · [Polski](../../pl/v1.3.1/installation.md) · [Indeks](README.md)

Wybierz **UPGRADE** dla rozpoznanego własnego M300Boot, a **FACTORY** dla zakwalifikowanego oryginalnego OEM v3. Lista hashy źródła obejmuje rc1/rc2/rc3, 1.1, 1.1-u1, 1.2, 1.2.1, 1.3 i 1.3.1. Nadal obowiązują osobne kontrole tożsamości/profilu. Zatrzymaj Klippera na podłączonym hoście. Zapewnij stabilne zasilanie podczas zapisu.

## Przygotowanie karty

1. Zachowaj zweryfikowane kopie na osobnym fizycznym nośniku. Nie zastępuj wykonanych kopii pustymi szablonami.
2. Pobierz właściwe archiwum z `firmware/v1.3.1` lub Release v1.3.1 i porównaj SHA-256 z manifestem tej wersji. Rozpakuj do nowego katalogu. Sześć plików SD jest w głównym katalogu ZIP.
3. Na świeżej karcie FAT32 umieść w katalogu głównym dokładnie sześć plików właściwej drogi:

| Droga | Pliki na karcie |
|---|---|
| UPGRADE | `M300APP.M3B`, `RESTORE.BIN`, `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT` |
| FACTORY | `Update.bin`, `RESTORE.BIN`, `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT` |

`M3FLASH.BIN` / `ZBACK2.BIN` (po 262144 B) i `M3INFO.BIN` / `ZINFO2.DAT` (po 1024 B) to początkowo **szablony A5, nie backupy**. Instalator sprawdza rozłączność fizycznych klastrów przed zapisem. Nie mieszaj `Update.bin` i instalacyjnego `M300APP.M3B` na jednej karcie.

Z głównego katalogu repozytorium, aktualnymi narzędziami:

```sh
python3 tools/verify_sd_i2.py --card "/Volumes/M300_CARD" --route upgrade
# Dla FACTORY użyj --route factory.
```

Oczekiwane `PASS_SD_V131_CARD_FILES`. To kontrola plików na komputerze, nie zapis w drukarce ani kontrola klastrów FAT.

## UPGRADE: działający własny bootloader

1. Przerwij odliczanie pokrętłem i puść przycisk.
2. `Firmware on SD → Choose firmware file → M300APP.M3B → Check selected file`.
3. `Install selected file`; na prośbę puść i przytrzymaj pokrętło przez 2 s. Zastępujesz **APP pośrednikiem**, jeszcze nie stały BOOT.
4. `Diagnostics → Verify Flash`, potem `Start application → Launch application`; potwierdź ręczny start. Ekran ma pokazać **SD installer 1.3.1**.
5. Wykonaj wspólną część poniżej.

## FACTORY: oryginalny OEM v3

1. Włóż kartę FACTORY przy wyłączonym zasilaniu. OEM może natychmiast zapisać `Update.bin` po włączeniu; to nie jest próba samego wykrycia pliku.
2. Zaczekaj na zakończenie fabrycznej aktualizacji. Wyłącz, wyjmij kartę i włącz bez niej. Oczekuj **SD installer 1.3.1**. Stały oryginalny boot nadal jest zachowany. Techniczna wersja otoczki **9.8.7** jest prawidłowa i różni się od wersji instalatora.
3. W stabilnym menu pośrednika, gdy nic nie pracuje, włóż tę samą kartę. Wykonaj część wspólną bez restartów pomiędzy kontrolą, kopiami i wymianą BOOT.

## Wspólna transakcja instalatora

1. `Check board + SD` → oczekuj `CHECK_SOURCE_CARD_RESTORE_OK`.
2. `Backup Flash x2` → oczekuj `PASS_SD_FULL_FLASH_X2` w tej sesji. Niezależne odczyty mają już pośrednik zamiast APP; nie są fabrycznym zrzutem sprzed pierwszej aktualizacji.
3. `Install / upgrade boot`. Potwierdzenie: **puść → świeży klik → puść → nowe naciśnięcie i pełne 5 s przytrzymania**. Obrót anuluje. Klik wejścia do ekranu nie jest potwierdzeniem.
4. Oczekuj `INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED`. Dla identycznego celu może zostać wykonana zweryfikowana ścieżka bez ponownego zapisu. Przy odmowie nie zmieniaj hashy ani ochrony.
5. `Restart to boot`; zatrzymaj odliczanie i sprawdź **M300 boot v1.3.1**.
6. Zachowaj cztery wykonane pliki kopii SD w dwóch prywatnych lokalizacjach i sprawdź:

```sh
python3 tools/verify_sd_i2.py --backups "/sciezka/do/wykonanych-kopii"
```

Oczekiwane `PASS_SD_V131_BACKUPS_X2`. Kopie pozostają prywatne.

## Przywrócenie aplikacji drukującej lub Klippera

Po migracji SD w slocie aplikacji jest pośrednik. W `Firmware on SD → Choose firmware file` wybierz `RESTORE.BIN`; sprawdź, zainstaluj po potwierdzeniu 2 s, zweryfikuj Flash i uruchom. To oryginalny **Zortrax M300 1.3.1**. Przed testami wykonawczymi sprawdź dane sprzętu, licznik i ustawienia.

Dla Klippera zastąp na karcie instalacyjny `M300APP.M3B` **aplikacją z odpowiadającej paczki MCU**, a potem sprawdź/zainstaluj/zweryfikuj/uruchom tę aplikację. Pośrednik BOOT w tym wydaniu ma **102280 B** i nie jest aplikacją MCU Klippera. Osobna paczka MCU/host nie jest tu dołączona.

Do 1500000 MCU i host muszą obsługiwać **UART8**. Przy zatrzymanym hoście zapisz baud w `Diagnostics → UART → UART baud rate`, ustaw tę samą wartość `[mcu] baud` na hoście, uruchom drukarkę bez trzymania pokrętła, a potem hosta. Do zwykłego startu z Orange Pi wybierz bootwait **OFF**. [Dokładna procedura UART](uart-examples.md).

Nie ma automatycznego rollbacku BOOT po utracie zasilania. `Recover saved boot` wymaga zachowanej działającej sesji pośrednika i jej poprawnych kopii. [Warunki ST-Link](stlink-and-recovery.md).
