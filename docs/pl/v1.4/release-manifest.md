# Manifest wydania — M300Boot 1.4

[English](../../en/v1.4/release-manifest.md) · [Polski](../../pl/v1.4/release-manifest.md) · [Index](README.md)

[Manifest maszynowy](../../../firmware/v1.4/RELEASE_MANIFEST.json) i [lista SHA-256](../../../firmware/v1.4/SHA256SUMS.txt) określają dokładne długości i tożsamości składników. Sprawdź pobrane archiwa przed rozpakowaniem. Nie łącz instalatora, docelowych segmentów ani walidatorów z różnych wydań.

| Plik | Zastosowanie |
|---|---|
| `M300Boot_v1.4_SD_UPGRADE.zip` | Rozpoznany własny BOOT; sześć płaskich plików SD |
| `M300Boot_v1.4_SD_FACTORY_OEMV3.zip` | Zakwalifikowany OEMv3; sześć płaskich plików SD |
| `M300Boot_v1.4_STLINK.zip` | Dwa adresowane obszary, rzadki HEX i narzędzia kontroli |
| `M300_BACKUP_0.5.5_UART.zip` | Niezależna niezmieniona diagnostyka; zachowuje własną wersję i instrukcję |

Stały BOOT i instalator pośredni mają 1.4. Oryginalna aplikacja Zortraxa w RESTORE.BIN pozostaje 1.3.1. Diagnostyka pozostaje 0.5.5. Techniczna numeracja kontenera OEM jest niezależna. To rozróżnienie pozwala odróżnić stary BOOT lub instalator od nowego wydania.

Firmware jest udostępniany jako binaria, z narzędziami hosta i instrukcjami EN/PL. Prywatne C/ASM, linker/ELF/mapy, narzędzia kluczy OEM i dane drukarki są wyłączone. Archiwalne składniki1.3.1 i1.1 pozostają niezmienione. Ilustracje 1.4 powstają z renderera OLED wydania, z oryginalnymi znakami i pikselami ekranu cyan. [Kolejność instalacji](installation.md) · [Walidacja](validation.md).
