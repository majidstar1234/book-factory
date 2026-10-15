from __future__ import annotations

import unittest

from scripts.build_book import markdown_to_tex


class FencedCodeBlockTests(unittest.TestCase):
    def test_fenced_python_is_preserved_verbatim(self) -> None:
        source = (
            "# Example\n\n"
            "```python\n"
            "def clean_text(text):\n"
            "    return re.findall(r'\\w+', text.lower())\n"
            "```\n"
        )
        tex = markdown_to_tex(source)
        self.assertIn(r"\begin{verbatim}", tex)
        self.assertIn("def clean_text(text):", tex)
        self.assertIn(r"r'\w+'", tex)
        self.assertIn(r"\end{verbatim}", tex)
        self.assertNotIn(r"\textbackslash{}", tex)

    def test_fenced_code_does_not_consume_following_heading(self) -> None:
        source = "```yaml\non: [push]\n```\n\n## بعد از کد\n"
        tex = markdown_to_tex(source)
        self.assertIn("on: [push]", tex)
        self.assertIn(r"\section{بعد از کد}", tex)
        self.assertEqual(tex.count(r"\begin{verbatim}"), 1)
        self.assertEqual(tex.count(r"\end{verbatim}"), 1)


if __name__ == "__main__":
    unittest.main()
