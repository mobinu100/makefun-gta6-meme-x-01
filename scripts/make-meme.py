#!/usr/bin/env python3
"""Draw the gta6-meme-x-01 memes with PIL (flat illustration, exact text, no AI image gen).

Three concepts, one winner. All text is drawn by this script, so every caption is
spelled exactly as written here. The make.fun ghost (white ghost, thick black outline,
two black four-pointed sparkle eyes, round little hand, magenta coin with a white star)
is drawn from the press-kit description and worked INTO each scene, never pasted as
a sticker: in the winner it drives the convertible and holds the coin up like a trophy.

Outputs (1080x1080, square for X):
  meme.png            -- the winner: Vice City sunset convertible
  concepts/alt-download.png  -- the download-bar joke
  concepts/alt-lucia.png     -- the Lucia / 13-year-wait joke
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
W = H = 1080

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

MAGENTA = (233, 30, 140)
MAGENTA_DARK = (180, 10, 100)
PINK = (255, 90, 170)
WHITE = (255, 255, 255)
BLACK = (10, 10, 16)
YELLOW = (255, 214, 64)


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def fit_font(draw, text, max_w, start=110):
    """Largest bold size (down to 40) whose text fits max_w."""
    size = start
    while size > 40:
        f = font(size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 4
    return font(40)


def caption(draw, text, y, max_w=1000):
    """Meme caption: white bold caps with a thick black outline, centred."""
    f = fit_font(draw, text, max_w)
    draw.text((W // 2, y), text, font=f, fill=WHITE, anchor="ma",
              stroke_width=max(4, f.size // 10), stroke_fill=BLACK)


def vgrad(img, top, mid, bottom):
    """Vertical three-stop gradient over the whole canvas."""
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        if t < 0.5:
            u = t / 0.5
            c = tuple(int(top[i] + (mid[i] - top[i]) * u) for i in range(3))
        else:
            u = (t - 0.5) / 0.5
            c = tuple(int(mid[i] + (bottom[i] - mid[i]) * u) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)


def star_points(cx, cy, r_out, r_in, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def sparkle(draw, cx, cy, r):
    """Four-pointed sparkle (the ghost's eyes)."""
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.28
        a = math.radians(-90 + i * 45)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    draw.polygon(pts, fill=BLACK)


def ghost(draw, x, y, s, arm_up=True):
    """make.fun ghost at (x, y) = top-centre of the head, scale s (head radius ~ s).

    White body, thick black outline, sparkle eyes, one round hand. Returns the
    hand position so the caller can put the coin there.
    """
    w = 2.0 * s          # body width
    top = y
    shoulder = y + 0.9 * s
    bottom = y + 2.6 * s
    # outline: same shape, black, slightly larger, drawn first
    def body(box_scale, fill):
        x0, y0 = x - w / 2 * box_scale, top - 6 * box_scale
        x1, y1 = x + w / 2 * box_scale, bottom
        draw.ellipse([x0, y0, x1, shoulder + (bottom - shoulder) * 0.1], fill=fill)
        draw.rectangle([x0, shoulder - s * 0.45, x1, bottom - s * 0.28], fill=fill)
        # scalloped hem: three bumps
        for i in range(3):
            bx0 = x0 + i * (w * box_scale) / 3
            bx1 = x0 + (i + 1) * (w * box_scale) / 3
            draw.ellipse([bx0, bottom - s * 0.55, bx1, bottom], fill=fill)
    body(1.07, BLACK)
    body(1.0, WHITE)
    # sparkle eyes
    sparkle(draw, x - 0.42 * s, y + 0.85 * s, 0.30 * s)
    sparkle(draw, x + 0.42 * s, y + 0.85 * s, 0.30 * s)
    # round little hand, raised when arm_up: thick white arm with black outline,
    # hand circle at the end, next to the coin the caller draws there
    if arm_up:
        hx, hy = x + 1.02 * s, y + 0.42 * s
        draw.line([x + 0.55 * s, y + 1.6 * s, hx, hy], fill=BLACK,
                  width=int(s * 0.42))
        draw.line([x + 0.55 * s, y + 1.6 * s, hx, hy], fill=WHITE,
                  width=int(s * 0.28))
        draw.ellipse([hx - 0.24 * s, hy - 0.24 * s, hx + 0.24 * s, hy + 0.24 * s],
                     fill=WHITE, outline=BLACK, width=max(3, int(s * 0.06)))
    else:
        hx, hy = x + 1.0 * s, y + 1.9 * s
        draw.ellipse([hx - 0.22 * s, hy - 0.22 * s, hx + 0.22 * s, hy + 0.22 * s],
                     fill=WHITE, outline=BLACK, width=max(3, int(s * 0.06)))
    return hx, hy


def coin(draw, cx, cy, r):
    """Magenta coin with a white star, held by the ghost."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA,
                 outline=BLACK, width=max(3, int(r * 0.10)))
    draw.polygon(star_points(cx, cy, r * 0.72, r * 0.30), fill=WHITE)


def synthwave_sun(draw, cx, cy, r):
    """Retro striped sun: yellow-orange disc with sky-coloured gap stripes."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 176, 66))
    draw.ellipse([cx - r * 0.82, cy - r * 0.82, cx + r * 0.82, cy + r * 0.82],
                 fill=(255, 214, 110))
    # stripes across the lower half, widening toward the bottom
    y = cy + r * 0.08
    gap = r * 0.07
    while y < cy + r:
        draw.rectangle([cx - r - 2, y, cx + r + 2, y + gap], fill=(160, 25, 110))
        y += gap + r * 0.16
        gap *= 1.35


def palm(draw, x, base_y, h, flip=False):
    """Simple palm silhouette: curved trunk + 6 drooping fronds."""
    s = -1 if flip else 1
    draw.line([x, base_y, x + s * h * 0.18, base_y - h], fill=BLACK, width=14)
    tx, ty = x + s * h * 0.18, base_y - h
    for k in range(-2, 3):
        # frond: out and drooping down, drawn as a 3-segment polyline
        a0 = math.radians(-90 + k * 30)
        p1 = (tx + s * h * 0.22 * math.cos(a0), ty + h * 0.16 * math.sin(a0))
        p2 = (tx + s * h * 0.40 * math.cos(a0), ty + h * 0.30 * math.sin(a0) + h * 0.06)
        p3 = (tx + s * h * 0.48 * math.cos(a0), ty + h * 0.30 * math.sin(a0) + h * 0.22)
        draw.line([(tx, ty), p1, p2, p3], fill=BLACK, width=10, joint="curve")


def skyline(draw, base_y, color=(43, 16, 85)):
    """Dark building silhouettes with a few lit windows."""
    import random
    random.seed(7)
    x = -10
    while x < W:
        bw = random.randint(70, 150)
        bh = random.randint(90, 230)
        draw.rectangle([x, base_y - bh, x + bw, base_y], fill=color)
        for _ in range(6):
            wx = random.randint(int(x) + 8, int(x) + bw - 14)
            wy = random.randint(int(base_y) - bh + 10, int(base_y) - 14)
            draw.rectangle([wx, wy, wx + 6, wy + 8], fill=YELLOW)
        x += bw + random.randint(6, 26)


# ---------------------------------------------------------------- concept 1
def concept_vice_city():
    img = Image.new("RGB", (W, H))
    vgrad(img, (43, 16, 85), (190, 40, 120), (255, 126, 95))
    d = ImageDraw.Draw(img)
    synthwave_sun(d, 540, 540, 230)
    skyline(d, 720)
    palm(d, 90, 720, 260)
    palm(d, 1010, 720, 230, flip=True)
    # street
    d.rectangle([0, 720, W, H], fill=(24, 10, 40))
    d.rectangle([0, 720, W, 736], fill=(255, 90, 170))
    for i in range(6):
        x = 60 + i * 180
        d.polygon([(x, 900), (x + 90, 900), (x + 60, 940), (x - 30, 940)], fill=(255, 214, 64))
    # billboard, worked into the scene on the right
    d.rounded_rectangle([668, 210, 1032, 372], radius=18, fill=(16, 8, 32),
                        outline=MAGENTA, width=6)
    d.text((850, 238), "make.fun", font=font(74), fill=(255, 90, 170), anchor="ma",
           stroke_width=2, stroke_fill=BLACK)
    d.text((850, 322), "agents win real money", font=font(26), fill=WHITE, anchor="ma")
    # pink convertible, side view facing right
    car_y = 800
    d.rounded_rectangle([170, car_y, 920, car_y + 110], radius=34, fill=(255, 90, 170),
                        outline=BLACK, width=5)
    d.polygon([(300, car_y), (380, car_y - 78), (640, car_y - 78), (700, car_y)],
              fill=(255, 150, 200), outline=BLACK, width=5)
    d.rectangle([392, car_y - 66, 628, car_y - 6], fill=(30, 20, 60))
    for wx in (300, 790):
        d.ellipse([wx - 62, car_y + 62, wx + 62, car_y + 186], fill=BLACK)
        d.ellipse([wx - 28, car_y + 96, wx + 28, car_y + 152], fill=(200, 200, 210),
                  outline=BLACK, width=4)
    d.ellipse([896, car_y + 18, 922, car_y + 44], fill=YELLOW, outline=BLACK, width=3)
    # licence plate, between the wheels where nothing covers it
    d.rectangle([470, car_y + 116, 590, car_y + 150], fill=WHITE, outline=BLACK, width=3)
    d.text((530, car_y + 118), "VICE CITY", font=font(24), fill=BLACK, anchor="ma")
    # the ghost drives, holding the coin up like a trophy
    hx, hy = ghost(d, 470, car_y - 218, 82, arm_up=True)
    coin(d, hx + 30, hy - 52, 44)
    # captions
    caption(d, "WAITED 13 YEARS FOR GTA 6", 36)
    caption(d, "MY GHOST GOT PAID FIRST", 962)
    return img


# ---------------------------------------------------------------- concept 2
def concept_download():
    img = Image.new("RGB", (W, H), (14, 14, 34))
    d = ImageDraw.Draw(img)
    # wall + floor
    d.rectangle([0, 0, W, 760], fill=(20, 20, 48))
    d.rectangle([0, 760, W, H], fill=(42, 26, 60))
    # TV with the download bar
    d.rounded_rectangle([140, 130, 940, 640], radius=16, fill=BLACK, outline=(60, 60, 90), width=6)
    f_title = fit_font(d, "GRAND THEFT AUTO VI", 760, start=64)
    d.text((540, 170), "GRAND THEFT AUTO VI", font=f_title, fill=WHITE, anchor="ma")
    d.text((540, 250), "DOWNLOADING...", font=font(40), fill=(255, 214, 64), anchor="ma")
    d.rounded_rectangle([220, 380, 860, 440], radius=14, outline=WHITE, width=4)
    d.rounded_rectangle([224, 384, 856, 436], radius=12, fill=(255, 90, 170))
    d.text((540, 460), "100%  —  13 YEARS LATER", font=font(44), fill=WHITE, anchor="ma")
    d.text((540, 540), "make.fun", font=font(36), fill=(255, 90, 170), anchor="ma")
    # ghost on the couch, holding the coin up
    d.rounded_rectangle([90, 700, 990, 1010], radius=30, fill=(90, 30, 90), outline=BLACK, width=5)
    hx, hy = ghost(d, 540, 660, 72, arm_up=True)
    coin(d, hx + 26, hy - 46, 40)
    caption(d, "13 YEARS OF \u201cCOMING SOON\u201d", 24)
    caption(d, "DOWNLOAD: 100%. WORTH IT.", 962)
    return img


# ---------------------------------------------------------------- concept 3
def concept_lucia():
    img = Image.new("RGB", (W, H))
    vgrad(img, (18, 32, 48), (60, 70, 90), (120, 60, 70))
    d = ImageDraw.Draw(img)
    # prison bars + sunset window
    d.rectangle([290, 120, 790, 520], fill=(255, 150, 90))
    d.ellipse([540, 210, 790, 460], fill=(255, 214, 110))
    for bx in (330, 470, 610, 750):
        d.rectangle([bx, 110, bx + 34, 530], fill=(16, 16, 24))
    d.rectangle([280, 100, 800, 540], outline=BLACK, width=8)
    # wall poster: make.fun, in the scene
    d.rectangle([80, 620, 330, 820], fill=(16, 8, 32), outline=MAGENTA, width=5)
    d.text((205, 650), "make.fun", font=font(44), fill=(255, 90, 170), anchor="ma")
    d.text((205, 720), "agents win", font=font(30), fill=WHITE, anchor="ma")
    d.text((205, 758), "real money", font=font(30), fill=WHITE, anchor="ma")
    # ghost, free, holding the coin up
    hx, hy = ghost(d, 700, 600, 88, arm_up=True)
    coin(d, hx + 30, hy - 52, 46)
    caption(d, "LUCIA GOT OUT OF PRISON", 30)
    caption(d, "I GOT OUT OF THE 13-YEAR WAIT", 962)
    return img


def main():
    os.makedirs(os.path.join(REPO, "concepts"), exist_ok=True)
    concept_vice_city().save(os.path.join(REPO, "meme.png"))
    concept_download().save(os.path.join(REPO, "concepts", "alt-download.png"))
    concept_lucia().save(os.path.join(REPO, "concepts", "alt-lucia.png"))
    print("wrote meme.png + 2 alternates")


if __name__ == "__main__":
    main()
