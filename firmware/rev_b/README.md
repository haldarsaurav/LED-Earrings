# Rev B firmware — motion water earring

**Status:** source draft for the proposed ATtiny1616 board. It has not been compiled with megaTinyCore or flashed to hardware.

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

1. Install the current [megaTinyCore](https://github.com/SpenceKonde/megaTinyCore) in Arduino IDE. Its included `tinyNeoPixel_Static` library supports the modern tinyAVR parts.
2. Open `WaterEarring/WaterEarring.ino`. Choose ATtiny1616, a supported 16 or 20 MHz clock and your actual UPDI programmer. Keep PA0 configured as UPDI.
3. Compile before connecting a cell. Program through the P4 3V45, P2 GND and P3 UPDI pads with a programmer that senses target voltage. Battery installed and earring switch on. Do not feed 5 V onto 3V45. See [`PROGRAM_AND_TEST.md`](../../PROGRAM_AND_TEST.md) for the full home procedure.
4. Test one LED, then a short chain, then the full matrix from a current-limited supply. Verify color order, first pixel and sensor orientation. The firmware displays an automatic wave when the accelerometer is absent, allowing a visual bench test.

Short button press cycles water, heart, sparkle and rainbow. Long press cycles three restrained brightness budgets, now 10/16/24 channel-sum units for the 150 mAh cell. A hardware switch on the regulator enable pin is the true off control. A sustained low-battery reading blanks the LEDs until reset. The LED budget is a **software estimate**, not a certified current limit; measure real peak and average current and revise it before wearing.

## Source basis

- [megaTinyCore ATtiny1616 pin map](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/variants/txy6/pins_arduino.h)
- [megaTinyCore tinyNeoPixel_Static API](https://github.com/SpenceKonde/megaTinyCore/blob/master/megaavr/extras/tinyNeoPixel.md)
- [ST LIS2DW12 datasheet](https://www.st.com/resource/en/datasheet/lis2dw12.pdf)
