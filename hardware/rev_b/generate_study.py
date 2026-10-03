"""Generate a coordinate-accurate board study and LED chain CSV (not fabrication data)."""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).parent
BOARD_W, BOARD_H = 24.0, 38.0
COLS, ROWS, PITCH = 8, 10, 2.4
X0, Y0 = 3.6, 8.0


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
        ("HOOK", 12, 2.7, "1.5 mm mechanical hole, copper clearance TBD"),
        ("U1_MCU", 6, 33.2, "ATtiny1616; provisional reservation"),
        ("U2_CHARGER", 11, 33.2, "BQ25185; provisional reservation"),
        ("U3_REG", 16, 33.2, "TPS63030 + inductor; provisional reservation"),
        ("U4_ACCEL", 20.5, 33.2, "LIS2DW12; axes TBD"),
        ("BAT", 12, 19, "rear cell envelope 18 x 24 mm; overlaps circuitry vertically"),
        ("P1_5V", 5, 36, "rear charging pad"),
        ("P2_GND", 12, 36, "rear charging pad"),
        ("P3_UPDI", 19, 36, "rear programming pad"),
    ]:
        out.writerow([ref, "mechanical" if ref == "HOOK" else "rear", x, y, note])

scale = 12
parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 540">',
    '<style>text{font-family:Arial,sans-serif;fill:#e7edf7} .small{font-size:11px;fill:#a9bacb} .label{font-size:14px;font-weight:bold}</style>',
    '<rect width="700" height="540" fill="#101820"/>',
    '<text class="label" x="62" y="28">FRONT · LED face</text><text class="label" x="390" y="28">BACK · space study</text>',
]


def rect(x, y, w, h, fill, stroke="#8fb7b5", rx=0):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>')


for ox in (50, 378):
    rect(ox, 46, BOARD_W * scale, BOARD_H * scale, "#142b2b", "#93c7bf", 24)
    parts.append(f'<circle cx="{ox+12*scale}" cy="{46+2.7*scale}" r="9" fill="#101820" stroke="#e7edf7"/>')

for index, x, y, px, py in leds:
    cx, cy = 50 + px * scale, 46 + py * scale
    rect(cx - 12, cy - 12, 24, 24, "#172632", "#516e74", 4)
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="#75dcf4"/>')

ox = 378
rect(ox + 3*scale, 46 + 7*scale, 18*scale, 24*scale, "#26353a", "#e0ae7e", 8)
parts.append(f'<text class="small" x="{ox+8*scale}" y="{46+19*scale}">CELL</text>')
for label, x, w in [("MCU", 2.5, 4), ("CHG", 7.2, 4), ("REG", 12, 4), ("ACC", 17, 4)]:
    rect(ox + x*scale, 46 + 31*scale, w*scale, 3.2*scale, "#314a52", "#d3e0de", 4)
    parts.append(f'<text class="small" x="{ox+(x+0.2)*scale}" y="{46+33*scale}">{label}</text>')
for label, x in [("5V", 5), ("GND", 12), ("UPDI", 19)]:
    parts.append(f'<circle cx="{ox+x*scale}" cy="{46+36*scale}" r="7" fill="#d2aa5d"/>')
    parts.append(f'<text class="small" x="{ox+(x-1.5)*scale}" y="{46+37.6*scale}">{label}</text>')
parts.append('<text class="small" x="50" y="530">24 × 38 mm board · outline and placements provisional · NO COPPER / NO GERBERS</text></svg>')
(HERE / "board_study.svg").write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {len(leds)} LED positions and board study to {HERE}")
