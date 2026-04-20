"""Peace themes – Norwegian keywords used to filter Lovdata search results.

Each keyword represents a thematic area that underpins a harmonious, sustainable
society (clean energy, clean water, ethics, environment, etc.).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Core peace-theme keyword list (case-insensitive matching applied at runtime)
# ---------------------------------------------------------------------------

PEACE_THEMES: list[str] = [
    "energi",       # energy
    "vann",         # water
    "miljø",        # environment
    "etikk",        # ethics
    "selskap",      # company / corporation
    "oppløsning",   # dissolution
    "fred",         # peace
    "klima",        # climate
    "bolig",        # housing
    "arbeidsmiljø", # working environment
]


def matches_theme(title: str, themes: list[str] | None = None) -> bool:
    """Return True if *title* contains at least one peace-theme keyword.

    Parameters
    ----------
    title:
        The Norwegian title of a Lovdata document.
    themes:
        Optional custom keyword list.  Defaults to :data:`PEACE_THEMES`.
    """
    if themes is None:
        themes = PEACE_THEMES
    lower = title.lower()
    return any(theme in lower for theme in themes)


def count_themes(title: str, themes: list[str] | None = None) -> int:
    """Return how many distinct peace-theme keywords appear in *title*.

    A higher count means the document is more centrally relevant to the
    project's peace-and-sustainability mission.

    Parameters
    ----------
    title:
        The Norwegian title of a Lovdata document.
    themes:
        Optional custom keyword list.  Defaults to :data:`PEACE_THEMES`.
    """
    if themes is None:
        themes = PEACE_THEMES
    lower = title.lower()
    return sum(1 for theme in themes if theme in lower)
