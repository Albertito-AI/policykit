"""Offline evidence views and an adapter to the original ledger schema."""

from __future__ import annotations

import hashlib
import html
import json
import re
from urllib.parse import urlsplit


def _safe_id(value):
    return "s" + hashlib.sha256(str(value).encode("utf-8")).hexdigest()[:16]


def _citation(candidate):
    return candidate.get("citation", candidate.get("anchor", {}))


def _text(candidate):
    return candidate.get("text", candidate.get("claim", candidate.get("quote", "")))


def _validate_pair(document, extraction):
    from .ingest import validate_document
    from .model import literal_field_present
    validate_document(document)
    if not isinstance(extraction, dict):
        raise ValueError("Extraction must be an object")
    source = extraction.get("source", {})
    if not isinstance(source, dict):
        raise ValueError("Extraction source must be an object")
    if source.get("source_id") != document["source"]["source_id"] or source.get("sha256") != document["source"]["sha256"]:
        raise ValueError("Extraction and document source identities do not match")
    if not isinstance(extraction.get("fields"), list):
        raise ValueError("Extraction fields must be an array")
    for field in extraction["fields"]:
        if not isinstance(field, dict) or not isinstance(field.get("candidates"), list):
            raise ValueError("Invalid extraction field")
        for candidate in field["candidates"]:
            if not isinstance(candidate, dict):
                raise ValueError("Invalid candidate")
            cite = _citation(candidate)
            if not isinstance(cite, dict):
                raise ValueError("Candidate citation must be an object")
            number, start, end = cite.get("page_number"), cite.get("start"), cite.get("end")
            if type(number) is not int or not 1 <= number <= len(document["pages"]):
                raise ValueError("Candidate page is outside the source")
            page = document["pages"][number - 1]
            if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(page["text"]):
                raise ValueError("Candidate offsets are outside the source page")
            if (cite.get("source_id") != source["source_id"] or cite.get("source_sha256") != source["sha256"] or
                    cite.get("page_text_sha256") != page["text_sha256"] or cite.get("exact_quote") != page["text"][start:end] or
                    cite.get("page_basis") != document["parser"]["page_basis"] or _text(candidate) != cite["exact_quote"]):
                raise ValueError("Candidate citation does not match retained source text")
            captured = candidate.get("captured_fields", {})
            if not isinstance(captured, dict) or len(captured) > 32:
                raise ValueError("Candidate captured fields must be a bounded object")
            for key, value in captured.items():
                if not isinstance(key, str) or len(key) > 100 or not literal_field_present(value, cite["exact_quote"]):
                    raise ValueError("Captured field is not present in the cited passage")
    for warnings in (document.get("warnings", []), extraction.get("warnings", [])):
        if not isinstance(warnings, list) or any(not isinstance(w, str) for w in warnings):
            raise ValueError("Warnings must be an array of strings")


def _page_label(document):
    return "Physical page" if document.get("parser", {}).get("page_basis") == "physical_pdf_page" else "Text segment"


