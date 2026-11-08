# Zmiany wydania — M300Boot 1.4

[English](../../en/v1.4/release-notes.md) · [Polski](../../pl/v1.4/release-notes.md) · [Index](README.md)

BOOT i instalator pośredni spójnie identyfikują się jako **1.4**, bez dopisków rozwojowych. Aktywny zestaw UART/menu to dokładnie **115200,250000,500000,750000,1500000**; domyślnie 250000 i bootwait OFF. Obsługiwane rekordy zachowują pierwotne kody. Usunięte prędkości dają 250000 bez domyślnego zapisu dziennika; przed starszą APP odczytującą dawny rekord jawnie zapisz 250000.

Aktualizacja zachowuje ochronę prefiksu/NVM, kontrole źródła i urządzenia, dwie zweryfikowane kopie, niezależną zgodę na BOOT, kolejność przywrócenia APP i adresy dwóch segmentów ST-Link. Razem zaktualizowano narzędzia hosta, kod osadzony w launcherze, walidatory paczek i manifesty. Zobacz [instalację](installation.md) i [migrację UART](uart-examples.md).

Dokumentacja obejmuje pełne pary EN/PL z krokami SD i ST-Link. Natywne rendery OLED obrazują BOOT, instalator, UART oraz postęp pikselami cyan. Są wygenerowanymi ekranami, a nie zdjęciami ani nowym dowodem odbioru sprzętowego.

Firmware 1.4 jest przebudowany i sprawdzany programowo. [Dowody walidacji](validation.md) opisują kontrole; odbiór fizyczny 1.4 pozostaje do wykonania. Wcześniejsze obserwacje sprzętowe1.3.1 i niezmienione pliki zachowano w [archiwum](../v1.3.1/README.md). RESTORE.BIN nadal zawiera oryginalny Zortrax 1.3.1, a diagnostyka 0.5.5 zachowuje niezależny numer.
