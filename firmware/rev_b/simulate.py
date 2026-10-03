"""Preview the Rev B 8x10 water effect; no hardware or Arduino install needed.

The pixel and spring equations mirror WaterEarring.ino. The simulated tilt is
only an input demonstration and does not claim measured sensor response.
"""

from math import pi, sin, tan
from pathlib import Path

from PIL import Image, ImageDraw


OUT = Path(__file__).parent
FRAMES = 100
WIDTH, HEIGHT = 8, 10
CELL = 36
START_X, START_Y = 116, 250


def make_frame(frame_number: int, slope_q8: int) -> Image.Image:
    image = Image.new("RGB", (520, 800), "#101621")
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((84, 120, 436, 728), radius=50, fill="#252d3b", outline="#4b596b", width=4)
    draw.ellipse((246, 82, 274, 110), outline="#b8c7d6", width=6)
    draw.arc((250, 56, 270, 100), 175, 365, fill="#c4d1dc", width=5)
    draw.text((112, 158), "TIDAL LIGHT", fill="#a8cee9")
    draw.text((112, 189), "motion water preview", fill="#778ea4")
    for x in range(WIDTH):
        dx2 = x * 2 - (WIDTH - 1)
        wave = 18 if (frame_number + x * 7) % 23 < 5 else 0
        surface = 6 * 256 + (slope_q8 * dx2) // 2 + wave
        for y in range(HEIGHT):
            point = y * 256
            if point >= surface:
                color = "#087bad" if (x + y + frame_number // 4) % 5 else "#16a8cf"
            elif point + 256 >= surface:
                color = "#56c3da"
            else:
                color = "#0b1827"
            x0, y0 = START_X + x * CELL, START_Y + y * CELL
            draw.rounded_rectangle((x0, y0, x0 + 29, y0 + 29), radius=5, fill=color)
    draw.text((113, 663), "8 x 10 RGB  |  accelerometer tilt", fill="#a8cee9")
    return image


def main() -> None:
    slope_q8 = 0
    slope_speed = 0
    frames = []
    for frame_number in range(FRAMES):
        angle = 32 * sin(2 * pi * frame_number / FRAMES)
        target = round(-tan(angle * pi / 180) * 256)
        target = max(-320, min(320, target))
        slope_speed += (target - slope_q8) // 7 - slope_speed // 4
        slope_q8 += slope_speed // 4
        frames.append(make_frame(frame_number, slope_q8))
    frames[0].save(OUT / "water_preview.png")
    frames[0].save(
        OUT / "water_preview.gif", save_all=True, append_images=frames[1:],
        duration=40, loop=0, optimize=True,
    )


if __name__ == "__main__":
    main()
