"""High-level analysis helpers for peace-law exploration.

Functions
---------
analyze_peace_laws
    Synchronous: search → filter → DataFrame pipeline.
batch_analyze
    Run multiple queries and concatenate results into one DataFrame.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

from loven.client import LovDataClient

logger = logging.getLogger(__name__)


def analyze_peace_laws(
    client: LovDataClient,
    query: str,
    *,
    limit: int = 20,
    themes: list[str] | None = None,
    **search_kwargs,
) -> "pd.DataFrame":
    """Run a single query, filter for peace-relevant laws, and return a DataFrame.

    This is the primary entry point for synchronous analysis.

    Parameters
    ----------
    client:
        An initialised :class:`~loven.client.LovDataClient` instance.
    query:
        Norwegian search term(s), e.g. ``"vannressursloven"``.
    limit:
        Maximum number of results to request from the API.
    themes:
        Optional custom keyword list.  Defaults to :data:`~loven.themes.PEACE_THEMES`.
    **search_kwargs:
        Extra keyword arguments forwarded to :meth:`~loven.client.LovDataClient.search`
        (e.g. ``doc_type="lov"``, ``date_from="2010-01-01"``).

    Returns
    -------
    pd.DataFrame
        Columns: ``tittel``, ``url``, ``dato``, ``dokumenttype``,
        ``relevans_for_fred``, ``tema_treff``.
        Returns an empty DataFrame if no matching results are found.

    Examples
    --------
    >>> client = LovDataClient()
    >>> df = analyze_peace_laws(client, "energilov miljø")
    >>> print(df[["tittel", "tema_treff"]])
    """
    raw = client.search(query, limit=limit, **search_kwargs)
    hits = client.filter_peace_laws(raw, themes)
    df = client.to_dataframe(hits)
    print(
        f"Analysert {len(df)} lover relatert til '{query}' (Global Peace Agreement)."
    )
    return df


def batch_analyze(
    client: LovDataClient,
    queries: list[str],
    *,
    limit: int = 20,
    themes: list[str] | None = None,
    **search_kwargs,
) -> "pd.DataFrame":
    """Run multiple queries sequentially and return a single combined DataFrame.

    Parameters
    ----------
    client:
        An initialised :class:`~loven.client.LovDataClient` instance.
    queries:
        List of Norwegian search terms.
    limit:
        Maximum number of results per query.
    themes:
        Optional custom keyword list.
    **search_kwargs:
        Extra keyword arguments forwarded to each search.

    Returns
    -------
    pd.DataFrame
        Combined results with an extra ``_query`` column indicating the source query.
        Sorted by ``tema_treff`` descending.

    Examples
    --------
    >>> client = LovDataClient()
    >>> queries = ["energilov", "vannressursloven", "miljøvern"]
    >>> df = batch_analyze(client, queries)
    >>> df.head()
    """
    import pandas as pd

    frames = []
    for query in queries:
        df = analyze_peace_laws(client, query, limit=limit, themes=themes, **search_kwargs)
        if not df.empty:
            df["_query"] = query
            frames.append(df)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = combined.sort_values("tema_treff", ascending=False).reset_index(drop=True)
    return combined
