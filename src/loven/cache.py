"""Disk-based JSON cache for Lovdata API responses.

Stores API responses as JSON files under a configurable cache directory,
keyed by a hash of the request parameters.  This eliminates redundant
network calls during repeated development/analysis sessions.

Classes
-------
DiskCache
    Simple file-system cache with optional TTL (time-to-live).

Usage
-----
>>> from loven.cache import DiskCache
>>> cache = DiskCache()
>>> cache.set("energi_20", {"hits": [...]})
>>> data = cache.get("energi_20")
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = Path.home() / ".loven_cache"
DEFAULT_TTL = 3600  # seconds (1 hour)


class DiskCache:
    """Persist Lovdata API responses as JSON files on disk.

    Parameters
    ----------
    cache_dir:
        Directory where cached files are stored.
        Defaults to ``~/.loven_cache/``.
    ttl:
        Time-to-live in seconds.  Entries older than *ttl* are treated as
        cache misses.  Set to ``None`` to keep entries indefinitely.

    Examples
    --------
    >>> cache = DiskCache()
    >>> cache.set("my_key", {"hits": []})
    >>> result = cache.get("my_key")
    >>> result
    {'hits': []}
    """

    def __init__(
        self,
        cache_dir: str | Path = DEFAULT_CACHE_DIR,
        ttl: int | None = DEFAULT_TTL,
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.ttl = ttl
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info("DiskCache initialised at %s (ttl=%s).", self.cache_dir, ttl)

    # ------------------------------------------------------------------
    # Key helpers
    # ------------------------------------------------------------------

    @staticmethod
    def make_key(query: str, **params: Any) -> str:
        """Build a stable cache key from a query string and optional parameters.

        Parameters
        ----------
        query:
            The search query string.
        **params:
            Additional request parameters (e.g. ``limit=20``).

        Returns
        -------
        str
            A short hexadecimal hash string suitable for use as a filename.
        """
        raw = json.dumps({"q": query, **params}, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.json"

    # ------------------------------------------------------------------
    # Core get / set / clear
    # ------------------------------------------------------------------

    def get(self, key: str) -> dict[str, Any] | None:
        """Retrieve a cached response.

        Parameters
        ----------
        key:
            Cache key (usually from :meth:`make_key`).

        Returns
        -------
        dict or None
            The cached data, or ``None`` if not found / expired.
        """
        path = self._path(key)
        if not path.exists():
            return None

        try:
            envelope = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Cache read error for key %s: %s", key, exc)
            return None

        if self.ttl is not None:
            age = time.time() - envelope.get("_cached_at", 0)
            if age > self.ttl:
                logger.debug("Cache miss (expired) for key %s.", key)
                path.unlink(missing_ok=True)
                return None

        logger.debug("Cache hit for key %s.", key)
        return envelope.get("data")

    def set(self, key: str, data: dict[str, Any]) -> None:
        """Store a response in the cache.

        Parameters
        ----------
        key:
            Cache key (usually from :meth:`make_key`).
        data:
            The API response dict to cache.
        """
        envelope = {"_cached_at": time.time(), "data": data}
        path = self._path(key)
        try:
            path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.debug("Cache set for key %s.", key)
        except OSError as exc:
            logger.warning("Cache write error for key %s: %s", key, exc)

    def clear(self) -> int:
        """Delete all cached files.

        Returns
        -------
        int
            Number of files removed.
        """
        removed = 0
        for f in self.cache_dir.glob("*.json"):
            try:
                f.unlink()
                removed += 1
            except OSError:
                pass
        logger.info("Cache cleared: %d files removed.", removed)
        return removed

    def __len__(self) -> int:
        return sum(1 for _ in self.cache_dir.glob("*.json"))

    def __repr__(self) -> str:  # pragma: no cover
        return f"DiskCache(cache_dir={self.cache_dir!r}, ttl={self.ttl!r})"
