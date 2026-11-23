"""Branded Zinlea QR codes pointing to zinlea.com/card/. Each variant is checked with OpenCV before saving."""
import sys
import qrcode, cv2, numpy as np
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw

URL = "https://zinlea.com/card/"
det = cv2.QRCodeDetector()

def render(fg, bg, dots, finder_round, logo, size=1200):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=0, box_size=1); q.add_data(URL); q.make(fit=True)
    m = q.get_matrix(); n = len(m); quiet = 4; cells = n + 2 * quiet; px = size // cells; S = px * cells
    im = Image.new('RGB', (S, S), bg); d = ImageDraw.Draw(im)
    fz = {(r, c) for (R, C) in [(0, 0), (0, n - 7), (n - 7, 0)] for r in range(R, R + 7) for c in range(C, C + 7)}
    cut = 5 if logo else 0; c0 = (n - cut) // 2
    for r in range(n):
        for c in range(n):
            if m[r][c] and (r, c) not in fz and not (logo and c0 <= r < c0 + cut and c0 <= c < c0 + cut):
                X, Y = (c + quiet) * px, (r + quiet) * px
                if dots: d.ellipse([X + px * .06, Y + px * .06, X + px * .94, Y + px * .94], fill=fg)
                else: d.rectangle([X, Y, X + px - 1, Y + px - 1], fill=fg)
    for (R, C) in [(0, 0), (0, n - 7), (n - 7, 0)]:
        X, Y = (C + quiet) * px, (R + quiet) * px
        rr = lambda k: int(px * k * finder_round)
        d.rounded_rectangle([X, Y, X + 7 * px - 1, Y + 7 * px - 1], radius=rr(1.6), fill=fg)
        d.rounded_rectangle([X + px, Y + px, X + 6 * px - 1, Y + 6 * px - 1], radius=rr(1.1), fill=bg)
        d.rounded_rectangle([X + 2 * px, Y + 2 * px, X + 5 * px - 1, Y + 5 * px - 1], radius=rr(.8), fill=fg)
    if logo:  # the "z" with the moon dot, in a small disc
        cx = cy = S // 2; rad = cut * px // 2 + px // 3
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=bg)
        z = rad * .62; w = max(4, int(rad * .2))
        d.line([(cx - z * .55, cy - z * .5), (cx + z * .5, cy - z * .5), (cx - z * .55, cy + z * .55), (cx + z * .5, cy + z * .55)], fill=fg, width=w, joint='curve')
        mr = int(rad * .17); mx, my = int(cx + z * .85), int(cy - z * .85)
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=fg)
    return im

def scans(im):
    a = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    tests = [a, cv2.resize(a, (300, 300), interpolation=cv2.INTER_AREA), cv2.resize(a, (180, 180), interpolation=cv2.INTER_AREA)]
    if np.mean(a) < 128: tests += [255 - t for t in tests]  # light-on-dark: also try inverted, as phone cameras do
    return sum(1 for t in tests if det.detectAndDecode(t)[0] == URL), len(tests)

if __name__ == "__main__":
    for name, fg, bg in [("dark-on-white", "#0E1116", "#FFFFFF"), ("moon-on-midnight", "#CCD9EF", "#070B17")]:
        for dots in (True, False):
            for fr in (1.0, 0.5, 0.0):
                im = render(fg, bg, dots, fr, logo=True)
                ok, tot = scans(im)
                print(f"{name:18} dots={dots!s:5} round={fr} logo -> {ok}/{tot}")
