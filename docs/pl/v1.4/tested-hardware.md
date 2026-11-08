# Sprzęt i odbiór — M300Boot 1.4

[English](../../en/v1.4/tested-hardware.md) · [Polski](../../pl/v1.4/tested-hardware.md) · [Index](README.md)

M300Boot **1.4** jest przeznaczony dla zakwalifikowanego profilu klasycznej M300 HW05 / PCB Rev.5.3 / zmierzone 256 KiB Flash. BOOT, instalator SD, aplikacja oryginalna i aplikacja MCU Klippera pełnią odrębne role. Wydanie 1.4 jest sprawdzane programowo; przebudowany firmware wymaga potwierdzenia na drukarce. Wcześniejsze próby sprzętowe dotyczą archiwalnej wersji 1.3.1.

## Sprzęt i chroniona pamięć

| Element | Zakres |
|---|---|
| Drukarka | Klasyczna M300 HW05 / PCB Rev.5.3 |
| MCU / pamięć | Rodzina STM32F103; zmierzone 256 KiB Flash, strony 2 KiB |
| Ekran | Natywny OLED 256×64 i enkoder z przyciskiem |
| Profil instalacji | Zachowane kontrole urządzenia/UID/opcji/danych fabrycznych |
| Zachowane obszary | Prefiks OEM 0x08000000–0x08000FFF; APP przy ST-Link; ustawienia i NVM producenta poza dwoma obszarami docelowymi |

## Dowody i odbiór sprzętowy

Przebudowa i kontrole paczek 1.4 są programowe. [Walidacja](validation.md) wskazuje bieżący raport maszynowy. Potwierdzenia fizyczne FACTORY/UPGRADE/ST-Link oraz UART1500000 dla 1.3.1 pozostają w [archiwum](../v1.3.1/tested-hardware.md); nie zmieniono ich na wyniki sprzętowe 1.4.

Na zakwalifikowanej drukarce osobno potwierdź wykorzystaną drogę instalacji, oznaczenie 1.4 BOOT i instalatora, pięć pozycji UART, domyślne 250000/bootwait OFF, zachowanie obsługiwanych zapisów, jawną migrację usuniętych prędkości, restart i poprawne przywrócenie APP. Porównaj rzeczywiste ekrany z ilustracjami cyan, które są renderami, a nie fotografiami. Próba UART musi obejmować oba kierunki i status po restarcie. Udany start nie kwalifikuje innej PCB, niezgłoszonego MCU ani całego zachowania ruchów, grzania i drukowania.

Zachowaj prywatnie surową tożsamość, logi oraz własne zrzuty Flash. Publikuj wynik odbioru i obserwacje bez danych identyfikujących.
