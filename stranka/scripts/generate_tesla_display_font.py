#!/usr/bin/env python3
"""Build the display font from font-sources/tesla-slovak-uppercase-vector.svg.

Lowercase Unicode characters intentionally map to uppercase outlines. Digits,
punctuation and the additional Czech accents are drawn by this script.
"""

from math import ceil
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "font-sources/tesla-slovak-uppercase-vector.svg"
OUTPUT = ROOT / "static/fonts/tesla-katalog-display.ttf"
UPM = 1000
CAP = 1000
STROKE = 170
SIDE = 55
KAPPA = 0.55228475
# IDs are source glyph groups, not their position in the laid-out SVG sheet.
SOURCE_ALPHABET = (
    "A Á Ä B C Č D Ď E É F G H I Í J K L Ĺ Ľ M N Ň O Ó Ô "
    "P Q R Ŕ S Š T Ť U Ú V W X Y Ý Z Ž"
).split()


class Outline:
    def __init__(self):
        self.raw_pen = TTGlyphPen(None)
        self.pen = Cu2QuPen(self.raw_pen, max_err=1)

    def polygon(self, points, hole=False):
        points = list(reversed(points)) if hole else points
        self.pen.moveTo(points[0])
        for point in points[1:]:
            self.pen.lineTo(point)
        self.pen.closePath()

    def rect(self, x, y, width, height, hole=False):
        self.polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)], hole)

    def diagonal(self, start, end, width=STROKE):
        x1, y1 = start
        x2, y2 = end
        dx, dy = x2 - x1, y2 - y1
        length = (dx * dx + dy * dy) ** 0.5
        px, py = -dy * width / (2 * length), dx * width / (2 * length)
        self.polygon([(x1 - px, y1 - py), (x2 - px, y2 - py), (x2 + px, y2 + py), (x1 + px, y1 + py)])

    def ellipse(self, cx, cy, rx, ry, hole=False):
        # The two contours use opposite winding directions, as required by TTF.
        direction = -1 if hole else 1
        self.pen.moveTo((cx, cy + ry))
        for end, controls in (
            ((cx + direction * rx, cy), ((cx + direction * KAPPA * rx, cy + ry), (cx + direction * rx, cy + KAPPA * ry))),
            ((cx, cy - ry), ((cx + direction * rx, cy - KAPPA * ry), (cx + direction * KAPPA * rx, cy - ry))),
            ((cx - direction * rx, cy), ((cx - direction * KAPPA * rx, cy - ry), (cx - direction * rx, cy - KAPPA * ry))),
            ((cx, cy + ry), ((cx - direction * rx, cy + KAPPA * ry), (cx - direction * KAPPA * rx, cy + ry))),
        ):
            self.pen.curveTo(*controls, end)
        self.pen.closePath()

    def glyph(self):
        return self.raw_pen.glyph()


def simple(width=760, draw=None):
    outline = Outline()
    if draw:
        draw(outline, width)
    return outline.glyph(), width


def rounded_counter(outline, x, y, width, height):
  # Rectangular counters retain the square-cut, technical character.
  outline.rect(x, y, width, height, hole=True)


def octagonal_o(outline, width, weight=210):
    """Draw a heavy, squared O with a deliberately generous counter."""
    l, r = SIDE, width - SIDE
    outer_cut = 105
    inner_width = r - l - 2 * weight
    # Keep a real horizontal counter even in the heavier Ó cut.
    inner_cut = max(25, min(70, inner_width * 0.22))
    outline.polygon([
        (l + outer_cut, CAP), (r - outer_cut, CAP), (r, CAP - outer_cut), (r, outer_cut),
        (r - outer_cut, 0), (l + outer_cut, 0), (l, outer_cut), (l, CAP - outer_cut),
    ])
    outline.polygon([
        (l + weight + inner_cut, CAP - weight), (r - weight - inner_cut, CAP - weight),
        (r - weight, CAP - weight - inner_cut), (r - weight, weight + inner_cut),
        (r - weight - inner_cut, weight), (l + weight + inner_cut, weight),
        (l + weight, weight + inner_cut), (l + weight, CAP - weight - inner_cut),
    ], hole=True)


