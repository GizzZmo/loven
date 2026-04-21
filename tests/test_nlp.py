"""Unit tests for loven.nlp."""

from __future__ import annotations

import pytest

from loven.nlp import SYNONYMS, expand_themes
from loven.themes import PEACE_THEMES


def test_synonyms_dict_has_all_base_themes():
    for theme in PEACE_THEMES:
        assert theme in SYNONYMS, f"Missing synonym entry for theme: {theme}"


def test_expand_themes_includes_base():
    result = expand_themes(["energi"])
    assert "energi" in result


def test_expand_themes_adds_synonyms():
    result = expand_themes(["energi"])
    assert "kraft" in result
    assert "strøm" in result


def test_expand_themes_no_duplicates():
    result = expand_themes(PEACE_THEMES)
    assert len(result) == len(set(result))


def test_expand_themes_custom_list():
    result = expand_themes(["vann"])
    assert "drikkevann" in result
    assert "vassdrag" in result


def test_expand_themes_exclude_base():
    result = expand_themes(["energi"], include_base=False)
    assert "energi" not in result
    assert "kraft" in result


def test_expand_themes_defaults_to_peace_themes():
    result_default = expand_themes()
    result_explicit = expand_themes(PEACE_THEMES)
    assert result_default == result_explicit


def test_expand_themes_unknown_keyword_returns_base():
    """An unknown keyword has no synonyms; it just returns itself."""
    result = expand_themes(["ukjentord"])
    assert "ukjentord" in result
    assert len(result) == 1


def test_expand_themes_spacy_raises_without_spacy(monkeypatch):
    """expand_themes_spacy should raise ImportError when spacy is absent."""
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "spacy":
            raise ImportError("No module named 'spacy'")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)

    from loven.nlp import expand_themes_spacy
    with pytest.raises(ImportError, match="spacy"):
        expand_themes_spacy(["energi"])
