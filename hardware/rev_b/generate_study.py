"""Generate a coordinate-accurate board study and LED chain CSV (not fabrication data)."""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).parent
BOARD_W, BOARD_H = 26.0, 42.0
COLS, ROWS, PITCH = 8, 10, 2.4
X0, Y0 = 4.6, 8.0


def led_order():
    for y in range(ROWS):
        for step in range(COLS):
            x = step if y % 2 == 0 else COLS - 1 - step
            yield y * COLS + step + 1, x, y, X0 + PITCH * x, Y0 + PITCH * y


leds = list(led_order())
assert len(leds) == 80
assert len({(x, y) for _, x, y, _, _ in leds}) == 80
assert all(1 < px - 1 and px + 1 < BOARD_W - 1 and 6 < py - 1 and py + 1 < BOARD_H - 6
           for _, _, _, px, py in leds)
with (HERE / "led_chain.csv").open("w", newline="", encoding="utf-8") as fh:
    out = csv.writer(fh)
    out.writerow(["index", "reference", "x", "y", "center_x_mm", "center_y_mm", "DIN_net", "DOUT_net"])
    for index, x, y, px, py in leds:
        out.writerow([index, f"LED{index:02d}", x, y, f"{px:.2f}", f"{py:.2f}",
                      f"LED_DATA_{index-1}", f"LED_DATA_{index}" if index < 80 else "NC"])

with (HERE / "placements.csv").open("w", newline="", encoding="utf-8") as fh:
    out = csv.writer(fh)
    out.writerow(["reference", "side", "center_x_mm", "center_y_mm", "note"])
    for index, x, y, px, py in leds:
        out.writerow([f"LED{index:02d}", "front", f"{px:.2f}", f"{py:.2f}", "2.4 mm pitch; rotation TBD"])
    for ref, x, y, note in [
        ("HOOK", 13, 2.7, "1.5 mm mechanical hole, copper clearance TBD"),
        ("U1_MCU", 5.5, 35.2, "ATtiny1616; provisional reservation"),
        ("U2_CHARGER", 11, 35.2, "BQ25185; provisional reservation"),
        ("U3_REG", 17, 35.2, "TPS63030 + inductor; provisional reservation"),
        ("U4_ACCEL", 22, 35.2, "LIS2DW12; axes TBD"),
        ("BAT", 13, 19, "rear 20 x 25 x 4 mm protected cell + NTC; wire space TBD"),
        ("P1_5V", 4, 39.5, "rear charging pad; keyed dock"),
        ("P2_GND", 10, 39.5, "rear charging/programming pad"),
        ("P3_UPDI", 16, 39.5, "rear programming pad; no dock contact"),
        ("P4_3V45", 22, 39.5, "rear programmer target-voltage sense; no dock contact"),
    ]:
        out.writerow([ref, "mechanical" if ref == "HOOK" else "rear", x, y, note])

scale = 12
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 590">',
    '<style>text{font-family:Arial,sans-serif;fill:#e7edf7} .small{font-size:11px;fill:#a9bacb} .label{font-size:14px;font-weight:bold}</style>',
    '<rect width="700" height="540" fill="#101820"/>',
    '<text class="label" x="62" y="28">FRONT · LED face</text><text class="label" x="390" y="28">BACK · space study</text>',
]


def rect(x, y, w, h, fill, stroke="#8fb7b5", rx=0):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')


for ox in (50, 390):
    rect(ox, 46, BOARD_W * scale, BOARD_H * scale, "#142b2b", "#93c7bf", 24)
    parts.append(f'<circle cx="{ox+13*scale}" cy="{46+2.7*scale}" r="9" fill="#101820" stroke="#e7edf7"/>')

for index, x, y, px, py in leds:
    cx, cy = 50 + px * scale, 46 + py * scale
    rect(cx - 12, cy - 12, 24, 24, "#172632", "#516e74", 4)
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#75dcf4"/>')

ox = 390
rect(ox + 3*scale, 46 + 7*scale, 20*scale, 25*scale, "#26353a", "#e0ae7e", 8)
parts.append(f'<text class="small" x="{ox+8*scale}" y="{46+19*scale}">CELL</text>')
for label, x, w in [("MCU", 2, 4), ("CHG", 7.5, 4), ("REG", 13, 4), ("ACC", 19, 4)]:
    rect(ox + x*scale, 46 + 34*scale, w*scale, 3.2*scale, "#314a52", "#d3e0de", 4)
    parts.append(f'<text class="small" x="{ox+(x+0.2)*scale}" y="{46+36*scale}">{label}</text>')
for label, x in [("5V", 4), ("GND", 10), ("UPDI", 16), ("VTG", 22)]:
    parts.append(f'<circle cx="{ox+x*scale}" cy="{46+39.5*scale}" r="7" fill="#d2aa5d"/>')
    parts.append(f'<text class="small" x="{ox+(x-1.5)*scale}" y="{46+41*scale}">{label}</text>')
parts.append('<text class="small" x="50" y="575">26 × 42 mm board · outline and placements provisional · NO COPPER / NO GERBERS</text></svg>')
(HERE / "board_study.svg").write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {len(leds)} LED positions and board study to {HERE}")
