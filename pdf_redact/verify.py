"""Independent proof that redacted values are gone from the output file.

This deliberately does not trust the redaction step. It reopens the finished
file as if it were a hostile reader and tries to get the sensitive strings back
out: through normal text extraction, through digits-only normalisation (which
defeats a value merely reformatted from ``123-45-6789`` to ``123456789``), and
through a raw sweep of every object and stream in the PDF, which catches text
that survived somewhere other than the page content - metadata, annotations,
form fields, an embedded file.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import pymupdf

from .patterns import Pattern
from .redactor import mask


def _digits_only(text: str) -> str:
    return re.sub(r"\D", "", text)


def _extracted_text(doc: pymupdf.Document) -> str:
    parts = []
    for index in range(doc.page_count):
        page = doc.load_page(index)
        for mode in ("text", "words"):
            try:
                if mode == "text":
                    parts.append(page.get_text("text"))
                else:
                    parts.append(" ".join(w[4] for w in page.get_text("words")))
            except Exception:
                continue
    return "\n".join(parts)


def _raw_blobs(doc: pymupdf.Document, limit: int = 20000) -> Tuple[List[bytes], bool]:
    """Every object definition and decompressed stream in the file.

    Glyphs in a content stream are font-encoded and often will not appear as
    readable ASCII, so a hit here is meaningful but a miss is not proof on its
    own. Its real value is catching plaintext that never went through a font:
    metadata, annotation contents, form field values, attachments.
    """
    blobs: List[bytes] = []
    truncated = False
    try:
        total = doc.xref_length()
    except Exception:
        return blobs, truncated
    length = min(total, limit)
    truncated = total > limit
    for xref in range(1, length):
        try:
            definition = doc.xref_object(xref, compressed=False)
            if definition:
                blobs.append(definition.encode("utf-8", "replace"))
        except Exception:
            pass
        try:
            if doc.xref_is_stream(xref):
                blobs.append(doc.xref_stream(xref))
        except Exception:
            pass
    return blobs, truncated


def _needles(value: str) -> List[bytes]:
    """Byte forms of a value worth searching for in raw objects."""
    forms = {value, value.strip()}
    digits = _digits_only(value)
    if len(digits) >= 6:
        forms.add(digits)
    needles: List[bytes] = []
    for form in forms:
        if len(form) < 4:
            continue
        needles.append(form.encode("utf-8", "replace"))
        # PDF text strings are frequently stored UTF-16BE.
        needles.append(form.encode("utf-16-be", "replace"))
    return needles



def residual_scan(doc: pymupdf.Document, patterns: Sequence[Pattern]) -> List[Dict]:
    """Re-run the patterns against the finished file.

    Checking only the values the redactor already found cannot catch the case
    that matters most: text in a place the redactor never looked. If it never
    saw an SSN in a comment, it has no value to check for, and a verifier
    driven by that list reports a clean pass over a live leak. Re-scanning the
    output from scratch - page text, annotations and form fields - is
    independent of what the first pass happened to notice.
    """
    hits: List[Dict] = []

    def _check(text: str, where: str) -> None:
        if not text or not text.strip():
            return
        for pattern in patterns:
            for match in pattern.regex.finditer(text):
                group = pattern.group
                if group and group > (match.re.groups or 0):
                    continue
                value = match.group(group) if group else match.group(0)
                if not value:
                    continue
                if pattern.validator is not None and not pattern.validator(value):
                    continue
                hits.append({"pattern": pattern.name, "value": mask(value), "where": where})

    for index in range(doc.page_count):
        page = doc.load_page(index)
        _check(page.get_text("text"), f"page {index + 1} text")

        try:
            for annot in page.annots():
                info = annot.info or {}
                for key in ("content", "title", "subject"):
                    _check(info.get(key) or "", f"page {index + 1} annotation /{key}")
        except Exception:
            pass

        try:
            for widget in page.widgets():
                value = widget.field_value
                if isinstance(value, str):
                    _check(value, f"page {index + 1} form field")
        except Exception:
            pass

    return hits


def verify_output(
    output: Path,
    values: Sequence[str],
    *,
    deep: bool = True,
    patterns: Optional[Sequence[Pattern]] = None,
) -> Dict:
    """Check that none of ``values`` can be recovered from ``output``.

    Returns a report dict with ``passed``, the list of any leaked values (masked)
    and which channel leaked them.
    """
    report: Dict = {
        "checked_values": len(set(values)),
        "deep_scan": deep,
        "leaks": [],
        "residual": [],
        "rescanned": patterns is not None,
        "truncated_scan": False,
        "metadata_clean": True,
        "passed": True,
        "error": None,
    }

    try:
        doc = pymupdf.open(output)
    except Exception as exc:
        report["passed"] = False
        report["error"] = f"cannot reopen output for verification: {exc}"
        return report

    try:
        text = _extracted_text(doc)
        text_digits = _digits_only(text)
        blobs, truncated = _raw_blobs(doc) if deep else ([], False)
        report["truncated_scan"] = truncated

        for value in sorted(set(values)):
            stripped = value.strip()
            if len(stripped) < 3:
                continue
            channels = []

            if stripped.lower() in text.lower():
                channels.append("text extraction")

            digits = _digits_only(stripped)
            if len(digits) >= 6 and digits in text_digits:
                channels.append("digits-only text")

            if blobs:
                needles = _needles(stripped)
                for blob in blobs:
                    if any(needle in blob for needle in needles):
                        channels.append("raw object/stream")
                        break

            if channels:
                report["leaks"].append(
                    {"value": mask(stripped), "channels": sorted(set(channels))}
                )

        if patterns:
            report["residual"] = residual_scan(doc, patterns)

        metadata = doc.metadata or {}
        leftover = {
            key: val
            for key, val in metadata.items()
            if val and key not in ("format", "encryption")
        }
        if leftover:
            report["metadata_clean"] = False
            report["metadata_remaining"] = sorted(leftover)
    finally:
        doc.close()

    report["passed"] = not report["leaks"] and not report["residual"]
    return report
