# UART, saved settings and MCU handoff — v1.3.1

[Polski](KONSOLA_UART_PRZYKLADY_PL.md) · [Features](FEATURES_AND_CONSOLE_EN.md)

## Connect the boot console

Use **3.3-V TTL**, PA9/USART1_TX → adapter RX, PA10/USART1_RX ← adapter TX, common GND. These are MCU signal names, **not physical header pin numbers**. Use independently verified M300 wiring. Do not apply 5 V. VCP TX/RX is distinct from SWDIO/SWCLK. Stop other serial clients, including the Orange Pi host, before opening the console.

With bootwait OFF, enter the service menu locally first. For diagnostic access during countdown, save bootwait ON first; a complete allowed command such as `INFO` can then open service mode. Hold the knob at power-on for temporary 250000 if the active rate is uncertain. The intermediary uses 250000 regardless of saved baud.

```sh
python3 -m pip install -r tools/requirements.txt
bash tools/KONSOLA_M300_v1.3.1.command --port /dev/cu.usbmodem14203 --baud 250000
bash tools/KONSOLA_M300_v1.3.1.command --port /dev/cu.usbmodem14203 --baud 1500000 --dump-all
```

The two examples assume different active rates; choose the matching one. Console status requires `M300BOOT v1.3.1`, `BOARD_CHECK OK`, PONG and final READY. Output is private. The launcher is read-only, while `ibtool.py serial --update` is an explicitly separate APP write.

| Console command | Function |
|---|---|
| `INFO`, `PING`, `HELP` | Current version/hardware/UART/OLED state, link test, command list. |
| `MENU`, `HOME`, `BACK` | Return to the main boot menu. |
| `VERIFY` | Verify installed Flash. |
| `LIST`, `SELECT n`, `SELECT AUTO` | Refresh/list SD catalog, select zero-based entry or automatic selection. |
| `SDCHECK`, `SDUPDATE` | Check/install selected SD application; write still needs physical confirmation. |
| `UARTCHECK N`, `UARTUPDATE N` | M3B file-server protocol; use `ibtool.py`, not manual binary entry. |
| `DUMP FLASH`, `DUMP BOOT`, `DUMP NVM`, `DUMP FACTORY`, `DUMP SYSROM`, `DUMP SIZE`, `DUMP UID`, `DUMP OPTIONS` | Read fixed regions; the receiver checks offsets, CRC and full SHA-256. |
| `BACKUP`, `LOGSAVE` | Explicit SD backup or history write; prepared SD files required. |
| `RESETINFO`, `RECOVERY CLEAR`, `DIAG`, `DISPLAY`, `CARDINFO`, `LOG` | Service diagnostics; clearing recovery is a deliberate state change. |
| `BOOT`, `REBOOT` | Explicit application launch/controller reset. |

```sh
python3 tools/ibtool.py inspect "/path/to/M300APP.M3B"
python3 tools/ibtool.py pack "/path/to/own-app.bin" "/path/to/NEW.M3B"
python3 tools/ibtool.py serial "/path/to/NEW.M3B" --port /dev/cu.usbmodem14203 --baud 250000
```

`pack` requires an already compiled APP for 0x08008000, not stage2. `serial` without `--update` verifies only. M3B has SHA-256 integrity, not a signature, and this tool has no OEM keys/decryption function.

## Match Klipper to the saved rate

The boot release does not install Klipper host modules. A matching **UART8** MCU and host validator are required for 1500000; older UART7 must not be forced to accept it. The standalone `Waiting for Klipper` screen is drawn by the MCU application, before the Orange Pi connects, using the saved baud. Bootloader v1.3.1 alone cannot add this screen to an unrelated APP.

On the Orange Pi, stop Klipper. In BOOT choose `Diagnostics → UART → UART baud rate → 1500000` and require confirmation that Flash was saved. Choose `UART on bootwait → OFF` for normal startup. In the existing host section change only baud:

```ini
[mcu]
serial = /dev/ttyS1
baud = 1500000
restart_method = command
```

The device path above is the tested Orange Pi UART1 setup, not a universal Linux mapping. Restart the printer **without holding the knob**, wait for its compatible MCU application's waiting screen, then start Klipper. Check in Fluidd:

```gcode
STATUS
ZORTRAX_MCU_STATUS
ZORTRAX_OLED_STATUS
```

Expect Ready, `uart.baud = host_baud = 1500000`, `index = 7`, `match = true`, and no reported fault. The owner confirmed this link with MCU UART8 and later OLED-R3.2. That does not qualify motion/heating or prove print-load headroom. Do not alter SPI or actuator gates as part of setting baud.

If connection fails, stop the host and return **both sides** to a previously working rate, restart the MCU, then the host. Merely changing `[mcu] baud` does not change the saved MCU rate. [Troubleshooting](TROUBLESHOOTING_EN.md).