def draw_letter(letter, outline, width):
    l, r, mid = SIDE, width - SIDE, width / 2
    if letter == "B":
        outline.rect(l, 0, STROKE, CAP)
        outline.rect(l, CAP - STROKE, r - l - STROKE, STROKE)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l - STROKE, STROKE)
        outline.rect(l, 0, r - l - STROKE, STROKE)
        outline.rect(r - STROKE, STROKE, STROKE, CAP / 2 - STROKE)
        outline.rect(r - STROKE, CAP / 2 + STROKE / 2, STROKE, CAP / 2 - STROKE)
        rounded_counter(outline, l + STROKE, CAP / 2 + STROKE, r - l - 2 * STROKE, CAP / 2 - 2 * STROKE)
        rounded_counter(outline, l + STROKE, STROKE, r - l - 2 * STROKE, CAP / 2 - 2 * STROKE)
    elif letter == "C":
        outline.rect(l, STROKE, STROKE, CAP - 2 * STROKE)
        outline.rect(l + STROKE, CAP - STROKE, r - l - STROKE, STROKE)
        outline.rect(l + STROKE, 0, r - l - STROKE, STROKE)
        outline.diagonal((l + STROKE / 2, CAP - STROKE), (l + STROKE * 1.4, CAP - STROKE / 3))
        outline.diagonal((l + STROKE / 2, STROKE), (l + STROKE * 1.4, STROKE / 3))
    elif letter == "D":
        outline.rect(l, 0, STROKE, CAP)
        outline.rect(l + STROKE, CAP - STROKE, r - l - 2 * STROKE, STROKE)
        outline.rect(l + STROKE, 0, r - l - 2 * STROKE, STROKE)
        outline.rect(r - STROKE, STROKE, STROKE, CAP - 2 * STROKE)
        rounded_counter(outline, l + STROKE, STROKE, r - l - 3 * STROKE, CAP - 2 * STROKE)
    elif letter == "F":
        outline.rect(l, 0, STROKE, CAP)
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l - STROKE / 2, STROKE)
    elif letter == "G":
        # Conventional G: flat technical cap, rounded lower bowl and right opening.
        heavy = 215
        outline.ellipse(mid, CAP / 2, (r - l) / 2, CAP / 2)
        outline.ellipse(mid, CAP / 2, (r - l) / 2 - heavy, CAP / 2 - heavy, hole=True)
        outline.rect(l + 110, CAP - heavy, r - l - 220, heavy)
        outline.rect(mid + 100, 470, r - mid + 80, 320, hole=True)
        outline.rect(mid - 20, 390, r - mid + 20, 200)
    elif letter == "H":
        outline.rect(l, 0, STROKE, CAP)
        outline.rect(r - STROKE, 0, STROKE, CAP)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l, STROKE)
    elif letter == "I":
        outline.rect(mid - STROKE / 2, 0, STROKE, CAP)
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.rect(l, 0, r - l, STROKE)
    elif letter == "J":
        outline.rect(r - STROKE, STROKE, STROKE, CAP - STROKE)
        outline.rect(l + STROKE, 0, r - l - 2 * STROKE, STROKE)
        outline.rect(l, STROKE, STROKE, STROKE * 1.4)
    elif letter == "K":
        # A new, stable K: a single heavy spine with two unbroken wedges.
        heavy = 235
        outline.rect(l, 0, heavy, CAP)
        outline.polygon([
            (l + heavy - 25, CAP / 2 - 15), (l + heavy - 25, CAP / 2 + heavy),
            (r, CAP), (r, CAP - heavy),
        ])
        outline.polygon([
            (l + heavy - 25, CAP / 2 - heavy), (l + heavy - 25, CAP / 2 + 15),
            (r, heavy), (r, 0),
        ])
    elif letter == "M":
        outline.rect(l, 0, STROKE, CAP)
        outline.rect(r - STROKE, 0, STROKE, CAP)
        outline.diagonal((l + STROKE / 2, CAP), (mid, CAP / 2), STROKE)
        outline.diagonal((r - STROKE / 2, CAP), (mid, CAP / 2), STROKE)
    elif letter == "N":
        outline.rect(l, 0, STROKE, CAP)
        outline.rect(r - STROKE, 0, STROKE, CAP)
        outline.diagonal((l + STROKE / 2, CAP), (r - STROKE / 2, 0), STROKE)
    elif letter == "O":
        octagonal_o(outline, width, weight=270)
    elif letter == "P":
        outline.rect(l, 0, STROKE, CAP)
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l, STROKE)
        outline.rect(r - STROKE, CAP / 2, STROKE, CAP / 2 - STROKE)
        rounded_counter(outline, l + STROKE, CAP / 2 + STROKE / 2, r - l - 2 * STROKE, CAP / 2 - 1.5 * STROKE)
    elif letter == "Q":
        draw_letter("O", outline, width)
        outline.diagonal((mid, CAP / 3), (r + STROKE / 3, -STROKE / 4), STROKE)
    elif letter == "R":
        draw_letter("P", outline, width)
        outline.diagonal((mid, CAP / 2), (r, 0), STROKE)
    elif letter == "U":
        outline.rect(l, STROKE, STROKE, CAP - STROKE)
        outline.rect(r - STROKE, STROKE, STROKE, CAP - STROKE)
        outline.rect(l + STROKE, 0, r - l - 2 * STROKE, STROKE)
    elif letter == "V":
        outline.diagonal((l + STROKE / 2, CAP), (mid, 0), STROKE)
        outline.diagonal((r - STROKE / 2, CAP), (mid, 0), STROKE)
    elif letter == "W":
        outline.diagonal((l + STROKE / 2, CAP), (width * 0.3, 0), STROKE)
        outline.diagonal((width * 0.3, 0), (mid, CAP / 2), STROKE)
        outline.diagonal((mid, CAP / 2), (width * 0.7, 0), STROKE)
        outline.diagonal((width * 0.7, 0), (r - STROKE / 2, CAP), STROKE)
    elif letter == "X":
        outline.diagonal((l, CAP), (r, 0), STROKE)
        outline.diagonal((l, 0), (r, CAP), STROKE)
    elif letter == "Y":
        outline.diagonal((l, CAP), (mid, CAP / 2), STROKE)
        outline.diagonal((r, CAP), (mid, CAP / 2), STROKE)
        outline.rect(mid - STROKE / 2, 0, STROKE, CAP / 2)
    elif letter == "Z":
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.rect(l, 0, r - l, STROKE)
        outline.diagonal((r - STROKE / 2, CAP - STROKE), (l + STROKE / 2, STROKE), STROKE)
    elif letter == "0":
        draw_letter("O", outline, width)
    elif letter == "1":
        outline.rect(mid - STROKE / 2, 0, STROKE, CAP)
        outline.diagonal((mid - STROKE / 2, CAP), (l, CAP - STROKE * 1.7), STROKE)
        outline.rect(l, 0, r - l, STROKE)
    elif letter == "2":
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.rect(r - STROKE, CAP / 2, STROKE, CAP / 2 - STROKE)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l, STROKE)
        outline.rect(l, 0, STROKE, CAP / 2)
        outline.rect(l, 0, r - l, STROKE)
    elif letter == "3":
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l, STROKE)
        outline.rect(l, 0, r - l, STROKE)
        outline.rect(r - STROKE, 0, STROKE, CAP)
    elif letter == "4":
        outline.rect(r - STROKE, 0, STROKE, CAP)
        outline.diagonal((l, CAP / 2), (mid, CAP), STROKE)
        outline.diagonal((l, CAP / 2), (r, CAP / 2), STROKE)
    elif letter == "5":
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.rect(l, CAP / 2, STROKE, CAP / 2 - STROKE)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l, STROKE)
        outline.rect(r - STROKE, 0, STROKE, CAP / 2)
        outline.rect(l, 0, r - l, STROKE)
    elif letter == "6":
        draw_letter("C", outline, width)
        outline.rect(l, CAP / 2 - STROKE / 2, r - l, STROKE)
        outline.rect(r - STROKE, 0, STROKE, CAP / 2)
    elif letter == "7":
        outline.rect(l, CAP - STROKE, r - l, STROKE)
        outline.diagonal((r - STROKE / 2, CAP - STROKE), (mid, 0), STROKE)
    elif letter == "8":
        draw_letter("B", outline, width)
    elif letter == "9":
        draw_letter("P", outline, width)
        outline.rect(r - STROKE, 0, STROKE, CAP / 2)


