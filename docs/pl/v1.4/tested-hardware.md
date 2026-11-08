# Sprzęt i odbiór — M300Boot 1.4

[English](../../en/v1.4/tested-hardware.md) · [Polski](../../pl/v1.4/tested-hardware.md) · [Index](README.md)

M300Boot **1.4** jest przeznaczony dla zakwalifikowanego profilu klasycznej M300 HW05 / PCB Rev.5.3 / zmierzone 256 KiB Flash. BOOT, instalator SD, aplikacja oryginalna i aplikacja MCU Klippera pełnią odrębne role. Wydanie 1.4 jest sprawdzane programowo, a właściciel potwierdził na drukarce instalację FACTORY, UPGRADE i ST-Link; zgłoszenie zapisano 09.11.2026. [Odbiór właściciela](../../reports/v1.4/HARDWARE_ACCEPTANCE.json) jest osobny od dawnych raportów archiwalnej 1.3.1.

Udostępnione instalatory zachowują kwalifikację konkretnego egzemplarza według UID, prefiksu OEM i danych fabrycznych. Sama zgodność modelu M300, HW05 lub PCB Rev.5.3 nie kwalifikuje innej drukarki; odmowę profilu trzeba wyjaśnić na podstawie jej własnej zweryfikowanej kopii, bez omijania kontroli.

## Sprzęt i chroniona pamięć

| Element | Zakres |
|---|---|
| Drukarka | Klasyczna M300 HW05 / PCB Rev.5.3 |
| MCU / pamięć | Rodzina STM32F103; zmierzone 256 KiB Flash, strony 2 KiB |
| Ekran | Natywny OLED 256×64 i enkoder z przyciskiem |
| Profil instalacji | Zachowane kontrole urządzenia/UID/opcji/danych fabrycznych |
| Zachowane obszary | Prefiks OEM 0x08000000–0x08000FFF; APP przy ST-Link; ustawienia i NVM producenta poza dwoma obszarami docelowymi |

## Dowody i odbiór sprzętowy

Przebudowa i kontrole paczek 1.4 są programowe. Osobno właściciel zgłosił walidację na drukarce wszystkich trzech metod instalacji; zapisano ją w [HARDWARE_ACCEPTANCE.json](../../reports/v1.4/HARDWARE_ACCEPTANCE.json).

| Metoda instalacji 1.4 | Wynik sprzętowy | Dowód |
|---|---|---|
| FACTORY OEMv3 | Potwierdzona przez właściciela | Zgłoszenie zapisane 09.11.2026 |
| UPGRADE | Potwierdzona przez właściciela | Zgłoszenie zapisane 09.11.2026 |
| ST-Link | Potwierdzona przez właściciela | Zgłoszenie zapisane 09.11.2026 |

Zgłoszenie potwierdza trzy drogi instalacji. Nie zgłoszono osobno testów każdej prędkości UART, ruchów, grzania, drukowania ani przywrócenia oryginalnego BOOT OEM. Niezmienny manifest wydania i pierwotne raporty programowe zachowują status z chwili publikacji; późniejsze zgłoszenie właściciela uzupełnia wynik sprzętowy. Dawne dowody 1.3.1 pozostają w [archiwum](../v1.3.1/tested-hardware.md).

Przy kolejnym odbiorze sprzętu zapisz wykorzystaną drogę instalacji, oznaczenie 1.4 BOOT i instalatora, pięć pozycji UART, domyślne 250000/bootwait OFF, zachowanie obsługiwanych zapisów, jawną migrację usuniętych prędkości, restart i poprawne przywrócenie APP. Porównaj rzeczywiste ekrany z ilustracjami cyan, które są renderami, a nie fotografiami. Próba UART musi obejmować oba kierunki i status po restarcie. Udany start nie kwalifikuje innej PCB, niezgłoszonego MCU ani całego zachowania ruchów, grzania i drukowania.

Zachowaj prywatnie surową tożsamość, logi oraz własne zrzuty Flash. Publikuj wynik odbioru i obserwacje bez danych identyfikujących.
