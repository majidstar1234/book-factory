from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "golden_examples" / "chapter_architecture.tex"


class GoldenPersianLatexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = GOLDEN.read_text(encoding="utf-8")

    def test_chapter_and_hierarchical_headings_exist(self) -> None:
        self.assertRegex(self.source, r"\\chapter\{")
        self.assertRegex(self.source, r"\\section\{")
        self.assertRegex(self.source, r"\\subsection\{")

    def test_labels_are_unique(self) -> None:
        labels = re.findall(r"\\label\{([^}]+)\}", self.source)
        self.assertTrue(labels, "Expected at least one LaTeX label")
        self.assertEqual(len(labels), len(set(labels)), "Duplicate LaTeX labels found")

    def test_equation_and_table_patterns_are_present(self) -> None:
        self.assertIn(r"\begin{equation}", self.source)
        self.assertIn(r"\begin{table}", self.source)
        self.assertIn(r"\begin{tabular}", self.source)
        self.assertIn(r"\toprule", self.source)
        self.assertIn(r"\bottomrule", self.source)

    def test_mixed_language_and_persian_decimal_examples_are_present(self) -> None:
        self.assertIn(r"\lr{Horizontal Thrust", self.source)
        self.assertIn("۶۶/۰۰", self.source)
        self.assertIn("۰/۴۲۷", self.source)


if __name__ == "__main__":
    unittest.main()
