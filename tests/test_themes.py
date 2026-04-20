"""Unit tests for loven.themes."""

from loven.themes import PEACE_THEMES, count_themes, matches_theme


def test_peace_themes_is_list_of_strings():
    assert isinstance(PEACE_THEMES, list)
    assert all(isinstance(t, str) for t in PEACE_THEMES)


def test_matches_theme_positive():
    assert matches_theme("Lov om vannressurser (vannressursloven)")
    assert matches_theme("Lov om energiproduksjon")
    assert matches_theme("Lov om miljøvern")
    assert matches_theme("Lov om klimamål")


def test_matches_theme_negative():
    assert not matches_theme("Lov om pass og reisedokumenter")
    assert not matches_theme("Vegtrafikkloven")


def test_matches_theme_case_insensitive():
    assert matches_theme("Lov om ENERGI og kraftnett")
    assert matches_theme("MILJØVERN og natur")


def test_matches_theme_custom_themes():
    custom = ["helse", "skatt"]
    assert matches_theme("Lov om helsepersonell", custom)
    assert not matches_theme("Lov om energi", custom)


def test_count_themes_zero():
    assert count_themes("Vegtrafikkloven") == 0


def test_count_themes_one():
    assert count_themes("Lov om energiproduksjon") == 1


def test_count_themes_multiple():
    # Contains both "energi" and "miljø"
    title = "Lov om energilov og miljøvern"
    assert count_themes(title) == 2


def test_count_themes_custom():
    custom = ["a", "b", "c"]
    assert count_themes("a b c", custom) == 3
    assert count_themes("a x y", custom) == 1
