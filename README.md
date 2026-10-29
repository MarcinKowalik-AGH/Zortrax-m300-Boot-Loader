# M300 boot v1.1

Independent service bootloader for the **classic Zortrax M300**. Author: **Marcin Kowalik**, mkowalik@agh.edu.pl.

## Release scope / Zakres wydania

The publication is being assembled from the tested **M300Boot v1.1 + SD installer 1.1-i4** artifacts. This is **not** firmware for M300 Plus, M300 Dual or Inventure. Do not flash an Inventure binary onto an M300.

Hardware reported as tested by the owner: **one classic M300, PCB Rev. 5.3, menu hardware version 05, STM32F1 high-density device ID 0x414, 256 KiB of main Flash established by two matching internal SIZE-register reads**. The full MCU part marking was not reliably read; no exact ordering code is claimed. SWD originally displayed 512 KB, but the measured size is 256 KiB.

The owner confirmed upgrade from the custom M300Boot, completion of installer i4, restoration of the original **Zortrax 1.3.1** application, and successful startup. The factory-entry i4 route and ST-Link installation are documented separately; they must not be described as independently hardware-tested merely because the upgrade passed. These reports do not qualify power-loss recovery, arbitrary M300 revisions, or printing performance.

## Backup first / Najpierw kopia

Before changing anything, preserve the original bootloader, NVM/calibration/preferences, factory identity and operating-time records, UID, Option Bytes and the measured Flash size. Never upload personal dumps to a public issue.

**Do not disable RDP just to obtain a backup.** On this STM32F1, removing read protection erases main Flash. Preserve a verified copy before any destructive recovery. A temporary diagnostic application can export retained regions from internally executing code, but its installation replaces the previous application; this is not a pristine pre-update full dump.

## Distribution policy

Public firmware binaries and PL/EN operating instructions follow the Inventure publication model. No C/ASM firmware sources, ELF/map files, private full-Flash dumps, UID bytes, NVM or serial-number photographs are intended for publication.

**Important:** the existing i4 SD installer checks a fixed device profile, including identity hashes. It is not a universal installer for every PCB labelled HW05. These safety gates must not be removed to make an incompatible printer accept it. The final asset manifest will state the exact scope.

This initial documentation commit is not a claim that a GitHub Release or its assets have already been published.

Independent project; not affiliated with or endorsed by Zortrax or STMicroelectronics.
