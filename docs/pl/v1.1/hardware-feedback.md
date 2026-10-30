# Zgłoszenia sprzętowe właściciela — M300Boot v1.1

[English](../../en/v1.1/hardware-feedback.md) · [Polski](../../pl/v1.1/hardware-feedback.md) · [Indeks](README.md)

**Archiwalny zapis v1.1 z 29 października 2026.** Poniższe ustalenia zachowują historyczny zakres. [Bieżąca v1.3.1](../v1.3.1/README.md).

**Data zgłoszenia: 29 października 2026.** Boot v1.1, pośrednik 1.1-i4. Źródłem są wypowiedzi właściciela w projekcie, nie niezależna inspekcja logów drugiej drukarki.

| Egzemplarz | Droga | Zgłoszony wynik | Zakres dowodów |
|---|---|---|---|
| A | UPGRADE z M300Boot | Zakończona instalacja i4, odtworzenie oryginalnego 1.3.1 i poprawny start | Klasyczna M300, Rev.5.3/HW05, zmierzone 256 KiB, ID 0x414; potwierdzenie właściciela i wcześniejsze logi UART/readback/zdjęcie |
| B | FACTORY z oryginalnego boota | Właściciel jednoznacznie zgłosił, że działa na drugiej drukarce | Nie przekazano PCB/HW/Flash/wersji oryginału ani szczegółowych punktów zakończenia; zapisano zgłoszenie bez dopisywania etapów |
| Dowolny | ST-Link/SWD v1.1 | W tym datowanym raporcie brak osobnego potwierdzenia sprzętowego | Sprawdzony generator obrazu offline, nie fizyczne programowanie |

## Zgodność profilu

Opublikowany i4 ma stałe kontrole UID/Option Bytes/strony fabrycznej powiązane z zakwalifikowanym egzemplarzem. Zgłoszenie FACTORY na B było nowym dowodem wymagającym ustalenia, czy ukończono tylko wgranie `Update.bin` do APP, czy również osobną wymianę stałego BOOT. Nie przypisywano zgłoszeniu nieudokumentowanych etapów.

Zgłoszenie właściciela przyjęto bez osłabiania, ale nie uogólniono na wszystkie M300 ani zgodę na zdjęcie blokad. Nie przenoś cudzych UID/NVM i nie zmieniaj RDP/WRP w celu obejścia odmowy.

## Możliwe dodatkowe potwierdzenie bez ponownego flashowania

Można zachować zanonimizowane dane sprzętu i zapisane etapy: `PASS_SD_FULL_FLASH_X2`, `INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED`, nagłówek v1.1 i start oryginału. To przykłady dowodów, nie twierdzenie, że wszystkie zostały wtedy dostarczone. Nie ma potrzeby powtarzania udanej instalacji tylko dla logu.

Raport zmieniał opis na `main`, bez wymiany tagu, ZIP-ów, sum ani firmware v1.1. Wcześniejszych datowanych raportów audytu nie przepisano wstecz. Późniejsze potwierdzenia FACTORY i ST-Link dla bieżącego v1.3.1 znajdują się w [aktualnej macierzy](../v1.3.1/tested-hardware.md).
