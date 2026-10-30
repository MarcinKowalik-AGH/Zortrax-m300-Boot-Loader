# M300Boot v1.3.1 — 2026-10-30

## English

Independent service bootloader for **classic Zortrax M300, Rev.5.3 / HW05 / measured 256 KiB**. Permanent BOOT and OLED installer version: **1.3.1**. The owner confirmed **UPGRADE, FACTORY and ST-Link** on hardware, and an active **1500000-baud UART8** link. The qualified per-device gates remain.

- New visible rate sequence: **115200 → 250000 → 500000 → 750000 → 1000000 → 1500000**. Legacy 19200/57600 records remain readable; 2000000 is not supported.
- Persistent **UART on bootwait OFF/ON**. OFF ignores host RX during autostart; ON admits complete allowed diagnostic lines. Binary Klipper traffic does not stop the countdown.
- Corrected local baud-change busy handling, partial-line cleanup and settings-screen isolation from host probes. Real operation/refusal guards remain.
- Incremental OLED updates, direct detent navigation, pinned Back and bounded scrolling retained and reviewed; progress reports measured phases.
- 1.3 → 1.3.1 preserves baud and bootwait journals, metadata and NVM. Empty journals default to 250000/OFF. Knob-at-start recovery is temporary 250000.
- Public UPGRADE, FACTORY and **two-segment STLINK** packages, updated public console/checkers, complete paired PL/EN manuals, checksums and native renderer previews. Historical v1.1 assets/tags are unchanged.

**SD migration replaces APP with the intermediary first; restore `RESTORE.BIN` or your matching MCU M3B afterwards. ST-Link preserves APP.** The standalone Klipper waiting screen belongs to the separate MCU APP; this publication is bootloader-only. 2941 boot/installer tests were re-run successfully; public package checks are in the publication validation report. No power-loss rollback or general print qualification is claimed.

## Polski

Bootloader serwisowy dla **klasycznej Zortrax M300, Rev.5.3 / HW05 / zmierzone 256 KiB**. Wersja stałego BOOT i instalatora na OLED: **1.3.1**. Właściciel potwierdził sprzętowo **UPGRADE, FACTORY i ST-Link** oraz działające połączenie UART8 **1500000 baud**. Zachowano blokady konkretnego profilu.

- Menu baud: **115200 → 250000 → 500000 → 750000 → 1000000 → 1500000**; stare zapisy 19200/57600 pozostają czytelne. Bez 2000000.
- Trwałe **UART on bootwait OFF/ON**. OFF odrzuca odbiór hosta w odliczaniu, ON wpuszcza pełne dozwolone polecenia diagnostyczne. Binarny ruch Klippera nie przerywa autostartu.
- Poprawione fałszywe busy zmiany baud, usuwanie części komend i ochrona lokalnego menu przed ruchem hosta; rzeczywiste blokady pozostają.
- Częściowe aktualizacje OLED, bezpośrednie kroki enkodera, przypięty Back, przewijanie bez zawijania i postęp bieżącej fazy.
- Migracja 1.3 → 1.3.1 zachowuje dzienniki baud/bootwait, metadane i NVM. Puste ustawienia: 250000/OFF. Trzymanie pokrętła przy starcie wymusza 250000 tylko chwilowo.
- Paczki publiczne UPGRADE, FACTORY i **STLINK z dwoma segmentami**, aktualna konsola/kontrolery, pełne instrukcje EN/PL, sumy i podglądy rzeczywistego renderera. Historyczne v1.1 i tag pozostają bez zmian.

**Migracja SD najpierw zastępuje APP pośrednikiem; potem przywróć `RESTORE.BIN` lub zgodny MCU M3B. ST-Link zachowuje APP.** Ekran oczekiwania Klippera należy do osobnej aplikacji MCU. Ponownie wykonano 2941 poprawnych testów BOOT/instalatora. Wyniki kontroli publikacji są w raporcie walidacji. Nie deklarujemy automatycznego rollbacku ani kwalifikacji druku.

[Installation EN](INSTALLATION_EN.md) · [Instalacja PL](INSTALACJA_PL.md) · [Manifest](RELEASE_MANIFEST.md)
