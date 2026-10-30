# Troubleshooting — v1.3.1

[Polski](DIAGNOSTYKA_PL.md) · [Index](README.md)

| Symptom | Check/action |
|---|---|
| Orange Pi stops the countdown | Confirm `M300 boot v1.3.1`; set `Diagnostics → UART → UART on bootwait → OFF`. OFF rejects host RX during the countdown. Recovery lock or a physical knob event can independently keep the menu open. |
| Need a console from the beginning | Set bootwait ON. Send a full allowed line, e.g. `INFO` plus newline. A single byte or binary Klipper probe does not enter the menu. |
| `busy` / `Operation rejected` when changing baud | Confirm the new boot, release the knob, enter the local UART setting with no operation active. Settings pages ignore host probes. A genuine UART timeout, wrong environment or full journal remains a valid refusal; do not erase settings to force it. |
| Saved 1500000 but active 250000 | Holding the knob at power-on forces service 250000 for that boot. Restart normally. `INFO` distinguishes active `UART_BAUD` from `SAVED`. The SD intermediary also temporarily uses 250000. |
| Klipper MCU still expects 250000 | Confirm the installed APP supports the saved journal and UART8; installing BOOT alone cannot update an APP's serial driver. Match the existing host `[mcu] baud`. |
| No `Waiting for Klipper` until host connects | That screen belongs to the MCU APP. Use the matching standalone-start OLED firmware; this boot-only archive does not supply it. |
| New boot starts the SD installer again | SD migration leaves the intermediary as APP. Enter BOOT and restore `RESTORE.BIN` or your intended, checked MCU M3B. Do not repeatedly replace BOOT. |
| Installer refuses source/profile/card | Keep the exact error and copies. Confirm six files, source allowlist, original profile and fresh A5 templates. Do not remove gates or borrow another printer's data. |
| `Settings full` | The append-only journal is exhausted; selecting the current value does not consume a record. No automatic erase is performed. Preserve a full verified snapshot before any separately planned service. |
| MCU remains shutdown after a host service stop | Capture the first shutdown reason from Klipper logs before reset. A communication loss and an OLED transport fault are different cases; do not infer a baud error from the last generic message. |
| ST-Link cannot read with RDP active | Use the SD route and original backup procedure. Read Unprotect erases main Flash; the two-segment archive is not a complete erased-chip image. |
| Readback differs after SWD programming | Keep the core halted and preserve before/after/UID/options files privately. Do not automatically run, reset or mass-erase. |

For normal use, one UART client owns the link. Firmware version, the two matching baud values and fresh status matter more than a Linux service merely being `active`. Ready/working OLED is not motion, heater or print qualification.
