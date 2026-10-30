# Changelog / Historia zmian

## 1.3.1 — 2026-10-30

- UART up to **1500000**, ordered menu from 115200; legacy saved indices retained. / UART do 1500000, zgodność starych zapisów.
- Persistent bootwait UART OFF/ON, binary RX isolation, corrected local baud busy handling. / Trwałe OFF/ON i poprawki autostartu oraz ustawiania baud.
- Reviewed OLED dirty rectangles/direct detents and protected settings journals. / Częściowe OLED, kroki enkodera, zachowane dzienniki.
- Public FACTORY, UPGRADE and two-segment STLINK packages; current PL/EN manuals and tools. / Nowe paczki i dokumentacja.
- Owner confirms all three installation routes on hardware and UART8 at 1500000. / Wszystkie drogi potwierdzone sprzętowo przez właściciela.
- 2941 boot/installer tests re-run PASS; v1.1 assets and tag preserved.

[Full release notes / Pełne zmiany](docs/v1.3.1/RELEASE_NOTES.md).


## 1.1 — documentation follow-up 2026-10-29

- Owner confirmed that **FACTORY works on a second printer**. The original UPGRADE/stock 1.3.1 confirmation on unit A remains valid.
- Public docs now distinguish owner-reported second-device FACTORY operation from independent evidence of each permanent BOOT write/stock start checkpoint. The second board identity and log remain unreported.
- Compiled installer i4 still has device-profile gates; no firmware binaries or release assets changed. Physical ST-Link remains unconfirmed.

## 1.1 — publication 2026-10-29

- Stable display name M300 boot v1.1 © Marcin Kowalik.
- Hardware information decoded from current device records, not a fixed OK.
- Progress rings in bootloader and installer, measured per operation phase.
- Responsive encoder and non-wrapping long menus retained from rc3.
- SD installer 1.1-i4 fixes missed click/hold sampling during OLED rendering, redraw throttling and detailed refusal messages. Physical consent, paired backups and write-range gates remain mandatory.
- FACTORY OEM v3 and UPGRADE archives plus ST-Link/offline personal-image route.
- Mandatory original-memory preservation guide, tested-board matrix and public operational tools.
- Firmware machine code is unchanged from the owner's successful i4 upgrade and stock 1.3.1 startup report. Public backup/image-building host adaptations have separate offline validation; they are not new on-device tests.
