# Oryginalny Zortrax Bootloader v3 — klasyczna M300

[English](README.md) · [Polski](README_PL.md)

[Pobierz OEM_BOOT_V3.bin](OEM_BOOT_V3.bin) · [Manifest](MANIFEST.json) · [SHA-256](SHA256SUMS.txt)

To niezmieniony **oryginalny Zortrax Bootloader v3 o rozmiarze 32 KiB**, zachowany w archiwum projektu M300. Jest udostępniony osobno od M300Boot 1.4.

| Właściwość | Wartość |
|---|---|
| Plik | `OEM_BOOT_V3.bin` |
| Format | Surowy obraz binarny, 32768 bajtów |
| Oryginalny zakres Flash | `0x08000000–0x08007FFF` |
| Identyfikator w obrazie | `Zortrax Bootloader v3` |
| Początkowy wskaźnik stosu | `0x20003FF0` |
| Wektor resetu, Thumb | `0x08000165` |
| Zapisany profil sprzętu | Klasyczna M300, HW05 / PCB Rev.5.3 / rodzina STM32F103 / zmierzone 256 KiB Flash |

SHA-256:

```text
dcc69ce6ad7d4ca46ba9363239f1f39863559e286fa3e53abfeb5eb47c82de3a
```

## Pochodzenie i weryfikacja

Plik pochodzi z `04_OEM_ROLLBACK/OEM_BOOT_V3.bin` w zachowanym archiwum projektu `M300Boot_v1.3.1_KOMPLET_2026-10-30.zip`. Jest identyczny bajt w bajt z prywatną kopią referencyjną oraz pierwszymi 32768 bajtami zachowanego oryginalnego obrazu Flash. To sprawdzenie zgodności materiałów archiwalnych, a nie trzy nowe niezależne odczyty drukarki. Żaden bajt nie został zmieniony ani odtworzony.

W głównym katalogu repozytorium sprawdź plik przy użyciu Python 3.9 lub nowszego:

```sh
python3 tools/validate_original_boot.py --json
```

Po pobraniu samego pliku porównaj jego SHA-256 z wartością powyżej. W tym katalogu polecenie `sha256sum -c SHA256SUMS.txt` sprawdza także manifest i oba opisy.

## Zakres pliku

Podany adres określa położenie oryginalnego BOOT. Surowy obraz nie jest pakietem aktualizacji SD, kompletnym obrazem drukarki ani aplikacją `RESTORE.BIN` (Zortrax M300 1.3.1). Zawiera wyłącznie obszar BOOT, bez APP, końcowego obszaru NVM/danych producenta, UID i Option Bytes. Nie zastępuje niezależnych kopii konkretnej drukarki ani nie potwierdza zgodności z innymi płytami, Plus, Dual lub Inventure.

[Potwierdzenie trzech metod instalacji M300Boot 1.4 przez właściciela](../../docs/pl/v1.4/tested-hardware.md) dotyczy FACTORY, UPGRADE i ST-Link własnego bootloadera. Przywrócenie tego obrazu OEM nie zostało osobno zgłoszone jako przetestowane. Obowiązujące procedury instalacji i odzyskiwania opisuje [bieżąca instrukcja](../../docs/pl/v1.4/README.md).

Firmware producenta zachowuje pierwotne prawa; licencja MIT projektu nie zmienia licencji tego pliku. Zobacz [zasady dystrybucji](../../THIRD_PARTY_NOTICES.md).
