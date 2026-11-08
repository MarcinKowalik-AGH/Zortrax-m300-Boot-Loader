# M300Boot 1.4 — dokumentacja

[English](../../en/v1.4/README.md) · [Polski](../../pl/v1.4/README.md) · [Index](README.md)

**Bieżące wydanie: 1.4.**

M300Boot **1.4** jest przeznaczony dla zakwalifikowanego profilu klasycznej M300 HW05 / PCB Rev.5.3 / zmierzone 256 KiB Flash. BOOT, instalator SD, aplikacja oryginalna i aplikacja MCU Klippera pełnią odrębne role. Wydanie 1.4 jest sprawdzane programowo; przebudowany firmware wymaga potwierdzenia na drukarce. Wcześniejsze próby sprzętowe dotyczą archiwalnej wersji 1.3.1.

- [Instalacja SD i kolejność wgrywania](installation.md)
- [Oryginalna pamięć i niezależne kopie](original-backup.md)
- [Menu, funkcje i konsola](features-and-console.md)
- [UART i przekazanie ustawień aplikacji](uart-examples.md)
- [Instalacja ST-Link i odzyskiwanie](stlink-and-recovery.md)
- [Rozwiązywanie problemów](troubleshooting.md)
- [Zakres sprzętowy i odbiór](tested-hardware.md)
- [Walidacja i dowody wydania](validation.md)
- [Pliki wydania i sumy kontrolne](release-manifest.md)
- [Zmiany wydania](release-notes.md)

Dokładnie pięć prędkości UART: **115200, 250000, 500000, 750000, 1500000**. Domyślnie **250000 / bootwait OFF**. Zacznij od kopii, wybierz drogę instalacji, zakończ zapis BOOT, a następnie jawnie przywróć docelową aplikację APP. Starsze wydania zachowano jako archiwum.

[Wszystkie wersje](../README.md) · [Projekt](../../../README_PL.md)
