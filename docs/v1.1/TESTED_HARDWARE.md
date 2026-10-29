# Tested hardware / Przetestowany sprzęt

Release: **M300 boot v1.1**, installer **1.1-i4**. Publication date: **29 October 2026**. This table describes the evidence in the project, not a manufacturer compatibility guarantee.

| Parameter / Parametr | Evidence-backed value / Ustalenie |
|---|---|
| Printer | Classic **Zortrax M300**, not Plus, Dual or Android/LCD generation |
| Mainboard silkscreen | **Rev. 5.3** — photographs of the actual board |
| Hardware version shown by stock | **05**; the factory record stores raw `E5` and the stock display decodes it |
| MCU | STM32F101/F103 high-density as reported by ST-Link; target code is STM32F103-family Cortex-M3 |
| Exact full part number | **Not established**: the chip marking was not reliably legible. Do not assert an exact VDT6/VET6 ordering code |
| Device ID / silicon revision | **0x414 / Rev X**, observed with SWD |
| CPUID | **0x411FC231**, observed by the running diagnostic app |
| Main Flash | **256 KiB, 262144 bytes**: two matching 16-bit SIZE reads at `0x1FFFF7E0`, plus corroborating bytes in SYSROM |
| Misleading old label | CubeProgrammer originally displayed 512 KB. This is **not** the accepted size; runtime `512_PRIOR_SWD` was also only an old label |
| Memory geometry used | 128 pages × 2048 B, `0x08000000–0x0803FFFF` |
| Original loader | **Zortrax Bootloader v3**, recovered and independently compared |
| Original printer application | **1.3.1**; owner also tested **1.3.1 → 1.2.0 → 1.3.1** |
| Protection during successful migration | RDP active; extra WRP inactive; no Option Bytes changes by the installer |
| Display/input | OLED and rotary encoder; readable screen, both rotation directions, click, Back, bounded scrolling and smooth rc3-derived rendering confirmed by owner |
| Host/probe used | MacBook Air/macOS, Python 3.9/3.11 sessions with pySerial 3.5; STM32CubeProgrammer 2.23.0; **STLINK-V3SET** for SWD inspection and later VCP/UART at **250000 8N1** |
| Fully characterized printers | **One** (unit A, full board/Flash/firmware evidence) |
| Additional owner-reported printer | **One more** (unit B; FACTORY reported working; PCB/HW/Flash/firmware and checkpoints not supplied) |

## What the owner confirmed

For **unit A**, the owner confirmed i4 **UPGRADE** completing and original **1.3.1 starting afterwards**. Earlier logs verify rc3 migration and exact 1.3.1 payload readback, and a photo confirms retained model, HW05, serial and accumulated operating time. **For unit B**, the owner subsequently reported that **FACTORY works on the second printer**; no second-unit hardware details or exact installer success log were supplied. [Hardware feedback and route test matrix](HARDWARE_FEEDBACK_2026-10-29.md). No public raw identity or personal snapshot is bundled.

### Confirmed / Potwierdzone

- Read-only internal Flash export while RDP remained active, with two matching complete 256-KiB snapshots and separate identity/options copies.
- Custom rc3 FULL boot and exact original 1.3.1 restored via UART; stock UI startup.
- i2 SD upgrade procedure on an already-identical rc3, including the no-write branch and stock restoration reported by the owner.
- Owner report: **i4 upgrade to v1.1 and successful return to stock 1.3.1** on unit A.
- Owner report: **FACTORY route works on a second printer** (unit B); exact OEM/intermediary/permanent-BOOT milestones not independently documented.

### Not established / Niepotwierdzone

- Independent logs and hardware characteristics for the second printer’s FACTORY path, including whether permanent-BOOT write verification and stock application launch occurred. The owner reports FACTORY working; the exact observed stages are not available here.
- Physical programming/recovery of v1.1 via ST-Link.
- Power interruption tolerance, automatic rollback, every menu branch, all baud-rate/reboot combinations, full print/heater/motor qualification or other mainboard revisions.
- Universality across all HW05 boards. The distributed installer is bound to the qualification unit through UID/options/factory-page hashes.

## Why the installer may reject another printer

The unchanged i4 images compare a fixed profile: OEM prefix, source code hashes, UID hash, options hash and factory-page hash. **Two printers may both say M300/HW05 and still not match.** The owner’s second-printer FACTORY report is therefore important but leaves a **profile-gate versus observed-stage question** until the second unit’s log is examined. Loading the intermediary from OEM is not identical to verifying permanent boot replacement. There is no FORCE mode. Do not edit hashes, erase factory records, copy another printer's identity, or remove RDP to get around a refusal.

Before using an installer, run the read-only profile checker against your private verified backups. `BACKUP_VALID_BUT_INSTALL_PROFILE_MISMATCH` means the backup may be useful but this installer must not be used. A different printer needs independent qualification and a separate build; this release does not silently produce one.

Brak zgody profilu nie jest błędem pliku ani powodem do wyzerowania numeru seryjnego/licznika. Nie wgrywaj pośrednika tylko po to, żeby poznać wynik blokady: jego instalacja już zastępuje aplikację drukującą.
