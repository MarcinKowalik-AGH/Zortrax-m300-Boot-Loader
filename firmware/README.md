# Firmware packages

[English](README.md) · [Polski](README_PL.md)

| Version | Status | Files | Instructions |
|---|---|---|---|
| **v1.3.1** | **Current** | [Packages and SHA-256](v1.3.1) | [English manuals](../docs/en/v1.3.1/README.md) |
| v1.1 / i4 | Archive | [Original assets](v1.1) | [Historical manuals](../docs/en/v1.1/README.md) |

Choose UPGRADE for recognized custom M300Boot, FACTORY for recognized OEM v3 with the matching profile, or STLINK for the separately checked SWD procedure. The diagnostic 0.5.5 archive preserves original BOOT/NVM through its own backup workflow.

The release manifest and SHA-256 file beside each version identify its exact public ZIPs. Do not mix versions or confuse the BOOT intermediary M300APP.M3B with a Klipper MCU application. SD migration replaces APP temporarily; ST-Link preserves APP.

Documentation reorganization does not modify these packages or published release tags. [Current installation](../docs/en/v1.3.1/installation.md).
