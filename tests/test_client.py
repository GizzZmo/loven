"""Unit tests for LovDataClient."""

from __future__ import annotations

import json

import pytest
import responses as resp_lib

from loven import LovDataClient

BASE = "https://api.lovdata.no"


@pytest.fixture
def sample_data(tmp_path):
    from pathlib import Path
    return json.loads(
        (Path(__file__).parent.parent / "sample_data" / "mock_lovdata_response.json")
        .read_text(encoding="utf-8")
    )


# ---------------------------------------------------------------------------
# search()
# ---------------------------------------------------------------------------

@resp_lib.activate
def test_search_returns_hits(sample_data):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=sample_data, status=200)
    client = LovDataClient()
    result = client.search("energi")
    assert "hits" in result
    assert len(result["hits"]) > 0


@resp_lib.activate
def test_search_error_returns_error_key():
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", status=503)
    client = LovDataClient()
    result = client.search("anything")
    assert "error" in result


@resp_lib.activate
def test_search_passes_limit_param(sample_data):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=sample_data, status=200)
    client = LovDataClient()
    client.search("energi", limit=5)
    request = resp_lib.calls[0].request
    assert "limit=5" in request.url


@resp_lib.activate
def test_search_passes_optional_params(sample_data):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=sample_data, status=200)
    client = LovDataClient()
    client.search("energi", doc_type="lov", department="OED")
    request = resp_lib.calls[0].request
    assert "type=lov" in request.url
    assert "departement=OED" in request.url


# ---------------------------------------------------------------------------
# filter_peace_laws()
# ---------------------------------------------------------------------------

@resp_lib.activate
def test_filter_peace_laws_returns_subset(sample_data):
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=sample_data, status=200)
    client = LovDataClient()
    result = client.search("energi")
    filtered = client.filter_peace_laws(result)
    # All filtered hits must match at least one theme
    from loven.themes import matches_theme
    for hit in filtered:
        assert matches_theme(str(hit.get("tittel", "")))


@resp_lib.activate
def test_filter_peace_laws_empty_on_no_hits():
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json={"hits": []}, status=200)
    client = LovDataClient()
    result = client.search("xyz")
    assert client.filter_peace_laws(result) == []


def test_filter_peace_laws_handles_missing_hits_key():
    client = LovDataClient()
    assert client.filter_peace_laws({"error": "some error"}) == []


# ---------------------------------------------------------------------------
# to_dataframe()
# ---------------------------------------------------------------------------

def test_to_dataframe_columns(sample_data):
    client = LovDataClient()
    hits = sample_data["hits"]
    df = client.to_dataframe(hits)
    for col in ("tittel", "url", "relevans_for_fred", "tema_treff"):
        assert col in df.columns


def test_to_dataframe_sorted_by_tema_treff(sample_data):
    client = LovDataClient()
    df = client.to_dataframe(sample_data["hits"])
    scores = df["tema_treff"].tolist()
    assert scores == sorted(scores, reverse=True)


def test_to_dataframe_empty_input():
    import pandas as pd
    client = LovDataClient()
    df = client.to_dataframe([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty


# ---------------------------------------------------------------------------
# Custom base_url
# ---------------------------------------------------------------------------

def test_custom_base_url():
    client = LovDataClient(base_url="http://localhost:9999")
    assert client.base_url == "http://localhost:9999"
