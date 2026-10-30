# Sprzęt i potwierdzenia / Hardware and evidence — v1.3.1

**30 October 2026.** [PL/EN index](README.md) · [Historical v1.1 evidence](../v1.1/TESTED_HARDWARE.md).

| Parametr / Parameter | Ustalenie / Evidence |
|---|---|
| Drukarka / Printer | Classic Zortrax M300, PCB Rev.5.3 / HW05 |
| MCU | STM32F103-family Cortex-M3, high-density; exact ordering code not established / pełny symbol nieustalony |
| Silicon / CPUID | Device ID 0x414 / Rev X; CPUID 0x411FC231 |
| Flash | Measured 256 KiB / 262144 B; 128 × 2048-B pages. An old GUI label of 512 KB was not the accepted measurement. |
| Original BOOT / APP | OEM v3 / Zortrax M300 1.3.1; BOOT version and stock APP version are separate. |
| Display / Input | Native 256×64 OLED, rotary encoder / pokrętło z przyciskiem |
| Host in confirmed link | Orange Pi Zero / UART1, 24-MHz observed clock; /dev/ttyS1 in the user's setup |
| Compatible MCU reported | UART8; later `0.13.3-TEST01-OLED-R32-UART8`; host OLED-R3.2 |
| Compatibility gate / Blokada | Retained per-device UID/options/factory-page hashes; HW05 alone is insufficient / samo HW05 nie wystarcza. |

## Macierz prób / Test matrix

| Ścieżka/funkcja / Route/function | Status | Źródło / Basis |
|---|---|---|
| UPGRADE to M300Boot v1.3.1 | **Potwierdzone na sprzęcie / Hardware confirmed** | Owner's installed-boot and operating-MCU reports / zgłoszenia właściciela |
| FACTORY | **Potwierdzone na sprzęcie / Hardware confirmed** | Owner explicitly confirmed FACTORY tested on 30 October 2026. |
| ST-Link | **Potwierdzone na sprzęcie / Hardware confirmed** | Owner explicitly confirmed ST-Link tested on 30 October 2026. |
| UART 1500000 / saved index 7 | **Potwierdzone / Confirmed** | User status: MCU and host 1500000, match true, saved 1, index 7, fault 0. |
| Standalone waiting OLED and display link | **Zaakceptowane / Accepted** | Owner closed bootloader/display-transmission stage after UART8/OLED-R3.2 tests. |
| Boot and installer software | **2941 tests PASS** | Re-run of 2116 boot + 825 installer/ST-Link/migration tests during this publication. |

Potwierdzenie FACTORY i ST-Link jest bieżącym zgłoszeniem użytkownika, a nie założeniem na podstawie testów jednostkowych. Zastępuje wcześniejsze „niepotwierdzone” dla bieżącej wersji. Nie zmieniamy historycznych raportów v1.1. / The new owner confirmations supersede the earlier unconfirmed status for the current release; historical v1.1 evidence remains unchanged.

No new serial, UID, raw logs or second-board parameters are inferred or published. These confirmations do not establish every M300 board, power-interruption recovery, all baud/reboot combinations, motion/heating qualification or print-load headroom. The existing installer identity gates remain intact. / Nie rozszerzamy tych potwierdzeń na wszystkie płyty, zanik zasilania ani kwalifikację druku.
