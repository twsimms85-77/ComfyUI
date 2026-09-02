# pdf-redact

Offline, verifiable PDF redaction for documents containing sensitive data —
tax returns, W-2s, 1099s, bank statements, anything with an SSN on it.

Nothing leaves your machine. There is no server, no upload, no account.

## Why not just draw a black box

Because a black box is not redaction. Drawing a filled rectangle over an SSN
leaves the characters sitting in the PDF's content stream, where copy/paste,
`pdftotext`, or any PDF library will hand them straight back. It is the single
most common way redactions fail, and it fails silently — the document *looks*
correct.

This tool uses PyMuPDF's redaction annotations, which rewrite the content
stream and delete the glyphs, then saves to a new file with full garbage
collection (`garbage=4`) so that earlier incremental revisions of the file
cannot carry the original text along either.

Then it checks its own work. After writing each file it reopens the output as a
hostile reader and tries to get the values back out three ways:

1. normal text extraction,
2. digits-only comparison — so a value merely reformatted from `123-45-6789`
   to `123456789` is still caught,
3. a raw sweep of every object and stream in the file, which catches text that
   survived somewhere other than the page: metadata, annotations, form field
   values, an embedded attachment,
4. **a fresh pattern scan of the finished file** — page text, annotations and
   form fields — which is the only check that can catch a leak in a place the
   first pass never looked. Checking only the values already found cannot: if
   the redactor never saw an SSN in a comment, it has no value to look for, and
   reports a clean pass over a live leak.

If anything is still recoverable, the run **fails** with a non-zero exit code
and the report says which value leaked and through which channel.

## Install

```bash
pip install pymupdf

# Strongly recommended - lets scanned documents be redacted at all:
pip install ocrmypdf         # plus the tesseract binary, see requirements.txt
```

## Use

```bash
# Look before you leap: report what would be redacted, write nothing.
python -m pdf_redact 1040.pdf --dry-run

# Redact one file.
python -m pdf_redact 1040.pdf -o redacted/

# Batch a whole folder, recursively, preserving the directory structure.
python -m pdf_redact client_returns/ -o redacted/ --recursive

# Add the client's name and anything else literal.
python -m pdf_redact returns/ -o redacted/ --term "Jane Q. Client" --term "Acme LLC"

# Everything, including phone numbers, emails and dates.
python -m pdf_redact returns/ -o redacted/ --all-patterns
```

**Always `--dry-run` first on a new kind of document.** Read the report, confirm
it caught what you expected and did not catch what you need to keep, then run it
for real.

## What it looks for

| Pattern | On by default | Notes |
|---|---|---|
| `ssn` | yes | Dashed, spaced, dotted, or bare 9 digits. Separators must be **consistent** (both or neither), which is what keeps a hyphenated ZIP+4 out. Rejects area `000`/`666`/`9xx`, group `00`, serial `0000`, and repeated-digit placeholders. |
| `ssn_strict` | no | Same, but separators are required — never matches bare 9 digits. Use when false positives cost more than a miss. |
| `itin` | yes | `9xx-NN-NNNN` with `NN` in the IRS-assigned ranges. |
| `ein` | yes | `NN-NNNNNNN`. |
| `routing` | yes | 9 digits **validated against the ABA checksum**, so ordinary 9-digit numbers are not touched. |
| `creditcard` | yes | 13–19 digits **validated with Luhn**. |
| `account` | yes | A number following an `account` / `acct` / `policy` / `loan` / `member` label. Only the number is destroyed, the label stays. |
| `email` | no | `--all-patterns` or `--patterns ...,email` |
| `phone` | no | North American formats. |
| `dob` | no | Any `M/D/YYYY` date — matches far more than birthdates, so it is opt-in. |

`python -m pdf_redact --list-patterns` prints this at any time.

### The tradeoff, with real numbers

`ssn` and `itin` match **bare, unseparated 9-digit numbers**, because dependent
SSNs on real tax documents are frequently typed without dashes and missing one
is much worse than over-redacting.

Measured against 200,000 random 9-digit numbers, that costs:

