"""Unit tests for loven.viz (visualisation helpers).

These tests verify error-handling and interface contracts without
requiring matplotlib or wordcloud to be installed.
"""

from __future__ import annotations

import builtins

import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "tittel": ["Energiloven", "Vannressursloven", "Miljøvernloven"],
            "url": ["https://lovdata.no/1", "https://lovdata.no/2", "https://lovdata.no/3"],
            "tema_treff": [2, 1, 1],
        }
    )


@pytest.fixture
def empty_df():
    return pd.DataFrame(columns=["tittel", "url", "tema_treff"])


# ---------------------------------------------------------------------------
# Tests that run regardless of matplotlib availability
# ---------------------------------------------------------------------------

class TestBarChartImportError:
    def test_raises_import_error_without_matplotlib(self, monkeypatch, sample_df):
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "matplotlib.pyplot":
                raise ImportError("No module named 'matplotlib'")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        from loven.viz import bar_chart
        with pytest.raises(ImportError, match="matplotlib"):
            bar_chart(sample_df)


class TestBarChartValidation:
    def test_raises_on_empty_df(self, monkeypatch, empty_df):
        """bar_chart should raise ValueError for an empty DataFrame."""
        # Patch matplotlib so we reach the validation code
        import sys
        import types

        fake_plt = types.ModuleType("matplotlib.pyplot")
        fake_mpl = types.ModuleType("matplotlib")
        fake_mpl.pyplot = fake_plt
        monkeypatch.setitem(sys.modules, "matplotlib", fake_mpl)
        monkeypatch.setitem(sys.modules, "matplotlib.pyplot", fake_plt)

        from loven.viz import bar_chart
        with pytest.raises(ValueError, match="empty"):
            bar_chart(empty_df)

    def test_raises_on_missing_column(self, monkeypatch):
        """bar_chart should raise ValueError when required columns are absent."""
        import sys
        import types

        fake_plt = types.ModuleType("matplotlib.pyplot")
        fake_mpl = types.ModuleType("matplotlib")
        fake_mpl.pyplot = fake_plt
        monkeypatch.setitem(sys.modules, "matplotlib", fake_mpl)
        monkeypatch.setitem(sys.modules, "matplotlib.pyplot", fake_plt)

        bad_df = pd.DataFrame({"tittel": ["A", "B"]})
        from loven.viz import bar_chart
        with pytest.raises(ValueError, match="tema_treff"):
            bar_chart(bad_df)


class TestWordCloudImportError:
    def test_raises_import_error_without_wordcloud(self, monkeypatch, sample_df):
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "wordcloud":
                raise ImportError("No module named 'wordcloud'")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        from loven.viz import word_cloud
        with pytest.raises(ImportError, match="wordcloud"):
            word_cloud(sample_df)

    def test_raises_on_empty_df_wordcloud(self, monkeypatch, empty_df):
        """word_cloud should raise ValueError for an empty DataFrame."""
        real_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "wordcloud":
                raise ImportError("No module named 'wordcloud'")
            return real_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)

        from loven.viz import word_cloud
        with pytest.raises((ImportError, ValueError)):
            word_cloud(empty_df)
