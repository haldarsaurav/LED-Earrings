# LED earrings — Rev B execution plan

_3 October 2026. This is the selected direction for the next prototype. The PCB is not ready to order._

## The product

Make a matched pair of black-PCB pixel earrings, each with an 8 × 10 RGB face, a rear insulated battery tray, a small button, a hard on/off switch and a steel jump ring and hook. A motion-aware cyan “water” animation should stay roughly level as the wearer tilts; a heart and two other effects provide gift-friendly alternatives. The pair runs independently and charges in a small common USB-C dock, with separate charging circuits in the earrings.

The proposed board is **26 × 42 mm** with a 2.4 mm LED pitch. The larger outline reserves 20 × 25 mm for the selected battery plus room for its wires and service pads. This is a fit target; actual footprints and comfort testing may change it.

## Decisions

- **Controller:** ATtiny1616, using the owned breakout and UPDI programmer for bench tests. The final board uses the bare chip. The older ESP32-C3 firmware remains useful for the existing 8 × 8 matrix prototype but is not the firmware for this PCB.
- **Motion:** LIS2DW12 accelerometer. Its gravity vector supplies the tilt; the firmware adds damping so the water surface sloshes briefly when moved. A six-axis gyro is unnecessary for this effect.
- **LED:** 80 × WS2812B-2020-V6, subject to validating the exact assembly footprint and first article. All 80 share a regulated nominal 3.45 V rail.
- **Power:** Akyga AKY0153 / LP402025, protected 1S 150 mAh, 20 × 25 × 4 mm, 5 g. Retain its PCM and use a separate Vishay NTCAFLEX05103GL 10 kΩ, B3435 temperature sensor pressed against the pouch. Verify physical fit and cell documentation before ordering boards.
- **Charging:** BQ25185 on each earring, targeting 30 mA charge with 10 kΩ ISET and 100 mA input limit with 24 kΩ ILIM/VSET, pending TI low-current compensation and bench verification. Two rear pogo contacts take 5 V/GND from a keyed USB-C dock.
- **Home programming:** four rear pads: dock 5 V, GND, UPDI and target 3V45. A separate 3-pin programming jig touches GND, UPDI and 3V45, with the battery installed and switch on; the programmer senses target voltage and must not inject 5 V. The back tray remains removable.
- **Regulation:** TPS63030 buck-boost, nominal 3.45 V in forced PWM while enabled. This is a design study to keep the LEDs above their 3.3 V minimum and the sensor below its 3.6 V maximum; verify worst-case voltage with a real circuit.
- **Case:** exposed front display and a removable, insulating rear tray. The parametric 3D model is in `mechanical/rev_b`.

## Build sequence

1. **Bench proof:** use the owned ESP32-C3 and 8 × 8 matrix to preview animations. Obtain the exact 2020 LED and LIS2DW12 sample. Run the new ATtiny1616 sketch on a small chain, then a dense test display. Record LED color order and sensor axis orientation.
2. **Power proof:** obtain the specified cell and NTC, verify their dimensions, polarity, maximum charge/discharge ratings and NTC thermal contact. Build the 3.45 V regulator and 30 mA charger test circuits. Measure voltage at battery full/low, display off/on and dock connected. Measure peak and average current for every effect and brightness step. At 150 mAh and 50 mA average, 3 h is ideal arithmetic only; actual runtime and safe current must be measured.
3. **Wearability proof:** print the tray and a dummy board, place the actual cell and components, weigh the assembly and test hook strength and comfort. Adjust board outline or battery if it is thick or heavy.
4. **Native CAD:** continue the saved [EasyEDA Rev B project](https://easyeda.com/haldarsaurav123456/led-earrings-rev-b-motion-water). It has the four sourced IC symbols and two WS2812B-2020-V6 symbols plus a provisional 26 × 42 mm PCB with five footprints. Capture the parts and pin-level nets in [PIN_CONNECTIONS.md](hardware/rev_b/PIN_CONNECTIONS.md) and the other 78 LEDs, then place and route the earring and a separate two-pocket charging-dock PCB. The LED library footprint is named for WS2815C-2020-4P, so compare pad geometry and pin 1 orientation against the exact Worldsemi LED before duplication. Run ERC and DRC, inspect manufacturing output and independently check charger, regulator and all 80 LED chain links.
5. **First article:** order a small prototype batch, build one board and prove charging, cutoff, regulator stability, LED current, temperature and runtime. Revise the design before assembling and gifting the matched pair.

## Current deliverables and limits

The folder contains an ATtiny firmware sketch **compiled** with megaTinyCore 2.6.11 and a reproducible build script and HEX, an animated motion-water preview, explicit 80-LED chain map, a pin-level capture contract and draft BOM, placement CSV, front/back board study, three OpenSCAD models and rendered STL **fit dummies**, plus a home programming/test guide. The saved EasyEDA schematic and PCB are partial. There are **no Gerbers or assembly files**. Battery fit, charging, NTC contact, runtime, flashing and PCB routing remain unverified. Ordering this revision now would be premature.
