# M300Boot 1.4 — OLED renders

These PNGs are rendered by the actual bootloader and installer C OLED code with the original packed M300 bitmap font and ring resources. They are not photographs or evidence of a hardware test.

The native framebuffer is 256 × 64. Documentation previews are enlarged to 1024 × 256 using nearest-neighbour scaling. Cyan (#00FFFF) replaces full grayscale brightness; all 16 intensity levels are preserved against black.

Menus use their real label tables and viewport code. Countdown, progress and result frames are deterministic illustrative states. Hardware pages deliberately use unavailable information, so no device serial number, unique identifiers or real operating-time values are published. The compiled Device decoder is used only to format the invalid-information fixture; no private Flash backup is read.

The UART default preview selects 250000 in the actual menu. The other UART preview scrolls to 1500000; together they show all five selectable rates.

RENDER_MANIFEST.json records renderer inputs and source/framebuffer/PNG SHA-256 values.
