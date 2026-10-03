# Rev B earring schematic capture contract

This is the pin-by-pin capture checklist for **one** earring. Build two identical copies. It complements `led_chain.csv`, which lists all 80 LED positions and data links. It is not an ERC-checked schematic or a manufacturing netlist.

## Power and charging

| Ref | Pin | Net or connection |
|---|---:|---|
| P1 rear pad | 1 | DOCK_5V, to U3 IN and C1 |
| P2 rear pad | 1 | GND |
| B1 protected 1S cell | + | BAT; verify connector polarity by meter |
| B1 | − | GND |
| TH1 pouch NTC 10 kΩ B3435 | 1 | U3 TS/MR |
| TH1 | 2 | GND |
| U3 BQ25185DLHR | 1 SYS | SYS; C2 and U4 VIN/VINA |
| U3 | 2 BAT | BAT; C3 and R4 high side |
| U3 | 3 STAT2 | Test point or explicit no-connect |
| U3 | 4 /CE | GND so charging is enabled when dock power is present |
| U3 | 5 GND, 11 exposed pad | GND plane |
| U3 | 6 TS/MR | TH1 to GND, thermally attached to the cell |
| U3 | 7 ILIM/VSET | R7 24 kΩ 1% to GND: 4.2 V cell / 100 mA input setting |
| U3 | 8 ISET | R6 10 kΩ 1% to GND: nominal 30 mA charge; reserve footprint for low-current compensation per TI |
| U3 | 9 STAT1 | Test point or explicit no-connect |
| U3 | 10 IN | DOCK_5V; C1 close to pin |
| U4 TPS63030DSKR | 1 VOUT | 3V45; C6/C7 output capacitors, R8 feedback top |
| U4 | 2 L2, 4 L1 | L1 1.5 µH between these pins; place very close |
| U4 | 3 PGND, 9 GND, 11 exposed pad | GND plane |
| U4 | 5 VIN, 8 VINA | SYS; C4 10 µF and C5 100 nF close to pins |
| U4 | 6 EN | SW1 common; SW1 chooses SYS (on) or GND (off), never floats |
| U4 | 7 PS/SYNC | SYS for forced PWM |
| U4 | 10 FB | Junction of R8 1.18 MΩ to 3V45 and R9 200 kΩ to GND |

C1 is 1 µF from DOCK_5V to GND; C2 10 µF SYS to GND; C3 1 µF BAT to GND. Follow the [BQ25185 datasheet](https://www.ti.com/lit/ds/symlink/bq25185.pdf) for voltage rating and capacitance after DC bias. C4 is 10 µF SYS to GND; C5 100 nF SYS to GND; C6 and C7 are each 10 µF 3V45 to GND. Follow the [TPS63030 datasheet](https://www.ti.com/lit/ds/symlink/tps63030.pdf) for the inductor saturation rating, capacitor DC-bias performance and the very short switching loop. The 3.45 V resistor pair gives an ideal 0.5 × (1 + 1.18 M / 200 k) = 3.45 V. At ±1% resistors and the specified 0.495–0.505 V forced-PWM feedback range, the simple DC divider calculation spans about **3.36–3.55 V** before layout, ripple and load transients. Measure the actual output; the sensor limit is 3.6 V and the LEDs need at least 3.3 V.

The charger datasheet recommends additional ISET compensation below 50 mA. The exact network needs a bench check at 30 mA; include nearby optional pads before a board release. Do not call this charging design validated solely from the resistor equation.

## Controller, accelerometer and LEDs

| Ref | Pin | Net or connection |
|---|---:|---|
| U1 ATtiny1616-MNR | 3 GND, 21 exposed pad | GND |
| U1 | 4 VDD | 3V45; C8 100 nF to GND at pin |
| U1 | 5 PA4 | R1 330 Ω to LED_DATA_0 = LED01 DI |
| U1 | 6 PA5 | VBAT_SENSE; R4 1 MΩ to BAT, R5 330 kΩ to GND |
| U1 | 7 PA6 | BTN1 normally open to GND, firmware internal pull-up |
| U1 | 13 PB1 | SDA; R2 10 kΩ to 3V45; U2 pin 4 |
| U1 | 14 PB0 | SCL; R3 10 kΩ to 3V45; U2 pin 1 |
| U1 | 19 PA0/UPDI | P3 rear programming pad; keep UPDI fuse function |
| U2 LIS2DW12TR | 1 SCL, 4 SDA | SCL and SDA nets above |
| U2 | 2 CS | 3V45 for I²C |
| U2 | 3 SA0 | GND for 7-bit address 0x18 |
| U2 | 5 NC | Explicit no-connect |
| U2 | 6 GND, 7 RES, 8 GND | GND |
| U2 | 9 VDD, 10 VDDIO | 3V45; C9 100 nF at the package |
| U2 | 11 INT2, 12 INT1 | Explicit no-connect in this polling firmware |
| P4 rear pad | 1 | 3V45 target-voltage sense; programmer must not drive it |
| LED01…LED80 WS2812B-2020-V6 | 4 VDD, 2 GND | 3V45 and GND; C10 10 µF bulk near array feed |
| LED01…LED80 | 3 DI, 1 DO | Follow every adjacent `DIN_net`/`DOUT_net` in `led_chain.csv`; LED80 DO is a declared no-connect |

Use the [ST LIS2DW12 datasheet](https://www.st.com/resource/en/datasheet/lis2dw12.pdf) for sensor pin 7 RES to GND and 10 kΩ I²C pull-ups. The schematic must explicitly mark unused pins so ERC can distinguish intentional no-connects from missed wires. Check Worldsemi's exact LED pin 1 mark against the chosen EasyEDA footprint **before** multiplying the symbol or generating placement files.

## Charging dock PCB

The dock is a separate USB-C **sink**, carrying USB 5 V and GND only. Put 5.1 kΩ Rd from each CC1 and CC2 pin to GND on the dock PCB. Feed both keyed pogo pairs in parallel through a suitable protected 5 V path; each earring limits its own input current to 100 mA. Align the positive spring only to P1 and the negative spring only to P2. Leave P3/P4 completely inaccessible to the gift dock. Choose the exact USB-C receptacle, ESD device, fuse and spring contacts from real mechanical drawings, then verify source detection and polarity before connecting cells. The printed dock STL is a fit dummy until those parts and the dock PCB are final.
