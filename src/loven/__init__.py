"""loven – WorldPeace-Lovdata-Kompendium.

A multi-paradigm Python toolkit for exploring Norwegian law (Lovdata)
with a focus on energy, water, environment, and ethics.

Public API
----------
>>> from loven import LovDataClient, AsyncLovDataClient, analyze_peace_laws, PEACE_THEMES
"""

from loven.analysis import analyze_peace_laws, batch_analyze
from loven.client import BASE_URL, AsyncLovDataClient, LovDataClient
from loven.themes import PEACE_THEMES, count_themes, matches_theme

__all__ = [
    "PEACE_THEMES",
    "count_themes",
    "matches_theme",
    "BASE_URL",
    "LovDataClient",
    "AsyncLovDataClient",
    "analyze_peace_laws",
    "batch_analyze",
]

__version__ = "0.1.0"
