"""Tests for the PDF redactor.

The central test is `test_verifier_catches_a_fake_redaction`: it builds a PDF
redacted the wrong way - a black rectangle drawn over live text - and asserts
that the verifier reports it as a leak. A verifier that cannot fail is worthless,
so that case matters as much as the ones that pass.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pdf_redact import patterns as patterns_mod
from pdf_redact.cli import main
from pdf_redact.redactor import find_matches, mask, redact_file
from pdf_redact.verify import verify_output

SSN = "123-45-6789"
EIN = "02-1234567"
ROUTING = "021000021"
CARD = "4111 1111 1111 1111"
NAME = "Jane Q. Client"

SAMPLE_LINES = [
    "FORM 1040 - U.S. Individual Income Tax Return",
    f"Name:        {NAME}",
    f"Your SSN:    {SSN}",
    f"Employer EIN: {EIN}",
    f"Routing number: {ROUTING}",
    f"Card on file: {CARD}",
    "Account No: 1234567890123",
    "Wages, line 1a: 145,900",
]


def build_pdf(path: Path, lines=SAMPLE_LINES, metadata=None) -> Path:
    doc = pymupdf.open()
    page = doc.new_page()
    y = 60
    for line in lines:
        page.insert_text((60, y), line, fontname="cour", fontsize=11)
        y += 18
    if metadata:
        doc.set_metadata(metadata)
    doc.save(str(path))
    doc.close()
    return path


def page_text(path: Path) -> str:
    doc = pymupdf.open(path)
    text = "\n".join(doc.load_page(i).get_text("text") for i in range(doc.page_count))
    doc.close()
    return text


# --------------------------------------------------------------------------
# Validators
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "value,expected",
    [
        ("4111 1111 1111 1111", True),   # Visa test number
        ("5500 0000 0000 0004", True),   # Mastercard test number
        ("4111 1111 1111 1112", False),  # check digit broken
        ("1234", False),                 # too short
    ],
)
def test_luhn(value, expected):
    assert patterns_mod.luhn_ok(value) is expected


@pytest.mark.parametrize(
    "value,expected",
    [("021000021", True), ("011401533", True), ("021000022", False), ("000000000", False)],
)
def test_aba(value, expected):
    assert patterns_mod.aba_ok(value) is expected


@pytest.mark.parametrize(
    "value,expected",
    [
        ("123-45-6789", True),
        ("001020003", True),
        ("666-45-6789", False),   # 666 area never issued
        ("900-45-6789", False),   # 9xx is ITIN space, not SSN
        ("123-00-6789", False),   # group 00 never issued
        ("123-45-0000", False),   # serial 0000 never issued
        ("111111111", False),     # placeholder, not a real number
    ],
)
def test_ssn_validator(value, expected):
    assert patterns_mod.ssn_ok(value) is expected


@pytest.mark.parametrize(
    "value,expected",
    [("912-70-1234", True), ("987-65-4321", True), ("912-69-1234", False), ("123-70-1234", False)],
)
def test_itin_validator(value, expected):
    assert patterns_mod.itin_ok(value) is expected


def test_mask_never_reveals_the_body_of_a_value():
    masked = mask(SSN)
    assert masked.endswith("89")
    assert "123" not in masked
    assert len(masked) == len(SSN)


# --------------------------------------------------------------------------
# Matching
# --------------------------------------------------------------------------


def test_finds_expected_patterns(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    doc = pymupdf.open(source)
    matches = find_matches(doc.load_page(0), patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS), 1)
    doc.close()
    found = {m.pattern for m in matches}
    assert {"ssn", "ein", "routing", "creditcard", "account"} <= found


def test_wages_figure_is_not_redacted(tmp_path):
    """Over-redaction destroys the return. Ordinary figures must survive."""
    source = build_pdf(tmp_path / "in.pdf")
    out = tmp_path / "out.pdf"
    redact_file(source, out, patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS))
    assert "145,900" in page_text(out)


def test_literal_term_does_not_match_across_a_line_break(tmp_path):
    """A term spanning lines must not produce one huge rectangle between them."""
    source = build_pdf(tmp_path / "in.pdf", lines=["Jane", "Client"])
    doc = pymupdf.open(source)
    matches = find_matches(doc.load_page(0), [patterns_mod.literal_pattern("Jane Client")], 1)
    doc.close()
    assert matches == []


# --------------------------------------------------------------------------
# End to end redaction
# --------------------------------------------------------------------------


def test_redaction_removes_text_not_just_covers_it(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    out = tmp_path / "out.pdf"
    patterns = patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS)
    patterns.append(patterns_mod.literal_pattern(NAME))

    result = redact_file(source, out, patterns)
    assert result.errors == []

    text = page_text(out)
    for secret in (SSN, EIN, ROUTING, NAME, "1234567890123"):
        assert secret not in text
    # And with every separator stripped, defeating a reformatted match.
    digits = re.sub(r"\D", "", text)
    for secret in (SSN, EIN, ROUTING, CARD):
        assert re.sub(r"\D", "", secret) not in digits


def test_raw_bytes_do_not_contain_the_secrets(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    out = tmp_path / "out.pdf"
    redact_file(source, out, patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS))
    raw = out.read_bytes()
    assert SSN.encode() not in raw
    assert ROUTING.encode() not in raw


def test_metadata_is_scrubbed(tmp_path):
    source = build_pdf(
        tmp_path / "in.pdf",
        metadata={"title": f"1040 {NAME} {SSN}", "author": NAME, "subject": SSN},
    )
    out = tmp_path / "out.pdf"
    redact_file(source, out, patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS))
    doc = pymupdf.open(out)
    metadata = doc.metadata or {}
    doc.close()
    assert not metadata.get("title")
    assert not metadata.get("author")
    assert not metadata.get("subject")


def test_dry_run_writes_nothing(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    out = tmp_path / "out.pdf"
    result = redact_file(
        source, out, patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS), dry_run=True
    )
    assert result.matches
    assert not out.exists()


# --------------------------------------------------------------------------
# Verification
# --------------------------------------------------------------------------


def test_verification_passes_on_a_real_redaction(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    out = tmp_path / "out.pdf"
    result = redact_file(source, out, patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS))
    report = verify_output(out, [m.text for m in result.matches])
    assert report["passed"], report["leaks"]


def test_verifier_catches_a_fake_redaction(tmp_path):
    """A black box over live text must be reported as a leak, not a pass.

    This is the failure mode the whole tool exists to prevent, so the verifier
    is required to detect it.
    """
    source = build_pdf(tmp_path / "in.pdf")
    fake = tmp_path / "fake.pdf"

    doc = pymupdf.open(source)
    page = doc.load_page(0)
    for rect in page.search_for(SSN):
        # Draw over it, but leave the characters in the content stream.
        page.draw_rect(rect, color=(0, 0, 0), fill=(0, 0, 0))
    doc.save(str(fake))
    doc.close()

    report = verify_output(fake, [SSN])
    assert not report["passed"]
    assert report["leaks"][0]["value"] == mask(SSN)


def test_verifier_reports_leftover_metadata(tmp_path):
    source = build_pdf(tmp_path / "in.pdf", metadata={"author": NAME})
    report = verify_output(source, [])
    assert report["metadata_clean"] is False


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def test_cli_batches_a_directory(tmp_path):
    indir = tmp_path / "in"
    indir.mkdir()
    build_pdf(indir / "a.pdf")
    build_pdf(indir / "b.pdf")
    outdir = tmp_path / "out"

    code = main([str(indir), "-o", str(outdir), "-q"])
    assert code == 0
    assert (outdir / "a.pdf").exists() and (outdir / "b.pdf").exists()
    assert (outdir / "redaction-report.txt").exists()
    assert (outdir / "redaction-report.json").exists()
    assert SSN not in page_text(outdir / "a.pdf")


def test_cli_report_does_not_contain_the_raw_secret(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    outdir = tmp_path / "out"
    main([str(source), "-o", str(outdir), "-q"])
    report = (outdir / "redaction-report.txt").read_text()
    assert SSN not in report
    assert ROUTING not in report
    assert "ssn" in report


def test_cli_refuses_to_overwrite_the_input(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    assert main([str(source), "-o", str(source), "-q"]) == 2


def test_cli_will_not_clobber_existing_output_without_flag(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    outdir = tmp_path / "out"
    assert main([str(source), "-o", str(outdir), "-q"]) == 0
    assert main([str(source), "-o", str(outdir), "-q"]) == 1
    assert main([str(source), "-o", str(outdir), "-q", "--overwrite"]) == 0


def test_cli_fails_when_a_page_has_no_text_layer(tmp_path, monkeypatch):
    """A scanned page silently matching nothing is the trap; it must be loud."""
    monkeypatch.setattr("pdf_redact.redactor.ocr_available", lambda: False)
    doc = pymupdf.open()
    doc.new_page()  # entirely blank: no text layer at all
    scan = tmp_path / "scan.pdf"
    doc.save(str(scan))
    doc.close()

    outdir = tmp_path / "out"
    assert main([str(scan), "-o", str(outdir), "-q"]) == 1
    assert main([str(scan), "-o", str(outdir), "-q", "--overwrite", "--allow-image-pages"]) == 0


def test_cli_list_patterns():
    assert main(["--list-patterns"]) == 0


def test_cli_rejects_unknown_pattern(tmp_path):
    source = build_pdf(tmp_path / "in.pdf")
    assert main([str(source), "-o", str(tmp_path / "out"), "--patterns", "nope"]) == 2


def test_overlapping_patterns_do_not_suppress_each_other(tmp_path):
    """A partially overlapping match must still be redacted.

    A user-supplied regex that extends past a built-in match shares some
    characters with it. Suppressing it as a duplicate would leave the
    non-overlapping remainder of the value on the page.
    """
    source = build_pdf(tmp_path / "in.pdf", lines=[f"Employer EIN: {EIN} on file"])
    doc = pymupdf.open(source)
    selected = patterns_mod.resolve(["ein"])
    selected.append(patterns_mod.custom_pattern(r"EIN: [0-9-]+ on file"))
    matches = find_matches(doc.load_page(0), selected, 1)
    doc.close()
    assert {m.pattern for m in matches} == {"ein", "regex"}


def test_identical_matches_are_not_double_counted(tmp_path):
    """Two patterns matching the exact same span collapse into one entry."""
    source = build_pdf(tmp_path / "in.pdf", lines=[f"Your SSN: {SSN}"])
    doc = pymupdf.open(source)
    selected = patterns_mod.resolve(["ssn"])
    selected.append(patterns_mod.custom_pattern(re.escape(SSN)))
    matches = find_matches(doc.load_page(0), selected, 1)
    doc.close()
    assert len(matches) == 1


# --------------------------------------------------------------------------
# Text outside the page content stream
# --------------------------------------------------------------------------


def _pdf_with_comment(path: Path, comment: str) -> Path:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((60, 80), "Nothing sensitive on the page", fontname="cour", fontsize=11)
    annot = page.add_text_annot((300, 80), comment)
    annot.update()
    doc.save(str(path))
    doc.close()
    return path


def test_ssn_in_a_comment_is_found_and_removed(tmp_path):
    """A reviewer note is text too, and it is not in the content stream.

    Before this was handled the tool reported "0 redactions, 1 clean" while the
    SSN sat in plaintext in the output - a real leak behind an all-clear.
    """
    source = _pdf_with_comment(tmp_path / "in.pdf", f"Confirm client SSN {SSN}")
    out = tmp_path / "out.pdf"
    result = redact_file(source, out, patterns_mod.resolve(["ssn"]))

    assert any("annotation" in m.pattern for m in result.matches)
    assert SSN.encode() not in out.read_bytes()

    doc = pymupdf.open(out)
    contents = [(a.info or {}).get("content", "") for a in doc.load_page(0).annots()]
    doc.close()
    assert not any(SSN in c for c in contents)


def test_residual_scan_catches_a_leak_the_redactor_never_found(tmp_path):
    """Verification must not depend on what the first pass happened to notice.

    Given an empty list of known values, the rescan still has to fail this file.
    """
    source = _pdf_with_comment(tmp_path / "in.pdf", f"SSN {SSN}")
    report = verify_output(source, [], patterns=patterns_mod.resolve(["ssn"]))
    assert not report["passed"]
    assert report["residual"][0]["where"].endswith("annotation /content")


def test_form_field_value_is_caught_by_the_residual_scan(tmp_path):
    doc = pymupdf.open()
    page = doc.new_page()
    widget = pymupdf.Widget()
    widget.field_name = "ssn"
    widget.field_type = pymupdf.PDF_WIDGET_TYPE_TEXT
    widget.rect = pymupdf.Rect(60, 60, 260, 80)
    widget.field_value = SSN
    page.add_widget(widget)
    source = tmp_path / "form.pdf"
    doc.save(str(source))
    doc.close()

    report = verify_output(source, [], patterns=patterns_mod.resolve(["ssn"]))
    assert not report["passed"]


# --------------------------------------------------------------------------
# Separator consistency / ZIP+4
# --------------------------------------------------------------------------


def test_zip_plus_four_is_not_mistaken_for_an_ssn(tmp_path):
    """Every tax document carries an address; destroying the ZIP is a real bug.

    "03301-1234" parses as 033 + "" + 01 + "-" + 1234 under a rule that lets
    the two separators differ, which is why they must match.
    """
    source = build_pdf(tmp_path / "in.pdf", lines=["Concord, NH 03301-1234", f"SSN {SSN}"])
    out = tmp_path / "out.pdf"
    redact_file(source, out, patterns_mod.resolve(patterns_mod.DEFAULT_PATTERNS))
    text = page_text(out)
    assert "03301-1234" in text
    assert SSN not in text


@pytest.mark.parametrize(
    "value", ["123-45-6789", "234 56 7890", "345.67.8901", "456789012", "001020003"]
)
def test_every_real_ssn_format_still_matches(value):
    match = patterns_mod.REGISTRY["ssn"].regex.search(value)
    assert match and patterns_mod.ssn_ok(match.group(0))


@pytest.mark.parametrize("value", ["03301-1234", "90210-4567", "12345-6789"])
def test_mixed_separator_shapes_are_rejected(value):
    match = patterns_mod.REGISTRY["ssn"].regex.search(value)
    assert not (match and patterns_mod.ssn_ok(match.group(0)))


def test_ssn_strict_refuses_bare_nine_digits():
    strict = patterns_mod.REGISTRY["ssn_strict"].regex
    assert strict.search("123-45-6789")
    assert not strict.search("456789012")
