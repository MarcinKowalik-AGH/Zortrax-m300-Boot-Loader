# Changelog

[English](CHANGELOG.md) · [Polski](docs/pl/changelog.md)

## 1.5 — 2026-11-18

- Rebuilt permanent BOOT and the SD intermediary as 1.5, including the OLED startup header, About version, installer title, UART banners and guarded `INSTALL V15` command. The 1.4.1 release and assets remain archived with their original identities.
- Retained the audited 1.4.1 fixes: constrained same-APP retry after an interrupted metadata commit, service-card preflight, exact console identity checks and log/manifest retention on connection or close errors. Protected ranges, device qualification and physical confirmation remain.
- Published matching FACTORY, UPGRADE and STLINK packages, complete EN/PL guides and new native C OLED renders for 1.5. [Bilingual release notes and downloads](RELEASE_NOTES_v1.5.md).
- UART still offers only 115200/250000/500000/750000/1500000; default 250000 / bootwait OFF. 1000000 was removed in 1.4 and remains unsupported, as does 10000000.
- Recorded separate validation for the rebuilt 1.5 release. The owner's approximately two-week history remains evidence for baseline 1.4, not this build. [Current audit](docs/reports/v1.5/AUDIT_2026-11-18.json) · [Hardware status](docs/reports/v1.5/HARDWARE_STATUS.json).

## 1.4.1 — 2026-11-18

- Fixed the APP retry dead end after an interrupted metadata commit: the same verified candidate, recognized torn record, matching complete Flash payload and fresh physical confirmation are required. Incomplete commits still block launch; unrelated records and damaged APP remain refused.
- Rebuilt BOOT and installer as 1.4.1. Recovery checks use the existing vector-to-OEM-hook gap; the fixed hook, APP base, programming slots, OEM prefix, NVM and setting journals remain protected.
- Hardened service-card preparation to reject invalid existing destinations before creating missing templates. Fixed serial/log cleanup on connection failures and exact console version/board-response validation. Matching current tools are provided; 1.4 tools remain archived.
- Retained exactly 115200/250000/500000/750000/1500000, default 250000 / bootwait OFF. 1000000 was already removed in 1.4; 10000000 is unsupported. Supported saved codes and explicit older-APP migration remain.
- Updated all three variants: FACTORY, UPGRADE and STLINK, with complete EN/PL manuals, package instructions, direct downloads, manifests, checksums and current native C OLED renders.
- Evidence is separated: the owner reports approximately two weeks of using baseline 1.4 and its previously accepted installation routes; the new 1.4.1 patch has offline validation dated 2026-11-18, without a two-week hardware-test claim. [Hardware status](docs/reports/v1.4.1/HARDWARE_STATUS.json) · [Audit](docs/reports/v1.4.1/AUDIT_2026-11-18.json).
- The retry fix needs working BOOT 1.4.1. An older device already stuck in `NO_COMMIT` requires separate recovery review; ordinary ST-Link preflight still requires a valid APP. No automatic power-loss rollback is added. [Bilingual release notes and downloads](RELEASE_NOTES_v1.4.1.md).

## 1.4 — 2026-11-08

- Owner acceptance recorded 2026-11-09: FACTORY, UPGRADE and ST-Link validated on the printer. Published the unmodified original Zortrax Bootloader v3, with provenance and SHA-256. Installation packages and release tag are unchanged.

- Documentation review, 2026-11-09: complete menu/command catalog, OLED-only installation and recovery steps, option-coverage checks and current-manual links in the release description. Firmware assets retain their original identities.

- Unified permanent BOOT and intermediary identity 1.4, without development suffixes.
- Exactly five UART rates 115200/250000/500000/750000/1500000; default 250000 / bootwait OFF.
- Unsupported historical saved rates use active 250000 without automatic Flash rewriting; supported codes are preserved and explicit older-APP migration is documented.
- Rebuilt packages, matching current tools and offline validation; later owner hardware acceptance is recorded separately.
- Complete EN/PL instructions and native-font cyan OLED renders. [Release notes](docs/en/v1.4/release-notes.md).

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
