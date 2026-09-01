"""True PDF redaction: locate sensitive text, delete the glyphs, scrub the file.

The important word is *delete*. A black rectangle drawn over a text run leaves
the characters in the content stream, where copy/paste and any text extractor
will find them. Everything here goes through PyMuPDF's redaction annotations,
which rewrite the content stream and drop the glyphs, and the result is always
written to a fresh file with full garbage collection so that prior incremental
revisions cannot carry the original text along.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import pymupdf

from .patterns import Pattern

# Older/newer PyMuPDF builds have moved these constants around; resolve defensively.
_REDACT_TEXT_REMOVE = getattr(pymupdf, "PDF_REDACT_TEXT_REMOVE", 0)
_REDACT_IMAGE_PIXELS = getattr(pymupdf, "PDF_REDACT_IMAGE_PIXELS", 2)
_REDACT_LINE_ART_NONE = getattr(pymupdf, "PDF_REDACT_LINE_ART_NONE", 0)

# A page with fewer extractable characters than this is treated as an image
# scan: pattern matching would silently find nothing on it.
IMAGE_PAGE_TEXT_THRESHOLD = 12


def mask(value: str) -> str:
    """Render a matched value safe to print in a report.

    The report is itself a document about sensitive data; writing full SSNs into
    it would just relocate the problem. Keep the last two characters for
    traceability and destroy the rest.
    """
    stripped = value.strip()
    if len(stripped) <= 2:
        return "*" * len(stripped)
    keep = stripped[-2:]
    return "*" * (len(stripped) - 2) + keep


@dataclass
class Match:
    """One located occurrence of sensitive text on one page."""

    page: int
    pattern: str
    text: str
    rects: List[pymupdf.Rect] = field(default_factory=list)

    @property
    def masked(self) -> str:
        return mask(self.text)


@dataclass
class FileResult:
    """Everything that happened to a single input file."""

    source: Path
    output: Optional[Path] = None
    matches: List[Match] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    image_pages: List[int] = field(default_factory=list)
    ocr_applied: bool = False
    form_fields_cleared: int = 0
    page_count: int = 0
    verification: Optional[dict] = None

    @property
    def ok(self) -> bool:
        if self.errors:
            return False
        if self.verification is not None and not self.verification.get("passed", False):
            return False
        return True

    def counts_by_pattern(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for match in self.matches:
            counts[match.pattern] = counts.get(match.pattern, 0) + 1
        return counts


def _page_charmap(page: pymupdf.Page) -> Tuple[str, List[Optional[pymupdf.Rect]]]:
    """Flatten a page into a string plus a per-character bounding box.

    Working at character level (rather than PyMuPDF's word or span level) is what
    lets a regex match land on an exact pixel region even when the sensitive
    value is split across spans by a font or colour change mid-number, which is
    common in generated tax forms. A newline is inserted between text lines so
    that no single-line pattern can match across a line break and produce a
    redaction box spanning half the page.
    """
    chars: List[str] = []
    boxes: List[Optional[pymupdf.Rect]] = []
    raw = page.get_text("rawdict")
    for block in raw.get("blocks", []):
        if block.get("type") != 0:  # 0 == text; skip image blocks
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                for char in span.get("chars", []):
                    chars.append(char["c"])
                    boxes.append(pymupdf.Rect(char["bbox"]))
            chars.append("\n")
            boxes.append(None)
    return "".join(chars), boxes


def _rects_for_span(
    boxes: Sequence[Optional[pymupdf.Rect]], start: int, end: int
) -> List[pymupdf.Rect]:
    """Union the character boxes in [start, end) into one rect per text run.

    Consecutive characters that share a vertical band belong to the same visual
    run and collapse into a single rectangle; anything else starts a new one, so
    a match that somehow wraps still produces tight boxes instead of one giant
    rectangle covering the space between them.
    """
    runs: List[pymupdf.Rect] = []
    current: Optional[pymupdf.Rect] = None
    for box in boxes[start:end]:
        if box is None or box.is_empty:
            continue
        if current is None:
            current = pymupdf.Rect(box)
            continue
        mid = (box.y0 + box.y1) / 2
        same_line = current.y0 - 1 <= mid <= current.y1 + 1
        if same_line:
            current |= box
        else:
            runs.append(current)
            current = pymupdf.Rect(box)
    if current is not None:
        runs.append(current)
    # Grow each box a hair so antialiased glyph edges are covered too.
    return [rect + (-0.6, -0.6, 0.6, 0.6) for rect in runs]


def find_matches(page: pymupdf.Page, patterns: Sequence[Pattern], page_number: int) -> List[Match]:
    """Run every pattern over one page and return located, validated matches."""
    text, boxes = _page_charmap(page)
    if not text.strip():
        return []

    found: List[Match] = []
    claimed: List[Tuple[int, int]] = []

    for pattern in patterns:
        for m in pattern.regex.finditer(text):
            group = pattern.group
            if group and group > (m.re.groups or 0):
                continue
            start, end = m.span(group)
            if start < 0 or start == end:
                continue
            value = m.group(group)
            if pattern.validator is not None and not pattern.validator(value):
                continue
            # Collapse a span already fully covered by an earlier pattern so the
            # report does not double-count the same digits. Containment, not
            # mere overlap, is the test on purpose: a partially overlapping
            # match still has uncovered characters, and skipping it would leave
            # part of a sensitive value on the page.
            if any(c_start <= start and end <= c_end for c_start, c_end in claimed):
                continue
            rects = _rects_for_span(boxes, start, end)
            if not rects:
                continue
            claimed.append((start, end))
            found.append(Match(page=page_number, pattern=pattern.name, text=value, rects=rects))
    return found


def _clear_form_fields(page: pymupdf.Page, patterns: Sequence[Pattern]) -> int:
    """Blank fillable-form values that look sensitive.

    Form field values live in the AcroForm dictionary, not the page content
    stream, so redacting the visible text does not touch them. A filled 1040
    can therefore still hand over an SSN through its field value after the
    rendered number is gone.
    """
    cleared = 0
    try:
        widgets = list(page.widgets())
    except Exception:
        return 0
    for widget in widgets:
        value = widget.field_value
        if not isinstance(value, str) or not value.strip():
            continue
        for pattern in patterns:
            for m in pattern.regex.finditer(value):
                candidate = m.group(pattern.group) if pattern.group else m.group(0)
                if not candidate:
                    continue
                if pattern.validator is not None and not pattern.validator(candidate):
                    continue
                try:
                    widget.field_value = ""
                    widget.update()
                    cleared += 1
                except Exception:
                    pass
                break
            else:
                continue
            break
    return cleared


def _scrub_document(doc: pymupdf.Document) -> None:
    """Strip metadata, XMP, embedded files and attachments from the document."""
    try:
        doc.set_metadata({})
    except Exception:
        pass
    try:
        doc.del_xml_metadata()
    except Exception:
        pass
    try:
        for name in list(doc.embfile_names()):
            doc.embfile_del(name)
    except Exception:
        pass


def ocr_available() -> bool:
    return shutil.which("ocrmypdf") is not None


def _image_pages(doc: pymupdf.Document) -> List[int]:
    """Page numbers (1-based) that carry no meaningful text layer."""
    pages = []
    for index in range(doc.page_count):
        page = doc.load_page(index)
        if len(page.get_text("text").strip()) < IMAGE_PAGE_TEXT_THRESHOLD:
            pages.append(index + 1)
    return pages


def run_ocr(source: Path, workdir: Path, timeout: int = 900) -> Tuple[Optional[Path], Optional[str]]:
    """OCR the pages that lack a text layer, returning the new file or an error."""
    if not ocr_available():
        return None, "ocrmypdf is not installed"
    target = workdir / f"ocr-{source.name}"
    command = [
        "ocrmypdf",
        "--skip-text",       # leave pages that already have real text alone
        "--optimize", "0",   # never re-encode; keep the redaction surface simple
        "--quiet",
        str(source),
        str(target),
    ]
    try:
        proc = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, f"ocrmypdf timed out after {timeout}s"
    except Exception as exc:  # pragma: no cover - environment dependent
        return None, f"ocrmypdf failed to start: {exc}"
    if proc.returncode != 0 or not target.exists():
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        return None, f"ocrmypdf exited {proc.returncode}: {detail[-1] if detail else 'no output'}"
    return target, None


def redact_file(
    source: Path,
    output: Optional[Path],
    patterns: Sequence[Pattern],
    *,
    dry_run: bool = False,
    ocr: str = "auto",
    fill: Tuple[float, float, float] = (0, 0, 0),
    label: Optional[str] = None,
    scrub_form_fields: bool = True,
) -> FileResult:
    """Redact one PDF. With ``dry_run`` the file is only inspected, never written."""
    result = FileResult(source=source, output=None if dry_run else output)

    with tempfile.TemporaryDirectory(prefix="pdfredact-") as tmp:
        workdir = Path(tmp)
        working_source = source

        try:
            doc = pymupdf.open(source)
        except Exception as exc:
            result.errors.append(f"cannot open PDF: {exc}")
            return result

        if doc.needs_pass:
            result.errors.append("PDF is password protected; decrypt it before redacting")
            doc.close()
            return result

        blank = _image_pages(doc)
        doc.close()

        if blank and ocr != "never":
            ocred, error = run_ocr(source, workdir)
            if ocred is not None:
                working_source = ocred
                result.ocr_applied = True
            else:
                result.warnings.append(f"OCR skipped ({error})")

        try:
            doc = pymupdf.open(working_source)
        except Exception as exc:
            result.errors.append(f"cannot open PDF after OCR: {exc}")
            return result

        result.page_count = doc.page_count
        result.image_pages = _image_pages(doc)
        if result.image_pages:
            result.warnings.append(
                "no text layer on page(s) "
                + ", ".join(str(p) for p in result.image_pages)
                + " - nothing could be scanned there"
            )

        for index in range(doc.page_count):
            page = doc.load_page(index)
            matches = find_matches(page, patterns, index + 1)
            result.matches.extend(matches)

            if scrub_form_fields:
                result.form_fields_cleared += _clear_form_fields(page, patterns)

            if dry_run or not matches:
                continue

            for match in matches:
                for rect in match.rects:
                    page.add_redact_annot(rect, text=label, fill=fill)
            try:
                page.apply_redactions(
                    images=_REDACT_IMAGE_PIXELS,
                    graphics=_REDACT_LINE_ART_NONE,
                    text=_REDACT_TEXT_REMOVE,
                )
            except TypeError:
                # Very old PyMuPDF: only the images keyword exists.
                page.apply_redactions(images=_REDACT_IMAGE_PIXELS)

        if dry_run:
            doc.close()
            return result

        _scrub_document(doc)

        try:
            output.parent.mkdir(parents=True, exist_ok=True)
            # garbage=4 is what actually drops the now-unreferenced original
            # objects, including any earlier incremental revisions of the file.
            doc.save(
                str(output),
                garbage=4,
                deflate=True,
                clean=True,
                incremental=False,
            )
        except Exception as exc:
            result.errors.append(f"cannot write output: {exc}")
            doc.close()
            return result
        doc.close()

    return result
