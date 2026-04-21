"""Unit tests for loven.export."""

from __future__ import annotations

import pandas as pd
import pytest

from loven.export import export, to_csv, to_excel, to_markdown


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "tittel": ["Energiloven", "Vannressursloven", "Miljøvernloven"],
            "url": [
                "https://lovdata.no/1",
                "https://lovdata.no/2",
                "https://lovdata.no/3",
            ],
            "dato": ["1990-06-29", "2000-11-24", "2009-06-19"],
            "dokumenttype": ["lov", "lov", "lov"],
            "tema_treff": [2, 1, 1],
        }
    )


# ---------------------------------------------------------------------------
# to_csv
# ---------------------------------------------------------------------------

def test_to_csv_creates_file(tmp_path, sample_df):
    path = tmp_path / "results.csv"
    result = to_csv(sample_df, path)
    assert result.exists()
    loaded = pd.read_csv(result)
    assert len(loaded) == 3


def test_to_csv_columns(tmp_path, sample_df):
    path = tmp_path / "results.csv"
    to_csv(sample_df, path)
    loaded = pd.read_csv(path)
    assert "tittel" in loaded.columns
    assert "tema_treff" in loaded.columns


# ---------------------------------------------------------------------------
# to_excel
# ---------------------------------------------------------------------------

def test_to_excel_creates_file(tmp_path, sample_df):
    path = tmp_path / "results.xlsx"
    result = to_excel(sample_df, path)
    assert result.exists()
    loaded = pd.read_excel(result)
    assert len(loaded) == 3


# ---------------------------------------------------------------------------
# to_markdown
# ---------------------------------------------------------------------------

def test_to_markdown_creates_file(tmp_path, sample_df):
    path = tmp_path / "results.md"
    result = to_markdown(sample_df, path)
    assert result.exists()


def test_to_markdown_content(tmp_path, sample_df):
    path = tmp_path / "results.md"
    to_markdown(sample_df, path)
    content = path.read_text(encoding="utf-8")
    assert "Energiloven" in content
    assert "---" in content
    # Header pipe-table row
    assert "|" in content


def test_to_markdown_custom_columns(tmp_path, sample_df):
    path = tmp_path / "results.md"
    to_markdown(sample_df, path, columns=["tittel", "tema_treff"])
    content = path.read_text(encoding="utf-8")
    assert "tittel" in content
    assert "url" not in content  # excluded column


# ---------------------------------------------------------------------------
# export (auto-detect)
# ---------------------------------------------------------------------------

def test_export_csv(tmp_path, sample_df):
    path = tmp_path / "out.csv"
    export(sample_df, path)
    assert path.exists()


def test_export_xlsx(tmp_path, sample_df):
    path = tmp_path / "out.xlsx"
    export(sample_df, path)
    assert path.exists()


def test_export_md(tmp_path, sample_df):
    path = tmp_path / "out.md"
    export(sample_df, path)
    assert path.exists()


def test_export_markdown_extension(tmp_path, sample_df):
    path = tmp_path / "out.markdown"
    export(sample_df, path)
    assert path.exists()


def test_export_unsupported_raises(tmp_path, sample_df):
    with pytest.raises(ValueError, match="Unsupported export format"):
        export(sample_df, tmp_path / "out.txt")
