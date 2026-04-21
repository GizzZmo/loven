"""loven – WorldPeace-Lovdata-Kompendium.

A multi-paradigm Python toolkit for exploring Norwegian law (Lovdata)
with a focus on energy, water, environment, and ethics.

Public API
----------
>>> from loven import LovDataClient, AsyncLovDataClient, analyze_peace_laws, PEACE_THEMES
>>> from loven.cache import DiskCache
>>> from loven.export import export
>>> from loven.nlp import expand_themes
"""

from loven.analysis import analyze_peace_laws, batch_analyze
from loven.cache import DiskCache
from loven.client import BASE_URL, AsyncLovDataClient, LovDataClient
from loven.export import export, to_csv, to_excel, to_markdown
from loven.nlp import SYNONYMS, expand_themes
from loven.themes import PEACE_THEMES, count_themes, matches_theme

__all__ = [
    # themes
    "PEACE_THEMES",
    "count_themes",
    "matches_theme",
    # client
    "BASE_URL",
    "LovDataClient",
    "AsyncLovDataClient",
    # analysis
    "analyze_peace_laws",
    "batch_analyze",
    # cache
    "DiskCache",
    # export
    "export",
    "to_csv",
    "to_excel",
    "to_markdown",
    # nlp
    "SYNONYMS",
    "expand_themes",
]

__version__ = "1.0.0"
