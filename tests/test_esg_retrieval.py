import tempfile
import unittest
from pathlib import Path

from regnav_esg.ingest import IngestionError, ingest_document
from regnav_esg.retrieval import search_pages


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        path = Path(self.temporary.name) / "fictional.txt"
        path.write_text("Fictional emissions Scope 1 report.\fWater water withdrawal 200 m3.\fThe board reviews the report.", encoding="utf-8")
        self.document = ingest_document(path)

    def test_bm25_finds_page_and_exact_excerpt(self):
        result = search_pages(self.document, "water withdrawal")
        self.assertEqual(result["method"], "bm25")
        self.assertEqual(result["hits"][0]["page_number"], 2)
        self.assertEqual(result["hits"][0]["text"], result["hits"][0]["citation"]["exact_quote"])
        self.assertGreater(result["hits"][0]["score"], 0)

    def test_no_lexical_match_returns_no_invented_answer(self):
        self.assertEqual(search_pages(self.document, "biodiversity")["hits"], [])

    def test_query_limits_and_determinism(self):
        self.assertEqual(search_pages(self.document, "report"), search_pages(self.document, "report"))
        self.assertEqual(len(search_pages(self.document, "report", limit=1)["hits"]), 1)
        for query in ["", "!!!", "x" * 2001]:
            with self.assertRaises(IngestionError):
                search_pages(self.document, query)
        with self.assertRaises(IngestionError):
            search_pages(self.document, "water", limit=100)

    def test_unicode_casefold_does_not_shift_source_offsets(self):
        path = Path(self.temporary.name) / "unicode.txt"
        path.write_text("ß " * 1000 + "WATER withdrawal evidence.", encoding="utf-8")
        document = ingest_document(path)
        hit = search_pages(document, "water")["hits"][0]
        self.assertIn("WATER", hit["text"])
        self.assertEqual(document["pages"][0]["text"][hit["citation"]["start"]:hit["citation"]["end"]], hit["text"])


if __name__ == "__main__":
    unittest.main()
