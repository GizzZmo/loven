"""Generate static assets, export artifacts, and chart screenshots from sample data.

This script is used by the ``generate-assets`` CI workflow and can also be run locally::

    pip install "loven[viz]" openpyxl
    python scripts/generate_assets.py

Outputs (written to ``artifacts/``)
------------------------------------
* ``bar_chart.png``      – horizontal bar chart of top peace-relevant laws
* ``word_cloud.png``     – word-cloud from law titles weighted by tema_treff
* ``sample_output.csv``  – CSV export of the sample search results
* ``sample_output.xlsx`` – Excel export of the same results
* ``sample_output.md``   – Markdown table export of the same results
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve paths relative to the repository root
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
SAMPLE_DATA = REPO_ROOT / "sample_data" / "mock_lovdata_response.json"
OUT_DIR = REPO_ROOT / "artifacts"


def build_dataframe():
    """Load mock data and return a filtered, scored DataFrame."""
    import pandas as pd  # noqa: F401 – ensure pandas is available early

    from loven.client import LovDataClient

    raw = json.loads(SAMPLE_DATA.read_text(encoding="utf-8"))
    client = LovDataClient.__new__(LovDataClient)  # skip __init__; no network needed
    hits = client.filter_peace_laws(raw)
    df = client.to_dataframe(hits)
    return df


def generate_charts(df, out_dir: Path) -> None:
    """Render bar chart and word cloud PNGs into *out_dir*."""
    from loven.viz import bar_chart, save_figure, word_cloud

    bar = bar_chart(df, title="Top Peace-Relevant Laws (sample data)")
    save_figure(bar, str(out_dir / "bar_chart.png"))
    bar.clf()

    wc = word_cloud(df, title="Peace Law Word Cloud (sample data)")
    save_figure(wc, str(out_dir / "word_cloud.png"))
    wc.clf()

    print("Charts written.")


def generate_exports(df, out_dir: Path) -> None:
    """Write CSV, Excel, and Markdown exports into *out_dir*."""
    from loven.export import to_csv, to_excel, to_markdown

    to_csv(df, out_dir / "sample_output.csv")
    to_excel(df, out_dir / "sample_output.xlsx")
    to_markdown(df, out_dir / "sample_output.md")

    print("Export files written.")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading sample data from {SAMPLE_DATA} …")
    df = build_dataframe()

    if df.empty:
        print("ERROR: no peace-relevant rows found in sample data.", file=sys.stderr)
        return 1

    print(f"DataFrame has {len(df)} rows.")

    generate_charts(df, OUT_DIR)
    generate_exports(df, OUT_DIR)

    print(f"\nAll assets written to: {OUT_DIR}")
    for p in sorted(OUT_DIR.iterdir()):
        print(f"  {p.name}  ({p.stat().st_size:,} bytes)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
