# Changelog

[English](CHANGELOG.md) · [Polski](docs/pl/changelog.md)

## Documentation organization — 2026-10-30

- Complete manuals separated into `docs/en/<version>` and `docs/pl/<version>` with matching filenames and language switches.
- English and Polish project, tools and firmware indexes; separate changelogs, release descriptions, hardware matrices and manifests.
- Shared images under `docs/assets`, historical machine-readable evidence under `docs/reports`; old URLs retained as compatibility links.
- Current v1.3.1 and archived v1.1 are explicit. Firmware, public ZIPs, release tags and hardware-confirmation scope are not changed.

## v1.3.1 — 2026-10-30

- UART menu from 115200 through 1500000, with legacy saved-index compatibility.
- Persistent UART on bootwait OFF/ON; binary host RX does not cancel autostart; corrected local baud busy handling.
- Incremental OLED transfer, direct encoder detents and protected journals retained.
- UPGRADE, FACTORY and two-segment ST-Link packages, paired EN/PL instructions and current public tools.
- Owner confirmed all three installation routes, UART8 at 1500000 and standalone/display operation.
- 2941 BOOT/installer tests and 94 public-host checks PASS for the publication. [Release notes](docs/en/v1.3.1/release-notes.md).

## v1.1 documentation follow-up — 2026-10-29

- Owner reported FACTORY working on a second printer. The characterized unit's UPGRADE/stock-1.3.1 confirmation remained valid.
- Documentation distinguished that report from individually logged permanent-BOOT checkpoints. ST-Link was not separately confirmed in that historical record; profile gates and binaries remained unchanged.

## v1.1 publication — 2026-10-29

- M300 boot v1.1 display/version and device-derived hardware records.
- Phase-based progress, responsive encoder and bounded menus retained from rc3.
- SD installer 1.1-i4 confirmation sampling, progress throttling and refusal details.
- FACTORY, UPGRADE, offline personal-image ST-Link route and original-memory preservation procedures.
- Binary-only firmware publication, public host adaptations and separate offline validation; original release assets retained. [Historical notes](docs/en/v1.1/release-notes.md).