def to_ledger(documents, extractions, source_urls, *, title="RegNav extracted evidence candidates", jurisdiction="UNSPECIFIED"):
    """Export candidates as unreviewed context links, never checked evidence."""
    from regnav_evidence.validation import validate

    if len(documents) != len(extractions) or len(documents) != len(source_urls):
        raise ValueError("Provide one extraction and original source URL for every document")
    ledger = {"schema_version": "1.0", "title": title,
              "description": "Automatically extracted candidate passages. Context links do not establish claim support, legal compliance or human review.",
              "sources": [], "claims": []}
    seen = set()
    for document, extraction, url in zip(documents, extractions, source_urls):
        _validate_pair(document, extraction)
        if not isinstance(url, str):
            raise ValueError("An original HTTP(S) source URL is required for ledger export")
        parsed = urlsplit(url)
        if parsed.scheme not in {"https", "http"} or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("An original HTTP(S) source URL is required for ledger export")
        source = document["source"]
        sid = _safe_id(source["source_id"] + source["sha256"])
        if sid in seen:
            raise ValueError("The same document was supplied more than once")
        seen.add(sid)
        ledger["sources"].append({"id": sid, "title": source["filename"], "url": url,
                                  "source_type": "other", "jurisdiction": jurisdiction,
                                  "version": "sha256:" + source["sha256"],
                                  "notes": "Page text extracted by " + str(document.get("parser", {}).get("name", "unspecified parser"))})
        for field in extraction.get("fields", []):
            for index, item in enumerate(field.get("candidates", [])):
                cite = _citation(item)
                page = cite.get("page_number", item.get("page_number"))
                if type(page) is not int or page < 1:
                    raise ValueError("A candidate lacks a physical-page citation")
                start, end = cite.get("start"), cite.get("end")
                pinpoint = _page_label(document) + " " + str(page)
                if type(start) is int and type(end) is int:
                    pinpoint += f", extracted-text offsets {start}:{end}"
                identity = sid + str(field.get("field_id", field.get("id", "field"))) + str(index) + str(page) + _text(item)
                cid = "c" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
                ledger["claims"].append({"id": cid, "text": _text(item), "review_status": "unreviewed",
                                         "evidence": [{"source_id": sid, "pinpoint": pinpoint, "relation": "context"}],
                                         "notes": "Extracted passage, classified using transparent rules. Check context and original document before relying on it."})
    checked = validate(ledger)
    if checked.errors:
        raise ValueError("Generated ledger was structurally rejected: " + "; ".join(f.code for f in checked.errors))
    return ledger


