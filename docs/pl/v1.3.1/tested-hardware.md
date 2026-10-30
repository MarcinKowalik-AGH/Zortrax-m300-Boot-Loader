# Sprzęt i potwierdzenia — M300Boot v1.3.1

[English](../../en/v1.3.1/tested-hardware.md) · [Polski](../../pl/v1.3.1/tested-hardware.md) · [Indeks](README.md)

**Data raportu: 30 października 2026.**

| Parametr | Potwierdzone ustalenie |
|---|---|
| Drukarka | Klasyczna Zortrax M300, PCB Rev.5.3 / HW05 |
| MCU | STM32F103, rodzina Cortex-M3 high-density; pełny symbol układu nieustalony |
| Krzem / CPUID | Device ID 0x414 / Rev X; CPUID 0x411FC231 |
| Flash | Zmierzone 256 KiB / 262144 B, 128 stron po 2048 B; dawny opis 512 KB w GUI nie był poprawnym pomiarem |
| Oryginalny BOOT / APP | OEM v3 / Zortrax M300 1.3.1; niezależne numery wersji |
| Wyświetlacz / wejście | Natywny OLED 256×64 i enkoder z przyciskiem |
| Potwierdzone połączenie hosta | Orange Pi Zero UART1, zgłoszony zegar UART 24 MHz; `/dev/ttyS1` w zestawie właściciela |
| Zgłoszona zgodna aplikacja | UART8, później `0.13.3-TEST01-OLED-R32-UART8`; host OLED-R3.2 |
| Blokada instalacji | Zachowane hashe UID/opcji/strony fabrycznej konkretnego egzemplarza; samo HW05 nie wystarcza |

## Macierz prób

| Droga lub funkcja | Status | Podstawa |
|---|---|---|
| UPGRADE do v1.3.1 | **Potwierdzone sprzętowo** | Zgłoszenia działającego boota i MCU właściciela |
| FACTORY | **Potwierdzone sprzętowo** | Jednoznaczne potwierdzenie właściciela 30 października 2026 |
| ST-Link | **Potwierdzone sprzętowo** | Jednoznaczne potwierdzenie właściciela 30 października 2026 |
| UART 1500000, zapisany indeks 7 | **Potwierdzone** | MCU i host 1500000, match true, saved 1, index 7, fault 0 |
| Samodzielny ekran oczekiwania i transmisja OLED | **Zaakceptowane** | Właściciel zamknął ten etap po testach UART8/OLED-R3.2 |
| Oprogramowanie BOOT / instalatora | **2941 testów PASS** | Ponownie wykonane 2116 testów BOOT i 825 instalatora/ST-Link/migracji |

FACTORY i ST-Link potwierdził właściciel na sprzęcie. To zastępuje wcześniejszy status niepotwierdzony bieżącego wydania. [Historyczne ustalenia v1.1](../v1.1/tested-hardware.md) zachowują datę i pierwotny zakres.

Nie publikujemy numerów seryjnych, UID, prywatnych logów ani nieustalonych parametrów drugiej płyty. Potwierdzenia nie obejmują wszystkich M300, odzyskania po zaniku zasilania, wszystkich kombinacji baud/restart, kwalifikacji ruchu/grzania ani zapasu podczas druku. Blokady tożsamości pozostają zachowane.
