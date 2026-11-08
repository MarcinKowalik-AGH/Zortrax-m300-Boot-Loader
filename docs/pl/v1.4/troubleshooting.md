# Rozwiązywanie problemów — M300Boot 1.4

[English](../../en/v1.4/troubleshooting.md) · [Polski](../../pl/v1.4/troubleshooting.md) · [Index](README.md)

| Objaw | Postępowanie |
|---|---|
| Host pozornie przerywa odliczanie | Sprawdź BOOT 1.4 i bootwait OFF. Zdarzenie enkodera i blokada odzyskiwania niezależnie utrzymują serwis. |
| Po migracji wyświetlane UART 250000 | Usunięte zapisy 1000000/19200/57600 dają w BOOT 250000 bez przepisania rekordu. Przed starszą APP jawnie wybierz/zapisz 250000 i ustaw tak hosta. |
| Zapisano 1500000, aktywne chwilowo 250000 | Przytrzymanie pokrętła podczas włączania wymusza prędkość serwisową. Uruchom bez przytrzymania. Instalator SD także niezależnie korzysta z 250000. |
| Klipper nie łączy się | Osobno sprawdź aktywny baud BOOT, rekord, obsługę APP i baud hosta. Instalacja BOOT nie aktualizuje dowolnej APP. Zamknij inne programy korzystające z portu. |
| Ponownie startuje instalator SD | APP nadal zawiera program pośredni. Przez BOOT przywróć/sprawdź/zainstaluj/zweryfikuj docelową aplikację stock lub Klipper. |
| Odmowa źródła/profilu/karty | Zachowaj dokładny błąd. Sprawdź właściwe sześć plików, zakwalifikowany profil, zgodne kopie i kartę FAT. Nie omijaj kontroli tożsamości i zabezpieczeń. |
| Settings full | Zachowaj pełny zweryfikowany zrzut. Dzienniki są dopisywane, bez automatycznego kasowania. Wymagana jest osobna procedura serwisowa. |
| Busy lub timeout UART podczas zapisu | Zwolnij pokrętło, zakończ aktywną operację i ponów lokalny wybór po usunięciu przyczyny. Nie wymuszaj kasowania Flash. |
| ST-Link nie odczytuje przy RDP | Użyj drogi SD/diagnostycznej. Read Unprotect kasuje główny Flash; paczka segmentowa nie odtwarza całego skasowanego urządzenia. |
| Niezgodny odczyt po SWD | Zachowaj przed/po/UID/opcje i pozostaw rdzeń zatrzymany. Nie uruchamiaj, nie resetuj i nie wykonuj mass erase automatycznie. |

Tożsamość 1.4 musi być zgodna w stałym BOOT, instalatorze pośrednim i aktualnych narzędziach. Oryginalna aplikacja OEM pozostaje 1.3.1, a niezależna diagnostyka kopii 0.5.5. Te różne numery są prawidłowe i nie oznaczają pozostałości starej wersji bootloadera.

Brak samodzielnego ekranu oczekiwania diagnozuj w zainstalowanej APP MCU Klippera; paczka BOOT jej nie zawiera. Przy shutdown zachowaj pierwszy błąd Klippera oraz status UART/OLED, zamiast wnioskować z późniejszego ogólnego komunikatu. Walidacja programowa i czytelny ekran nie stanowią odbioru ruchów, grzania ani druku pod obciążeniem. Zobacz [walidację](validation.md), [UART](uart-examples.md) i [instalację](installation.md).
