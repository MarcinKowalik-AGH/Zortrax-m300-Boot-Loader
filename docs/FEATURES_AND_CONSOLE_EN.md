# M300 boot v1.1 — features and Hardware

Header: M300 boot v1.1 © Marcin Kowalik. Responsive non-wrapping menus, pinned Back, direct encoder input and dirty-rectangle OLED updates retain rc3 navigation behavior.

Diagnostics → Hardware displays Model, Hardware version, Serial number and Total operating time. Hardware/serial/time are decoded from current device records at each entry; Model denotes the target profile. Invalid records display Unavailable. The view waits for another click and never writes NVM. Installer i4 provides the same information.

Progress rings use bytes/pages/hold time for the current phase. Separate write/check phases may each begin at zero. Unknown waits use --; errors never masquerade as 100%.

Functions include manual verified launch, cancellable five-second autoboot, SD/UART application check/install, identical-image skip, file browser, Flash/identity backup, diagnostics and 24-event history. There is one replaceable application slot, not simultaneous dual boot or a ready-made Klipper port.

USART1 PA9/TX → adapter RX, PA10/RX ← adapter TX, ground, 3.3-V logic; verify header pins independently of Inventure. No 5 V or active SWD. Baud rates 19200/57600/115200/250000/500000, 8N1 without flow control. Hold the encoder at startup for service entry at 250000. Persistent selection is separate from stock NVM; the intermediary temporarily uses 250000 while preserving the journal.

The public console requires Python/pyserial. --dump-all creates paired read-only backups; m300_service.py checks dumps/SD copies/history. ibtool.py packs raw applications linked at 0x08008000 and serves M3B, without OEM decryption/signing tools. Never pack stage2 as an application or reuse old rc3 installation scripts for i4/v1.1. Keep logs/dumps private.
