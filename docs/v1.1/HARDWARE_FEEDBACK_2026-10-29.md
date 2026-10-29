# M300 boot v1.1 — owner hardware feedback / Raport z testów sprzętowych

**Data zgłoszenia / Report date:** 29 October 2026. **Firmware:** M300 boot v1.1; **intermediary:** SD installer 1.1-i4. **Source:** direct owner reports in project conversation, not an independent inspection of the second printer's logs.

## Hardware-test matrix / Macierz prób

| Printer / Drukarka | Installation route / Droga | Outcome / Wynik | Hardware evidence / Sprzęt | Evidence level |
|---|---|---|---|---|
| Unit A / Egzemplarz A | **UPGRADE** from custom M300Boot | Owner confirmed completed i4 installation, restored original Zortrax **1.3.1**, and successful startup | Classic M300; **PCB Rev. 5.3**, stock **HW05**, measured **256 KiB** Flash, STM32F1 ID `0x414` | Owner confirmation plus earlier UART, binary readback and photo evidence |
| Unit B / Egzemplarz B | **FACTORY** from original bootloader | **Owner explicitly reported that FACTORY works on the second printer** | Second printer in the M300 project. PCB revision, hardware value, MCU Flash size, stock firmware, test log and exact successful checkpoints have **not** been supplied here | Owner statement only; do not infer successful permanent-boot write/readback or 1.3.1 startup without further evidence |
| Any unit / Dowolny egzemplarz | **ST-Link/SWD** writing/recovery of v1.1 | No separate hardware confirmation | Offline image generation tested, not a physical ST-Link bootloader installation | Not hardware qualified |

## Important compatibility qualification / Ważna niezgodność do wyjaśnienia

The published i4 binary and existing documentation have **fixed UID/Option Bytes/factory-page profile checks** tied to a qualified unit. The second-printer FACTORY success report is therefore **new evidence that warrants inspecting the second unit's exact log and installation checkpoints**. A successful OEM loading of `Update.bin` into the application slot is not, by itself, proof that the intermediary subsequently rewrote the permanent bootloader; those are separate operations. Do not assume which stage succeeded until it is logged.

The owner report is recorded **without rejecting or weakening it**, but it does **not establish universal compatibility** or authorization to remove identity checks. Do not flash an unqualified board, transfer another printer's UID/NVM, or alter RDP/WRP to force acceptance. Prior backup recommendations remain mandatory.

Polski: **Właściciel potwierdził działanie FACTORY na drugiej drukarce.** Ponieważ binarium i4 według istniejących ustaleń zawiera blokady indywidualnego profilu (UID, Option Bytes i strona fabryczna), zakres przejścia wymaga doprecyzowania na podstawie logu lub odczytu diagnostycznego. W szczególności fabryczne wgranie pośrednika nie musi oznaczać zakończenia osobnej podmiany stałego BOOT. Nie wyłączamy blokad i nie uogólniamy zgodności na wszystkie M300.

## Optional read-only evidence / Opcjonalne potwierdzenie bez kolejnego flashowania

If available, preserve the second unit's **redacted** original hardware/Flash-size details and any saved installer completion lines such as `PASS_SD_FULL_FLASH_X2`, `INSTALL_OK_STAGE2_AND_ASSETS_VERIFIED`, boot banner v1.1, and successful stock launch. These are examples of possible checkpoints, **not claims that they were observed**. Do not post raw UID, unredacted serial number, factory NVM, or private full-Flash backups. There is no need to repeat a successful installation merely to produce evidence.

**Publication impact:** updated owner-reported FACTORY status on `main` only. Existing `v1.1` tag, factory/upgrade/ST-Link ZIPs, SHA-256 values, and installed firmware remain unchanged. The dated publication-audit JSON files describe their earlier audit snapshot and are not retroactively rewritten.
