"""Exercise actual local text/PDF parsing and exact source locations."""

import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from regnav_esg.ingest import IngestionError, document_to_markdown, ingest_document, match_quote, validate_document


def tiny_pdf(pages):
    """Create a minimal, fictional PDF fixture without a PDF-writing dependency."""
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b""]
    kids = []
    for text in pages:
        page_id = len(objects) + 1
        stream_id = page_id + 1
        kids.append(f"{page_id} 0 R")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /Contents {stream_id} 0 R >>".encode())
        escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET".encode("ascii") if text else b""
        objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(kids)} >>".encode()
    data = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{i} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(data)
    data.extend(f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode())
    data.extend(f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    return bytes(data)


class IngestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def text(self, value, suffix=".md"):
        path = self.root / ("fictional" + suffix)
        path.write_text(value, encoding="utf-8")
        return path

    def test_text_pages_byte_hash_and_unchanged_input(self):
        path = self.text("Fictional report\nScope 1: 100 tCO2e.\fWater: 200 m3.")
        before = path.read_bytes()
        document = ingest_document(path)
        self.assertEqual(document["page_count"], 2)
        self.assertEqual(document["source"]["sha256"], hashlib.sha256(before).hexdigest())
        self.assertEqual(document["parser"]["page_basis"], "form_feed_segment")
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(document["status"], "ready")
        json.dumps(document, allow_nan=False)

    def test_duplicate_exact_quote_retains_all_locations(self):
        document = ingest_document(self.text("water 20. water 20.\fwater 20."))
        found = match_quote(document, "water 20.")
        self.assertEqual(found["status"], "ambiguous_exact")
        self.assertEqual(found["match_count"], 3)
        for anchor in found["matches"]:
            text = document["pages"][anchor["page_number"] - 1]["text"]
            self.assertEqual(text[anchor["start"]:anchor["end"]], "water 20.")
        self.assertEqual(match_quote(document, "water 20.", page_number=2)["status"], "exact")

    def test_whitespace_match_keeps_original_quote_and_offsets(self):
        document = ingest_document(self.text("前言 Scope\n  1 emissions\t100 tCO2e."))
        absent = match_quote(document, "Scope 1 emissions 100 tCO2e")
        self.assertEqual(absent["status"], "not_found")
        found = match_quote(document, "Scope 1 emissions 100 tCO2e", normalise_whitespace=True)
        self.assertEqual(found["status"], "normalised")
        anchor = found["matches"][0]
        self.assertEqual(anchor["exact_quote"], "Scope\n  1 emissions\t100 tCO2e")
        self.assertEqual(anchor["start"], 3)

    def test_tampered_page_hash_rejected(self):
        document = ingest_document(self.text("Source text"))
        document["pages"][0]["text"] = "Altered source text"
        with self.assertRaises(IngestionError) as error:
            validate_document(document)
        self.assertEqual(error.exception.code, "page_hash_mismatch")

    def test_source_hash_must_be_text(self):
        document = ingest_document(self.text("Source text"))
        document["source"]["sha256"] = int("1" * 64)
        with self.assertRaises(IngestionError):
            validate_document(document)

    def test_limits_encoding_and_empty_input(self):
        with self.assertRaises(IngestionError):
            ingest_document(self.text("abc"), max_bytes=2)
        with self.assertRaises(IngestionError):
            ingest_document(self.text("a\fb"), max_pages=1)
        path = self.root / "invalid.txt"
        path.write_bytes(b"\xff\xfe")
        with self.assertRaises(IngestionError):
            ingest_document(path)
        document = ingest_document(self.text("   "))
        self.assertEqual(document["status"], "empty_document")
        with self.assertRaises(IngestionError):
            validate_document(document)

    @unittest.skipUnless(importlib.util.find_spec("pypdf"), "Optional pypdf is not installed")
    def test_real_pdf_two_pages_and_needs_ocr(self):
        path = self.root / "fictional.pdf"
        path.write_bytes(tiny_pdf(["Scope 1: 100 tCO2e.", "Water: 200 m3."]))
        document = ingest_document(path, pdf_backend="pypdf")
        self.assertEqual(document["page_count"], 2)
        self.assertEqual(match_quote(document, "Water: 200 m3.")["matches"][0]["page_number"], 2)
        self.assertEqual(document["parser"]["page_basis"], "physical_pdf_page")
        path.write_bytes(tiny_pdf([""]))
        empty = ingest_document(path, pdf_backend="pypdf")
        self.assertEqual(empty["status"], "needs_ocr")
        with self.assertRaises(IngestionError) as error:
            validate_document(empty)
        self.assertEqual(error.exception.code, "needs_ocr")

    @unittest.skipUnless(shutil.which("pdftotext"), "Optional pdftotext is not installed")
    def test_real_pdftotext_backend_and_page_limit(self):
        path = self.root / "fictional.pdf"
        path.write_bytes(tiny_pdf(["Scope 1: 100 tCO2e.", "Water: 200 m3."]))
        document = ingest_document(path, pdf_backend="pdftotext")
        self.assertEqual(document["page_count"], 2)
        self.assertEqual(document["parser"]["name"], "pdftotext")
        with self.assertRaises(IngestionError) as error:
            ingest_document(path, pdf_backend="pdftotext", max_pages=1)
        self.assertEqual(error.exception.code, "page_limit")

    @unittest.skipUnless(importlib.util.find_spec("pypdf"), "Optional pypdf is not installed")
    def test_mixed_pdf_does_not_hide_missing_text(self):
        path = self.root / "fictional.pdf"
        path.write_bytes(tiny_pdf(["Water 20 m3.", ""]))
        document = ingest_document(path)
        self.assertEqual(document["status"], "partial_text")
        self.assertEqual(document["empty_pages"], [2])
        self.assertTrue(document["warnings"])

    def test_markdown_transcription_labels_segments_and_preserves_fences(self):
        document = ingest_document(self.text("Literal ``` source fence.\fScope 1 evidence."))
        exported = document_to_markdown(document)
        self.assertIn("## Text segment 1", exported)
        self.assertIn("## Text segment 2", exported)
        self.assertIn("````text", exported)
        self.assertIn("Literal ``` source fence.", exported)
        self.assertIn(document["source"]["sha256"], exported)
        self.assertNotIn("PDF page", exported)

    def test_malformed_optional_tables_are_rejected_before_export(self):
        document = ingest_document(self.text("Water evidence."))
        document["tables"] = ["not a table"]
        with self.assertRaises(IngestionError):
            document_to_markdown(document)

    def test_markdown_metacharacters_in_metadata_and_table_cells_are_literal(self):
        document = ingest_document(self.text("Fictional source text."))
        value = "~~excluded~~ *covered* [scope](https://example.invalid) `code` | <tag>"
        document["source"]["filename"] = value
        document["parser"]["name"] = value
        document["warnings"] = [value]
        document["tables"] = [{
            "page_number": 1, "table_number": 1, "bbox": [0, 0, 200, 40],
            "source_id": document["source"]["source_id"],
            "source_sha256": document["source"]["sha256"],
            "rows": [[{"row": 1, "column": 1, "text": value, "bbox": [0, 0, 200, 40]}]],
        }]
        exported = document_to_markdown(document)
        self.assertNotIn("~~excluded~~", exported)
        self.assertNotIn("*covered*", exported)
        self.assertNotIn("[scope](", exported)
        self.assertNotIn("`code`", exported)
        self.assertNotIn("<tag>", exported)
        self.assertIn(r"\~\~excluded\~\~", exported)
        self.assertIn(r"\*covered\*", exported)
        self.assertIn(r"\[scope\]", exported)
        self.assertIn(r"\`code\`", exported)
        self.assertIn(r"\| &lt;tag&gt;", exported)
        # Optional renderer verifies the original regression's visual effect.
        if importlib.util.find_spec("mistune"):
            import mistune
            rendered = mistune.create_markdown(plugins=["table", "strikethrough"])(exported)
            self.assertNotIn("<del>", rendered)
            self.assertNotIn("<em>", rendered)
            self.assertNotIn("<a href=", rendered)
            self.assertNotIn("<code>code</code>", rendered)
            self.assertIn("~~excluded~~ *covered* [scope](https://example.invalid)", rendered)

    @unittest.skipUnless(shutil.which("pdftotext") and importlib.util.find_spec("pypdf"), "Both optional PDF backends are needed")
    def test_auto_parser_fallback_is_recorded_and_explicit_failure_preserved(self):
        path = self.root / "fictional.pdf"
        path.write_bytes(tiny_pdf(["Fictional source evidence."]))
        with patch("regnav_esg.ingest._pdf_worker", side_effect=IngestionError("invalid_pdf", "Parser fixture failure")):
            document = ingest_document(path)
            self.assertEqual(document["parser"]["name"], "pdftotext")
            self.assertEqual(document["parser"]["fallback"]["reason"], "invalid_pdf")
            self.assertTrue(document["warnings"])
            with self.assertRaises(IngestionError):
                ingest_document(path, pdf_backend="pypdf")

    @unittest.skipUnless(importlib.util.find_spec("pdfplumber") and importlib.util.find_spec("reportlab"), "Optional table fixtures need pdfplumber and reportlab")
    def test_actual_pdf_table_cells_regions_and_markdown(self):
        from reportlab.pdfgen import canvas
        path = self.root / "fictional-table.pdf"
        pdf = canvas.Canvas(str(path))
        pdf.drawString(60, 760, "FICTIONAL TRAINING TABLE")
        for y in (700, 670, 640):
            pdf.line(60, y, 340, y)
        for x in (60, 230, 340):
            pdf.line(x, 640, x, 700)
        pdf.drawString(70, 680, "Metric")
        pdf.drawString(240, 680, "Value")
        pdf.drawString(70, 650, "Water")
        pdf.drawString(240, 650, "200 m3")
        pdf.save()
        document = ingest_document(path, tables=True)
        self.assertEqual(len(document["tables"]), 1)
        table = document["tables"][0]
        self.assertEqual(table["rows"][1][1]["text"], "200 m3")
        self.assertEqual(len(table["rows"][1][1]["bbox"]), 4)
        self.assertEqual(table["source_sha256"], document["source"]["sha256"])
        self.assertEqual(table["page_number"], 1)
        self.assertIn("## PDF page 1", document_to_markdown(document))
        self.assertIn("| Water | 200 m3 |", document_to_markdown(document))

    @unittest.skipUnless(importlib.util.find_spec("PIL") and importlib.util.find_spec("pypdf") and shutil.which("pdftoppm") and shutil.which("tesseract"), "Optional OCR fixture needs Pillow, pypdf and OCR tools")
    def test_actual_scanned_pdf_requires_opt_in_ocr(self):
        from PIL import Image, ImageDraw, ImageFont
        path = self.root / "fictional-scan.pdf"
        image = Image.new("RGB", (1600, 500), "white")
        draw = ImageDraw.Draw(image)
        font_path = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        if not font_path.is_file():
            self.skipTest("The OCR fixture font is not installed")
        draw.text((80, 100), "FICTIONAL TRAINING REPORT", font=ImageFont.truetype(str(font_path), 45), fill="black")
        image.save(path, "PDF", resolution=120)
        self.assertEqual(ingest_document(path)["status"], "needs_ocr")
        document = ingest_document(path, ocr=True)
        self.assertEqual(document["status"], "ready")
        self.assertTrue(document["parser"]["ocr"]["used"])
        self.assertEqual(match_quote(document, "FICTIONAL TRAINING REPORT")["status"], "exact")


if __name__ == "__main__":
    unittest.main()
