"""Render an illustrative water/heart preview. No measured brightness is implied."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
im = Image.new("RGB", (1040, 470), "#101820")
d = ImageDraw.Draw(im)
font_path = Path("C:/Windows/Fonts/segoeui.ttf")
bold_path = Path("C:/Windows/Fonts/segoeuib.ttf")
font = ImageFont.truetype(str(font_path), 18) if font_path.exists() else ImageFont.load_default()
bold = ImageFont.truetype(str(bold_path), 24) if bold_path.exists() else font
d.text((32, 20), "Motion-water LED earrings", font=bold, fill="#f3f6f5")
d.text((32, 53), "8 × 10 pixel face  ·  provisional 26 × 42 mm board  ·  illustration only", font=font, fill="#a5b8bc")


def board(ox, title, slope=0, heart=False):
    oy, bw, bh = 105, 232, 320
    d.rounded_rectangle((ox, oy, ox + bw, oy + bh), radius=22, fill="#182829", outline="#5f8385", width=3)
    d.ellipse((ox + 105, oy + 9, ox + 127, oy + 31), fill="#101820", outline="#a5b8bc", width=2)
    for y in range(10):
        for x in range(8):
            cx = ox + 28 + x * 25.2
            cy = oy + 53 + y * 25.5
            active = y >= 6 + slope * (x - 3.5)
            if heart:
                rows = [0, 0b01100110, 0b11111111, 0b11111111, 0b11111111,
                        0b01111110, 0b00111100, 0b00011000, 0, 0]
                color = "#fc5275" if rows[y] & (0x80 >> x) else "#26383a"
            else:
                color = "#3bbfe4" if active else ("#b1f2f5" if y >= 5 + slope * (x - 3.5) else "#26383a")
            d.rounded_rectangle((cx - 10, cy - 10, cx + 10, cy + 10), radius=4,
                                fill="#0e1d20", outline="#536b6a")
            d.ellipse((cx - 6, cy - 6, cx + 6, cy + 6), fill=color)
    d.text((ox + 13, oy + bh + 10), title, font=font, fill="#d9e8e8")


board(36, "upright water", slope=0)
board(390, "tilted water", slope=-0.7)
board(744, "heartbeat mode", heart=True)
im.save(HERE / "preview.png")
