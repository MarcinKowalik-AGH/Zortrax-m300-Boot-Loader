# M300Boot 1.5 — 2026-11-18

[English](#english) · [Polski](#polski)

## Downloads / Pobieranie

| Route / Wariant | Direct download / Bezpośrednie pobieranie | Starting state / Stan początkowy |
|---|---|---|
| FACTORY | [M300Boot_v1.5_SD_FACTORY_OEMV3.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_SD_FACTORY_OEMV3.zip) | Qualified original OEM v3 / zakwalifikowany oryginalny OEM v3 |
| UPGRADE | [M300Boot_v1.5_SD_UPGRADE.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_SD_UPGRADE.zip) | Recognized custom M300Boot / rozpoznany własny M300Boot |
| STLINK | [M300Boot_v1.5_STLINK.zip](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/releases/download/v1.5/M300Boot_v1.5_STLINK.zip) | Working SWD reads, RDP already off, valid APP / działający odczyt SWD, już wyłączone RDP, poprawna APP |

[SHA256SUMS.txt](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/raw/refs/tags/v1.5/firmware/v1.5/SHA256SUMS.txt) · [RELEASE_MANIFEST.json](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/raw/refs/tags/v1.5/firmware/v1.5/RELEASE_MANIFEST.json) · [English manual](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/en/v1.5/README.md) · [Polskie instrukcje](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/pl/v1.5/README.md)

## English

### Release and test status

Permanent BOOT and the SD intermediary are **1.5**. This release carries forward the audited fixes published as **1.4.1** and updates every active version identity: OLED startup `M300 boot v1.5`, About `Version v1.5`, installer `SD installer 1.5`, UART banners and `INSTALL V15`. The owner reports approximately **two weeks of using baseline 1.4**; acceptance of its FACTORY, UPGRADE and ST-Link routes was recorded on 2026-11-09. **The rebuilt 1.5 binaries have their own offline validation dated 2026-11-18; they have not undergone two weeks of printer testing.** No exact start date or continuous endurance hours are claimed. See [hardware status](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/reports/v1.5/HARDWARE_STATUS.json) and the [current audit report](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/reports/v1.5/AUDIT_2026-11-18.json) for evidence and actual results.

### Fixes and retained behavior

- **APP retry after interrupted metadata commit:** baseline 1.4 correctly refused to launch an uncommitted APP, but could also block reinstallation with `NO_COMMIT`. The guarded retry introduced in 1.4.1 is retained in BOOT 1.5: it is permitted only when the same verified candidate matches the recognized interrupted record and the complete APP already in Flash. Profile checks and a fresh physical 2-second confirmation remain mandatory. An incomplete commit still blocks launch; unrelated records, different candidates and damaged APP remain refused. See the [retry procedure and limitations](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/en/v1.5/installation.md#reinstalling-app-after-an-interrupted-metadata-write).
- **Build and space use:** BOOT and installer were rebuilt from source. The recovery checks use previously unused space between the vector table and fixed OEM hook. The hook, APP base and both programming-slot boundaries stay fixed; no UART throughput improvement is claimed.
- **Host tools:** service-card preparation checks every existing destination before creating missing files, refusing wrong sizes, directories and symlinks while preserving existing regular files of the expected size; their contents are not revalidated. The console cleans up partially opened serial/log resources after connection errors, requires exact expected version/board response lines, and retains the manifest/archive with a failure result when closing fails. Current tools and the `KONSOLA_M300_v1.5.command` launcher match this release; historical 1.4.1 and 1.4 tools remain archived.
- **UART:** exactly **115200, 250000, 500000, 750000, 1500000**, 8N1; default **250000**, bootwait **OFF**. **1000000 was already removed in 1.4** and remains unavailable; **10000000 is unsupported**. Supported saved codes are preserved. Removed saved rates fall back to active 250000 without automatic journal rewriting; explicitly save 250000 before starting an older APP that reads the old record, and match the host baud.
- **Publication:** complete EN/PL manuals, matching ST-Link package instructions, direct downloads, checksums and current C-rendered OLED illustrations. Renders use documented example inputs and are not hardware test records. [Complete menu and command reference](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/en/v1.5/features-and-console.md).

### Installation scope

The target remains the qualified **classic M300 HW05 / PCB Rev.5.3 / measured 256-KiB Flash** profile. UID, OEM-prefix, factory-data and source checks remain; matching the model alone does not qualify another device. BOOT replacement preserves the first 4 KiB, NVM and setting journals. ST-Link writes only the two BOOT/asset slots, preserves APP and requires complete readback. SD installation requires two verified session backups, separate BOOT confirmation and explicit restoration of the intended APP. The installer command is `INSTALL V15`.

The guarded retry is present in working BOOT **1.4.1 and 1.5**. An old 1.4 device already stuck in `NO_COMMIT` may reject the ordinary SD upgrade, and normal ST-Link preflight deliberately requires a valid APP: that state needs a separately reviewed recovery plan. The release does not add automatic rollback or recovery from every interrupted APP/BOOT write.

`RESTORE.BIN` remains stock **Zortrax M300 1.3.1**; the independent backup diagnostic remains **0.5.5** and is not a fourth installation route. Klipper MCU/host is separate. Firmware source and personal Flash/identity data remain private; public firmware is distributed as binaries with host tools and documentation. Existing 1.4.1, 1.4, 1.3.1 and 1.1 release assets retain their identities.

## Polski

### Wydanie i zakres testów

Stały BOOT i instalator SD mają wersję **1.5**. Wydanie zachowuje poprawki audytu opublikowane jako **1.4.1** i zmienia wszystkie bieżące oznaczenia: start OLED `M300 boot v1.5`, About `Version v1.5`, instalator `SD installer 1.5`, bannery UART oraz `INSTALL V15`. Właściciel zgłasza około **dwóch tygodni używania bazowej wersji 1.4**; odbiór jej wariantów FACTORY, UPGRADE i ST-Link zapisano 09.11.2026. **Przebudowane binaria 1.5 mają własną walidację offline z 18.11.2026; nie przeszły dwóch tygodni testów na drukarce.** Nie przypisujemy im dokładnej daty rozpoczęcia ani liczby godzin ciągłego testu. Zakres potwierdzeń i rzeczywiste wyniki zawierają [status sprzętowy](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/reports/v1.5/HARDWARE_STATUS.json) oraz [raport audytu](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/reports/v1.5/AUDIT_2026-11-18.json).

### Poprawki i zachowane działanie

- **Ponowienie APP po przerwanym zapisie metadanych:** bazowa 1.4 prawidłowo blokowała uruchomienie niezatwierdzonej APP, ale mogła też odmawiać ponownej instalacji z `NO_COMMIT`. W BOOT 1.5 zachowano kontrolowane ponowienie wprowadzone w 1.4.1: jest dopuszczone wyłącznie wtedy, gdy ta sama zweryfikowana paczka pasuje do rozpoznanego przerwanego rekordu oraz całej APP zapisanej we Flash. Nadal wymagane są kontrole profilu i nowe fizyczne przytrzymanie przez 2 sekundy. Niepełny commit wciąż blokuje start; obce rekordy, inny obraz i uszkodzona APP powodują odmowę. [Procedura i ograniczenia](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/pl/v1.5/installation.md#ponowna-instalacja-app-po-przerwanym-zapisie-metadanych).
- **Kompilacja i wykorzystanie miejsca:** BOOT i instalator przebudowano ze źródeł. Kontrole ponowienia wykorzystują dotychczas wolne miejsce pomiędzy tablicą wektorów a stałym punktem wejścia OEM. Jego adres, początek APP i granice obu obszarów programowania pozostają stałe; nie deklarujemy zwiększenia przepustowości UART.
- **Narzędzia hosta:** przygotowanie karty serwisowej sprawdza wszystkie istniejące pliki docelowe przed utworzeniem brakujących. Odrzuca niewłaściwe rozmiary, katalogi i dowiązania, zachowując istniejące zwykłe pliki o oczekiwanym rozmiarze; nie weryfikuje ponownie ich zawartości. Konsola sprząta częściowo otwarte zasoby portu i logów po błędzie połączenia, wymaga dokładnych oczekiwanych linii wersji i kontroli płyty, a przy błędzie zamykania zachowuje manifest/archiwum z wynikiem niepowodzenia. Bieżące narzędzia i `KONSOLA_M300_v1.5.command` odpowiadają temu wydaniu; narzędzia historycznych 1.4.1 i 1.4 zachowano w archiwum.
- **UART:** dokładnie **115200, 250000, 500000, 750000, 1500000**, 8N1; domyślnie **250000**, bootwait **OFF**. **1000000 usunięto już w 1.4** i pozostaje niedostępne; **10000000 nie jest obsługiwane**. Zachowano obsługiwane kody ustawień. Dawny nieobsługiwany zapis daje aktywne 250000 bez automatycznego przepisywania dziennika; przed startem starszej APP czytającej dawny zapis jawnie zapisz 250000 i dopasuj prędkość hosta.
- **Publikacja:** komplet instrukcji EN/PL, zgodne instrukcje wewnątrz paczki ST-Link, bezpośrednie pobieranie, sumy kontrolne i aktualne ilustracje OLED z renderera C. Rendery używają udokumentowanych danych przykładowych i nie są wynikami testów sprzętowych. [Pełny wykaz menu i komend](https://github.com/MarcinKowalik-AGH/Zortrax-m300-Boot-Loader/blob/main/docs/pl/v1.5/features-and-console.md).

### Zakres instalacji

Celem pozostaje zakwalifikowany profil **klasycznego M300 HW05 / PCB Rev.5.3 / zmierzone 256 KiB Flash**. Obowiązują kontrole UID, prefiksu OEM, danych fabrycznych i źródłowego BOOT; zgodność modelu nie kwalifikuje automatycznie kolejnej drukarki. Wymiana BOOT zachowuje pierwsze 4 KiB, NVM i dzienniki ustawień. ST-Link zapisuje wyłącznie dwa obszary BOOT/zasobów, zachowuje APP i wymaga pełnego odczytu kontrolnego. Instalacja SD wymaga dwóch zweryfikowanych kopii w tej samej sesji, osobnego potwierdzenia BOOT i jawnego przywrócenia docelowej APP. Komenda instalatora to `INSTALL V15`.

Kontrolowane ponowienie działa w BOOT **1.4.1 i 1.5**. Stara 1.4 już zatrzymana w `NO_COMMIT` może odrzucić zwykłą aktualizację SD, a standardowy ST-Link preflight celowo wymaga poprawnej APP: taki stan wymaga osobno ocenionego planu odzyskania. Wydanie nie dodaje automatycznego powrotu do poprzedniej wersji ani odzyskiwania po każdym przerwanym zapisie APP/BOOT.

`RESTORE.BIN` pozostaje oryginalnym **Zortrax M300 1.3.1**; niezależna diagnostyka kopii pozostaje **0.5.5** i nie jest czwartym wariantem instalacji. Klipper MCU/host jest osobny. Źródła firmware oraz osobiste kopie Flash i dane identyfikacyjne pozostają prywatne; publicznie udostępniono binaria, narzędzia hosta i dokumentację. Dotychczasowe załączniki wydań 1.4.1, 1.4, 1.3.1 i 1.1 zachowują swoją tożsamość.
