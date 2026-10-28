"""Local document ingestion and mechanical quotation matching.

Text and Markdown use only Python's standard library. PDF text extraction uses
either the optional ``pypdf`` package or the operator-installed ``pdftotext``
executable. Optional OCR needs ``pdftoppm`` and ``tesseract``. No remote service
is contacted. Page numbers are physical PDF pages, not printed page labels.
Offsets are Python Unicode character offsets in the retained extracted text.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from array import array

SCHEMA_VERSION = "regnav-esg-document/1"
MAX_BYTES = 25 * 1024 * 1024
MAX_PAGES = 500
MAX_CHARS = 5_000_000
MAX_OCR_PAGES = 20
MAX_MATCHES = 1000

# Optional Python PDF libraries run outside the parent process. On POSIX the
# worker limits address space and CPU; all platforms also have a wall timeout.
_PDF_WORKER = r'''
import json, sys
try:
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024, 1024 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_CPU, (35, 35))
    resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024 * 1024, 64 * 1024 * 1024))
except (ImportError, AttributeError, ValueError, OSError):
    pass
source, destination, mode, max_pages, max_chars = sys.argv[1:]
max_pages, max_chars = int(max_pages), int(max_chars)
class ControlledError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
try:
    import importlib.metadata
    if mode == "text":
        from pypdf import PdfReader
        reader = PdfReader(source, strict=False)
        if reader.is_encrypted:
            raise ControlledError("encrypted_pdf", "Provide a permitted, unencrypted PDF copy.")
        if len(reader.pages) > max_pages:
            raise ControlledError("page_limit", "PDF exceeds the selected page limit.")
        pages, total = [], 0
        for page in reader.pages:
            text = page.extract_text() or ""
            total += len(text)
            if total > max_chars:
                raise ControlledError("text_limit", "Extracted text exceeds the selected character limit.")
            pages.append(text)
        result = {"pages": pages, "parser": {"name": "pypdf", "version": importlib.metadata.version("pypdf")}}
    else:
        import pdfplumber
        tables, total_cells, total_chars = [], 0, 0
        with pdfplumber.open(source) as document:
            if len(document.pages) > max_pages:
                raise ControlledError("page_limit", "PDF exceeds the selected page limit.")
            for page_number, page in enumerate(document.pages, 1):
                for table_number, table in enumerate(page.find_tables(), 1):
                    values = table.extract()
                    rows = []
                    for row_number, (values_row, row) in enumerate(zip(values, table.rows), 1):
                        cells = []
                        for column_number, (value, box) in enumerate(zip(values_row, row.cells), 1):
                            total_cells += 1
                            total_chars += len(value or "")
                            if total_cells > 10000 or total_chars > max_chars or len(value or "") > 10000:
                                raise ControlledError("table_limit", "Extracted tables exceed the cell or text limits.")
                            cells.append({"row": row_number, "column": column_number, "text": value,
                                "bbox": list(box) if box is not None else None})
                        rows.append(cells)
                    tables.append({"page_number": page_number, "table_number": table_number,
                        "bbox": list(table.bbox), "coordinate_system": "pdf_points_from_top_left",
                        "rows": rows, "extraction_method": "pdfplumber_default_line_detection"})
                    if len(tables) > 100:
                        raise ControlledError("table_limit", "Extracted tables exceed the 100-table limit.")
        result = {"tables": tables, "table_parser": {"name": "pdfplumber", "version": importlib.metadata.version("pdfplumber")}}
except ControlledError as exc:
    result = {"error": {"code": exc.code, "message": exc.message}}
except MemoryError:
    result = {"error": {"code": "parser_resource_limit", "message": "PDF processing exceeded the memory limit."}}
except Exception:
    result = {"error": {"code": "invalid_pdf", "message": "The optional PDF parser could not process this document."}}
with open(destination, "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=True, allow_nan=False)
'''


class IngestionError(ValueError):
    """An input or optional parser failure with a stable machine-readable code."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _limit(value: int, maximum: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise IngestionError("invalid_limit", f"{name} must be between 1 and {maximum}.")
    return value


