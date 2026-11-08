# Release manifest — M300Boot 1.4

[English](../../en/v1.4/release-manifest.md) · [Polski](../../pl/v1.4/release-manifest.md) · [Index](README.md)

The [machine-readable manifest](../../../firmware/v1.4/RELEASE_MANIFEST.json) and [SHA-256 list](../../../firmware/v1.4/SHA256SUMS.txt) are authoritative for exact byte lengths and identities. Verify the downloaded archives before extraction. Do not mix an installer, target segments or host validators from different releases.

| File | Use |
|---|---|
| `M300Boot_v1.4_SD_UPGRADE.zip` | Recognized custom BOOT; six flat SD files |
| `M300Boot_v1.4_SD_FACTORY_OEMV3.zip` | Qualified OEMv3; six flat SD files |
| `M300Boot_v1.4_STLINK.zip` | Two addressed target slots, sparse HEX and offline tools |
| `M300_BACKUP_0.5.5_UART.zip` | Independent unchanged diagnostic; keep its own version/instructions |

The permanent BOOT and SD intermediary are 1.4. The original Zortrax application in RESTORE.BIN remains 1.3.1. The diagnostic remains 0.5.5. Technical OEM container numbering is independent. These distinctions prevent an old boot or intermediary from being mistaken for the new release.

Firmware is distributed as binaries, with operational host tools and EN/PL manuals. Private C/ASM, linker/ELF/maps, OEM-key tools and personal printer data are excluded. Historical 1.3.1 and1.1 assets remain unchanged. Current 1.4 images are generated from the release OLED renderer with original glyphs and cyan display pixels. [Installation sequence](installation.md) · [Validation](validation.md).

The [original Zortrax Bootloader v3](../../../firmware/original/README.md) is published separately as an unmodified 32-KiB raw binary with provenance and SHA-256. It is outside the immutable 1.4 installation asset catalog. The later [owner hardware acceptance](../../reports/v1.4/HARDWARE_ACCEPTANCE.json) supplements the publication-time manifest without changing it.
