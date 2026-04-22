"""Unit tests for the loven CLI (src/loven/cli.py)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import responses as resp_lib

from loven.cli import _build_parser, _parse_themes, cmd_export, cmd_search, cmd_themes_list, main

BASE = "https://api.lovdata.no"
SAMPLE = json.loads(
    (Path(__file__).parent.parent / "sample_data" / "mock_lovdata_response.json")
    .read_text(encoding="utf-8")
)


# ---------------------------------------------------------------------------
# _parse_themes
# ---------------------------------------------------------------------------

def test_parse_themes_none():
    assert _parse_themes(None) is None


def test_parse_themes_single():
    assert _parse_themes("energi") == ["energi"]


def test_parse_themes_multiple():
    assert _parse_themes("energi,vann,miljø") == ["energi", "vann", "miljø"]


def test_parse_themes_strips_whitespace():
    assert _parse_themes(" energi , vann ") == ["energi", "vann"]


def test_parse_themes_ignores_empty_segments():
    assert _parse_themes("energi,,vann") == ["energi", "vann"]


# ---------------------------------------------------------------------------
# _build_parser
# ---------------------------------------------------------------------------

def test_parser_search_defaults():
    parser = _build_parser()
    args = parser.parse_args(["search", "energi"])
    assert args.command == "search"
    assert args.query == "energi"
    assert args.limit == 20
    assert args.themes is None
    assert args.base_url is None


def test_parser_search_options():
    parser = _build_parser()
    args = parser.parse_args(
        ["search", "energi", "--limit", "5", "--themes", "energi,vann", "--base-url", "http://mock"]
    )
    assert args.limit == 5
    assert args.themes == "energi,vann"
    assert args.base_url == "http://mock"


def test_parser_export_defaults():
    parser = _build_parser()
    args = parser.parse_args(["export", "energi", "--output", "out.csv"])
    assert args.command == "export"
    assert args.query == "energi"
    assert args.output == "out.csv"
    assert args.limit == 20


def test_parser_export_missing_output_raises():
    parser = _build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["export", "energi"])


def test_parser_themes_list():
    parser = _build_parser()
    args = parser.parse_args(["themes", "list"])
    assert args.command == "themes"
    assert args.themes_command == "list"


def test_parser_no_command_raises():
    parser = _build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


# ---------------------------------------------------------------------------
# cmd_search
# ---------------------------------------------------------------------------

@resp_lib.activate
def test_cmd_search_prints_results(capsys):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    parser = _build_parser()
    args = parser.parse_args(["search", "energi"])
    cmd_search(args)
    captured = capsys.readouterr()
    assert "tittel" in captured.out
    assert "url" in captured.out
    assert "tema_treff" in captured.out


@resp_lib.activate
def test_cmd_search_no_results_message(capsys):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json={"hits": []}, status=200)
    parser = _build_parser()
    args = parser.parse_args(["search", "xyz_no_match_xyz"])
    cmd_search(args)
    captured = capsys.readouterr()
    assert "No peace-relevant results found." in captured.out


@resp_lib.activate
def test_cmd_search_custom_themes(capsys):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    parser = _build_parser()
    args = parser.parse_args(["search", "energi", "--themes", "energi"])
    cmd_search(args)
    captured = capsys.readouterr()
    assert captured.out.strip()
    assert "No peace-relevant results found." not in captured.out


@resp_lib.activate
def test_cmd_search_custom_base_url():
    resp_lib.add(resp_lib.GET, "http://mock/sok", json=SAMPLE, status=200)
    parser = _build_parser()
    args = parser.parse_args(["search", "energi", "--base-url", "http://mock"])
    cmd_search(args)
    assert len(resp_lib.calls) == 1
    assert resp_lib.calls[0].request.url.startswith("http://mock/sok")


# ---------------------------------------------------------------------------
# cmd_export
# ---------------------------------------------------------------------------

@resp_lib.activate
def test_cmd_export_csv(tmp_path, capsys):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    out = tmp_path / "results.csv"
    parser = _build_parser()
    args = parser.parse_args(["export", "energi", "--output", str(out)])
    cmd_export(args)
    assert out.exists()
    captured = capsys.readouterr()
    assert "Saved" in captured.out
    assert str(out) in captured.out


@resp_lib.activate
def test_cmd_export_xlsx(tmp_path, capsys):
    pytest.importorskip("openpyxl")
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    out = tmp_path / "results.xlsx"
    parser = _build_parser()
    args = parser.parse_args(["export", "energi", "--output", str(out)])
    cmd_export(args)
    assert out.exists()
    captured = capsys.readouterr()
    assert "Saved" in captured.out


@resp_lib.activate
def test_cmd_export_empty_result(tmp_path, capsys):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json={"hits": []}, status=200)
    out = tmp_path / "empty.csv"
    parser = _build_parser()
    args = parser.parse_args(["export", "xyz", "--output", str(out)])
    cmd_export(args)
    assert out.exists()
    captured = capsys.readouterr()
    assert "Saved 0 rows" in captured.out


# ---------------------------------------------------------------------------
# cmd_themes_list
# ---------------------------------------------------------------------------

def test_cmd_themes_list_output(capsys):
    cmd_themes_list()
    captured = capsys.readouterr()
    assert "Norwegian" in captured.out
    assert "English" in captured.out
    assert "energi" in captured.out
    assert "vann" in captured.out
    assert "miljø" in captured.out


def test_cmd_themes_list_contains_all_themes(capsys):
    from loven import PEACE_THEMES
    cmd_themes_list()
    captured = capsys.readouterr()
    for theme in PEACE_THEMES:
        assert theme in captured.out


# ---------------------------------------------------------------------------
# main() integration
# ---------------------------------------------------------------------------

@resp_lib.activate
def test_main_search(capsys):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    main(["search", "energi"])


@resp_lib.activate
def test_main_export(tmp_path):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    out = str(tmp_path / "out.csv")
    main(["export", "energi", "--output", out])
    assert Path(out).exists()


def test_main_themes_list(capsys):
    main(["themes", "list"])
    captured = capsys.readouterr()
    assert "energi" in captured.out


def test_main_no_args_exits():
    with pytest.raises(SystemExit):
        main([])