def _tool_version(executable: str, argument: str) -> str:
    result = subprocess.run([executable, argument], capture_output=True, timeout=10, check=False)
    lines = (result.stdout + result.stderr).decode("utf-8", errors="replace").splitlines()
    return lines[0][:200] if lines else "unknown"


def _pdf_worker(data, mode, max_pages, max_chars):
    with tempfile.TemporaryDirectory(prefix="regnav-pdf-worker-") as directory:
        source, output = Path(directory) / "source.pdf", Path(directory) / "result.json"
        source.write_bytes(data)
        try:
            result = subprocess.run(
                [sys.executable, "-I", "-c", _PDF_WORKER, str(source), str(output), mode, str(max_pages), str(max_chars)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=45, check=False)
        except subprocess.TimeoutExpired as exc:
            raise IngestionError("parser_timeout", "PDF processing exceeded 45 seconds.") from exc
        if result.returncode != 0 or not output.is_file():
            raise IngestionError("parser_failed", "The PDF worker failed or reached its resource limit.")
        if output.stat().st_size > 64 * 1024 * 1024:
            raise IngestionError("output_limit", "PDF parser output exceeds the result limit.")
        parsed = json.loads(output.read_text(encoding="utf-8"))
    if "error" in parsed:
        raise IngestionError(parsed["error"]["code"], parsed["error"]["message"])
    return parsed


def _pdf_text(data: bytes, backend: str, max_pages: int, max_chars: int):
    if backend not in {"auto", "pypdf", "pdftotext"}:
        raise IngestionError("invalid_backend", "pdf_backend must be auto, pypdf or pdftotext.")
    if backend in {"auto", "pypdf"}:
        if importlib.util.find_spec("pypdf") is None:
            if backend == "pypdf":
                raise IngestionError("parser_unavailable", "Install the optional pypdf package for this backend.")
        else:
            try:
                parsed = _pdf_worker(data, "text", max_pages, max_chars)
                return parsed["pages"], parsed["parser"]
            except IngestionError as exc:
                if backend != "auto" or exc.code not in {"invalid_pdf", "parser_failed", "parser_timeout", "parser_resource_limit"} or not shutil.which("pdftotext"):
                    raise
                pages, parser = _pdf_text(data, "pdftotext", max_pages, max_chars)
                parser["fallback"] = {"requested": "auto", "from": "pypdf", "reason": exc.code}
                return pages, parser
    executable = shutil.which("pdftotext")
    if executable is None:
        raise IngestionError("parser_unavailable", "PDF input requires optional pypdf or pdftotext.")
    with tempfile.TemporaryDirectory(prefix="regnav-pdf-") as directory:
        source = Path(directory) / "source.pdf"
        output = Path(directory) / "pages.txt"
        source.write_bytes(data)
        try:
            result = subprocess.run(
                [executable, "-layout", "-enc", "UTF-8", "-f", "1", "-l", str(max_pages + 1), str(source), str(output)],
                capture_output=True, timeout=45, check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise IngestionError("parser_timeout", "PDF extraction exceeded 45 seconds.") from exc
        if result.returncode != 0 or not output.is_file():
            raise IngestionError("invalid_pdf", "pdftotext could not read the PDF; it may be encrypted or malformed.")
        if output.stat().st_size > max_chars * 4:
            raise IngestionError("text_limit", "Extracted text exceeds the selected character limit.")
        text = output.read_text(encoding="utf-8")
    pages = text.split("\f")
    if text.endswith("\f"):
        pages.pop()
    if len(pages) > max_pages:
        raise IngestionError("page_limit", "PDF exceeds the selected page limit.")
    return pages, {"name": "pdftotext", "version": _tool_version(executable, "-v")}


def _ocr_empty_pages(data: bytes, pages: list[str]):
    empty = [i for i, page in enumerate(pages) if not page.strip()]
    if not empty:
        return pages, {"requested": True, "used": False, "pages": []}
    if len(empty) > MAX_OCR_PAGES:
        raise IngestionError("ocr_page_limit", f"OCR is limited to {MAX_OCR_PAGES} pages per document.")
    renderer, engine = shutil.which("pdftoppm"), shutil.which("tesseract")
    if not renderer or not engine:
        raise IngestionError("ocr_unavailable", "Explicit OCR requires pdftoppm and tesseract on PATH.")
    pages = list(pages)
    with tempfile.TemporaryDirectory(prefix="regnav-ocr-") as directory:
        source = Path(directory) / "source.pdf"
        source.write_bytes(data)
        for index in empty:
            image_base = Path(directory) / "page"
            try:
                render = subprocess.run(
                    [renderer, "-f", str(index + 1), "-l", str(index + 1), "-scale-to", "2400", "-png", "-singlefile", str(source), str(image_base)],
                    capture_output=True, timeout=30, check=False,
                )
                if render.returncode != 0:
                    raise IngestionError("ocr_failed", "A PDF page could not be rendered for OCR.")
                result = subprocess.run(
                    [engine, str(image_base) + ".png", "stdout", "-l", "eng"],
                    capture_output=True, timeout=30, check=False,
                )
                if result.returncode != 0:
                    raise IngestionError("ocr_failed", "Tesseract could not process a rendered page.")
                pages[index] = result.stdout.decode("utf-8", errors="replace")
            except subprocess.TimeoutExpired as exc:
                raise IngestionError("ocr_timeout", "OCR exceeded its per-page time limit.") from exc
    return pages, {"requested": True, "used": True, "engine": "tesseract", "version": _tool_version(engine, "--version"), "language": "eng", "pages": [i + 1 for i in empty]}


def ingest_document(path, *, source_id=None, pdf_backend="auto", ocr=False, tables=False,
                    max_bytes=MAX_BYTES, max_pages=MAX_PAGES, max_chars=MAX_CHARS):
    """Retain local document pages and source identity; never fetch a URL.

    Scan-only PDFs return ``needs_ocr`` and cannot enter extraction/retrieval.
    A mixed PDF with empty pages returns ``partial_text``; empty pages might be
    blank or scanned, so coverage remains explicitly unresolved. Text/Markdown
    pages are form-feed segments; no physical page numbering is invented.
    """
    _limit(max_bytes, MAX_BYTES, "max_bytes")
    _limit(max_pages, MAX_PAGES, "max_pages")
    _limit(max_chars, MAX_CHARS, "max_chars")
    if not isinstance(ocr, bool):
        raise IngestionError("invalid_ocr", "ocr must be a boolean.")
    if not isinstance(tables, bool):
        raise IngestionError("invalid_tables", "tables must be a boolean.")
    if source_id is not None and (not isinstance(source_id, str) or not source_id.strip() or len(source_id) > 200):
        raise IngestionError("invalid_source_id", "source_id must be a non-empty string up to 200 characters.")
    source = Path(path)
    if not source.is_file():
        raise IngestionError("source_unavailable", "Input must be an existing local file.")
    if source.stat().st_size > max_bytes:
        raise IngestionError("byte_limit", "Input exceeds the selected byte limit.")
    with source.open("rb") as stream:
        data = stream.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise IngestionError("byte_limit", "Input exceeds the selected byte limit.")
    suffix = source.suffix.lower()
    is_pdf = data.startswith(b"%PDF-")
    if suffix == ".pdf" and not is_pdf:
        raise IngestionError("invalid_pdf", "A .pdf input must have a PDF header.")
    warnings = []
    table_result = None
    ocr_metadata = {"requested": ocr, "used": False, "pages": []}
    if is_pdf:
        pages, parser = _pdf_text(data, pdf_backend, max_pages, max_chars)
        media_type, page_basis = "application/pdf", "physical_pdf_page"
        if parser.get("fallback"):
            warnings.append("The pypdf parser failed; pdftotext was used as the recorded fallback. Inspect original page layout and extraction coverage.")
        if ocr:
            pages, ocr_metadata = _ocr_empty_pages(data, pages)
            if ocr_metadata["used"]:
                warnings.append("OCR text can contain recognition errors; matching it does not verify the page image.")
        if tables:
            if importlib.util.find_spec("pdfplumber") is None:
                raise IngestionError("table_parser_unavailable", "Explicit table extraction requires the optional pdfplumber package.")
            table_result = _pdf_worker(data, "tables", max_pages, max_chars)
            warnings.append("Table detection uses PDF text and ruling lines; merged cells and borderless/image tables may be missing or misaligned.")
    else:
        if suffix not in {".txt", ".md", ".markdown"}:
            raise IngestionError("unsupported_format", "Use a PDF, UTF-8 text or Markdown file.")
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise IngestionError("invalid_encoding", "Text and Markdown must be valid UTF-8.") from exc
        if "\x00" in text:
            raise IngestionError("binary_text", "Text input contains NUL bytes.")
        pages = text.split("\f")
        if text.endswith("\f"):
            pages.pop()
        media_type = "text/markdown" if suffix in {".md", ".markdown"} else "text/plain"
        page_basis = "form_feed_segment"
        parser = {"name": "regnav-utf8", "version": "1"}
        if ocr:
            warnings.append("OCR applies to PDF input only; this text input was read directly.")
        if tables:
            raise IngestionError("unsupported_tables", "Geometric table extraction applies to PDF input only.")
    if len(pages) > max_pages:
        raise IngestionError("page_limit", "Input exceeds the selected page limit.")
    if sum(len(page) for page in pages) > max_chars:
        raise IngestionError("text_limit", "Extracted text exceeds the selected character limit.")
    empty = [i + 1 for i, page in enumerate(pages) if not page.strip()]
    if not pages or len(empty) == len(pages):
        status = "needs_ocr" if is_pdf else "empty_document"
        warnings.append("No extractable text was obtained; downstream analysis must not treat this as a successful extraction.")
    elif empty and is_pdf:
        status = "partial_text"
        warnings.append("Some PDF pages contain no extracted text. They may be blank or need OCR; document coverage is incomplete until inspected.")
    else:
        status = "ready"
    sha256 = _digest(data)
    parser.update({"page_basis": page_basis, "ocr": ocr_metadata})
    document = {
        "schema_version": SCHEMA_VERSION,
        "source": {"source_id": source_id or "doc-" + sha256[:16], "filename": source.name,
                   "sha256": sha256, "byte_size": len(data), "media_type": media_type},
        "parser": parser, "status": status,
        "pages": [{"page_number": i + 1, "text": page, "char_count": len(page),
                   "text_sha256": _digest(page.encode("utf-8")),
                   "text_status": "text" if page.strip() else "empty"} for i, page in enumerate(pages)],
        "page_count": len(pages), "text_char_count": sum(len(page) for page in pages),
        "empty_pages": empty, "warnings": warnings,
    }
    if table_result is not None:
        document.update(table_result)
        for table in document["tables"]:
            table["source_id"] = document["source"]["source_id"]
            table["source_sha256"] = sha256
            table["verification"] = "unreviewed_table_candidate"
    return document


def validate_document(document):
    """Validate the local analysis contract, including retained page text hashes."""
    if not isinstance(document, dict) or document.get("schema_version") != SCHEMA_VERSION:
        raise IngestionError("invalid_document", "Expected a RegNav ESG document record.")
    status = document.get("status")
    if not isinstance(status, str) or status not in {"ready", "partial_text"}:
        raise IngestionError(status if isinstance(status, str) else "invalid_document", "Document has no usable extracted text.")
    parser = document.get("parser")
    if not isinstance(parser, dict) or parser.get("page_basis") not in ("physical_pdf_page", "form_feed_segment"):
        raise IngestionError("invalid_document", "Document page basis is missing or invalid.")
    if not isinstance(document.get("warnings", []), list) or any(not isinstance(warning, str) for warning in document.get("warnings", [])):
        raise IngestionError("invalid_document", "Document warnings must be a list of strings.")
    source = document.get("source")
    if not isinstance(source, dict) or not isinstance(source.get("source_id"), str) or not source["source_id"] or not isinstance(source.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", source["sha256"]):
        raise IngestionError("invalid_document", "Document source identity is missing or invalid.")
    if not isinstance(source.get("filename"), str) or not source["filename"] or len(source["source_id"]) > 200:
        raise IngestionError("invalid_document", "Document source filename or identifier is invalid.")
    pages = document.get("pages")
    if not isinstance(pages, list) or not 1 <= len(pages) <= MAX_PAGES:
        raise IngestionError("invalid_document", "Document pages are missing or exceed the limit.")
    total = 0
    for number, page in enumerate(pages, 1):
        if not isinstance(page, dict) or type(page.get("page_number")) is not int or page["page_number"] != number or not isinstance(page.get("text"), str):
            raise IngestionError("invalid_document", "Page numbers and retained text are invalid.")
        total += len(page["text"])
        if page.get("text_sha256") != _digest(page["text"].encode("utf-8")):
            raise IngestionError("page_hash_mismatch", "Retained page text differs from its recorded hash.")
    if total > MAX_CHARS:
        raise IngestionError("text_limit", "Document exceeds the character limit.")
    if not any(page["text"].strip() for page in pages):
        raise IngestionError("empty_document", "Document contains no non-whitespace extracted text.")
    if "tables" in document:
        _validate_tables(document)
    return document


def _validate_tables(document):
    tables = document["tables"]
    if not isinstance(tables, list) or len(tables) > 100:
        raise IngestionError("invalid_document", "Tables must be an array of at most 100 table records.")
    cells_count, total_chars = 0, 0

    def box(value, nullable=False):
        if nullable and value is None:
            return
        if (not isinstance(value, list) or len(value) != 4 or
                any(type(number) not in (int, float) or not math.isfinite(number) for number in value) or
                value[0] > value[2] or value[1] > value[3]):
            raise IngestionError("invalid_document", "Table geometry must contain four finite ordered coordinates.")

    for table in tables:
        if not isinstance(table, dict):
            raise IngestionError("invalid_document", "Each table must be an object.")
        page = table.get("page_number")
        number = table.get("table_number")
        if type(page) is not int or not 1 <= page <= len(document["pages"]) or type(number) is not int or number < 1:
            raise IngestionError("invalid_document", "A table has an invalid page or table number.")
        if table.get("source_id") != document["source"]["source_id"] or table.get("source_sha256") != document["source"]["sha256"]:
            raise IngestionError("invalid_document", "Table source identity does not match the document.")
        box(table.get("bbox"))
        rows = table.get("rows")
        if not isinstance(rows, list) or len(rows) > 10000:
            raise IngestionError("invalid_document", "Table rows must be a bounded array.")
        for row_number, row in enumerate(rows, 1):
            if not isinstance(row, list) or len(row) > 10000:
                raise IngestionError("invalid_document", "Table cells must be a bounded array.")
            for column_number, cell in enumerate(row, 1):
                cells_count += 1
                if not isinstance(cell, dict) or type(cell.get("row")) is not int or type(cell.get("column")) is not int or cell["row"] != row_number or cell["column"] != column_number:
                    raise IngestionError("invalid_document", "Table cell coordinates are invalid.")
                text = cell.get("text")
                if text is not None and (not isinstance(text, str) or len(text) > 10000):
                    raise IngestionError("invalid_document", "Table cell text is invalid or too long.")
                total_chars += len(text or "")
                box(cell.get("bbox"), nullable=True)
                if cells_count > 10000 or total_chars > MAX_CHARS:
                    raise IngestionError("table_limit", "Table cell or text limits were exceeded.")


def citation(document, page_number, start, end):
    if type(page_number) is not int or not 1 <= page_number <= len(document["pages"]):
        raise IngestionError("invalid_page", "Citation page is outside the document.")
    page = document["pages"][page_number - 1]
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(page["text"]):
        raise IngestionError("invalid_offsets", "Citation offsets are outside retained page text.")
    return {"source_id": document["source"]["source_id"], "source_sha256": document["source"]["sha256"],
            "page_number": page_number, "page_basis": document["parser"]["page_basis"],
            "page_text_sha256": page["text_sha256"], "start": start, "end": end,
            "exact_quote": page["text"][start:end], "offset_unit": "unicode_codepoint",
            "verification": "text_location_only"}


def _normalised_with_offsets(text):
    # Compact integer arrays avoid millions of Python tuple objects on a long
    # page while preserving exact offsets into the original extracted text.
    chunks, starts, ends = [], array("I"), array("I")
    for match in re.finditer(r"\s+|\S+", text):
        if match.group().isspace():
            chunks.append(" ")
            starts.append(match.start())
            ends.append(match.end())
        else:
            chunks.append(match.group())
            starts.extend(range(match.start(), match.end()))
            ends.extend(range(match.start() + 1, match.end() + 1))
    return "".join(chunks), starts, ends


def match_quote(document, quote, *, page_number=None, normalise_whitespace=False):
    """Locate a quote mechanically; location is not evidential support or truth."""
    validate_document(document)
    if not isinstance(quote, str) or not quote.strip() or len(quote) > 10_000:
        raise IngestionError("invalid_quote", "Quote must contain 1 to 10,000 characters and non-whitespace text.")
    if not isinstance(normalise_whitespace, bool):
        raise IngestionError("invalid_option", "normalise_whitespace must be a boolean.")
    if page_number is not None and (type(page_number) is not int or not 1 <= page_number <= len(document["pages"])):
        raise IngestionError("invalid_page", "Page number is outside the document.")
    selected = document["pages"] if page_number is None else [document["pages"][page_number - 1]]

    def locate(normalised):
        needle = re.sub(r"\s+", " ", quote) if normalised else quote
        found = []
        count = 0
        for page in selected:
            haystack, starts, ends = _normalised_with_offsets(page["text"]) if normalised else (page["text"], None, None)
            start = 0
            while True:
                at = haystack.find(needle, start)
                if at < 0:
                    break
                end = at + len(needle)
                real_start, real_end = (starts[at], ends[end - 1]) if normalised else (at, end)
                count += 1
                if len(found) < MAX_MATCHES:
                    found.append(citation(document, page["page_number"], real_start, real_end))
                start = at + 1
        return found, count

    matches, count = locate(False)
    mode = "exact"
    if count == 0 and normalise_whitespace:
        matches, count = locate(True)
        mode = "normalised"
    status = "not_found" if not count else ("ambiguous_" + mode if count > 1 else mode)
    return {"status": status, "requested_quote": quote, "match_count": count,
            "matches": matches, "truncated": count > len(matches),
            "limitation": "A match locates extracted text; it does not establish substantive support or verify an OCR image."}


def document_to_markdown(document, *, include_tables=True):
    """Export a page-labelled Markdown transcription of retained source text.

    Dynamic code fences preserve text literally. This does not reconstruct PDF
    layout, infer headings, or turn PDF cells into verified structured facts.
    """
    validate_document(document)
    if not isinstance(include_tables, bool):
        raise IngestionError("invalid_option", "include_tables must be a boolean.")
    from regnav_evidence.reports import markdown_text
    escape = lambda value: markdown_text(str(value))
    source = document["source"]
    lines = ["# RegNav document transcription", "", "Source: " + escape(source["filename"]), "",
             "SHA-256: `" + source["sha256"] + "`", "",
             "Parser: " + escape(document["parser"].get("name", "unknown")) + " " + escape(document["parser"].get("version", "unknown")), "",
             "Status: " + document["status"], ""]
    for warning in document.get("warnings", []):
        lines.extend(["Note: " + escape(warning), ""])
    physical = document["parser"]["page_basis"] == "physical_pdf_page"
    for page in document["pages"]:
        label = "PDF page" if physical else "Text segment"
        lines.extend([f"## {label} {page['page_number']}", ""])
        fence = "`" * max(3, 1 + max((len(match.group()) for match in re.finditer(r"`+", page["text"])), default=0))
        lines.extend([fence + "text", page["text"], fence, ""])
        if include_tables:
            for table in document.get("tables", []):
                if table.get("page_number") != page["page_number"]:
                    continue
                rows = table.get("rows", [])
                if not rows:
                    continue
                width = max(len(row) for row in rows)
                lines.extend([f"### Candidate table {table['table_number']}", "",
                              "Unreviewed PDF table; cell coordinates are retained in JSON.", "",
                              "| " + " | ".join(f"Column {i + 1}" for i in range(width)) + " |",
                              "| " + " | ".join("---" for _ in range(width)) + " |"])
                for row in rows:
                    cells = [escape(cell.get("text") or "") for cell in row] + [""] * (width - len(row))
                    lines.append("| " + " | ".join(cells) + " |")
                lines.append("")
    return "\n".join(lines)
