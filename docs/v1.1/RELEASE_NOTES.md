# M300 boot v1.1 · SD installer 1.1-i4

Independent service bootloader for **classic Zortrax M300**, tested on one **PCB Rev.5.3 / HW05 / measured 256-KiB STM32F1 high-density** unit. Original bootloader: OEM v3; original printer application: **1.3.1**. The owner confirmed custom-boot upgrade through i4 and subsequent successful stock 1.3.1 startup. FACTORY i4 and ST-Link programming are separately documented, not independently hardware-qualified.

## Choose your package

- **SD_UPGRADE_i4:** for an existing recognized M300Boot FULL.
- **SD_FACTORY_OEMV3_i4:** factory entry via recognized OEM v3.
- **STLINK_LOCAL_BUILDER:** exact stage2/assets plus a LOCAL generator using your OWN complete verified backup. No personal full-Flash image is published.
- **BACKUP_0.5.5_UART:** temporary diagnostic firmware plus read-only host to preserve OEM BOOT, NVM/factory, UID, SIZE and options before migration. Its installation replaces the application first, so the resulting full snapshot is post-update.

**All installation routes remain profile-gated to the qualified device. HW05 alone is not enough. Other units require independent qualification; do not remove identity checks.** Backup before any write. Removing active STM32F1 RDP causes mass erase; do not use it to obtain a backup. No automatic power-loss rollback.

Firmware is binary-only, without private raw UID/NVM/full-Flash dumps, sources/ELF/maps or vendor-key tools. RESTORE.BIN contains the original 1.3.1 and retains manufacturer rights. Full PL/EN instructions are in docs, SHA-256 beside the assets.


[Dokumentacja v1.1 / v1.1 documentation](README.md)
