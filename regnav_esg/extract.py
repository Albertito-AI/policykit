"""Transparent ESG candidate extraction and page-cited extractive summaries.

This module makes no model calls. Default categories are RegNav's illustrative
rules, not a reconstruction of any other supplier's unpublished schema. Matches
remain unreviewed candidates. Custom regular expressions are evaluated in a
bounded subprocess so pathological patterns cannot hang the calling process.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

from .ingest import IngestionError, citation, validate_document

MAX_FIELDS = 32
MAX_PATTERNS = 8
MAX_CANDIDATES = 50
PATTERN_TIMEOUT = 8


class ExtractionError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


DEFAULT_CONFIG = {
    "name": "RegNav illustrative ESG field rules",
    "version": "1",
    "fields": [
        {"id": "scope_1", "label": "Scope 1 emissions", "category": "emissions", "keywords": ["scope 1", "scope one"],
         "patterns": [r"\bScope\s*1(?:\s+(?:GHG\s+)?emissions?)?\s*(?:were|was|of|:|=)?\s*(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>tCO2e|tonnes?\s+CO2e|kgCO2e)\b"]},
        {"id": "scope_2", "label": "Scope 2 emissions", "category": "emissions", "keywords": ["scope 2", "scope two"],
         "patterns": [r"\bScope\s*2(?:\s+(?:GHG\s+)?emissions?)?\s*(?:were|was|of|:|=)?\s*(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>tCO2e|tonnes?\s+CO2e|kgCO2e)\b"]},
        {"id": "scope_3", "label": "Scope 3 emissions", "category": "emissions", "keywords": ["scope 3", "scope three"],
         "patterns": [r"\bScope\s*3(?:\s+(?:GHG\s+)?emissions?)?\s*(?:were|was|of|:|=)?\s*(?P<value>\d[\d,]*(?:\.\d+)?)\s*(?P<unit>tCO2e|tonnes?\s+CO2e|kgCO2e)\b"]},
        {"id": "energy", "label": "Energy", "category": "environment", "keywords": ["energy", "electricity", "renewable"], "patterns": []},
        {"id": "water", "label": "Water", "category": "environment", "keywords": ["water", "withdrawal", "discharge"], "patterns": []},
        {"id": "waste", "label": "Waste", "category": "environment", "keywords": ["waste", "recycling", "recycled"], "patterns": []},
        {"id": "targets", "label": "Targets and plans", "category": "strategy", "keywords": ["target", "net zero", "net-zero", "decarbonisation", "decarbonization"], "patterns": []},
        {"id": "governance", "label": "Governance", "category": "governance", "keywords": ["board", "committee", "oversight", "governance"], "patterns": []},
        {"id": "workforce", "label": "Workforce and safety", "category": "social", "keywords": ["employee", "workforce", "fatalities", "injury", "training"], "patterns": []},
        {"id": "assurance", "label": "Assurance statements", "category": "assurance", "keywords": ["assurance", "verified", "verification", "auditor"], "patterns": []},
    ],
}


def _config(config):
    if config is None:
        config = DEFAULT_CONFIG
    if not isinstance(config, dict) or set(config) - {"name", "version", "fields"}:
        raise ExtractionError("invalid_config", "Configuration must contain fields and optional name/version only.")
    fields = config.get("fields")
    if not isinstance(fields, list) or not 1 <= len(fields) <= MAX_FIELDS:
        raise ExtractionError("invalid_config", f"Supply 1 to {MAX_FIELDS} fields.")
    cleaned, seen = [], set()
    for field in fields:
        if not isinstance(field, dict) or set(field) - {"id", "label", "category", "keywords", "patterns"}:
            raise ExtractionError("invalid_config", "Each field allows id, label, category, keywords and patterns only.")
        identifier = field.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_\-]{0,63}", identifier) or identifier in seen:
            raise ExtractionError("invalid_config", "Field IDs must be unique identifiers up to 64 characters.")
        seen.add(identifier)
        label, category = field.get("label", identifier), field.get("category", "custom")
        if not isinstance(label, str) or not label.strip() or len(label) > 200 or not isinstance(category, str) or not category.strip() or len(category) > 100:
            raise ExtractionError("invalid_config", "Labels and categories must be bounded non-empty strings.")
        keywords, patterns = field.get("keywords", []), field.get("patterns", [])
        if not isinstance(keywords, list) or len(keywords) > 32 or any(not isinstance(word, str) or not word.strip() or len(word) > 120 for word in keywords):
            raise ExtractionError("invalid_config", "Supply at most 32 non-empty keywords of at most 120 characters.")
        if not isinstance(patterns, list) or len(patterns) > MAX_PATTERNS or any(not isinstance(pattern, str) or not pattern or len(pattern) > 1000 for pattern in patterns):
            raise ExtractionError("invalid_config", f"Supply at most {MAX_PATTERNS} regex patterns of at most 1,000 characters.")
        if not keywords and not patterns:
            raise ExtractionError("invalid_config", "Each field needs at least one keyword or pattern.")
        for pattern in patterns:
            try:
                compiled = re.compile(pattern, re.IGNORECASE)
            except (re.error, OverflowError, RecursionError) as exc:
                raise ExtractionError("invalid_pattern", f"Invalid regex for field {identifier}.") from exc
            if len(compiled.groupindex) > 16:
                raise ExtractionError("invalid_pattern", "A pattern may have at most 16 named capture groups.")
        cleaned.append({"id": identifier, "label": label, "category": category,
                        "keywords": list(keywords), "patterns": list(patterns)})
    for key in ("name", "version"):
        if key in config and (not isinstance(config[key], str) or len(config[key]) > 200):
            raise ExtractionError("invalid_config", "Configuration name and version must be strings up to 200 characters.")
    return {"name": config.get("name", "Operator-supplied field rules"),
            "version": config.get("version", "unspecified"), "fields": cleaned}


def sentence_spans(text):
    """Yield exact text spans separated by newlines or likely sentence endings."""
    start = 0
    for boundary in re.finditer(r"\n+|(?<=[.!?])\s+(?=[A-Z])", text):
        end = boundary.start()
        left, right = start, end
        while left < right and text[left].isspace():
            left += 1
        while right > left and text[right - 1].isspace():
            right -= 1
        if right > left:
            yield left, right
        start = boundary.end()
    left, right = start, len(text)
    while left < right and text[left].isspace():
        left += 1
    while right > left and text[right - 1].isspace():
        right -= 1
    if right > left:
        yield left, right


def _keyword_regex(word):
    return re.compile(r"(?<!\w)" + r"\s+".join(re.escape(part) for part in word.split()) + r"(?!\w)", re.IGNORECASE)


_PATTERN_WORKER = r'''
import json, re, sys
payload = json.load(sys.stdin)
result = {}
for field in payload["fields"]:
    matches = []
    truncated = False
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in field["patterns"]]
    if any(pattern.match("") is not None for pattern in compiled):
        print(json.dumps({"error": "invalid_pattern"}))
        sys.exit(0)
    for page in payload["pages"]:
        for pattern_index, pattern in enumerate(compiled):
            for match in pattern.finditer(page["text"]):
                if match.start() == match.end():
                    continue
                if len(matches) >= payload["limit"]:
                    truncated = True
                    break
                if match.end() - match.start() > 1200:
                    matches.append({"page_number": page["page_number"], "start": match.start(),
                        "end": match.start() + 1200, "groups": {}, "pattern_index": pattern_index,
                        "match_truncated": True, "omitted_capture_groups": list(match.groupdict())})
                else:
                    raw_groups = {key: value for key, value in match.groupdict().items() if value is not None}
                    # Lookarounds can capture values outside the matched span.
                    # Such a value must not appear as if this citation supports it.
                    groups = {key: value for key, value in raw_groups.items()
                              if match.start() <= match.start(key) <= match.end(key) <= match.end()}
                    matches.append({"page_number": page["page_number"], "start": match.start(),
                        "end": match.end(), "groups": groups, "pattern_index": pattern_index,
                        "match_truncated": False, "omitted_capture_groups": [key for key in raw_groups if key not in groups]})
            if truncated:
                break
        if truncated:
            break
    result[field["id"]] = {"matches": matches, "truncated": truncated}
print(json.dumps(result, ensure_ascii=True))
'''


def _pattern_matches(document, fields, limit):
    if not any(field["patterns"] for field in fields):
        return {field["id"]: {"matches": [], "truncated": False} for field in fields}
    payload = {"fields": fields, "pages": [{"page_number": page["page_number"], "text": page["text"]} for page in document["pages"]], "limit": limit}
    try:
        result = subprocess.run([sys.executable, "-I", "-c", _PATTERN_WORKER], input=json.dumps(payload),
                                capture_output=True, text=True, timeout=PATTERN_TIMEOUT, check=False)
    except subprocess.TimeoutExpired as exc:
        raise ExtractionError("pattern_timeout", "Custom/default pattern evaluation exceeded eight seconds; simplify the patterns or input.") from exc
    if result.returncode != 0:
        raise ExtractionError("pattern_failure", "Pattern evaluation failed; no extraction result was accepted.")
    if len(result.stdout) > 4_000_000:
        raise ExtractionError("output_limit", "Pattern result exceeded its output limit.")
    parsed = json.loads(result.stdout)
    if parsed.get("error") == "invalid_pattern":
        raise ExtractionError("invalid_pattern", "Patterns must not match empty text.")
    return parsed


def _context_span(text, start, end):
    """Retain the surrounding source sentence where the bounded excerpt permits."""
    left, right = start, end
    for sentence_start, sentence_end in sentence_spans(text):
        if sentence_start <= start < sentence_end:
            left = sentence_start
        if sentence_start < end <= sentence_end:
            right = sentence_end
            break
    if right - left <= 1200:
        return left, right, False
    clipped_left = max(left, start - 150)
    clipped_right = min(right, clipped_left + 1200)
    if clipped_right < end:
        clipped_left, clipped_right = start, end
    return clipped_left, clipped_right, True


def extract_candidates(document, *, config=None, max_per_field=20):
    """Find evidence candidates using explicit field rules and exact citations.

    Custom named regex groups are retained as strings under ``captured_fields``.
    No units are converted, periods assigned or missing values invented. A
    no-match result means only that these rules did not find a candidate.
    """
    validate_document(document)
    if type(max_per_field) is not int or not 1 <= max_per_field <= MAX_CANDIDATES:
        raise ExtractionError("invalid_limit", f"max_per_field must be between 1 and {MAX_CANDIDATES}.")
    rules = _config(config)
    pattern_results = _pattern_matches(document, rules["fields"], max_per_field)
    output = []
    for field in rules["fields"]:
        candidates = []
        seen = set()
        truncated = pattern_results[field["id"]]["truncated"]
        for match in pattern_results[field["id"]]["matches"]:
            matched_anchor = citation(document, match["page_number"], match["start"], match["end"])
            page_text = document["pages"][match["page_number"] - 1]["text"]
            context_start, context_end, context_truncated = _context_span(page_text, match["start"], match["end"])
            anchor = citation(document, match["page_number"], context_start, context_end)
            key = (match["page_number"], match["start"], match["end"])
            if key in seen:
                continue
            seen.add(key)
            candidates.append({"status": "unreviewed_candidate", "text": anchor["exact_quote"],
                               "method": "regex", "pattern_index": match["pattern_index"],
                               "captured_fields": match["groups"], "match_truncated": match["match_truncated"],
                               "omitted_capture_groups": match["omitted_capture_groups"],
                               "context_truncated": context_truncated, "matched_citation": matched_anchor,
                               "citation": anchor})
        compiled_keywords = [(word, _keyword_regex(word)) for word in field["keywords"]]
        full = False
        for page in document["pages"]:
            if full:
                break
            for start, end in sentence_spans(page["text"]):
                sentence = page["text"][start:end]
                matches = [(word, regex.search(sentence)) for word, regex in compiled_keywords]
                matches = [(word, match) for word, match in matches if match is not None]
                if not matches:
                    continue
                # If a bounded regex candidate already covers this sentence, do not duplicate it.
                if any(number == page["page_number"] and start <= left < right <= end for number, left, right in seen):
                    continue
                if len(candidates) >= max_per_field:
                    truncated = True
                    full = True
                    break
                first = min(match.start() for _, match in matches)
                quote_start = start + max(0, first - 200) if end - start > 1200 else start
                quote_end = min(end, quote_start + 1200)
                anchor = citation(document, page["page_number"], quote_start, quote_end)
                seen.add((page["page_number"], quote_start, quote_end))
                candidates.append({"status": "unreviewed_candidate", "text": anchor["exact_quote"],
                                   "method": "keyword_sentence", "matched_keywords": [word for word, _ in matches],
                                   "captured_fields": {}, "match_truncated": end - start > 1200,
                                   "citation": anchor})
        candidates.sort(key=lambda item: (item["citation"]["page_number"], item["citation"]["start"]))
        output.append({"field_id": field["id"], "label": field["label"], "category": field["category"],
                       "status": "candidates_found" if candidates else "not_found_by_rules",
                       "candidates": candidates, "truncated": truncated})
    return {"schema_version": "regnav-esg-extraction/1", "source": dict(document["source"]),
            "document_status": document["status"], "method": "local_rules", "rules": rules,
            "fields": output, "summary": extractive_summary(document, config=rules)["sentences"],
            "warnings": list(document.get("warnings", [])),
            "limitations": ["Candidates require human interpretation and review.",
                            "Not found by these rules does not mean absent from the report.",
                            "This is local rule-based extraction, not semantic or generative AI extraction.",
                            "Captured values, units and context are not independently verified."]}


def extractive_summary(document, *, max_sentences=8, config=None):
    """Select verbatim ESG-related passages; do not generate new factual claims."""
    validate_document(document)
    if type(max_sentences) is not int or not 1 <= max_sentences <= 50:
        raise ExtractionError("invalid_limit", "max_sentences must be between 1 and 50.")
    rules = _config(config)
    keywords = list(dict.fromkeys(word for field in rules["fields"] for word in field["keywords"]))
    compiled = [_keyword_regex(word) for word in keywords]
    ranked = []
    for page in document["pages"]:
        for start, end in sentence_spans(page["text"]):
            passage = page["text"][start:end]
            matches = [regex.search(passage) for regex in compiled]
            matches = [match for match in matches if match is not None]
            score = len(matches)
            if not score:
                continue
            first = min(match.start() for match in matches)
            quote_start = start + max(0, first - 200) if end - start > 1200 else start
            quote_end = min(end, quote_start + 1200)
            ranked.append((score, page["page_number"], quote_start, quote_end, end - start > 1200))
    selected = sorted(ranked, key=lambda item: (-item[0], item[1], item[2]))[:max_sentences]
    selected.sort(key=lambda item: (item[1], item[2]))
    sentences = []
    for score, page, start, end, truncated in selected:
        anchor = citation(document, page, start, end)
        sentences.append({"text": anchor["exact_quote"], "citation": anchor,
                          "selection_keyword_count": score, "excerpt_truncated": truncated})
    return {"method": "extractive_keyword_selection", "sentences": sentences,
            "document_status": document["status"], "warnings": list(document.get("warnings", [])),
            "limitation": "These are selected source passages, not a comprehensive or independently verified summary."}
