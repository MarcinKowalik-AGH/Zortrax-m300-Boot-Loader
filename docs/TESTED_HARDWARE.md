# Tested hardware — M300 boot v1.1 / installer 1.1-i4

Publication documentation: 29 October 2026. This table records project evidence, not manufacturer certification.

| Parameter | Established value |
|---|---|
| Printer | One classic Zortrax M300; not Plus/Dual/Android |
| Mainboard marking | PCB Rev.5.3, photographed |
| Stock menu hardware | 05; raw factory record E5 |
| MCU family | STM32F101/F103 high-density reported by ST-Link; target F103-family Cortex-M3 |
| Exact ordering code | Not established; chip marking not reliably legible |
| SWD device/silicon ID | 0x414 / Rev X |
| CPUID | 0x411FC231 |
| Main Flash | 256 KiB from matching internal SIZE reads, corroborated in SYSROM |
| Geometry | 128 pages of 2048 B; 0x08000000–0x0803FFFF |
| Original bootloader | Zortrax Bootloader v3, 32 KiB recovered |
| Original application | M300 1.3.1; owner also tested 1.3.1 → 1.2.0 → 1.3.1 |
| Protection during migration | RDP active, extra WRP inactive; options preserved |
| Host and probe | MacBook Air/macOS, Python 3.9/3.11, pySerial 3.5, CubeProgrammer 2.23.0, STLINK-V3SET and VCP 250000 8N1 |
| Input/display | OLED, encoder rotation both ways, click/Back, bounded scrolling and responsive rc3-derived rendering confirmed |

The old GUI report of 512 KB and diagnostic string 512_PRIOR_SWD are not the accepted capacity. Two SIZE reads gave 00 01, i.e. 256 KiB.

The owner confirmed complete custom-boot UPGRADE via corrected i4 to v1.1 and successful restoration/startup of original 1.3.1. Earlier records verify exact rc3/stock readback, paired full dumps and retained printer data. One unit has been qualified.

Not established: a separate FACTORY i4 execution, physical v1.1 programming/recovery through ST-Link, power-loss behavior, all menu/baud combinations, full printing qualification or other PCB revisions.

Unchanged i4 uses a fixed qualified identity profile. Two boards with the same HW05 label may still differ. A mismatch is not permission to patch hashes, clone identity, erase factory data or remove protection. Another unit requires independent qualification/build. No raw UID, private serial or personal snapshot is published.
