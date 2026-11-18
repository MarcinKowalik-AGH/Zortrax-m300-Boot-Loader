# Sprzęt i zakres potwierdzeń — M300Boot 1.5

[English](../../en/v1.5/tested-hardware.md) · [Polski](../../pl/v1.5/tested-hardware.md) · [Indeks](README.md)

Wydanie dotyczy **klasycznej Zortrax M300** z zakwalifikowanym profilem HW05 / PCB Rev.5.3 / zmierzone 256 KiB Flash. Sama zgodność nazwy modelu lub oznaczenia płyty nie zastępuje kontroli UID, opcji, prefiksu OEM i danych fabrycznych. Odmowę profilu wyjaśnij na podstawie własnych kopii; nie usuwaj kontroli tożsamości.

## Sprzęt i zachowane obszary

| Element | Zakres |
|---|---|
| Drukarka | Klasyczna M300; Plus, Dual i Inventure to osobne cele |
| MCU / pamięć | Rodzina STM32F103; zmierzone 256 KiB Flash, strony 2 KiB |
| Interfejs lokalny | Natywny OLED 256×64 i enkoder z przyciskiem |
| Kwalifikacja instalacji | Zachowane kontrole urządzenia, UID, opcji i danych fabrycznych |
| Pierwsze 4 KiB | Prefiks OEM 0x08000000–0x08000FFF pozostaje zachowany |
| Zapis BOOT | Stage2 0x08001000–0x08007FFF; zasoby 0x0803A000–0x0803CFFF |
| Pozostała pamięć | ST-Link zachowuje APP; dzienniki ustawień i NVM producenta pozostają poza segmentami BOOT |

## Historia sprzętowa i nowa kompilacja

| Wersja / dowód | Potwierdzony zakres | Znaczenie dla 1.5 |
|---|---|---|
| 1.4 — odbiór właściciela zapisany 09.11.2026 | FACTORY, UPGRADE i ST-Link wykonane na drukarce | Dowód dla bazowej 1.4 |
| 1.4 — zgłoszenie właściciela 18.11.2026 | Około dwóch tygodni użytkowania/testowania | Okres zgłoszony przez właściciela, bez ustalania dokładnej daty rozpoczęcia i liczby godzin ciągłej pracy |
| 1.4.1 — poprzednie wydanie po audycie | Ponowienie APP i poprawki hosta zwalidowane programowo | Wcześniejsze dowody programowe; nie są odbiorem sprzętowym 1.5 |
| 1.5 — bieżący audyt | Przebudowane BOOT/instalator, oznaczenie OLED, narzędzia i paczki objęte bieżącymi kontrolami offline | Osobna walidacja nowego wydania; bez przypisywania mu historycznych dwóch tygodni |

[Bieżący status sprzętowy](../../reports/v1.5/HARDWARE_STATUS.json) · [Historyczny odbiór 1.4](../../reports/v1.4/HARDWARE_ACCEPTANCE.json) · [Raport audytu 1.5](../../reports/v1.5/AUDIT_2026-11-18.json).

Poprawka ponowienia APP wprowadzona w 1.4.1 pozostaje w 1.5. Kontrole komputerowe mogą odtwarzać przerwania i sprawdzać odmowy niezgodnych obrazów; nie stanowią wykonania rzeczywistego zaniku zasilania na drukarce. Przy sporządzaniu późniejszego odbioru 1.5 zapisz numer widoczny w BOOT i instalatorze, wybraną drogę, wynik przywrócenia APP oraz używane baud. Zachowaj własne logi i kopie prywatnie.

Dotychczasowe zgłoszenia nie są automatyczną kwalifikacją wszystkich płyt, wszystkich prędkości UART, ruchów/grzania/drukowania ani przywracania oryginalnego OEM BOOT. Nie ma automatycznego cofania BOOT po utracie zasilania. Zasady działania [naprawy APP](installation.md#ponowna-instalacja-app-po-przerwanym-zapisie-metadanych) są odrębne od [odzyskiwania BOOT](stlink-and-recovery.md).
