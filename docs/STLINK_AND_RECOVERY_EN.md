# ST-Link installation and recovery

This is a deliberate service route, not a routine test. Physical SWD installation of v1.1 is not independently confirmed. Preserve two matching complete private backups and identity/options first.

The STLINK package contains stage2 (28672 B at 0x08001000), assets (12288 B at 0x0803A000), sparse HEX, RESTORE.BIN and an offline image builder. These components alone are insufficient after chip erase: they do not contain your original prefix/NVM/factory records. Never flash update containers directly through SWD.

```sh
python3 prepare_stlink.py --backup "/your/private/backup" --mode m300 --out "$HOME/Desktop/M300_PERSONAL_V11"
python3 prepare_stlink.py --backup "/your/private/OEM-backup" --mode oem --out "$HOME/Desktop/M300_PERSONAL_OEM"
```

OEM mode requires an original-OEM snapshot. Require PASS_PERSONAL_IMAGE_OFFLINE. The tool refuses existing output folders and foreign profiles; it makes no device calls. Output is a reconstructed personal 256-KiB BIN/HEX with stock 1.3.1 and your preserved data, not a pristine historic dump. Counter/settings revert to the chosen snapshot date.

With power off wire verified SWDIO, SWCLK, GND, 3.3-V reference and NRST. UART is not SWD. Do not connect 5 V or assume Inventure pin order. Use CubeProgrammer ST-LINK/SWD, Under reset, Hardware reset and initially 400 kHz. NRST must physically be connected. Inspect voltage/identity/options before writes.

Removing active STM32F1 RDP **mass-erases main Flash**. Only do this deliberately after verifying a complete personal recovery image. Raw A5 is unprotected; 00 is protected. Do not use F2/Inventure AA. If already unprotected, do not repeat Read Unprotect. Verify UID/SIZE on reconnection, inspect other options against your record, and never replay UID/SYSROM/SIZE or raw OPTIONS as an ordinary image. Keep RDP disabled for readback.

Program the generated complete PERSONAL BIN at **0x08000000**, length **0x40000**. Enable verify, disable automatic run and do not skip required erase. Before running, read all 256 KiB with the core stopped and compare exact bytes and SHA-256 with your image. Then end debug, power off, disconnect the probe and start without an update card. Check your identity/counter before motion/heating.

No automatic power-loss recovery or repair of damaged electronics is promised. Sources: [ST PM0075](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf), [CubeProgrammer](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_Command_Lines.html).
