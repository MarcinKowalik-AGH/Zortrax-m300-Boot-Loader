# M300Boot v1.3.1 — dokumentacja / documentation

**BOOT: 1.3.1 · SD installer: 1.3.1 · 30 October 2026.**
Classic M300, PCB Rev.5.3 / HW05, measured 256 KiB. The published installer retains its single-device profile checks.

| Temat / Topic | Polski | English |
|---|---|---|
| Instalacja i aktualizacja SD | [Instalacja](INSTALACJA_PL.md) | [Installation](INSTALLATION_EN.md) |
| Kopia oryginalnej pamięci | [Kopia oryginału](KOPIA_ORYGINALU_PL.md) | [Original backup](ORIGINAL_BACKUP_EN.md) |
| Menu, funkcje i nowe ustawienia | [Funkcje i konsola](FUNKCJE_I_KONSOLA_PL.md) | [Features and console](FEATURES_AND_CONSOLE_EN.md) |
| UART i przykłady poleceń | [Przykłady UART](KONSOLA_UART_PRZYKLADY_PL.md) | [UART examples](UART_EXAMPLES_EN.md) |
| ST-Link i odzyskiwanie | [ST-Link](STLINK_I_ODZYSKIWANIE_PL.md) | [ST-Link](STLINK_AND_RECOVERY_EN.md) |
| Rozwiązywanie problemów | [Diagnostyka](DIAGNOSTYKA_PL.md) | [Troubleshooting](TROUBLESHOOTING_EN.md) |
| Sprzęt i zakres testów | [Macierz PL/EN](TESTED_HARDWARE.md) | [PL/EN matrix](TESTED_HARDWARE.md) |
| Pliki i sumy kontrolne | [Manifest PL/EN](RELEASE_MANIFEST.md) | [PL/EN manifest](RELEASE_MANIFEST.md) |

[Zmiany / Release notes](RELEASE_NOTES.md) · [Firmware v1.3.1](../../firmware/v1.3.1) · [Wszystkie wersje / All versions](../README.md) · [Projekt / Project](../../README.md)

BOOT and application versions are separate. Stock Zortrax **1.3.1** and **M300Boot 1.3.1** happen to share a number. MCU Klipper UART8/OLED firmware and Orange Pi modules are a separate project/package; they are not included in this bootloader publication.

Wersje BOOT i aplikacji są niezależne. Ten zestaw aktualizuje bootloader; instalator SD tymczasowo zastępuje aplikację. Po migracji przywróć `RESTORE.BIN` lub swoją zgodną aplikację M3B. Nie uruchamiaj ponownie pośrednika zamiast właściwej aplikacji.
