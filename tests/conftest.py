"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

SAMPLE_DATA_PATH = Path(__file__).parent.parent / "sample_data" / "mock_lovdata_response.json"


@pytest.fixture
def mock_response() -> dict:
    """Load the local mock Lovdata response JSON."""
    return json.loads(SAMPLE_DATA_PATH.read_text(encoding="utf-8"))


@pytest.fixture
def client(mock_response):
    """Return a LovDataClient whose HTTP session is patched to return mock data."""
    import responses as resp_lib

    from loven import LovDataClient

    with resp_lib.RequestsMock() as rsps:
        rsps.add(
            method=resp_lib.GET,
            url="https://api.lovdata.no/sok",
            json=mock_response,
            status=200,
        )
        yield LovDataClient()
