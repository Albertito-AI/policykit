"""Deterministic local BM25 page retrieval over retained document text."""

from __future__ import annotations

import math
import re
from collections import Counter

from .ingest import IngestionError, citation, validate_document


def _tokens(text):
    return re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE)


def search_pages(document, query, *, limit=5):
    """Rank matching pages with BM25; scores are relevance scores, not confidence."""
    validate_document(document)
    if not isinstance(query, str) or not query.strip() or len(query) > 2000:
        raise IngestionError("invalid_query", "Query must contain 1 to 2,000 characters.")
    if type(limit) is not int or not 1 <= limit <= 50:
        raise IngestionError("invalid_limit", "limit must be between 1 and 50.")
    terms = list(dict.fromkeys(_tokens(query)))
    if not terms:
        raise IngestionError("invalid_query", "Query must contain searchable letters or digits.")
    pages = document["pages"]
    counts = [Counter(_tokens(page["text"])) for page in pages]
    lengths = [sum(count.values()) for count in counts]
    average = sum(lengths) / len(pages) or 1
    frequencies = {term: sum(term in count for count in counts) for term in terms}
    hits = []
    for page, count, length in zip(pages, counts, lengths):
        score = 0.0
        matched = []
        for term in terms:
            tf = count.get(term, 0)
            if not tf:
                continue
            matched.append(term)
            inverse = math.log(1 + (len(pages) - frequencies[term] + 0.5) / (frequencies[term] + 0.5))
            score += inverse * tf * 2.5 / (tf + 1.5 * (0.25 + 0.75 * length / average))
        if score <= 0:
            continue
        # Return a bounded, exactly located excerpt. Full text remains in the input.
        # Case-folded strings can change length (for example German sharp s).
        # Locate tokens in the original text so citation offsets stay exact.
        positions = [match.start() for match in re.finditer(r"[^\W_]+", page["text"], flags=re.UNICODE)
                     if match.group().casefold() in matched]
        first = min(positions)
        start = max(0, first - 180)
        end = min(len(page["text"]), start + 1200)
        hits.append({"page_number": page["page_number"], "score": round(score, 8),
                     "matched_terms": matched, "text": page["text"][start:end],
                     "citation": citation(document, page["page_number"], start, end)})
    hits.sort(key=lambda hit: (-hit["score"], hit["page_number"]))
    return {"query": query, "method": "bm25", "parameters": {"k1": 1.5, "b": 0.75},
            "hits": hits[:limit], "matching_pages": len(hits), "document_status": document["status"],
            "warnings": list(document.get("warnings", [])),
            "limitation": "Local lexical retrieval does not infer legal relevance, materiality or factual correctness."}
