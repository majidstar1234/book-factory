from __future__ import annotations

import os
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
            pdf_path = temp_dir / "fixture.pdf"
            self.assertTrue(pdf_path.is_file())
            if os.getenv("PRESERVE_XELATEX_FIXTURE") == "1":
                artifact_path = ROOT / "output" / "persian-table-fixture.pdf"
                artifact_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(pdf_path, artifact_path)


    def test_veresk_curve_family_table_compiles(self) -> None:
        """Compile the exact Veresk curve-comparison LaTeX fixture."""
        fixture = ROOT / "golden_examples" / "veresk_curve_family_comparison.tex"
        table_source = fixture.read_text(encoding="utf-8")

        self.assertIn(r"\resizebox{\textwidth}{!}", table_source)
        self.assertIn(r"\toprule", table_source)
        self.assertIn(r"\bottomrule", table_source)
        self.assertIn(r"\label{tab:ch3_curve_comparison}", table_source)

        template = TEMPLATE.read_text(encoding="utf-8")
        tex = template.replace(
            "%%BOOK_TITLE%%",
            tex_escape("آزمون جدول خانواده منحنی‌های ورسک")
        )
        tex = tex.replace(
            "%%BOOK_SUBTITLE%%",
            tex_escape("آزمون یکپارچه جدول هندسی و مکانیکی")
        )
        tex = tex.replace(
            "%%CHAPTERS%%",
            r"\chapter{آزمون جدول خانواده منحنی‌ها}" + "\n\n" + table_source
        )

        output_root = ROOT / "output"
        output_root.mkdir(parents=True, exist_ok=True)

        with tempfile.TemporaryDirectory(
            prefix="xelatex-veresk-table-",
            dir=output_root
        ) as temp:
            temp_dir = Path(temp)
            tex_file = temp_dir / "fixture.tex"
            tex_file.write_text(tex, encoding="utf-8")

            result = subprocess.run(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    "-file-line-error",
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
                msg=(result.stdout + "\n" + result.stderr)[-10000:],
            )

            pdf_path = temp_dir / "fixture.pdf"

            self.assertTrue(
                pdf_path.is_file(),
                "XeLaTeX returned success but did not produce the PDF.",
            )

            self.assertGreater(
                pdf_path.stat().st_size,
                10_000,
                "The generated fixture PDF is unexpectedly small.",
            )

            if os.getenv("PRESERVE_XELATEX_FIXTURE") == "1":
                artifact_path = (
                    ROOT / "output" / "veresk-curve-comparison-fixture.pdf"
                )
                shutil.copy2(pdf_path, artifact_path)

if __name__ == "__main__":
    unittest.main()
