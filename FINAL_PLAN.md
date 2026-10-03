# LED earrings — Rev B execution plan

_3 October 2026. This is the selected direction for the next prototype, not a claim that a PCB is ready to order._

## The product

Make a matched pair of black-PCB pixel earrings, each with an 8 × 10 RGB face, a rear insulated battery tray, a small button, a hard on/off switch and a steel jump ring and hook. A motion-aware cyan “water” animation should stay roughly level as the wearer tilts; a heart and two other effects provide gift-friendly alternatives. The pair runs independently and charges in a small common USB-C dock, with separate charging circuits in the earrings.

The proposed board is **24 × 38 mm** with a 2.4 mm LED pitch. This is a fit target. Comfort, electronics packing and battery dimensions can force a size change.

## Decisions

- **Controller:** ATtiny1616, using the owned breakout and UPDI programmer for bench tests. The final board uses the bare chip. The older ESP32-C3 firmware remains useful for the existing 8 × 8 matrix prototype but is not the firmware for this PCB.
- **Motion:** LIS2DW12 accelerometer. Its gravity vector supplies the tilt; the firmware adds damping so the water surface sloshes briefly when moved. A six-axis gyro is unnecessary for this effect.
- **LED:** 80 × WS2812B-2020-V6, subject to validating the exact assembly footprint and first article. All 80 share a regulated nominal 3.45 V rail.
- **Power:** a protected 1S LiPo, target 120–150 mAh. The exact cell, charge limit and NTC determine the final charger settings and enclosure.
- **Charging:** BQ25185 on each earring, with two rear pogo contacts for 5 V/GND. USB-C sits on the separate dock, which powers the two charger inputs in parallel. A third earring pad exposes UPDI for development but is absent from the daily dock.
- **Regulation:** TPS63030 buck-boost, nominal 3.45 V in forced PWM while enabled. This is a design study to keep the LEDs above their 3.3 V minimum and the sensor below its 3.6 V maximum; verify worst-case voltage with a real circuit.
- **Case:** exposed front display and a removable, insulating rear tray. The parametric 3D model is in `mechanical/rev_b`.

## Build sequence

1. **Bench proof:** use the owned ESP32-C3 and 8 × 8 matrix to preview animations. Obtain the exact 2020 LED and LIS2DW12 sample. Run the new ATtiny1616 sketch on a small chain, then a dense test display. Record LED color order and sensor axis orientation.
2. **Power proof:** choose the actual protected cell. Configure and test BQ25185 with that cell's NTC and recommended charge current. Build the 3.45 V regulator test circuit and measure voltage at battery full/low, display off/on and dock connected. Measure current for every effect and all brightness steps. At 120 mAh and 50 mA average, 2.4 h is only an ideal arithmetic upper bound; actual runtime must be measured.
3. **Wearability proof:** print the tray and a dummy board, place the actual cell and components, weigh the assembly and test hook strength and comfort. Adjust board outline or battery if it is thick or heavy.
4. **Native CAD:** sign in to EasyEDA, capture the named nets from `hardware/rev_b/README.md` using exact vendor parts, then route the board. Run ERC and DRC, inspect the manufacturing output and independently check charger, regulator and every LED chain connection. Create a separate two-pocket charging-dock PCB and fit-checked dock shell.
5. **First article:** order a small prototype batch, build one board and prove charging, cutoff, regulator stability, LED current, temperature and runtime. Revise the design before assembling and gifting the matched pair.

## Current deliverables and limits

The new folder contains a draft ATtiny firmware sketch, explicit 80-LED chain map, placement CSV, front/back board study and parametric tray. They are starting points for EasyEDA and OpenSCAD, **not Gerbers, assembly files or a final STL**. No exact battery, tested charge current, verified cell temperature sensing, measured runtime, compiled ATtiny binary or completed PCB routing exists yet. Ordering this revision now would be premature.
