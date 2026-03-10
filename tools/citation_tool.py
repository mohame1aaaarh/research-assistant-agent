# tools/citation_tool.py
from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Optional

from agno.tools import tool


# ─────────────────────────────────────────────
#  Enums & Constants
# ─────────────────────────────────────────────

class SourceType(str, Enum):
    WEBSITE    = "website"
    JOURNAL    = "journal"
    BOOK       = "book"
    CONFERENCE = "conference"
    REPORT     = "report"


CURRENT_YEAR = datetime.now().year
VALID_YEAR_RE = re.compile(r"^\d{4}$")


# ─────────────────────────────────────────────
#  Internal Helpers  (not exposed to the agent)
# ─────────────────────────────────────────────

def _validate_year(year: str) -> str:
    """Return the year if valid, else 'n.d.'"""
    if not year or year.strip().lower() in ("n.d.", "nd", "unknown", ""):
        return "n.d."
    year = year.strip()
    if VALID_YEAR_RE.match(year):
        y = int(year)
        if 1000 <= y <= CURRENT_YEAR + 1:
            return year
    return "n.d."


def _normalize_authors(authors: str) -> str:
    """
    Normalize author string to APA format.
    Accepts  'John Smith'  →  'Smith, J.'
    Accepts  'Smith, J.'  →  'Smith, J.'   (already correct, kept as-is)
    Multiple authors separated by ';' or '&' or 'and'.
    """
    if not authors or authors.strip().lower() in ("unknown", "unknown author", ""):
        return "Unknown Author"

    # Split multiple authors
    raw_authors = re.split(r"\s*(?:;|&|and)\s*", authors, flags=re.IGNORECASE)
    normalized: list[str] = []

    for author in raw_authors:
        author = author.strip()
        if not author:
            continue

        # Already in "LastName, F." format
        if re.match(r"^[A-Za-z\-']+,\s+[A-Z]\.", author):
            normalized.append(author)
            continue

        # "FirstName LastName" → "LastName, F."
        parts = author.split()
        if len(parts) >= 2:
            last   = parts[-1]
            initials = ". ".join(p[0].upper() for p in parts[:-1]) + "."
            normalized.append(f"{last}, {initials}")
        else:
            normalized.append(author)  # single-word name, keep as-is

    if not normalized:
        return "Unknown Author"

    # APA multi-author: A, B, & C
    if len(normalized) == 1:
        return normalized[0]
    if len(normalized) == 2:
        return f"{normalized[0]}, & {normalized[1]}"
    return ", ".join(normalized[:-1]) + f", & {normalized[-1]}"


def _clean_url(url: str) -> str:
    """Return the URL/DOI cleaned and prefixed if needed."""
    url = url.strip()
    if url.startswith("10."):          # raw DOI
        return f"https://doi.org/{url}"
    return url


# ─────────────────────────────────────────────
#  Agent Tools
# ─────────────────────────────────────────────

