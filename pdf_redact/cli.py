"""Command line interface for the batch PDF redactor."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Sequence

from . import patterns as patterns_mod
from .redactor import FileResult, ocr_available, redact_file
from .verify import verify_output

EXIT_OK = 0
EXIT_PROBLEM = 1
EXIT_USAGE = 2


def _collect_inputs(paths: Sequence[str], recursive: bool) -> List[Path]:
    found: List[Path] = []
    for raw in paths:
        path = Path(raw).expanduser()
        if path.is_dir():
            globber = path.rglob if recursive else path.glob
            found.extend(sorted(p for p in globber("*.pdf") if p.is_file()))
            found.extend(sorted(p for p in globber("*.PDF") if p.is_file()))
        elif path.is_file():
            found.append(path)
        else:
            raise FileNotFoundError(f"no such file or directory: {path}")
    # De-duplicate while preserving order.
    seen = set()
    unique = []
    for path in found:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def _output_path(source: Path, root: Optional[Path], outdir: Path) -> Path:
    if root is not None:
        try:
            relative = source.resolve().relative_to(root.resolve())
            return outdir / relative
        except ValueError:
            pass
    return outdir / source.name


def _build_patterns(args: argparse.Namespace) -> List[patterns_mod.Pattern]:
    names = patterns_mod.ALL_PATTERNS if args.all_patterns else args.patterns
    selected = list(patterns_mod.resolve(names))

    for index, term in enumerate(args.term or []):
        selected.append(patterns_mod.literal_pattern(term, name=f"term:{term}"))

    if args.terms_file:
        for line in Path(args.terms_file).read_text(encoding="utf-8").splitlines():
            term = line.strip()
            if term and not term.startswith("#"):
                selected.append(patterns_mod.literal_pattern(term, name=f"term:{term}"))

    for expression in args.regex or []:
        selected.append(patterns_mod.custom_pattern(expression, name=f"regex:{expression}"))

    return selected


def _render_report(results: List[FileResult], args: argparse.Namespace) -> str:
    lines: List[str] = []
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines.append("PDF REDACTION REPORT")
    lines.append(f"Generated: {stamp}")
    lines.append(f"Mode:      {'DRY RUN (nothing written)' if args.dry_run else 'redact'}")
    lines.append("")
    lines.append("Values below are masked. All but the last two characters are removed so")
    lines.append("this report does not itself become a disclosure.")
    lines.append("")

    total_matches = 0
    for result in results:
        lines.append("=" * 78)
        lines.append(f"SOURCE: {result.source}")
        if result.output:
            lines.append(f"OUTPUT: {result.output}")
        lines.append(f"PAGES:  {result.page_count}")
        if result.ocr_applied:
            lines.append("OCR:    applied to pages with no text layer")

        counts = result.counts_by_pattern()
        total_matches += len(result.matches)
        if counts:
            lines.append("")
            lines.append("REDACTED:")
            for name in sorted(counts):
                lines.append(f"  {name:<28} {counts[name]:>4}")
        else:
            lines.append("")
            lines.append("REDACTED: nothing matched")

        if result.form_fields_cleared:
            lines.append(f"  {'form field values cleared':<28} {result.form_fields_cleared:>4}")

        if result.matches:
            lines.append("")
            lines.append("DETAIL (page / pattern / masked value):")
            for match in result.matches:
                lines.append(f"  p{match.page:<4} {match.pattern:<24} {match.masked}")

        for warning in result.warnings:
            lines.append(f"  WARNING: {warning}")
        for error in result.errors:
            lines.append(f"  ERROR:   {error}")

        if result.verification is not None:
            verification = result.verification
            lines.append("")
            if verification.get("error"):
                lines.append(f"VERIFY: ERROR - {verification['error']}")
            elif verification["passed"]:
                lines.append(
                    f"VERIFY: PASS - {verification['checked_values']} value(s) confirmed "
                    "unrecoverable from the output"
                )
            else:
                lines.append("VERIFY: FAIL - values still recoverable from the output:")
                for leak in verification["leaks"]:
                    lines.append(f"  {leak['value']}  via {', '.join(leak['channels'])}")
            if not verification.get("metadata_clean", True):
                lines.append(
                    "  NOTE: metadata still present: "
                    + ", ".join(verification.get("metadata_remaining", []))
                )
        lines.append("")

    lines.append("=" * 78)
    ok = sum(1 for r in results if r.ok)
    lines.append(f"SUMMARY: {len(results)} file(s), {total_matches} redaction(s), {ok} clean, "
                 f"{len(results) - ok} with problems")
    return "\n".join(lines) + "\n"


def _json_report(results: List[FileResult], args: argparse.Namespace) -> dict:
    return {
        "generated": datetime.now(timezone.utc).isoformat(),
        "dry_run": args.dry_run,
        "files": [
            {
                "source": str(r.source),
                "output": str(r.output) if r.output else None,
                "pages": r.page_count,
                "ocr_applied": r.ocr_applied,
                "image_pages": r.image_pages,
                "form_fields_cleared": r.form_fields_cleared,
                "counts": r.counts_by_pattern(),
                "matches": [
                    {"page": m.page, "pattern": m.pattern, "masked": m.masked}
                    for m in r.matches
                ],
                "warnings": r.warnings,
                "errors": r.errors,
                "verification": r.verification,
                "ok": r.ok,
            }
            for r in results
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-redact",
        description=(
            "Permanently redact sensitive data from PDFs, entirely offline. "
            "Text is deleted from the content stream, not covered with a box."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  pdf-redact returns/ -o redacted/ --recursive\n"
            "  pdf-redact 1040.pdf -o out/ --term 'Jane Q. Client' --dry-run\n"
            "  pdf-redact statements/ -o out/ --patterns ssn,ein,account --all-patterns\n"
        ),
    )
    parser.add_argument("inputs", nargs="*", help="PDF files and/or directories")
    parser.add_argument("-o", "--output", help="output directory (or .pdf path for a single file)")
    parser.add_argument(
        "--patterns",
        type=lambda s: [p.strip() for p in s.split(",") if p.strip()],
        default=patterns_mod.DEFAULT_PATTERNS,
        help="comma separated pattern names (default: %(default)s)",
    )
    parser.add_argument("--all-patterns", action="store_true", help="enable every built-in pattern")
    parser.add_argument("--list-patterns", action="store_true", help="show patterns and exit")
    parser.add_argument("--term", action="append", help="literal phrase to redact (repeatable)")
    parser.add_argument("--terms-file", help="file of literal phrases, one per line")
    parser.add_argument("--regex", action="append", help="custom regex to redact (repeatable)")
    parser.add_argument("-r", "--recursive", action="store_true", help="recurse into directories")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would be redacted without writing any file",
    )
    parser.add_argument(
        "--ocr",
        choices=("auto", "never"),
        default="auto",
        help="OCR pages with no text layer before scanning (default: auto)",
    )
    parser.add_argument("--no-verify", action="store_true", help="skip output verification")
    parser.add_argument(
        "--fast-verify",
        action="store_true",
        help="verify via text extraction only, skipping the raw object sweep",
    )
    parser.add_argument(
        "--allow-image-pages",
        action="store_true",
        help="do not fail when a page has no text layer and could not be scanned",
    )
    parser.add_argument("--label", help="text to draw inside each redaction box")
    parser.add_argument(
        "--keep-form-fields",
        action="store_true",
        help="do not clear fillable form field values that match a pattern",
    )
    parser.add_argument("--report", help="path for the text report (default: <output>/redaction-report.txt)")
    parser.add_argument("--overwrite", action="store_true", help="overwrite existing output files")
    parser.add_argument("-q", "--quiet", action="store_true", help="only print the summary")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_patterns:
        print(f"{'NAME':<14} {'DEFAULT':<9} DESCRIPTION")
        for name in patterns_mod.ALL_PATTERNS:
            pattern = patterns_mod.REGISTRY[name]
            print(f"{name:<14} {'on' if pattern.default_on else 'off':<9} {pattern.description}")
        return EXIT_OK

    if not args.inputs:
        parser.error("no input files given")
    if not args.output and not args.dry_run:
        parser.error("--output is required unless --dry-run is used")

    try:
        selected = _build_patterns(args)
    except (KeyError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    if not selected:
        print("error: no patterns or terms selected; nothing to redact", file=sys.stderr)
        return EXIT_USAGE

    try:
        sources = _collect_inputs(args.inputs, args.recursive)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_USAGE

    if not sources:
        print("error: no PDF files found in the given inputs", file=sys.stderr)
        return EXIT_USAGE

    root = None
    if len(args.inputs) == 1 and Path(args.inputs[0]).expanduser().is_dir():
        root = Path(args.inputs[0]).expanduser()

    outdir: Optional[Path] = None
    single_output: Optional[Path] = None
    if args.output:
        out = Path(args.output).expanduser()
        if out.suffix.lower() == ".pdf":
            if len(sources) != 1:
                print(
                    "error: --output names a single .pdf but multiple inputs were given",
                    file=sys.stderr,
                )
                return EXIT_USAGE
            single_output = out
            outdir = out.parent
        else:
            outdir = out

    if not args.dry_run and args.ocr == "auto" and not ocr_available():
        if not args.quiet:
            print(
                "note: ocrmypdf not found - scanned pages cannot be scanned for patterns.\n"
                "      install it with: pip install ocrmypdf  (plus the tesseract binary)",
                file=sys.stderr,
            )

    results: List[FileResult] = []
    for source in sources:
        output = None
        if not args.dry_run:
            output = single_output or _output_path(source, root, outdir)
            if output.resolve() == source.resolve():
                print(f"error: refusing to overwrite input in place: {source}", file=sys.stderr)
                return EXIT_USAGE
            if output.exists() and not args.overwrite:
                result = FileResult(source=source, output=output)
                result.errors.append("output already exists (use --overwrite)")
                results.append(result)
                continue

        if not args.quiet:
            print(f"redacting {source} ...", flush=True)

        result = redact_file(
            source,
            output,
            selected,
            dry_run=args.dry_run,
            ocr=args.ocr,
            label=args.label,
            scrub_form_fields=not args.keep_form_fields,
        )

        if not args.dry_run and not args.no_verify and result.output and result.output.exists():
            result.verification = verify_output(
                result.output,
                [m.text for m in result.matches],
                deep=not args.fast_verify,
            )

        results.append(result)

    text_report = _render_report(results, args)

    report_path: Optional[Path] = None
    if args.report:
        report_path = Path(args.report).expanduser()
    elif outdir is not None:
        report_path = outdir / "redaction-report.txt"

    if report_path is not None:
        try:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(text_report, encoding="utf-8")
            report_path.with_suffix(".json").write_text(
                json.dumps(_json_report(results, args), indent=2), encoding="utf-8"
            )
        except OSError as exc:
            print(f"warning: could not write report: {exc}", file=sys.stderr)
            report_path = None

    print(text_report)
    if report_path is not None:
        print(f"Report written to {report_path} and {report_path.with_suffix('.json')}")

    problems = [r for r in results if not r.ok]
    unscannable = [
        r for r in results if r.image_pages and not args.allow_image_pages
    ]

    if unscannable:
        print(
            "\nFAILED: some pages had no text layer, so they were never scanned.\n"
            "        Install ocrmypdf, or pass --allow-image-pages to accept this.",
            file=sys.stderr,
        )
    if problems:
        print(
            f"\nFAILED: {len(problems)} file(s) had errors or failed verification.",
            file=sys.stderr,
        )

    return EXIT_PROBLEM if (problems or unscannable) else EXIT_OK
