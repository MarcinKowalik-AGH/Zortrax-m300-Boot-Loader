# Instalacja M300 boot v1.1 — FACTORY i UPGRADE

Dotyczy **klasycznej M300 Rev.5.3/HW05, 256 KiB, profilu rozpoznawanego przez i4**. Najpierw przeczytaj [kopię oryginału](KOPIA_ORYGINALU_PL.md) i [zakres zgodności](TESTED_HARDWARE.md). Nie używaj na Plus/Dual/Inventure. Instalator odmówi obcego UID/strony fabrycznej; nie jest to uniwersalny pakiet.

## 1. Wybór drogi

| Obecnie działa | Paczka |
|---|---|
| Oryginalny, rozpoznany **Zortrax Bootloader v3** | SD_FACTORY_OEMV3_i4 — start z `Update.bin` |
| Własny rozpoznany **M300Boot FULL rc1/rc2/rc3 lub v1.1** | SD_UPGRADE_i4 — ręczny wybór `M300APP.M3B` |
| Rozruch uszkodzony, potrzebne SWD | Osobna [procedura ST-Link](STLINK_I_ODZYSKIWANIE_PL.md); nie zamieniaj nazwy pliku SD na BIN |

Przebieg UPGRADE do v1.1/i4 i uruchomienie stock 1.3.1 potwierdził właściciel jednej drukarki. FACTORY i4 jest osobną drogą bez takiego odrębnego potwierdzenia. W obu paczkach znajduje się ta sama aplikacja i4 oraz ten sam docelowy boot v1.1.

## 2. Karta i kontrola

Użyj świeżej FAT32 (kod obsługuje też FAT16; nie exFAT). Zachowaj stare realne kopie przed kopiowaniem nowych szablonów. Rozpakuj jeden ZIP i skopiuj sześć plików **do katalogu głównego**, bez dodatkowego folderu:

- `Update.bin` **albo** `M300APP.M3B` — nigdy oba na tej samej karcie;
- `RESTORE.BIN` — dokładne oryginalne 1.3.1 w pakiecie nowego bootloadera;
- `M3FLASH.BIN`, `M3INFO.BIN`, `ZBACK2.BIN`, `ZINFO2.DAT` — początkowo szablony A5.

Szablony nie są backupem. Pierwszy i drugi plik Flash mają po **256 KiB**, nie 32 KiB jak kopie BOOT w instalatorze Inventure.

Sprawdzenie na komputerze, bez drukarki:

```sh
bash tools/SPRAWDZ_M300_SD_I4.command --card "/Volumes/M300" --route upgrade
# dla FACTORY: --route factory
```

Wynik `PASS_SD_I4_CARD_FILES` potwierdza nazwy/rozmiary/hashes, nie fizyczne klastry FAT ani zgodność płyty. Przed wgrywaniem wymagany jest też lokalny `check_backup_profile.py` na własnych kopiach.

## 3A. FACTORY — wejście przez OEM v3

1. Przy wyłączonej drukarce włóż kartę FACTORY, włącz i pozwól OEM zakończyć aktualizację aplikacji. Może zacząć się automatycznie; nie wkładaj karty „tylko żeby sprawdzić”. Nie przerywaj zapisu.
2. Po rzeczywistym zakończeniu wyłącz drukarkę, wyjmij kartę i uruchom bez niej. Powinno pojawić się **M300 SD installer 1.1-i4**.
3. Gdy pośrednik jest w menu i niczego nie zapisuje, włóż tę samą kartę FACTORY. Dalej punkt 4.

To instaluje tylko pośrednik w slocie aplikacji. OEM nadal istnieje do osobnej operacji podmiany. Oryginalna aplikacja jest już zastąpiona, dlatego nie nazywaj późniejszej kopii nienaruszonym obrazem stock.

## 3B. UPGRADE — wejście przez własny M300Boot

1. Włóż kartę UPGRADE przy wyłączonej drukarce. Włącz i przerwij pięciosekundowy autostart pokrętłem.
2. `Firmware on SD → Choose firmware file → M300APP.M3B`.
3. `Check selected file`, potem po sukcesie `Install selected file`. **Na prośbę** puść pokrętło, naciśnij i trzymaj **2 sekundy**. Nie trzymaj go podczas wcześniejszych kontroli.
4. Po zapisie: `Diagnostics → Verify Flash`, potem `Start application → Launch application`, z osobnym 2-sekundowym potwierdzeniem.
5. Uruchomi się i4. **Kartę UPGRADE pozostaw w czytniku.**

Nie wybieraj automatycznego pakietu: na karcie są instalator i RESTORE. Pośrednik ma wersję 1.1-i4; jego nagłówek v1.1 nie oznacza jeszcze podmiany stałego bootloadera.

