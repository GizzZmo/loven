"""Norwegian NLP helpers – keyword synonym expansion.

Expands the base peace-theme keyword list with Norwegian synonyms and
related terms.  Two backends are supported:

1. **Built-in synonym map** (no extra dependencies) – a hand-curated
   dictionary of Norwegian synonym clusters for each peace theme.
2. **spaCy Norwegian model** (optional) – uses the ``nb_core_news_sm``
   model for lemma-based matching when ``spacy`` is installed.

Install the NLP extras with::

    pip install "loven[nlp]"
    python -m spacy download nb_core_news_sm

Functions
---------
expand_themes
    Return an expanded keyword list using the built-in synonym map.
expand_themes_spacy
    Return an expanded list using a spaCy pipeline (if available).

Constants
---------
SYNONYMS
    Built-in Norwegian synonym map (theme → list of synonyms).

Usage
-----
>>> from loven.nlp import expand_themes
>>> themes = expand_themes(["energi", "vann"])
>>> "kraft" in themes
True
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Built-in synonym map – hand-curated Norwegian clusters
# ---------------------------------------------------------------------------

SYNONYMS: dict[str, list[str]] = {
    "energi": [
        "kraft",
        "strøm",
        "elektrisitet",
        "vindkraft",
        "solenergi",
        "vannkraft",
        "fornybar",
        "energiforsyning",
    ],
    "vann": [
        "vannforsyning",
        "vassdrag",
        "elv",
        "innsjø",
        "grunnvann",
        "drikkevann",
        "avløp",
        "kloakk",
    ],
    "miljø": [
        "natur",
        "naturvern",
        "forurensning",
        "utslipp",
        "biologisk mangfold",
        "økologi",
        "bærekraft",
    ],
    "etikk": [
        "moral",
        "integritet",
        "rettferdighet",
        "transparens",
        "åpenhet",
        "varsling",
    ],
    "selskap": [
        "aksjeselskap",
        "foretak",
        "virksomhet",
        "organisasjon",
        "stiftelse",
        "samvirke",
    ],
    "oppløsning": [
        "avvikling",
        "likvidasjon",
        "konkurs",
        "fusjon",
        "fisjon",
    ],
    "fred": [
        "konfliktløsning",
        "forsoning",
        "diplomati",
        "samarbeid",
        "bærekraft",
        "rettigheter",
    ],
    "klima": [
        "klimaendring",
        "klimamål",
        "utslippskutt",
        "karbon",
        "co2",
        "drivhuseffekt",
        "klimatilpasning",
    ],
    "bolig": [
        "husleie",
        "leilighet",
        "leietaker",
        "utleier",
        "borettslag",
        "sameie",
        "eiendom",
    ],
    "arbeidsmiljø": [
        "arbeidstid",
        "stillingsvern",
        "helse og sikkerhet",
        "yrkesskade",
        "permittering",
        "fagforeningsrettigheter",
    ],
}


def expand_themes(
    themes: list[str] | None = None,
    *,
    include_base: bool = True,
) -> list[str]:
    """Expand peace-theme keywords using the built-in synonym map.

    Parameters
    ----------
    themes:
        Base keyword list.  Defaults to :data:`~loven.themes.PEACE_THEMES`.
    include_base:
        If ``True`` (default), base keywords are included in the result.

    Returns
    -------
    list[str]
        Deduplicated list of original keywords plus their synonyms.

    Examples
    --------
    >>> from loven.nlp import expand_themes
    >>> "kraft" in expand_themes(["energi"])
    True
    """
    from loven.themes import PEACE_THEMES

    base = themes if themes is not None else PEACE_THEMES
    expanded: list[str] = list(base) if include_base else []

    for kw in base:
        for synonym in SYNONYMS.get(kw, []):
            if synonym not in expanded:
                expanded.append(synonym)

    logger.info(
        "expand_themes: %d base keywords → %d expanded keywords.",
        len(base),
        len(expanded),
    )
    return expanded


def expand_themes_spacy(
    themes: list[str] | None = None,
    *,
    model: str = "nb_core_news_sm",
    include_base: bool = True,
) -> list[str]:
    """Expand peace-theme keywords using a spaCy Norwegian model.

    Lemmatises each keyword and includes the lemma form alongside
    the built-in synonym expansion.

    Parameters
    ----------
    themes:
        Base keyword list.  Defaults to :data:`~loven.themes.PEACE_THEMES`.
    model:
        spaCy model name to load (must support Norwegian).
    include_base:
        If ``True`` (default), base keywords are included in the result.

    Returns
    -------
    list[str]
        Deduplicated list of original keywords, their spaCy lemmas, and
        built-in synonyms.

    Raises
    ------
    ImportError
        If ``spacy`` is not installed.
    OSError
        If the requested spaCy model is not downloaded.

    Examples
    --------
    >>> from loven.nlp import expand_themes_spacy
    >>> themes = expand_themes_spacy(["energi"])  # doctest: +SKIP
    """
    try:
        import spacy
    except ImportError as exc:
        raise ImportError(
            "spacy is required for expand_themes_spacy. "
            "Install it with:  pip install 'loven[nlp]'"
        ) from exc

    nlp = spacy.load(model)

    base_expanded = expand_themes(themes, include_base=include_base)
    spacy_extra: list[str] = []

    from loven.themes import PEACE_THEMES

    base = themes if themes is not None else PEACE_THEMES
    for kw in base:
        doc = nlp(kw)
        for token in doc:
            lemma = token.lemma_.lower()
            if lemma not in base_expanded and lemma not in spacy_extra:
                spacy_extra.append(lemma)

    result = base_expanded + spacy_extra
    logger.info(
        "expand_themes_spacy: %d base keywords → %d expanded keywords.",
        len(base),
        len(result),
    )
    return result
