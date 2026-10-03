# Rev B firmware — motion water earring

**Status:** compiled with Arduino CLI 1.5.2-rc.1 and megaTinyCore 2.6.11 for ATtiny1616 at 16 MHz. Build used 4537 / 16384 bytes flash and 357 / 2048 bytes static RAM. No hardware flash, current or sensor test has been performed.

## Hardware contract

| Signal | ATtiny1616 pad | Arduino name | Connection |
|---|---|---|---|
| LED_DIN | PA4 | `PIN_PA4` | 330 Ω then first WS2812B-2020-V6 DIN |
| BUTTON | PA6 | `PIN_PA6` | Normally open button to GND, internal pull-up |
| VBAT_SENSE | PA5 | `PIN_PA5` | 1 MΩ from battery, 330 kΩ to GND |
| SDA | PB1 | default Wire SDA | LIS2DW12 SDA, 10 kΩ pull-up to 3V45 |
| SCL | PB0 | default Wire SCL | LIS2DW12 SCL, 10 kΩ pull-up to 3V45 |
| UPDI | PA0 | — | Rear P3 programming pad, keep as UPDI |
| Target sense | VDD | — | Rear P4 3V45 pad for programmer voltage sensing only |

LIS2DW12 SA0 is tied to GND (I²C address 0x18); CS is tied to 3V45. The display is 8 × 10, starting at the top-left and snaking through rows. Change `SERPENTINE` or `FLIP_VERTICAL` if the actual routed chain differs. The earring's front X axis should point right and Y axis down. If sensor placement rotates the axes, adjust `readTiltTarget()`.

## Build and upload

1. Install [Arduino CLI](https://docs.arduino.cc/arduino-cli/installation) and [megaTinyCore](https://github.com/SpenceKonde/megaTinyCore). The verified build used megaTinyCore **2.6.11** and the included `tinyNeoPixel_Static` library.
2. Run `./firmware/rev_b/build.ps1` in PowerShell, or open `WaterEarring/WaterEarring.ino` in Arduino IDE. Choose ATtiny1616 at **16 MHz**, 2.6 V brown-out detector enabled and PA0 kept as UPDI. The build script records all board options and creates `WaterEarring_ATtiny1616_16MHz.hex`.
3. Compile before connecting a cell. Program through the P4 3V45, P2 GND and P3 UPDI pads with a programmer that senses target voltage. Battery installed and earring switch on. Do not feed 5 V onto 3V45. See [`PROGRAM_AND_TEST.md`](../../PROGRAM_AND_TEST.md) for the full home procedure.
4. Test one LED, then a short chain, then the full matrix from a current-limited supply. Verify color order, first pixel and sensor orientation. The firmware displays an automatic wave when the accelerometer is absent, allowing a visual bench test.

Short button press cycles water, heart, sparkle and rainbow. Long press cycles three restrained brightness budgets, now 10/16/24 channel-sum units for the 150 mAh cell. A hardware switch on the regulator enable pin is the true off control. A sustained low-battery reading blanks the LEDs until reset. The LED budget is a **software estimate**, not a certified current limit; measure real peak and average current and revise it before wearing.

For an assembled-unit check, **hold the effect button while switching on**. The first row shows one red, green and blue pixel. Column 5 is green if the LIS2DW12 responded and configured, red otherwise. Column 7 is green above 3.7 V, amber from 3.4–3.7 V and red below 3.4 V as estimated by the uncalibrated battery divider. Release the button and press it briefly to leave diagnostics. A green sensor indicator does not prove correct axis rotation; perform the tilt test separately.

`python firmware/rev_b/simulate.py` creates `water_preview.png` and `water_preview.gif`. They use the sketch's 8 × 10 surface and spring equations with a simulated tilt sweep. The animation is a visual preview, not a hardware measurement.

The checked `.hex` SHA-256 is `D03D51C9D4E94C5472F37E341999F4EA483CE88D4EE204009888D4E983B4F759`. Rebuild after any source, core or board-option change. The BOD menu choice is encoded in the build settings and may need a fuse-writing step on a blank part; confirm it when flashing with your actual UPDI programmer.

## Source basis

- [megaTinyCore ATtiny1616 pin map](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/variants/txy6/pins_arduino.h)
- [megaTinyCore tinyNeoPixel_Static API](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/extras/tinyNeoPixel.md)
- [ST LIS2DW12 datasheet](https://www.st.com/resource/en/datasheet/lis2dw12.pdf)