## 4. Pośrednik — check, dwie kopie, osobna zgoda

### Check board + SD

Wybierz i kliknij. Oczekuj `CHECK_SOURCE_CARD_RESTORE_OK` / poprawnego zakończenia. Sprawdzane są kod, tożsamość, RESTORE i rozdzielność sześciu łańcuchów FAT. Błąd zatrzymuje procedurę; nie zmieniaj zabezpieczeń.

### Backup Flash x2

Wybierz i poczekaj na oba odczyty, zapis, readback i SHA-256. Nie wyjmuj karty. Oczekiwane `PASS_SD_FULL_FLASH_X2`. Po zakończeniu wróć nowym kliknięciem do menu. **Nie resetuj instalatora pomiędzy Backup a Install** — autoryzacja jest powiązana z bieżącą sesją. Po restarcie trzeba ponownie wykonać/zweryfikować Backup; samo Check nie wystarcza.

### Install / upgrade boot

Poczekaj na koniec `Checking / Verifying`. Przy identycznym docelowym v1.1 instalator pomija programowanie. Dla rc3 → v1.1 nastąpi rzeczywisty zapis po zgodzie.

Pokrętło **nie ma być cały czas wciśnięte**. Gest jest następujący:

| Ekran | Czynność |
|---|---|
| `1 Release knob` | Niczego nie naciskaj; gdy już puszczone, po prostu czekaj |
| `2 Click knob once` | Naciśnij |
| `3 Release after click` | Puść po kliku |
| `4 Press and hold 5s` | Naciśnij ponownie |
| `5 Keep holding knob` | Trzymaj do ukończenia gestu; obrót anuluje |

Po `CONFIRM_OK CONFIRMED_5S` program ponownie sprawdza kopie i chronione obszary. Podczas `WRITING_FIXED_BOOT_PAGES` **nie resetuj, nie wyjmuj karty ani nie odłączaj zasilania**, chyba że występuje zagrożenie. Programuje tylko strony 2–15 i 116–121; pierwsze 4 KiB, aplikacja, metadane, dziennik UART i końcowe 8 KiB danych są poza tą transakcją. Oczekiwany wynik: `INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED`.

**Nie ma automatycznego rollbacku po przerwaniu zasilania.** Zachowany prefix OEM nie jest pełnym, niezależnym mechanizmem odzyskiwania. `Recover saved boot` może działać tylko w nadal żywej sesji pośrednika z poprawnymi kopiami.

### Restart to boot

Wybierz po poprawnym zakończeniu/pominięciu identycznego celu. Przy starcie przytrzymaj pokrętło, aby zatrzymać autostart, i puść po pojawieniu się menu M300 boot v1.1. Nie pozwól ponownie automatycznie wejść do pośrednika.

## 5. Przywrócenie 1.3.1

W bootloaderze, z tą samą kartą, wybierz ręcznie **RESTORE.BIN**, nie M300APP.M3B:

`Firmware on SD → Choose firmware file → RESTORE.BIN → Check selected file → Install selected file`.

Potwierdź na prośbę **2-sekundowym przytrzymaniem**. Po zapisie i readback: `Diagnostics → Verify Flash`, potem `Start application → Launch application` i osobne potwierdzenie. Sprawdź oryginalne menu, firmware 1.3.1, hardware, własny serial i zachowany bieżący czas. Pierwszy start nie jest jeszcze pełnym testem drukowania — nie zaczynaj od długiego wydruku bez kontroli stanu urządzenia.

RESTORE nie przywraca starych danych NVM z archiwum. Instalator nie zeruje licznika; stock po starcie może dalej normalnie zapisywać swój licznik i ustawienia.

## 6. Zachowanie kopii i błędy

Po zakończeniu, przy wyłączonej drukarce, skopiuj cztery realne pliki backupu do nowego prywatnego folderu. Sprawdź:

```sh
bash tools/SPRAWDZ_M300_SD_I4.command --backups "$HOME/Desktop/M300_KOPIE_SD"
```

Oczekiwany wynik: `PASS_SD_I4_BACKUPS_X2`. Nie zastępuj kopii plikami A5. Zachowaj drugi nośnik.

Przy `ERROR INSTALL ... OP ... PHASE ... REASON ...` zanotuj pełną treść. Nie uruchamiaj starego rc3 `--install` na i4, nie kopiuj starego 105-fix i nie usuwaj blokad. Przed zapisem błąd oznacza odmowę; po rozpoczęciu zapisu utrzymaj zasilanie, o ile nie ma zagrożenia, i postępuj według warunków odzyskiwania. Stara automatyczna karta OEM nie jest po migracji gwarantowaną ścieżką.
