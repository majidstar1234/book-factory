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

    def test_markdown_table_converts_to_page_width_tabularx(self) -> None:
        source = (
            "| مفهوم | مقدار |\n"
            "|---|---:|\n"
            "| دهانه | ۶۶/۰۰ |\n"
            "| انگلیسی | Horizontal Thrust |"
        )
        tex = markdown_to_tex(source)
        self.assertIn(r"\begin{tabularx}{\textwidth}", tex)
        self.assertIn(r"مفهوم & مقدار", tex)
        self.assertIn(r"دهانه & \lr{{\persianfont ۶۶/۰۰}}", tex)
        self.assertIn("Horizontal Thrust", tex)
        self.assertIn(r"\end{tabularx}", tex)

    def test_fenced_code_is_verbatim_and_wrapped_in_ltr(self) -> None:
        source = "متن فارسی قبل از کد.\\n\\n\x60\x60\x60python\\nfor i in range(3):\\n    print(i + 1)\\n\x60\x60\x60\\n\\nمتن فارسی بعد از کد."
        tex = markdown_to_tex(source)
        self.assertIn(r"\\begin{LTR}", tex)
        self.assertIn(r"\\begin{verbatim}", tex)
        self.assertIn("    print(i + 1)", tex)
        self.assertLess(tex.index(r"\\begin{LTR}"), tex.index(r"\\begin{verbatim}"))
        self.assertLess(tex.index(r"\\end{verbatim}"), tex.index(r"\\end{LTR}"))
        self.assertIn(r"\\end{LTR}", tex)

    def test_pipe_paragraph_without_separator_stays_text(self) -> None:
        tex = markdown_to_tex("گزینه A | گزینه B")
        self.assertNotIn(r"\begin{tabularx}", tex)
        self.assertIn(r"گزینه A | گزینه B", tex)

    def test_table_rows_with_wrong_cell_count_are_not_silently_broken(self) -> None:
        source = "| الف | ب |\n|---|---|\n| یک | دو | سه |"
        with self.assertRaisesRegex(ValueError, "expected 2"):
            markdown_to_tex(source)

    def test_english_parentheses_are_kept_left_to_right(self) -> None:
        tex = markdown_to_tex("قانون مور (Moore's Law) یکی از مفاهیم پایه است.")
        self.assertIn(r"\lr{(Moore's Law)}", tex)

    def test_persian_parentheses_are_not_wrapped_as_ltr(self) -> None:
        tex = markdown_to_tex("این یک توضیح (مفهوم پایه) است.")
        self.assertIn("(مفهوم پایه)", tex)
        self.assertNotIn(r"\lr{(مفهوم پایه)}", tex)

    def test_mixed_persian_english_parentheses_are_left_unchanged_for_now(self) -> None:
        tex = markdown_to_tex("انتخاب بین (CP یا AP) انجام می‌شود.")
        self.assertIn("(CP یا AP)", tex)
        self.assertNotIn(r"\lr{(CP یا AP)}", tex)


if __name__ == "__main__":
    unittest.main()