| Rule | Fires on a random number of that length |
|---|---|
| `ssn` | 88.9% of 9-digit |
| `itin` | 4.4% of 9-digit |
| `routing` (ABA checksum) | 10.0% of 9-digit |
| `creditcard` (Luhn) | 9.9% of 16-digit |
| **any default rule, bare 9-digit** | **94.0%** |

So a genuinely bare, unlabelled 9-digit number on your document is very likely
to be redacted. Checksums help, but a checksum that passes 1 in 10 numbers is
not a filter you should lean on. What actually keeps false positives down is
formatting: a hyphenated ZIP+4, a phone number, an EIN and a dollar figure are
all excluded structurally, not by luck.

Two ways to manage it: run `--dry-run` first on any new document type, and use
`--patterns ssn_strict,...` if you would rather require separators and accept
the risk of missing an undashed dependent SSN.

## Scanned documents

A scanned PDF is a picture. It has no text layer, so pattern matching finds
nothing and would report a clean run over a page full of visible SSNs — the
worst possible outcome.

So the tool refuses to pretend. Pages with no text layer are detected up front;
if `ocrmypdf` is installed they are OCR'd first (`--skip-text`, leaving real
text pages untouched), and if it is not, the run **fails** with a warning naming
the pages that could not be scanned. Pass `--allow-image-pages` only when you
have looked at those pages yourself and know they are safe.

When redaction does run on a scanned page, the overlapping image pixels are
destroyed too, not just the OCR text layer.

## Comments and annotations

Comments, sticky notes, callouts and stamps store their text in the annotation
dictionary rather than the page content stream, so removing the page glyphs does
not touch them. A reviewer note reading "confirm client SSN 123-45-6789"
survives an otherwise perfect redaction — and because nothing on the *page*
matched, the run would report a clean pass over a live leak.

Annotation text (`/Contents`, `/T`, `/Subj`, and the `/RC` rich-text copy) is
therefore scanned as a first-class source of text, and matches are replaced with
`[REDACTED]`. Any annotation that cannot be rewritten safely is deleted rather
than left in place.

## Fillable forms

Form field values live in the AcroForm dictionary, not the page content stream,
so redacting the visible text does not touch them — a filled 1040 can still hand
over an SSN through its field value after the printed number is gone. Any field
whose value matches a pattern is cleared as well. Use `--keep-form-fields` to
disable this.

## Reports

Every run writes `redaction-report.txt` and `redaction-report.json` next to the
output, listing per file and per page what was redacted, any warnings, and the
verification result.

**Values in the report are masked** — all but the last two characters are
removed. A report listing full SSNs would just relocate the problem, and the
report is the artifact most likely to get emailed.

## Options

```
-o, --output DIR        output directory, or a .pdf path for a single file
-r, --recursive         recurse into directories
    --dry-run           report only, write nothing
    --patterns LIST     comma separated pattern names
    --all-patterns      enable every built-in pattern
    --list-patterns     print the pattern table and exit
    --term TEXT         literal phrase to redact (repeatable)
    --terms-file FILE   file of literal phrases, one per line
    --regex RE          custom regex to redact (repeatable)
    --ocr auto|never    OCR pages with no text layer (default: auto)
    --no-verify         skip output verification
    --fast-verify       verify by text extraction only, skip the raw sweep
    --allow-image-pages accept pages that could not be scanned
    --label TEXT        draw text inside each redaction box
    --keep-form-fields  do not clear matching form field values
    --report PATH       where to write the report
    --overwrite         overwrite existing output files
-q, --quiet             print only the summary
```

Exit codes: `0` clean, `1` an error or a failed verification, `2` bad usage.

## Tests

```bash
pip install pytest
python -m pytest pdf_redact/tests -c /dev/null
```

The suite includes `test_verifier_catches_a_fake_redaction`, which builds a PDF
"redacted" the wrong way — a black rectangle over live text — and asserts the
verifier reports it as a leak. A verifier that cannot fail is worthless, so that
case is tested as carefully as the ones that pass.

## Limits

- Encrypted PDFs are rejected; decrypt them first.
- Redaction is only as good as the patterns. Review the dry-run report; for
  anything unusual, add `--term` or `--regex`.
- Text rendered as vector line art rather than glyphs or images is not
  extractable and will not be found. This is rare, but it is why you should spot
  check the output rather than trusting a green run blindly.