def generic_glyph(character):
    widths = {"M": 930, "W": 980, "I": 440, "K": 800, "O": 800, "G": 800, "1": 500, " ": 360}
    width = widths.get(character, 760)
    if character == " ":
        return simple(width)
    if character in "08":
        return SOURCE_GLYPHS[{"0": "O", "8": "B"}[character]]
    return simple(width, lambda outline, glyph_width: draw_letter(character, outline, glyph_width))


def source_glyphs():
    """Import letter-local paths; group transforms only lay out the SVG sheet.

    The source uses consistent 100-unit cap height and even-odd contours with
    opposite winding for its counters. Fail rather than silently misreading a
    structurally changed source, including nested transforms or SVG use nodes.
    """
    root = ET.parse(SOURCE).getroot()
    result = {}
    for index, character in enumerate(SOURCE_ALPHABET, 1):
        group = root.find(f'.//*[@id="glyph-{index}"]')
        if group is None or not group.get("transform", "").endswith("scale(0.7)"):
            raise ValueError(f"Unexpected source group for {character}: glyph-{index}")
        paths = list(group)
        if not paths or any(p.tag != "{http://www.w3.org/2000/svg}path" or p.get("transform") for p in paths):
            raise ValueError(f"Unexpected nested SVG structure in glyph-{index}")
        recording = RecordingPen()
        for path in paths:
            parse_path(path.attrib["d"], recording)
        bounds = BoundsPen(None)
        recording.replay(bounds)
        if bounds.bounds is None:
            raise ValueError(f"Empty glyph for {character}")
        x_min, _, x_max, _ = bounds.bounds
        pen = TTGlyphPen(None)
        transformed = TransformPen(Cu2QuPen(pen, max_err=1), (10, 0, 0, -10, SIDE - x_min * 10, 1000))
        recording.replay(transformed)
        result[character] = (pen.glyph(), ceil((x_max - x_min) * 10 + 2 * SIDE))
    return result


