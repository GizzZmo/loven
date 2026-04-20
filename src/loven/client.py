"""Lovdata API clients – synchronous and asynchronous.

Classes
-------
LovDataClient
    Thread-safe, synchronous wrapper around the Lovdata REST API.
AsyncLovDataClient
    Asynchronous subclass for high-throughput batch searches.
"""

from __future__ import annotations

import logging
from typing import Any

import requests

from loven.themes import PEACE_THEMES, count_themes, matches_theme

logger = logging.getLogger(__name__)

BASE_URL: str = "https://api.lovdata.no"


class LovDataClient:
    """Synchronous wrapper around the Lovdata public REST API.

    Parameters
    ----------
    base_url:
        Root URL for all API requests.  Override to point at a local mirror
        or a mock server during testing.

    Examples
    --------
    >>> client = LovDataClient()
    >>> result = client.search("vannressursloven", limit=5)
    >>> df = client.to_dataframe(client.filter_peace_laws(result))
    """

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        logger.info("LovDataClient initialised (base_url=%s).", base_url)

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        *,
        limit: int = 20,
        doc_type: str | None = None,
        department: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, Any]:
        """Send a GET request to the Lovdata search endpoint.

        Parameters
        ----------
        query:
            Norwegian search term(s), e.g. ``"vannressursloven"``.
        limit:
            Maximum number of results to return.
        doc_type:
            Optional Lovdata document type filter (``type`` parameter).
        department:
            Optional Norwegian government department filter.
        date_from:
            Optional ISO date string ``YYYY-MM-DD`` – earliest publication.
        date_to:
            Optional ISO date string ``YYYY-MM-DD`` – latest publication.

        Returns
        -------
        dict
            Parsed JSON response.  On error returns ``{"error": "<message>"}``.
        """
        params: dict[str, Any] = {"q": query, "limit": limit}
        if doc_type:
            params["type"] = doc_type
        if department:
            params["departement"] = department
        if date_from:
            params["dato_fra"] = date_from
        if date_to:
            params["dato_til"] = date_to

        url = f"{self.base_url}/sok"
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
            logger.info(
                "Searched for '%s' – found %d hits.",
                query,
                len(data.get("hits", [])),
            )
            return data
        except Exception as exc:
            logger.error("API error for query '%s': %s", query, exc)
            return {"error": str(exc)}

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------

    def filter_peace_laws(
        self,
        data: dict[str, Any],
        themes: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Keep only hits whose title contains at least one peace-theme keyword.

        Parameters
        ----------
        data:
            Raw response dict from :meth:`search`.
        themes:
            Optional custom theme list.  Defaults to :data:`~loven.themes.PEACE_THEMES`.

        Returns
        -------
        list[dict]
            Filtered subset of ``data["hits"]``.
        """
        hits: list[dict[str, Any]] = data.get("hits", [])
        return [
            hit for hit in hits
            if matches_theme(str(hit.get("tittel", "")), themes)
        ]

    # ------------------------------------------------------------------
    # DataFrame helper
    # ------------------------------------------------------------------

    def to_dataframe(self, hits: list[dict[str, Any]]):  # -> pd.DataFrame
        """Convert a list of Lovdata hit dicts to a Pandas DataFrame.

        Returns a DataFrame with columns:
        ``tittel``, ``url``, ``dato``, ``dokumenttype``, ``relevans_for_fred``,
        ``tema_treff`` (number of matching peace themes).

        Parameters
        ----------
        hits:
            List of hit dicts, typically from :meth:`filter_peace_laws`.
        """
        import pandas as pd  # imported here to keep the module importable without pandas

        rows = [
            {
                "tittel": hit.get("tittel"),
                "url": hit.get("url"),
                "dato": hit.get("dato"),
                "dokumenttype": hit.get("dokumenttype"),
                "relevans_for_fred": matches_theme(str(hit.get("tittel", ""))),
                "tema_treff": count_themes(str(hit.get("tittel", ""))),
            }
            for hit in hits
        ]
        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.sort_values("tema_treff", ascending=False).reset_index(drop=True)
        return df


# ---------------------------------------------------------------------------
# Async client
# ---------------------------------------------------------------------------

class AsyncLovDataClient(LovDataClient):
    """Asynchronous extension of :class:`LovDataClient` for batch searches.

    Uses ``asyncio`` and ``aiohttp`` to fetch multiple queries in parallel,
    which is significantly faster than sequential synchronous calls.

    .. note::
        Inside Jupyter notebooks, call ``nest_asyncio.apply()`` before using
        ``await`` at the top level.

    Examples
    --------
    >>> import asyncio
    >>> import nest_asyncio; nest_asyncio.apply()
    >>> client = AsyncLovDataClient()
    >>> df = asyncio.run(client.async_peace_batch_analysis(["energilov", "vannressursloven"]))
    """

    async def async_search(
        self,
        session: Any,  # aiohttp.ClientSession
        query: str,
        *,
        limit: int = 20,
        doc_type: str | None = None,
        department: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> dict[str, Any]:
        """Single async GET request to the Lovdata search endpoint.

        Parameters
        ----------
        session:
            An active ``aiohttp.ClientSession``.
        query:
            Norwegian search term(s).
        limit:
            Maximum number of results to return.

        Returns
        -------
        dict
            Parsed JSON response, or ``{"error": "..."}`` on failure.
        """
        params: dict[str, Any] = {"q": query, "limit": limit}
        if doc_type:
            params["type"] = doc_type
        if department:
            params["departement"] = department
        if date_from:
            params["dato_fra"] = date_from
        if date_to:
            params["dato_til"] = date_to

        url = f"{self.base_url}/sok"
        try:
            async with session.get(url, params=params, timeout=15) as resp:
                resp.raise_for_status()
                data = await resp.json()
                logger.info(
                    "Async search done for '%s' – %d hits.",
                    query,
                    len(data.get("hits", [])),
                )
                return data
        except Exception as exc:
            logger.error("Async search failed for '%s': %s", query, exc)
            return {"error": str(exc)}

    async def async_peace_batch_analysis(
        self,
        queries: list[str],
        themes: list[str] | None = None,
        **common_filters: Any,
    ):  # -> pd.DataFrame
        """Run all queries in parallel and return a combined, ranked DataFrame.

        Parameters
        ----------
        queries:
            List of Norwegian search terms to run concurrently.
        themes:
            Optional custom theme list.
        **common_filters:
            Keyword arguments forwarded to :meth:`async_search`
            (e.g. ``limit=30``, ``doc_type="lov"``).

        Returns
        -------
        pd.DataFrame
            Combined results sorted by ``tema_treff`` descending.
        """
        import asyncio

        import aiohttp
        import pandas as pd

        if themes is None:
            themes = PEACE_THEMES

        async with aiohttp.ClientSession() as session:
            tasks = [
                self.async_search(session, q, **common_filters)
                for q in queries
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        all_hits: list[dict[str, Any]] = []
        for query, result in zip(queries, results):
            if isinstance(result, Exception):
                logger.error("Exception for '%s': %s", query, result)
                continue
            for hit in result.get("hits", []):
                hit["_query"] = query
                hit["tema_treff"] = count_themes(str(hit.get("tittel", "")), themes)
            all_hits.extend(result.get("hits", []))

        df = pd.DataFrame(all_hits)
        if not df.empty:
            df = df.sort_values("tema_treff", ascending=False).reset_index(drop=True)
            cols = ["tittel", "url", "tema_treff", "_query"]
            existing = [c for c in cols if c in df.columns]
            df = df[existing + [c for c in df.columns if c not in existing]]

        print(
            f"Async batch complete: {len(queries)} queries → {len(df)} total hits."
        )
        return df
