# Rev B home programming and first-article checks

This is the intended service procedure for **each** earring. The EasyEDA board and printed fixture are still drafts; confirm actual pad coordinates and polarity on the manufactured PCB before using them. Record measurements for left and right earrings separately.

## Access and tools

- Keep the rear tray removable. The four rear pads, left to right in the board study, are **P1 DOCK_5V, P2 GND, P3 UPDI, P4 VTG_3V45**. The gift dock contacts only P1 and P2. A separate, clearly marked three-pin service jig contacts P2, P3 and P4.
- Use the owned UPDI programmer only if it supports an **externally powered 3.45 V target** and voltage sensing. Connect its ground to P2, UPDI to P3 and target-voltage sense to P4. P4 is not a power input. Never connect the programmer's 5 V output or the dock's P1 to P4 or P3. Check the specific programmer's manual before wiring the jig.
- With the cell installed, switch the earring on to bring up 3V45 for programming. Measure P4 to P2 with a meter before connecting the programmer. Keep the charging dock disconnected during programming.
- Open `firmware/rev_b/WaterEarring/WaterEarring.ino` in Arduino IDE with [megaTinyCore](https://github.com/SpenceKonde/megaTinyCore) installed. Select **ATtiny1616**, the clock setting used for the build, and the actual compatible UPDI programmer. Keep PA0 as UPDI. Compile, then use the programmer upload action appropriate to that programmer. Save the successful core version, board settings, fuse settings and upload log in your own build record. Never select a fuse setting that turns UPDI into GPIO.
- If using a Microchip programmer instead of an Arduino-compatible upload device, export a compiled `.hex` from the IDE and use that programmer's supported AVR UPDI software. Verify its target-voltage and pin mapping first. Do not assume a generic USB serial adapter can safely sense a 3.45 V target.

The service jig and tray in `mechanical/rev_b` are mechanical starts. A keyed shape and insulation around all pins must be proven with the actual spring contacts. Hold the earring still during flashing. Disconnect the jig before wearing.

## Bench sequence before connecting a cell

1. Inspect both PCB faces under magnification: LED orientation and 80-link data chain, IC pin 1 markers, QFN exposed pads, solder bridges, hook-hole clearance, charging-pad labeling and insulating film coverage.
2. With **no battery and no USB**, check resistance between GND and BAT, SYS, 3V45 and DOCK_5V. Investigate any near-short. Check that P1 is isolated from BAT/SYS/3V45 and P2 really is ground. Check that P3 reaches PA0 and P4 reaches the 3V45 rail.
3. Confirm the cell's connector polarity by meter, independent of wire colors. Confirm the actual charger footprint pin map and battery connector polarity before inserting the cell. The selected [Akyga AKY0153](https://b2b.akyga.com/en/eacuxxxaky-08771-aky0153.html) includes PCM but has no built-in temperature lead; mount the separate [Vishay flex NTC](https://www.vishay.com/doc/?29132=) flat against the pouch with insulating, temperature-appropriate adhesive and strain relief.
4. Verify the NTC reads near 10 kΩ around 25 °C and that its two leads are isolated from the cell terminals. Inspect the charger TS/MR network against the final TI design before first charge. Do not substitute a fixed resistor for a worn, rechargeable product.

## Powered bring-up

1. Prefer a current-limited bench setup with the cell disconnected for first power tests. Inject only at the approved BAT test interface, never through the exposed 3V45 sense pad, and use the regulator/charger data sheets to set safe limits. Verify rail voltages with the LEDs disabled before increasing current limit.
2. Connect the protected cell with the switch **off**. Measure BAT, SYS and P4 relative to P2. When switched on, P4 should be near the design target of 3.45 V. Test at cell full and near the chosen low-battery threshold; the LIS2DW12 supply must remain below 3.6 V and the WS2812B-2020-V6 supply above 3.3 V while active. These are release measurements, not assumed outcomes.
3. Flash firmware via P2/P3/P4. Read back/verify the programmed flash if the programmer supports it. Confirm first pixel, serpentine order, RGB color order, button modes and water surface tilt in all orientations. If the accelerometer is absent, the draft firmware shows an automatic wave for a bench visual check; that fallback is not proof of I²C operation.
4. Measure **peak and average cell current** in startup, water, heart, sparkle, rainbow and all three brightness settings. Include low-cell operation and LED transitions. The selected cell is rated at 150 mAh; keep the final measured pulse and sustained current within its documented limits and PCM behavior. The firmware's brightness budget is only an estimate.
5. Check low-battery blanking, the switch-off drain, and reprogramming after full assembly. The switch should leave the charger operative but turn off the regulator and display.

## Charging and wearable checks

1. Power the dock from a known 5 V USB-C source with **no earring inserted**. Check both pogo pairs for 5 V and correct polarity. Check that there is no 5 V on either UPDI/VTG position and that reversing an earring cannot short contacts. The current dock model does not yet provide this keying, so it is a fit study only.
2. Dock one earring with its switch off. Confirm the proposed charger setting produces roughly 30 mA initial battery charge current where the cell state permits it, and that charge tapers and terminates. Repeat with the second earring and both together. Measure cell and skin-side temperatures. Test that cold/hot or disconnected NTC conditions stop charging as specified by the final charger design.
3. Run a timed discharge from full charge to firmware cutoff in the intended water mode. Record runtime, average current and outside case temperature. Aim for at least two useful hours, but use measured results to set final brightness. Charge, unplug and re-run the effect to check repeatability.
4. Weigh each complete earring, test the hook/jump-ring pull path, wear the unpowered dummy first, then the powered unit. Inspect the removable tray, cell strain relief and insulation after handling. Never wear a unit with a damaged or swollen pouch.

## PCB release record

Before ordering the PCB, attach to the EasyEDA project: exact BOM/footprints, ERC and DRC results, checked Gerbers, the verified LED chain map, pad polarity drawing, charger/NTC test result, measured rail tolerance and a photo of the cell fitting in the printed dummy. After first article, record firmware version and test measurements for both pieces. A passing design review is required before ordering the gift pair.
