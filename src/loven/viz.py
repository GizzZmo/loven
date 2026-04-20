"""Data visualisation helpers for peace-law analysis.

Provides bar charts and word clouds based on Lovdata search results.
Both ``matplotlib`` and ``wordcloud`` are **optional** dependencies; this
module degrades gracefully with an :class:`ImportError` if they are missing.

Install the visualisation extras with::

    pip install "loven[viz]"

Functions
---------
bar_chart
    Horizontal bar chart of the most peace-relevant laws by ``tema_treff``.
word_cloud
    Word cloud built from law titles weighted by ``tema_treff``.
save_figure
    Convenience wrapper: render a figure to a file or show it interactively.

Usage
-----
>>> from loven import LovDataClient, analyze_peace_laws
>>> from loven.viz import bar_chart, save_figure
>>> client = LovDataClient()
>>> df = analyze_peace_laws(client, "energi")
>>> fig = bar_chart(df)
>>> save_figure(fig, "chart.png")
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)

_MATPLOTLIB_MISSING = (
    "matplotlib is required for visualisation. "
    "Install it with:  pip install 'loven[viz]'"
)
_WORDCLOUD_MISSING = (
    "wordcloud is required for word cloud generation. "
    "Install it with:  pip install 'loven[viz]'"
)


def bar_chart(
    df: "pd.DataFrame",
    *,
    top_n: int = 15,
    title: str = "Top Peace-Relevant Laws (tema_treff)",
    figsize: tuple[int, int] = (10, 6),
    color: str = "#2E86AB",
) -> Any:  # matplotlib.figure.Figure
    """Create a horizontal bar chart of the most peace-relevant laws.

    Parameters
    ----------
    df:
        DataFrame with at least ``tittel`` and ``tema_treff`` columns,
        as returned by :func:`~loven.analysis.analyze_peace_laws`.
    top_n:
        Number of top results to display.
    title:
        Chart title.
    figsize:
        Figure size ``(width, height)`` in inches.
    color:
        Bar colour (any valid matplotlib colour string).

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.  Call :func:`save_figure` or
        ``plt.show()`` to display it.

    Raises
    ------
    ImportError
        If ``matplotlib`` is not installed.
    ValueError
        If *df* is empty or lacks the required columns.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(_MATPLOTLIB_MISSING) from exc

    if df.empty:
        raise ValueError("DataFrame is empty – nothing to plot.")
    for col in ("tittel", "tema_treff"):
        if col not in df.columns:
            raise ValueError(f"DataFrame is missing required column '{col}'.")

    subset = df.nlargest(top_n, "tema_treff")[["tittel", "tema_treff"]].copy()
    # Truncate long titles for readability
    subset["tittel_short"] = subset["tittel"].str[:60]

    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(subset["tittel_short"][::-1], subset["tema_treff"][::-1], color=color)
    ax.set_xlabel("Tema Treff (matching peace themes)")
    ax.set_title(title)
    ax.tick_params(axis="y", labelsize=9)
    fig.tight_layout()
    logger.info("bar_chart: rendered %d bars.", len(subset))
    return fig


def word_cloud(
    df: "pd.DataFrame",
    *,
    max_words: int = 100,
    background_color: str = "white",
    colormap: str = "Blues",
    figsize: tuple[int, int] = (12, 6),
    title: str = "Peace Law Title Word Cloud",
) -> Any:  # matplotlib.figure.Figure
    """Generate a word cloud from law titles weighted by ``tema_treff``.

    Parameters
    ----------
    df:
        DataFrame with at least ``tittel`` and ``tema_treff`` columns.
    max_words:
        Maximum number of words in the cloud.
    background_color:
        Background colour of the cloud image.
    colormap:
        Matplotlib colormap name used to colour the words.
    figsize:
        Figure size ``(width, height)`` in inches.
    title:
        Figure title.

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure.

    Raises
    ------
    ImportError
        If ``wordcloud`` or ``matplotlib`` is not installed.
    ValueError
        If *df* is empty.
    """
    try:
        from wordcloud import WordCloud
    except ImportError as exc:
        raise ImportError(_WORDCLOUD_MISSING) from exc
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(_MATPLOTLIB_MISSING) from exc

    if df.empty:
        raise ValueError("DataFrame is empty – nothing to plot.")

    # Build frequency dict: each word weighted by tema_treff (+1 floor)
    freq: dict[str, float] = {}
    for _, row in df.iterrows():
        weight = float(row.get("tema_treff", 1)) + 1.0
        for word in str(row.get("tittel", "")).split():
            word_clean = word.strip("().,")
            if len(word_clean) > 2:
                freq[word_clean] = freq.get(word_clean, 0) + weight

    wc = WordCloud(
        max_words=max_words,
        background_color=background_color,
        colormap=colormap,
        width=figsize[0] * 100,
        height=figsize[1] * 100,
    ).generate_from_frequencies(freq)

    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(title, fontsize=14)
    fig.tight_layout()
    logger.info("word_cloud: rendered cloud with %d word frequencies.", len(freq))
    return fig


def save_figure(fig: Any, path: str | None = None) -> None:
    """Save or display a matplotlib figure.

    Parameters
    ----------
    fig:
        A ``matplotlib.figure.Figure`` object.
    path:
        File path to save the figure (e.g. ``"chart.png"``).
        If ``None``, the figure is displayed interactively via ``plt.show()``.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(_MATPLOTLIB_MISSING) from exc

    if path is not None:
        fig.savefig(path, bbox_inches="tight", dpi=150)
        logger.info("Figure saved to %s.", path)
    else:
        plt.show()
