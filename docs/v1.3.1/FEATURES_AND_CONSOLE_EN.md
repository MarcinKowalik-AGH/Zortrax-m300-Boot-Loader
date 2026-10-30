# Features and console — M300Boot v1.3.1

[Polski](FUNKCJE_I_KONSOLA_PL.md) · [Index](README.md)

The permanent loader and SD intermediary identify themselves as **1.3.1**. The OEM-compatible FACTORY container has technical wrapper version **9.8.7**; that is not the running loader version.

## Menu and display

| Main entry | Functions |
|---|---|
| Start application | Verify the installed application and launch it after local confirmation. |
| Firmware on SD | Check/install the selected package; browse up to 16 catalog entries; explicit selection does not itself verify or install. |
| Diagnostics | Verify Flash, Hardware, Reset / Recovery, Clear recovery lock, Encoder / raw inputs, Display test, UART, SD card info. |
| About | Author, email and current version. |
| Restart | Explicit controller restart. |
| Backup Flash | Flash and identity backup to prepared SD files. |
| Service history | View the 24-event service history on UART or explicitly save it to SD. |

English OLED menus retain the stock-style glyphs, direct encoder detents, a pinned `Back` row in submenus and bounded scrolling without wraparound. The last successfully sent framebuffer is retained; only the changed rectangle is transferred and identical frames are skipped. Queued navigation is applied before one redraw. These are bootloader optimizations, separate from the Klipper application's DMA/RLE display transport.

`Diagnostics → Hardware` reads hardware revision, serial and accumulated operating time from device records each time. Invalid records show `Unavailable`. Model is the configured M300 target, not marketing-model autodetection. This screen does not modify NVM. Progress rings report the current phase's measured bytes/pages/hold time; an indeterminate wait shows `--`, not a fabricated percentage.

## Five-second autostart and UART during bootwait

The five-second countdown begins after board/OLED initialization. A physical click or completed encoder detent cancels it. Application integrity, environment and recovery state are checked before handoff. Watchdog/recovery conditions can keep the loader in service mode.

`Diagnostics → UART → UART on bootwait → OFF / ON` is stored in Flash independently of baud:

| Setting | Behavior during countdown |
|---|---|
| **OFF — default** | Received UART traffic is discarded. An already running Orange Pi/Klipper host cannot stop autostart with binary probes. Local service entry still works. |
| **ON — diagnostics** | Only a complete printable line from `MENU`, `HOME`, `BACK`, `HELP`, `INFO`, `PING`, `VERIFY`, `ECHO ON`, `ECHO OFF` opens service mode. Binary, partial, overlong and write commands do not cancel or postpone the deadline. |

This setting controls **received commands during the countdown**, not whether UART exists or whether the boot banner is transmitted. After service entry the normal console is available in either mode. During the local baud and bootwait settings screens, host RX is discarded so it cannot overwrite the screen or leave a partial command.

## Persistent baud and compatibility

The visible baud menu is ordered **115200, 250000, 500000, 750000, 1000000, 1500000**, **8N1, no flow control**. Empty settings default to **250000 / bootwait OFF**. Older saved 19200/57600 values remain readable but are not offered in the new menu. 2000000 is not supported.

Selection waits for the last old-speed byte to finish, validates the UART, saves the record with readback, then applies the new rate. The corrected local operation lock permits a settings change while retaining real operation guards. Incomplete host lines are discarded. A genuine timeout, incompatible environment or full journal can still reject a change; there is no force/erase fallback.

Hold the knob at power-on for temporary **250000** service entry. This does not overwrite the saved choice; release the knob and restart normally to use it again. MCU application firmware must independently read the journal and support that rate. The SD intermediary always uses temporary **250000**.

| Saved index | Baud | v1.3.1 behavior |
|---:|---:|---|
| 0 | 19200 | Legacy read compatibility |
| 1 | 57600 | Legacy read compatibility |
| 2 | 115200 | Menu |
| 3 | 250000 | Default and menu |
| 4 | 500000 | Menu |
| 5 | 750000 | Menu |
| 6 | 1000000 | Menu |
| 7 | 1500000 | New rate, record `0xFF99` |

Baud journal: `0x0803D800–0x0803D9FF`; bootwait journal: `0x0803DA00–0x0803DBFF`. Each is append-only, 256 halfword slots. Re-selecting the current value consumes no slot. The running loader never erases these pages to reclaim space; `Settings full` requires a separately planned service procedure. Verified 1.3 → 1.3.1 migration preserves both journals, application metadata and manufacturer NVM. Older firmware does not gain support for 1500000 merely because the record exists.

## Application updates, backup and recovery

The FAT16/FAT32 SD menu and `UARTCHECK` / `UARTUPDATE` handle an application linked at **0x08008000**, in a single 200-KiB slot. M3B validates target, size, vectors and SHA-256; SHA integrity is **not a cryptographic signature**. Identical applications are skipped. Manual launch/application writes require release and a fresh 2-second knob hold; rotation cancels.

Replacing permanent BOOT uses the separate SD intermediary: source/profile/card checks, two independent complete Flash snapshots, then release → fresh click → release → fresh 5-second hold. Rotation cancels. Installer recovery is available only with valid backups in the same still-running session. This is not automatic power-loss rollback or dual-bank firmware.

The final 8 KiB, original first 4 KiB and Option Bytes are outside normal bootloader update targets. The public images retain UID/options/factory-page qualification gates; an arbitrary M300/HW05 is not automatically accepted. [Installation](INSTALLATION_EN.md) · [UART examples](UART_EXAMPLES_EN.md) · [Troubleshooting](TROUBLESHOOTING_EN.md).
