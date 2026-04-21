"""Export helpers – save DataFrames to various file formats.

Supported formats
-----------------
* **CSV** – standard comma-separated values
* **Excel** – ``.xlsx`` via ``openpyxl`` (requires ``pandas[excel]``)
* **Markdown** – GitHub-flavoured Markdown table

Functions
---------
to_csv
    Export a DataFrame to a CSV file.
to_excel
    Export a DataFrame to an Excel file.
to_markdown
    Export a DataFrame to a Markdown file.
export
    Auto-detect format from file extension and delegate.

Usage
-----
>>> from loven import LovDataClient, analyze_peace_laws
>>> from loven.export import export
>>> client = LovDataClient()
>>> df = analyze_peace_laws(client, "energi")
>>> export(df, "results.md")
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)

# Columns rendered by default when exporting
DEFAULT_COLUMNS = ["tittel", "url", "dato", "dokumenttype", "tema_treff"]


def to_csv(df: "pd.DataFrame", path: str | Path, **kwargs) -> Path:
    """Export *df* to a CSV file.

    Parameters
    ----------
    df:
        DataFrame to export.
    path:
        Destination file path.
    **kwargs:
        Extra keyword arguments forwarded to :func:`pandas.DataFrame.to_csv`.

    Returns
    -------
    Path
        Resolved output path.
    """
    out = Path(path)
    df.to_csv(out, index=False, **kwargs)
    logger.info("Exported %d rows to CSV: %s", len(df), out)
    return out


def to_excel(df: "pd.DataFrame", path: str | Path, **kwargs) -> Path:
    """Export *df* to an Excel ``.xlsx`` file.

    Parameters
    ----------
    df:
        DataFrame to export.
    path:
        Destination file path (should end with ``.xlsx``).
    **kwargs:
        Extra keyword arguments forwarded to :func:`pandas.DataFrame.to_excel`.

    Returns
    -------
    Path
        Resolved output path.
    """
    out = Path(path)
    df.to_excel(out, index=False, **kwargs)
    logger.info("Exported %d rows to Excel: %s", len(df), out)
    return out


def to_markdown(
    df: "pd.DataFrame",
    path: str | Path,
    columns: list[str] | None = None,
) -> Path:
    """Export *df* to a GitHub-flavoured Markdown table file.

    Parameters
    ----------
    df:
        DataFrame to export.
    path:
        Destination file path (e.g. ``results.md``).
    columns:
        Subset of columns to include.  Defaults to :data:`DEFAULT_COLUMNS`.

    Returns
    -------
    Path
        Resolved output path.
    """
    out = Path(path)
    cols = columns or [c for c in DEFAULT_COLUMNS if c in df.columns]
    subset = df[cols] if cols else df

    lines: list[str] = []
    # Header row
    lines.append("| " + " | ".join(str(c) for c in subset.columns) + " |")
    # Separator
    lines.append("| " + " | ".join("---" for _ in subset.columns) + " |")
    # Data rows
    for _, row in subset.iterrows():
        cells = [str(v).replace("|", "\\|") for v in row]
        lines.append("| " + " | ".join(cells) + " |")

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info("Exported %d rows to Markdown: %s", len(df), out)
    return out


def export(
    df: "pd.DataFrame",
    path: str | Path,
    columns: list[str] | None = None,
    **kwargs,
) -> Path:
    """Export *df* to a file, inferring the format from the file extension.

    Supported extensions: ``.csv``, ``.xlsx``, ``.md`` / ``.markdown``.

    Parameters
    ----------
    df:
        DataFrame to export.
    path:
        Destination file path.  Extension determines the format.
    columns:
        Subset of columns to include (Markdown export only).
    **kwargs:
        Extra keyword arguments forwarded to the underlying export function
        (CSV or Excel).

    Returns
    -------
    Path
        Resolved output path.

    Raises
    ------
    ValueError
        If the file extension is not supported.
    """
    out = Path(path)
    ext = out.suffix.lower()

    if ext == ".csv":
        return to_csv(df, out, **kwargs)
    if ext == ".xlsx":
        return to_excel(df, out, **kwargs)
    if ext in (".md", ".markdown"):
        return to_markdown(df, out, columns=columns)

    raise ValueError(
        f"Unsupported export format: '{ext}'. Use .csv, .xlsx, or .md."
    )
