# ST-Link installation and readback — M300Boot v1.3.1

[Polski](STLINK_I_ODZYSKIWANIE_PL.md) · [Backup](ORIGINAL_BACKUP_EN.md)

This version's STLINK route writes **two segments while preserving APP and device data**. It replaces the old complete-image reconstruction as the normal v1.3.1 SWD procedure. The owner confirmed physical ST-Link operation, as well as FACTORY and UPGRADE, on 30 October 2026. The plan/readback checker is also validated offline.

| File in `03_TARGET_FULL` | Address | Exact length | Erase only these 2-KiB pages |
|---|---|---:|---|
| `M300Boot_v1.3.1_FULL_ASSETS_0x0803A000.bin` | `0x0803A000` | 12288 B | 116–121 |
| `M300Boot_v1.3.1_FULL_STAGE2_0x08001000.bin` | `0x08001000` | 28672 B | 2–15 |
| `M300Boot_v1.3.1_FULL_SPARSE.hex` | Encoded in HEX | 40960 B addressed memory | Same two ranges |

**STAGE2 is not a BIN for 0x08000000.** The HEX has the full FF-padded tails and no application, OEM prefix, journal or NVM range. It is not a whole-chip recovery image after erase. `Update.bin`, `RESTORE.BIN` and M3B are containers, not direct SWD images.

## Preconditions and connection

RDP must be **already off**, SWD reads working, WRP permitting the required targets, hardware/UID/prefix/factory profile matching, and APP valid. If RDP is active, use SD. Do not perform Read Unprotect, Mass Erase, RDP changes or Apply Option Bytes to continue this procedure. Removing active STM32F1 RDP destroys main Flash, which these two segments cannot reconstruct.

With power off, connect independently verified **SWDIO, SWCLK, GND, 3.3-V VTref and NRST**. UART TX/RX is not SWD. No unverified M300 header numbering is specified here. In CubeProgrammer select ST-LINK/SWD, Under reset, Hardware reset, initially 400 kHz; NRST is required. Confirm target voltage, Cortex-M3/F103-family target and **measured 256 KiB**. Halt the core; do not run it between reads/writes.

Save two actual independent reads, `FLASH_A.bin` and `FLASH_B.bin`, from `0x08000000`, length `0x40000`. Save `UID.bin` from `0x1FFFF7E8` (12 B) and `OPTIONS.bin` from `0x1FFFF800` (16 B). Check the 16-bit SIZE register `0x1FFFF7E0` reads 256. Do not program these system addresses or option files.

## Prepare a private offline plan

Unzip the STLINK archive and change into its extracted root:

```sh
python3 tools/verify_package.py
python3 tools/stlink_preflight.py plan   --backup-a "/private/FLASH_A.bin" --backup-b "/private/FLASH_B.bin"   --uid "/private/UID.bin" --options "/private/OPTIONS.bin"   --out-dir "/private/NEW_M300_V131_PLAN"
```

Require `PASS_OFFLINE_STLINK_PLAN`. This writes only a private local plan, never opens the probe and refuses an existing output directory. If `changed: false`, do not reprogram an identical image. The retained UID/profile checks and already-unprotected option pattern are deliberate. A refusal does not authorize patching them. When using repository-root tools instead, add `--images "/path/to/extracted-STLINK/03_TARGET_FULL"` to both plan and verify.

## Program, verify, then run

1. Keep the core halted. Enable verify after programming; disable automatic Run and whole-chip erase.
2. Program **ASSETS at 0x0803A000**, erasing only pages 116–121; verify.
3. Program **STAGE2 at 0x08001000**, erasing only pages 2–15; verify. Preserve the first 4 KiB.
4. Still halted, read the entire 256 KiB as `FLASH_AFTER.bin`, plus `UID_AFTER.bin` and `OPTIONS_AFTER.bin`.
5. Check the complete expected image and every byte outside the two segments:

```sh
python3 tools/stlink_preflight.py verify   --plan "/private/NEW_M300_V131_PLAN/PRIVATE_STLINK_PLAN.json"   --before "/private/FLASH_A.bin" --after "/private/FLASH_AFTER.bin"   --uid-after "/private/UID_AFTER.bin" --options-after "/private/OPTIONS_AFTER.bin"
```

Require `PASS_STLINK_READBACK_ALL_256K`. If anything differs, preserve the reads and keep the core halted; do not automatically reset or erase. After a match, end debug, power off, disconnect the probe and start without an update card. Check **M300 boot v1.3.1**, saved baud/bootwait and the previously installed application. APP was not replaced, so this route does not require installing a new APP merely because BOOT changed.

Power loss during BOOT programming can prevent startup. Recovery after a whole-chip erase needs your complete verified personal recovery material and a separately reviewed plan. The old v1.1 `prepare_stlink.py` builds **v1.1**, not v1.3.1; do not use it for this release.

Manufacturer references: [ST PM0075](https://www.st.com/resource/en/programming_manual/pm0075-stm32f10xxx-flash-memory-microcontrollers-stmicroelectronics.pdf), Flash/RDP/WRP; [ST UM2237](https://www.st.com/resource/en/user_manual/dm00403500-stm32cubeprogrammer-stmicroelectronics.pdf), programming/readback.
