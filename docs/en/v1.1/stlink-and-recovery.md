# ST-Link installation and OEM recovery

[English](../../en/v1.1/stlink-and-recovery.md) · [Polski](../../pl/v1.1/stlink-and-recovery.md) · [Index](README.md)

**Archived v1.1 record, 29 October 2026.** Hardware statements below retain their historical scope. [Current v1.3.1](../v1.3.1/README.md).

For the **qualified classic M300 Rev.5.3/HW05, measured 256 KiB** only. This is a deliberate service/recovery route, not a routine test of a working printer. The image builder is tested offline; a physical ST-Link v1.1 installation has not been independently confirmed.

## Preserve your own data first

Follow [Original backup](original-backup.md). Require two matching complete Flash files and UID/SIZE/OPTIONS pairs, or the four completed installer SD backup files. Preserve original 32-KiB OEM BOOT, both NVM pages and the factory page on a separate medium. Never use another printer's identity.

The STLINK ZIP includes a **28672-byte stage2 at 0x08001000**, **12288-byte assets at 0x0803A000**, a sparse HEX covering only those ranges, RESTORE.BIN and offline Python tools. **The sparse image is not sufficient after chip erase:** it lacks the original 4-KiB prefix and your data. Update.bin, RESTORE.BIN and M300APP.M3B are containers, not direct SWD images.

## Build a PERSONAL complete image offline

From the extracted STLINK directory:

```sh
python3 prepare_stlink.py --backup "/path/to/private/backup" --mode m300 --out "$HOME/Desktop/M300_PERSONAL_V11"
```

For OEM v3 + stock 1.3.1 recovery, use an original-OEM snapshot:

```sh
python3 prepare_stlink.py --backup "/path/to/private/OEM-backup" --mode oem --out "$HOME/Desktop/M300_PERSONAL_OEM"
```

Expected `PASS_PERSONAL_IMAGE_OFFLINE`. The new private folder contains a 262144-byte BIN, equivalent addressed HEX, manifest and checksums. The tool never connects to hardware, modifies options or erases a chip. It refuses existing output folders, mismatching pairs and foreign profiles. It preserves your OEM prefix and final 8 KiB; M300 mode adds application commit metadata while retaining an existing baud journal. This is a reconstruction, not an original pristine dump. Your counter/settings revert to the chosen snapshot date.

## Wire and connect

Power off before changing wiring. Use verified **SWDIO, SWCLK, GND, 3.3-V target reference and NRST**. VCP TX/RX are not SWD. Do not inject 5 V or infer header numbering from Inventure. Supply the board correctly and keep power stable. In CubeProgrammer select ST-LINK/SWD, **Under reset**, **Hardware reset**, initially **400 kHz**. Under-reset requires physical NRST. Verify voltage/device identity and save current options. A connection error is not a reason to erase.

## Read protection is a destructive boundary

Removing active STM32F1 RDP **mass-erases main Flash**, including BOOT and factory/NVM data. Only perform Read Unprotect after verifying a complete personal recovery image. It is not part of normal SD upgrade. In STM32F1, raw **A5** is unprotected; **00** is protected. Do not use the Inventure/F2 AA value. If already unprotected, do not repeat this operation.

Reconnect after option reload. Verify UID and measured SIZE against your backup. Never program UID, system ROM or the SIZE field. Inspect USER/DATA/WRP against your saved settings; do not upload the raw OPTIONS file as a linear Flash image. Keep RDP disabled during programming/readback. Re-enabling it is a separate choice after verification, not an automatic action by this release.

## Program and verify before running

Select the generated **complete PERSONAL BIN**, address **0x08000000**, exact length **0x40000**. Enable verify, disable automatic run and do not skip the required erase. After successful programming, with the core stopped, read/save the entire range to READBACK.bin and compare:

```sh
cmp M300_BOOT_v1.1_STOCK_1.3.1_PERSONAL_256KiB.bin READBACK.bin
shasum -a 256 M300_BOOT_v1.1_STOCK_1.3.1_PERSONAL_256KiB.bin READBACK.bin
```

For OEM mode use its generated filename. Require exact equality. End debug, power off, disconnect the probe and start without an update card. In M300Boot stop autoboot using the encoder, inspect Hardware, then launch stock 1.3.1. Check your serial, HW and counter before motion/heater tests. ST-Link recovery cannot repair damaged electronics or guarantee recovery after every power interruption.

## References

- STMicroelectronics [PM0075, §§2.3–2.4](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf): STM32F1 Flash, RDP/WRP, first-page protection, option-byte changes.
- ST [STM32CubeProgrammer 2.23 command reference](https://dev.st.com/stm32cube-docs/prog/2.23.0/en/docs/markup/CubeProg_Command_Lines.html): SWD under reset, hardware reset, read/program/verify.
- The device-specific memory map and tested behavior are from the project's retained private audit and operator reports, not an endorsement by ST or Zortrax.
