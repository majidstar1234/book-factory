from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.build_book import TEMPLATE, markdown_to_tex, tex_escape

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("xelatex"), "XeLaTeX is not installed")
class XeLaTeXTableIntegrationTests(unittest.TestCase):
    def test_persian_table_compiles_with_project_template(self) -> None:
        markdown = (
            "# فصل آزمایشی\n\n"
            "## جدول نمونه\n\n"
            "| مفهوم | مقدار |\n"
            "|---|---:|\n"
            "| دهانه | ۶۶/۰۰ متر |\n"
            "| نیروی افقی | Horizontal Thrust |"
        )
        template = TEMPLATE.read_text(encoding="utf-8")
        tex = template.replace("%%BOOK_TITLE%%", tex_escape("آزمون جدول"))
        tex = tex.replace("%%BOOK_SUBTITLE%%", tex_escape("آزمون یکپارچه"))
        tex = tex.replace("%%CHAPTERS%%", markdown_to_tex(markdown))

        output_root = ROOT / "output"
        output_root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="xelatex-table-", dir=output_root) as temp:
            temp_dir = Path(temp)
            tex_file = temp_dir / "fixture.tex"
            tex_file.write_text(tex, encoding="utf-8")
            result = subprocess.run(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-output-directory={temp_dir}",
                    str(tex_file),
                ],
                cwd=output_root,
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                msg=(result.stdout + "\n" + result.stderr)[-6000:],
            )
            self.assertTrue((temp_dir / "fixture.pdf").is_file())


if __name__ == "__main__":
    unittest.main()