def render_html(documents, extractions, *, assessments=None, title="RegNav ESG Workbench"):
    if len(documents) != len(extractions):
        raise ValueError("Every document must have exactly one extraction")
    esc = lambda value: html.escape(str(value), quote=True)
    cards, sources = [], []
    count = 0
    page_count = sum(len(d.get("pages", [])) for d in documents)
    for document, extraction in zip(documents, extractions):
        _validate_pair(document, extraction)
        source = document["source"]
        sid = _safe_id(source["source_id"] + source["sha256"])
        cards.append(f'<h2>{esc(source["filename"])}</h2><p class="muted">Source SHA-256: <code>{esc(source["sha256"])}</code></p>')
        for warning in document.get("warnings", []) + extraction.get("warnings", []):
            cards.append(f'<p class="notice">{esc(warning)}</p>')
        for field in extraction.get("fields", []):
            label = field.get("label", field.get("field_id", field.get("id", "Field")))
            candidates = field.get("candidates", [])
            cards.append(f'<section class="field"><h3>{esc(label)} <span class="tag">{esc(field.get("status", "candidate"))}</span></h3>')
            if field.get("truncated"):
                cards.append('<p class="notice">The candidate limit was reached. Additional matching passages may exist; this view is not a complete extraction.</p>')
            if not candidates:
                cards.append('<p class="muted">No matching passage located by this rule. This does not establish that the information is absent.</p>')
            for candidate in candidates:
                count += 1
                cite = _citation(candidate)
                page = cite.get("page_number", candidate.get("page_number"))
                cards.append(f'<article class="candidate"><p>{esc(_text(candidate))}</p>')
                if type(page) is int:
                    cards.append(f'<a class="anchor" href="#{sid}-p{page}">Inspect {esc(_page_label(document).lower())} {page}</a>')
                for name, value in candidate.get("captured_fields", {}).items():
                    cards.append(f' <span class="tag">{esc(name)}: {esc(value)}</span>')
                cards.append('</article>')
            cards.append('</section>')
        sources.append(f'<h2>{esc(source["filename"])}</h2>')
        for page in document.get("pages", []):
            number = page["page_number"]
            sources.append(f'<details id="{sid}-p{number}" class="source"><summary>{esc(_page_label(document))} {number} · {esc(page.get("text_status", "extracted text"))}</summary><pre>{esc(page["text"])}</pre></details>')
    extra = []
    for key, value in (assessments or {}).items():
        extra.append(f'<section class="field"><h2>{esc(key.replace("_", " ").title())}</h2><pre>{esc(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False))}</pre></section>')
    css = """
    :root{color-scheme:light;--navy:#102b43;--teal:#087f8c;--paper:#f5f6f3;--ink:#172f43}
    *{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
    header{background:var(--navy);color:white;padding:36px max(24px,calc((100vw - 1240px)/2))}header p{color:#cddce5;max-width:860px}
    h1{font-size:38px;line-height:1.15;margin:8px 0 16px}h2{font-size:24px;line-height:1.3;margin:28px 0 12px}h3{font-size:17px;margin:0 0 10px}
    .eyebrow{text-transform:uppercase;letter-spacing:2px;font-size:12px;color:#9bddda}.stats{display:flex;gap:34px}.stats strong{font-size:27px;color:#9bddda}
    nav{padding:16px 24px;background:white;position:sticky;top:0;border-bottom:1px solid #d9e2e5;z-index:2;display:flex;gap:24px;align-items:center;flex-wrap:wrap}
    nav input{margin-left:auto;border:1px solid #aabcc5;border-radius:5px;padding:10px;min-width:240px}a{color:#086f7a;text-underline-offset:3px}
    main{max-width:1290px;margin:26px auto;padding:0 24px}.layout{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:26px}
    .field{background:white;border:1px solid #dde5e8;border-radius:8px;padding:20px;margin:16px 0}.candidate{border-top:1px solid #e9eef0;padding:12px 0}.candidate p{margin:0 0 8px;white-space:pre-wrap}
    .tag{font-size:11px;display:inline-block;background:#e8f2f2;color:#28616a;padding:3px 8px;border-radius:4px;font-weight:500}.muted{font-size:13px;color:#647683;overflow-wrap:anywhere}
    .notice{background:#fff4d9;border-left:4px solid #d9a738;padding:13px;font-size:14px}.source{background:white;border:1px solid #dae2e7;margin:10px 0;border-radius:6px;scroll-margin-top:90px}.source summary{padding:14px;cursor:pointer;font-weight:600}
    pre{font:13px/1.55 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;padding:14px;max-height:650px;overflow:auto;margin:0}.anchor{font-size:13px}.hidden{display:none}footer{padding:24px;text-align:center;color:#657786;font-size:12px}
    @media(max-width:850px){.layout{grid-template-columns:1fr}h1{font-size:29px}nav input{width:100%;margin:0}.stats{gap:20px}}
    @media print{nav{display:none}.layout{display:block}pre{max-height:none}.source{break-inside:avoid}header{background:white;color:#102b43}header p{color:#102b43}}
    """
    script = """document.querySelector('#search').addEventListener('input',function(){const q=this.value.toLowerCase();document.querySelectorAll('.candidate').forEach(x=>x.classList.toggle('hidden',!x.textContent.toLowerCase().includes(q)));});function reveal(){const id=decodeURIComponent(location.hash.slice(1));const x=document.getElementById(id);if(x&&x.tagName==='DETAILS'){x.open=true;}}addEventListener('hashchange',reveal);reveal();"""
    # All document-derived text is escaped. No source text is inserted as code.
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>{esc(title)}</title><style>{css}</style></head><body>
    <header><div class="eyebrow">RegNav · evidence workspace</div><h1>{esc(title)}</h1><p>Inspect extracted sustainability passages alongside their source pages, then record the questions that require professional judgement.</p><div class="stats"><div><strong>{len(documents)}</strong> documents</div><div><strong>{page_count}</strong> pages</div><div><strong>{count}</strong> candidate passages</div></div></header>
    <nav><a href="#findings">Extracted passages</a><a href="#assessments">Assessments</a><a href="#sources">Source pages</a><input id="search" type="search" aria-label="Filter candidate passages" placeholder="Filter candidate passages"></nav>
    <main><p class="notice">Automated candidate extraction. A page citation establishes a location in extracted text; it does not establish factual truth, complete extraction, compliance or completed human review.</p><div class="layout"><section id="findings">{''.join(cards)}</section><section id="sources">{''.join(sources)}</section></div><section id="assessments">{''.join(extra)}</section></main><footer>Offline view. No analytics, external resources or network requests. Original source bytes and JSON records remain authoritative.</footer><script>{script}</script></body></html>'''
