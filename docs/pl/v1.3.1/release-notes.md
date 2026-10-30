# M300Boot v1.3.1 — 2026-10-30

[English](../../en/v1.3.1/release-notes.md) · [Polski](../../pl/v1.3.1/release-notes.md) · [Indeks](README.md)

Bootloader serwisowy dla **klasycznej Zortrax M300, Rev.5.3 / HW05 / zmierzone 256 KiB**. Wersja stałego BOOT i instalatora na OLED: **1.3.1**. Właściciel potwierdził sprzętowo **UPGRADE, FACTORY i ST-Link** oraz działające połączenie UART8 **1500000 baud**. Zachowano blokady konkretnego profilu.

- Menu baud: **115200 → 250000 → 500000 → 750000 → 1000000 → 1500000**; stare zapisy 19200/57600 pozostają czytelne. Bez 2000000.
- Trwałe **UART on bootwait OFF/ON**. OFF odrzuca odbiór hosta w odliczaniu, ON wpuszcza pełne dozwolone polecenia diagnostyczne. Binarny ruch Klippera nie przerywa autostartu.
- Poprawione fałszywe busy zmiany baud, usuwanie części komend i ochrona lokalnego menu przed ruchem hosta; rzeczywiste blokady pozostają.
- Częściowe aktualizacje OLED, bezpośrednie kroki enkodera, przypięty Back, przewijanie bez zawijania i postęp bieżącej fazy.
- Migracja 1.3 → 1.3.1 zachowuje dzienniki baud/bootwait, metadane i NVM. Puste ustawienia: 250000/OFF. Trzymanie pokrętła przy starcie wymusza 250000 tylko chwilowo.
- Paczki publiczne UPGRADE, FACTORY i **STLINK z dwoma segmentami**, aktualna konsola/kontrolery, pełne instrukcje EN/PL, sumy i podglądy rzeczywistego renderera. Historyczne v1.1 i tag pozostają bez zmian.

**Migracja SD najpierw zastępuje APP pośrednikiem; potem przywróć `RESTORE.BIN` lub zgodny MCU M3B. ST-Link zachowuje APP.** Ekran oczekiwania Klippera należy do osobnej aplikacji MCU. Ponownie wykonano 2941 poprawnych testów BOOT/instalatora. Wyniki kontroli publikacji są w raporcie walidacji. Nie deklarujemy automatycznego rollbacku ani kwalifikacji druku.

[Installation EN](../../en/v1.3.1/installation.md) · [Instalacja PL](installation.md) · [Manifest](release-manifest.md)
