"""Unit tests for analysis helpers."""

from __future__ import annotations

import json
from pathlib import Path

import responses as resp_lib

from loven import LovDataClient, analyze_peace_laws, batch_analyze

BASE = "https://api.lovdata.no"
SAMPLE = json.loads(
    (Path(__file__).parent.parent / "sample_data" / "mock_lovdata_response.json")
    .read_text(encoding="utf-8")
)


@resp_lib.activate
def test_analyze_peace_laws_returns_dataframe():
    import pandas as pd
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    client = LovDataClient()
    df = analyze_peace_laws(client, "energi")
    assert isinstance(df, pd.DataFrame)


@resp_lib.activate
def test_analyze_peace_laws_no_results():
    import pandas as pd
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json={"hits": []}, status=200)
    client = LovDataClient()
    df = analyze_peace_laws(client, "xyz")
    assert isinstance(df, pd.DataFrame)
    assert df.empty


@resp_lib.activate
def test_analyze_peace_laws_columns():
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    client = LovDataClient()
    df = analyze_peace_laws(client, "energi")
    for col in ("tittel", "url", "relevans_for_fred", "tema_treff"):
        assert col in df.columns


@resp_lib.activate
def test_batch_analyze_multiple_queries():
    import pandas as pd
    # Return same mock data for each query
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json=SAMPLE, status=200)
    client = LovDataClient()
    df = batch_analyze(client, ["energi", "vann"])
    assert isinstance(df, pd.DataFrame)
    assert "_query" in df.columns
    assert set(df["_query"].unique()) == {"energi", "vann"}


@resp_lib.activate
def test_batch_analyze_all_empty():
    import pandas as pd
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json={"hits": []}, status=200)
    resp_lib.add(resp_lib.GET, f"{BASE}/sok", json={"hits": []}, status=200)
    client = LovDataClient()
    df = batch_analyze(client, ["xyz1", "xyz2"])
    assert isinstance(df, pd.DataFrame)
    assert df.empty
