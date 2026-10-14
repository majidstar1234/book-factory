from __future__ import annotations

import unittest

from scripts.build_book import markdown_to_tex


class MarkdownToTexTests(unittest.TestCase):
    def test_headings_and_lists_convert(self) -> None:
        source = "# فصل آزمایشی\n\n## بخش اول\n\n- مورد یک\n- مورد دو"
        tex = markdown_to_tex(source)
        self.assertIn(r"\chapter{فصل آزمایشی}", tex)
        self.assertIn(r"\section{بخش اول}", tex)
        self.assertIn(r"\begin{itemize}", tex)
        self.assertIn(r"\item مورد یک", tex)
        self.assertIn(r"\end{itemize}", tex)

    def test_markdown_table_converts_to_tabular(self) -> None:
        source = (
            "| مفهوم | مقدار |\n"
            "|---|---:|\n"
            "| دهانه | ۶۶/۰۰ |\n"
            "| انگلیسی | Horizontal Thrust |"
        )
        tex = markdown_to_tex(source)
        self.assertIn(r"\begin{tabular}", tex)
        self.assertIn(r"مفهوم & مقدار", tex)
        self.assertIn(r"دهانه & ۶۶/۰۰", tex)
        self.assertIn("Horizontal Thrust", tex)
        self.assertIn(r"\end{tabular}", tex)

    def test_pipe_paragraph_without_separator_stays_text(self) -> None:
        tex = markdown_to_tex("گزینه A | گزینه B")
        self.assertNotIn(r"\begin{tabular}", tex)
        self.assertIn(r"گزینه A | گزینه B", tex)

    def test_table_rows_with_wrong_cell_count_are_not_silently_broken(self) -> None:
        source = "| الف | ب |\n|---|---|\n| یک | دو | سه |"
        with self.assertRaisesRegex(ValueError, "expected 2"):
            markdown_to_tex(source)


if __name__ == "__main__":
    unittest.main()
