# Przetestowany sprzęt — M300Boot v1.1

[English](../../en/v1.1/tested-hardware.md) · [Polski](../../pl/v1.1/tested-hardware.md) · [Indeks](README.md)

**Archiwalny zapis v1.1 z 29 października 2026.** Poniższe ustalenia zachowują historyczny zakres. [Bieżąca v1.3.1](../v1.3.1/README.md).

Wydanie v1.1, instalator 1.1-i4. Poniższe informacje opisują stan dowodów z 29 października 2026.

| Parametr | Ustalenie |
|---|---|
| Drukarka | Klasyczna Zortrax M300, bez Plus, Dual i generacji Android/LCD |
| Nadruk płyty | Rev.5.3, potwierdzony zdjęciami |
| Wersja sprzętu | 05; rekord fabryczny E5 dekodowany przez oryginalny firmware |
| MCU | STM32F101/F103 high-density według ST-Link; cel Cortex-M3 rodziny F103; dokładny pełny symbol układu nieustalony |
| Identyfikator krzemu | Device ID 0x414 / Rev X; CPUID 0x411FC231 |
| Flash | Dwa zgodne 16-bitowe odczyty SIZE z 0x1FFFF7E0: 256 KiB, 262144 B; potwierdzenie w SYSROM |
| Dawna etykieta 512 KB | Opis GUI CubeProgrammer i 512_PRIOR_SWD nie były poprawnym pomiarem pojemności |
| Geometria | 128 stron po 2048 B, 0x08000000–0x0803FFFF |
| Oryginalny boot | Zortrax Bootloader v3, odzyskany i porównany |
| Oryginalna aplikacja | 1.3.1; właściciel sprawdził też 1.3.1 → 1.2.0 → 1.3.1 |
| Ochrona podczas migracji | RDP aktywne, dodatkowe WRP nieaktywne; instalator nie zmieniał opcji |
| OLED i wejście | Potwierdzony czytelny ekran, oba kierunki enkodera, klik, Back, ograniczone przewijanie i płynne renderowanie wywodzące się z rc3 |
| Komputer i programator | MacBook Air/macOS; Python 3.9/3.11, pySerial 3.5; CubeProgrammer 2.23.0; STLINK-V3SET do SWD i później VCP/UART 250000 8N1 |
| Scharakteryzowane egzemplarze | Jeden, A, z pełną dokumentacją płyty/Flash/firmware |
| Dodatkowy egzemplarz | Drugi, B; właściciel zgłosił działające FACTORY, bez danych płyty i szczegółowych etapów |

## Potwierdzone wtedy

- Odczyt wewnętrznej Flash przy aktywnym RDP: dwie zgodne pełne kopie 256 KiB oraz oddzielne kopie tożsamości/opcji.
- Uruchomienie rc3 FULL i odtworzenie dokładnej aplikacji 1.3.1 przez UART; start oryginalnego interfejsu.
- Procedura i2 na identycznym rc3, ze ścieżką bez ponownego zapisu i zgłoszonym odtworzeniem aplikacji.
- UPGRADE i4 do v1.1 i start oryginalnego 1.3.1 na A.
- Zgłoszenie właściciela: FACTORY działa na B; bez niezależnego odtworzenia etapów wymiany stałego BOOT.

## Zakres nieustalony w tym raporcie

Brakowało szczegółowego logu i charakterystyki drugiego urządzenia oraz osobnej próby fizycznego ST-Link v1.1. Nie kwalifikowano zaniku zasilania, automatycznego rollbacku, wszystkich menu/baud/restartów, druku/grzałek/silników ani innych płyt. [Datowane zgłoszenie sprzętowe](hardware-feedback.md).

## Znaczenie blokady profilu

Binaria i4 porównują prefix OEM, hashe kodu źródłowego, UID, Option Bytes i stronę fabryczną. Dwie M300/HW05 mogą nie mieć zgodnego profilu. Zgłoszenie FACTORY na B wymagało wtedy rozróżnienia wgrania pośrednika od zweryfikowanej wymiany stałego BOOT. Brak trybu FORCE.

Kontroler `check_backup_profile.py` sprawdza prywatne zgodne pary. `BACKUP_VALID_BUT_INSTALL_PROFILE_MISMATCH` nie oznacza uszkodzonej kopii, lecz odmowę użycia tego instalatora. Nie zmieniaj hashy, nie przenoś tożsamości/NVM ani nie usuwaj RDP, aby obejść blokadę. Samo wgranie pośrednika już zastępuje aplikację.
