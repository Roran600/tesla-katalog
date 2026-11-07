#!/usr/bin/env python3
"""Validate the generated fonts and their Slovak character coverage."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from fontTools.ttLib import TTFont
from generate_tesla_display_font import OUTPUT, SOURCE_ALPHABET


class DisplayFontTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.font = TTFont(OUTPUT)
        cls.cmap = cls.font.getBestCmap()

    def test_coverage_and_lowercase(self):
        for character in SOURCE_ALPHABET:
            with self.subTest(character=character):
                glyph_name = self.cmap[ord(character)]
                self.assertEqual(glyph_name, self.cmap[ord(character.lower())])
                glyph = self.font["glyf"][glyph_name]
                self.assertGreater(glyph.numberOfContours, 0)
                self.assertLessEqual(glyph.yMin, 0)
                self.assertGreaterEqual(glyph.yMax, 990)
        for character in "0123456789 .,:-/?":
            self.assertIn(ord(character), self.cmap)

    def test_accents_and_font_metrics(self):
        os2 = self.font["OS/2"]
        for character in "ÁÄČĎÉÍĹĽŇÓÔŔŠŤÚÝŽ":
            with self.subTest(character=character):
                glyph = self.font["glyf"][self.cmap[ord(character)]]
                self.assertGreater(glyph.yMax, 1000)
                self.assertLessEqual(glyph.yMax, os2.usWinAscent)
                self.assertGreaterEqual(glyph.yMin, -os2.usWinDescent)

    def test_woff2_matches_ttf(self):
        decompressor = shutil.which("woff2_decompress")
        if not decompressor:
            self.fail("Missing woff2_decompress")
        with tempfile.TemporaryDirectory() as tmp:
            compressed = Path(tmp) / OUTPUT.with_suffix(".woff2").name
            shutil.copyfile(OUTPUT.with_suffix(".woff2"), compressed)
            subprocess.run([decompressor, str(compressed)], check=True, capture_output=True)
            other = TTFont(compressed.with_suffix(".ttf"))
            self.assertEqual(self.cmap, other.getBestCmap())
            self.assertEqual(self.font["hmtx"].metrics, other["hmtx"].metrics)
            for glyph_name in self.font.getGlyphOrder():
                a, b = self.font["glyf"][glyph_name], other["glyf"][glyph_name]
                self.assertEqual(a.numberOfContours, b.numberOfContours, glyph_name)
                self.assertEqual(a.getCoordinates(self.font["glyf"]), b.getCoordinates(other["glyf"]), glyph_name)


if __name__ == "__main__":
    unittest.main()