def accented_glyph(base, accent):
    width = {"M": 930, "W": 980, "I": 440, "O": 800}.get(base, 760)
    outline = Outline()
    # Accented forms use the same new construction, leaving exact archival
    # contours untouched for the unaccented TESLA logotype.
    # Used only for Czech forms absent from the SVG; reuse its base outline.
    source, width = SOURCE_GLYPHS[base]
    recording = RecordingPen()
    source.draw(recording, None)
    recording.replay(outline.pen)
    center = width / 2
    if accent == "acute":
        outline.polygon([
            (center - 60, 1175), (center + 85, 1175),
            (center + 285, 1385), (center + 120, 1385),
        ])
    elif accent == "caron":
        outline.diagonal((center - 140, 1260), (center, 1090), 85)
        outline.diagonal((center, 1090), (center + 140, 1260), 85)
    elif accent == "umlaut":
        outline.rect(center - 190, 1110, 95, 130)
        outline.rect(center + 95, 1110, 95, 130)
    elif accent == "circumflex":
        outline.diagonal((center - 145, 1100), (center, 1270), 85)
        outline.diagonal((center, 1270), (center + 145, 1100), 85)
    elif accent == "ring":
        outline.ellipse(center, 1180, 120, 120)
        outline.ellipse(center, 1180, 58, 58, hole=True)
    return outline.glyph(), width