@tool
def generate_apa_citation(
    title: str,
    year: str,
    url: str,
    authors: str = "Unknown Author",
    source_type: str = "website",
    journal_name: Optional[str] = None,
    volume: Optional[str] = None,
    issue: Optional[str] = None,
    pages: Optional[str] = None,
    publisher: Optional[str] = None,
    access_date: Optional[str] = None,
) -> str:
    """
    Generate a properly formatted APA 7th-edition citation.
    Always call this tool even when some fields are missing — use the provided defaults.

    Args:
        title:        Title of the source (required).
        year:         Publication year e.g. '2024'. Use 'n.d.' if unknown.
        url:          Full URL or DOI (e.g. '10.1000/xyz123').
        authors:      Author(s). Accepts 'John Smith', 'Smith, J.', or multiple
                      authors separated by ';' or '&'. Default: 'Unknown Author'.
        source_type:  One of 'website' | 'journal' | 'book' | 'conference' | 'report'.
                      Default: 'website'.
        journal_name: Journal name (for source_type='journal').
        volume:       Volume number (journals/books).
        issue:        Issue number (journals).
        pages:        Page range e.g. '123-145' (journals/books).
        publisher:    Publisher name (books/reports).
        access_date:  Date you retrieved the page e.g. 'March 10, 2025' (websites).
    
    Returns:
        A formatted APA 7th-edition citation string.
    """
    # ── Sanitize inputs ──────────────────────
    clean_title   = title.strip() if title else "Untitled"
    clean_year    = _validate_year(year)
    clean_authors = _normalize_authors(authors)
    clean_url     = _clean_url(url) if url else ""

    try:
        stype = SourceType(source_type.strip().lower())
    except ValueError:
        stype = SourceType.WEBSITE

    # ── Build citation by type ────────────────
    if stype == SourceType.JOURNAL:
        citation = f"{clean_authors} ({clean_year}). {clean_title}."
        if journal_name:
            citation += f" *{journal_name.strip()}*"
            if volume:
                citation += f", *{volume}*"
                if issue:
                    citation += f"({issue})"
            if pages:
                citation += f", {pages}"
            citation += "."
        if clean_url:
            citation += f" {clean_url}"

    elif stype == SourceType.BOOK:
        citation = f"{clean_authors} ({clean_year}). *{clean_title}*."
        if publisher:
            citation += f" {publisher.strip()}."
        if clean_url:
            citation += f" {clean_url}"

    elif stype == SourceType.CONFERENCE:
        citation = f"{clean_authors} ({clean_year}). {clean_title}."
        if journal_name:   # reused as conference name
            citation += f" In *{journal_name.strip()}*"
            if pages:
                citation += f" (pp. {pages})"
            citation += "."
        if publisher:
            citation += f" {publisher.strip()}."
        if clean_url:
            citation += f" {clean_url}"

    elif stype == SourceType.REPORT:
        citation = f"{clean_authors} ({clean_year}). *{clean_title}*."
        if publisher:
            citation += f" {publisher.strip()}."
        if clean_url:
            citation += f" {clean_url}"

    else:  # WEBSITE (default)
        retrieval = f"Retrieved {access_date} from {clean_url}" if access_date else f"Retrieved from {clean_url}"
        citation  = f"{clean_authors} ({clean_year}). {clean_title}. {retrieval}"

    return citation.strip()


@tool
def generate_multiple_citations(sources: list[dict]) -> list[str]:
    """
    Generate APA citations for a list of sources in one call.
    Prefer this over calling generate_apa_citation multiple times.

    Args:
        sources: List of dicts. Each dict can have the same keys as
                 generate_apa_citation: title, year, url, authors,
                 source_type, journal_name, volume, issue, pages,
                 publisher, access_date.

    Returns:
        A list of formatted APA citation strings, one per source.
    """
    results: list[str] = []
    for src in sources:
        citation = generate_apa_citation(
            title       = src.get("title", "Untitled"),
            year        = src.get("year", "n.d."),
            url         = src.get("url", ""),
            authors     = src.get("authors", "Unknown Author"),
            source_type = src.get("source_type", "website"),
            journal_name= src.get("journal_name"),
            volume      = src.get("volume"),
            issue       = src.get("issue"),
            pages       = src.get("pages"),
            publisher   = src.get("publisher"),
            access_date = src.get("access_date"),
        )
        results.append(citation)
    return results


# ─────────────────────────────────────────────
#  Post-processing Helper  (human-side, not an agent tool)
# ─────────────────────────────────────────────

def add_sources_section(
    response_text: str,
    citations: list[str],
    *,
    sort_alphabetically: bool = True,
    heading: str = "🔗 Sources",
) -> str:
    """
    Append a formatted sources / references section to the agent's response.

    Args:
        response_text:       The main response body.
        citations:           List of APA citation strings.
        sort_alphabetically: Sort citations A→Z (default True, matches APA).
        heading:             Section heading text.

    Returns:
        response_text with the sources block appended.
    """
    if not citations:
        return response_text + f"\n\n{heading}:\n- No direct sources available."

    cleaned = [c.strip() for c in citations if c and c.strip()]

    if sort_alphabetically:
        cleaned.sort(key=lambda c: c.lower())

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for c in cleaned:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    items = "\n".join(f"- {c}" for c in unique)
    return f"{response_text}\n\n{heading}:\n{items}"