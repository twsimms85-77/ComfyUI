"""Pattern definitions for sensitive data commonly found in tax and financial PDFs.

Each pattern knows how to find candidate strings and, where a cheap structural
check exists (Luhn for card numbers, the ABA checksum for routing numbers), how
to reject false positives before anything is destroyed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass(frozen=True)
class Pattern:
    """A named rule for locating sensitive text.

    ``group`` selects which regex group is actually redacted, so a rule can match
    a label plus its value ("Account No: 12345678") while destroying only the
    value. ``validator`` gets the final matched text and may veto the match.
    """

    name: str
    regex: re.Pattern
    description: str
    group: int = 0
    validator: Optional[Callable[[str], bool]] = None
    default_on: bool = True


def _digits(text: str) -> str:
    return re.sub(r"\D", "", text)


def luhn_ok(text: str) -> bool:
    """Standard Luhn check digit, used by every major card network."""
    digits = [int(c) for c in _digits(text)]
    if not 13 <= len(digits) <= 19:
        return False
    checksum = 0
    for index, digit in enumerate(reversed(digits)):
        if index % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def aba_ok(text: str) -> bool:
    """ABA routing transit number checksum (weights 3-7-1, repeated)."""
    digits = [int(c) for c in _digits(text)]
    if len(digits) != 9:
        return False
    weights = (3, 7, 1, 3, 7, 1, 3, 7, 1)
    total = sum(d * w for d, w in zip(digits, weights))
    return total % 10 == 0 and any(digits)


def ssn_ok(text: str) -> bool:
    """Reject SSN-shaped strings the SSA never issues."""
    digits = _digits(text)
    if len(digits) != 9:
        return False
    area, group, serial = digits[:3], digits[3:5], digits[5:]
    if area in ("000", "666") or area.startswith("9"):
        return False
    if group == "00" or serial == "0000":
        return False
    # A run of one repeated digit is placeholder text, not a real number.
    if len(set(digits)) == 1:
        return False
    return True


def itin_ok(text: str) -> bool:
    """ITINs are 9xx-NN-NNNN where NN falls in the IRS-assigned ranges."""
    digits = _digits(text)
    if len(digits) != 9 or not digits.startswith("9"):
        return False
    group = int(digits[3:5])
    valid = (50 <= group <= 65) or (70 <= group <= 88) or (90 <= group <= 92) or (94 <= group <= 99)
    return valid and digits[5:] != "0000"


# A separator run that stays on one line: hyphen variants, spaces, dots.
_SEP = r"[-‐-―− .\t]?"

_ALL: List[Pattern] = [
    Pattern(
        name="ssn",
        regex=re.compile(rf"(?<![\d-])\d{{3}}{_SEP}\d{{2}}{_SEP}\d{{4}}(?![\d-])"),
        description="Social Security number (dashed, spaced, or bare 9 digits)",
        validator=ssn_ok,
    ),
    Pattern(
        name="itin",
        regex=re.compile(rf"(?<![\d-])9\d{{2}}{_SEP}\d{{2}}{_SEP}\d{{4}}(?![\d-])"),
        description="Individual Taxpayer Identification Number",
        validator=itin_ok,
    ),
    Pattern(
        name="ein",
        regex=re.compile(r"(?<![\d-])\d{2}[-‐-―− ]\d{7}(?![\d-])"),
        description="Employer Identification Number (NN-NNNNNNN)",
    ),
    Pattern(
        name="routing",
        regex=re.compile(r"(?<![\d-])\d{9}(?![\d-])"),
        description="Bank routing / ABA number (checksum verified)",
        validator=aba_ok,
    ),
    Pattern(
        name="creditcard",
        regex=re.compile(r"(?<![\d-])(?:\d[ -]?){12,18}\d(?![\d-])"),
        description="Payment card number (Luhn verified)",
        validator=luhn_ok,
    ),
    Pattern(
        name="account",
        regex=re.compile(
            r"(?:account|acct|a/c|policy|member|loan|routing|aba)"
            r"[ \t]*(?:number|no|nbr|#)?[ \t]*[:#.]?[ \t]*"
            r"([0-9][0-9‐-―− -]{4,24}[0-9])",
            re.IGNORECASE,
        ),
        description="Number following an account/policy/loan label",
        group=1,
    ),
    Pattern(
        name="email",
        regex=re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]{2,}\b"),
        description="Email address",
        default_on=False,
    ),
    Pattern(
        name="phone",
        regex=re.compile(
            r"(?<![\d-])(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}(?![\d-])"
        ),
        description="North American phone number",
        default_on=False,
    ),
    Pattern(
        name="dob",
        regex=re.compile(
            r"(?<![\d/])(?:0?[1-9]|1[0-2])[/‐-―-](?:0?[1-9]|[12]\d|3[01])"
            r"[/‐-―-](?:19|20)\d{2}(?![\d/])"
        ),
        description="Date of birth / any M/D/YYYY date",
        default_on=False,
    ),
]

REGISTRY: Dict[str, Pattern] = {p.name: p for p in _ALL}
DEFAULT_PATTERNS: List[str] = [p.name for p in _ALL if p.default_on]
ALL_PATTERNS: List[str] = [p.name for p in _ALL]


def resolve(names: List[str]) -> List[Pattern]:
    """Map pattern names to Pattern objects, raising on anything unknown."""
    unknown = [n for n in names if n not in REGISTRY]
    if unknown:
        raise KeyError(
            f"unknown pattern(s): {', '.join(sorted(unknown))}. "
            f"Available: {', '.join(ALL_PATTERNS)}"
        )
    return [REGISTRY[n] for n in names]


def literal_pattern(term: str, name: str = "term") -> Pattern:
    """Build a case-insensitive pattern for a literal phrase.

    Internal whitespace is allowed to stretch, but only horizontally: matches
    must not run across a line break, or the redaction box would swallow
    everything in between.
    """
    tokens = [re.escape(tok) for tok in term.split()]
    body = r"[ \t]+".join(tokens)
    return Pattern(
        name=name,
        regex=re.compile(body, re.IGNORECASE),
        description=f"literal term {term!r}",
    )


def custom_pattern(expression: str, name: str = "regex") -> Pattern:
    return Pattern(
        name=name,
        regex=re.compile(expression, re.IGNORECASE),
        description=f"custom regex {expression!r}",
    )