def punctuation(character):
    outline = Outline()
    if character == ".":
        outline.rect(70, 0, 150, 150)
        return outline.glyph(), 290
    if character == ",":
        outline.polygon([(70, 0), (220, 0), (130, -180)])
        return outline.glyph(), 290
    if character == ":":
        outline.rect(70, 130, 150, 150)
        outline.rect(70, 700, 150, 150)
        return outline.glyph(), 290
    if character == "-":
        outline.rect(40, 430, 420, STROKE)
        return outline.glyph(), 500
    if character == "/":
        outline.diagonal((40, 0), (600, CAP), STROKE)
        return outline.glyph(), 640
    if character == "?":
        draw_letter("2", outline, 760)
        outline.rect(305, 0, 150, 150)
        return outline.glyph(), 760
    return outline.glyph(), 500


def main():
    global SOURCE_GLYPHS
    SOURCE_GLYPHS = source_glyphs()
    compressor = shutil.which("woff2_compress")
    if not compressor:
        raise SystemExit("Missing woff2_compress; install the WOFF2 tools before generating fonts.")
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:-/?"
    accents = {"Ě": ("E", "caron"), "Ř": ("R", "caron"), "Ů": ("U", "ring")}

    glyphs = {".notdef": simple(760, lambda outline, width: (outline.rect(50, 50, width - 100, 900), outline.rect(170, 170, width - 340, 660, hole=True)))[0]}
    metrics = {".notdef": (760, 0)}
    cmap = {}

    for character in characters:
        name = "space" if character == " " else f"uni{ord(character):04X}"
        glyph, width = SOURCE_GLYPHS[character] if character in SOURCE_GLYPHS else (generic_glyph(character) if character.isalnum() or character == " " else punctuation(character))
        glyphs[name] = glyph
        metrics[name] = (width, 0)
        cmap[ord(character)] = name
        if character.isalpha():
            cmap[ord(character.lower())] = name

    for character in SOURCE_ALPHABET:
        if character in characters:
            continue
        name = f"uni{ord(character):04X}"
        glyph, width = SOURCE_GLYPHS[character]
        glyphs[name], metrics[name] = glyph, (width, 0)
        cmap[ord(character)] = cmap[ord(character.lower())] = name

    for character, (base, accent) in accents.items():
        name = f"uni{ord(character):04X}"
        glyph, width = accented_glyph(base, accent)
        glyphs[name] = glyph
        metrics[name] = (width, 0)
        cmap[ord(character)] = name
        cmap[ord(character.lower())] = name

    glyph_order = [".notdef"] + [name for name in glyphs if name != ".notdef"]
    font = FontBuilder(UPM, isTTF=True)
    font.setupGlyphOrder(glyph_order)
    font.setupCharacterMap(cmap)
    font.setupGlyf(glyphs)
    font.setupHorizontalMetrics(metrics)
    font.setupHorizontalHeader(ascent=1450, descent=-250)
    font.setupNameTable({
        "familyName": "Tesla Katalog Display",
        "styleName": "Bold",
        "uniqueFontIdentifier": "Tesla Katalog Display Bold 1.0",
        "fullName": "Tesla Katalog Display Bold",
        "psName": "TeslaKatalogDisplay-Bold",
        "version": "Version 1.0",
    })
    font.setupOS2(sTypoAscender=1450, sTypoDescender=-250, usWinAscent=1450, usWinDescent=250, usWeightClass=700)
    font.setupPost()
    font.setupMaxp()
    # Fixed timestamps keep repeated builds reproducible.
    font.font.recalcTimestamp = False
    font.font["head"].created = font.font["head"].modified = 2082844800
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".font-build-", dir=OUTPUT.parent) as tmp:
        staged = Path(tmp) / OUTPUT.name
        font.save(staged)
        subprocess.run([compressor, str(staged)], check=True)
        shutil.copyfile(staged, OUTPUT)
        shutil.copyfile(staged.with_suffix(".woff2"), OUTPUT.with_suffix(".woff2"))


if __name__ == "__main__":
    main()
