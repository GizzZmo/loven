"""Unit tests for loven.cache (DiskCache)."""

from __future__ import annotations

import time

import pytest

from loven.cache import DiskCache


@pytest.fixture
def cache(tmp_path):
    """DiskCache backed by a temporary directory."""
    return DiskCache(cache_dir=tmp_path, ttl=60)


def test_cache_miss_returns_none(cache):
    assert cache.get("nonexistent_key") is None


def test_cache_set_and_get(cache):
    data = {"hits": [{"tittel": "Energiloven"}]}
    cache.set("k1", data)
    assert cache.get("k1") == data


def test_cache_len(cache):
    assert len(cache) == 0
    cache.set("a", {"hits": []})
    cache.set("b", {"hits": []})
    assert len(cache) == 2


def test_cache_clear(cache):
    cache.set("x", {"hits": []})
    removed = cache.clear()
    assert removed == 1
    assert len(cache) == 0


def test_cache_ttl_expiry(tmp_path):
    cache = DiskCache(cache_dir=tmp_path, ttl=0)  # 0-second TTL
    cache.set("z", {"hits": []})
    time.sleep(0.05)
    # Should be expired immediately
    assert cache.get("z") is None


def test_cache_no_ttl(tmp_path):
    cache = DiskCache(cache_dir=tmp_path, ttl=None)
    cache.set("forever", {"hits": [1, 2, 3]})
    assert cache.get("forever") == {"hits": [1, 2, 3]}


def test_make_key_is_stable():
    k1 = DiskCache.make_key("energi", limit=20)
    k2 = DiskCache.make_key("energi", limit=20)
    assert k1 == k2


def test_make_key_differs_for_different_queries():
    assert DiskCache.make_key("energi") != DiskCache.make_key("vann")


def test_make_key_differs_for_different_params():
    assert DiskCache.make_key("energi", limit=10) != DiskCache.make_key("energi", limit=20)
