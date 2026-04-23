# Architecture

This page describes the internal design of **loven** — why it is structured the way it is, how components fit together, and the reasoning behind key decisions.

---

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interfaces                         │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────────┐│
│  │   Jupyter    │  │     CLI      │  │   Streamlit Dashboard  ││
│  │  Notebook    │  │ loven search │  │  app/streamlit_app.py  ││
│  └──────┬───────┘  └──────┬───────┘  └───────────┬────────────┘│
└─────────┼─────────────────┼──────────────────────┼─────────────┘
          │                 │                       │
          ▼                 ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      loven Python Package                       │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐│
│  │  analysis   │  │   themes    │  │          nlp             ││
│  │ analyze_    │  │ PEACE_THEMES│  │  expand_themes()         ││
│  │ peace_laws()│  │ count_themes│  │  (synonym expansion)     ││
│  └──────┬──────┘  └──────┬──────┘  └──────────────────────────┘│
│         │                │                                      │
│         ▼                ▼                                      │
│  ┌─────────────────────────────────┐  ┌────────────────────────┐│
│  │     client                      │  │      cache             ││
│  │ LovDataClient (sync)            │  │  DiskCache             ││
│  │ AsyncLovDataClient (async)      │◄─┤  (JSON, TTL)           ││
│  └──────────────┬──────────────────┘  └────────────────────────┘│
│                 │                                                │
│         ┌───────┴────────┐                                      │
│         │    export      │                                      │
│         │ to_csv()       │                                      │
│         │ to_excel()     │                                      │
│         │ to_markdown()  │                                      │
│         └────────────────┘                                      │
└─────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     External Services                           │
│                  api.lovdata.no (public API)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Package Structure

```
src/loven/
├── __init__.py      Public API surface – re-exports all symbols
├── themes.py        PEACE_THEMES constant and theme-matching utilities
├── client.py        LovDataClient (sync) + AsyncLovDataClient (async)
├── analysis.py      analyze_peace_laws() and batch_analyze()
├── cache.py         DiskCache – JSON-based caching with TTL
├── export.py        export(), to_csv(), to_excel(), to_markdown()
├── nlp.py           expand_themes(), SYNONYMS – synonym expansion
├── viz.py           bar_chart(), word_cloud() – matplotlib/wordcloud
└── cli.py           argparse-based CLI (loven search / export / themes)
```

---

## Module Responsibilities

### `themes.py`

The single source of truth for peace-theme keywords. Provides:

- `PEACE_THEMES: list[str]` — the canonical list of Norwegian keywords
- `matches_theme(text, themes)` — returns `True` if any theme appears in `text`
- `count_themes(text, themes)` — counts how many distinct themes appear in `text`

**Design decision:** keeping themes in their own module makes it easy to extend the list without touching the client or analysis logic.

### `client.py`

Two classes: `LovDataClient` (synchronous) and `AsyncLovDataClient` (asynchronous, inherits from the former).

`LovDataClient` wraps a persistent `requests.Session` to benefit from connection pooling and shared headers. All exceptions are caught internally so callers never need to handle network errors — they receive an empty result dict instead.

`AsyncLovDataClient` adds `async_search()` and `async_peace_batch_analysis()` for parallel batch fetching via `aiohttp`. It inherits the synchronous methods unchanged.

**Design decision:** composition via inheritance so that synchronous and asynchronous code share the same interface, but users can choose the right tool for their context (notebook cell vs. batch script).

### `analysis.py`

- `analyze_peace_laws(client, query, limit, themes)` — orchestrates search + filter + DataFrame construction for a single query.
- `batch_analyze(client, queries, **kwargs)` — runs `analyze_peace_laws` for each query and concatenates the results.

**Design decision:** functions are pure (given a client) and stateless, making them easy to test with a mock client.

### `cache.py`

`DiskCache` stores serialised JSON responses keyed by a hash of the request URL + parameters. Each entry records a timestamp so that entries older than `ttl` seconds are treated as stale and re-fetched. The cache lives in `~/.loven_cache/` by default.

**Design decision:** a simple flat-file JSON cache avoids a database dependency while still providing meaningful performance gains when running batch analyses repeatedly.

### `export.py`

Thin wrappers around pandas `DataFrame.to_csv`, `DataFrame.to_excel`, and a custom Markdown serialiser. The top-level `export()` function dispatches based on file extension.

### `nlp.py`

- `SYNONYMS: dict[str, list[str]]` — a hand-curated map from each theme keyword to related Norwegian terms.
- `expand_themes(themes)` — returns the input list extended with all known synonyms.
- `expand_themes_spacy(themes, nlp)` — (optional) uses a loaded spaCy Norwegian model to find additional synonyms at runtime.

**Design decision:** the built-in synonym map works without any external model download; spaCy support is opt-in.

### `viz.py`

- `bar_chart(df, top_n)` — horizontal bar chart of the top `n` laws by `tema_treff` score using `matplotlib`.
- `word_cloud(df)` — word cloud of law titles using the `wordcloud` package.

Both return a `matplotlib.figure.Figure` so the caller controls display (Jupyter `display()` or Streamlit `st.pyplot()`).

### `cli.py`

An `argparse`-based entry point registered as the `loven` console script in `pyproject.toml`. Three sub-commands: `search`, `export`, `themes list`.

---

## Data Flow

```
User query string
       │
       ▼
LovDataClient.search(query, limit)
       │  GET api.lovdata.no/sok?q=<query>&limit=<limit>
       │  → {"hits": [{tittel, url, dato, ...}, ...]}
       ▼
analyze_peace_laws() / filter_peace_laws()
       │  count_themes(tittel) → tema_treff integer
       │  keep rows where tema_treff > 0
       ▼
pd.DataFrame  columns: tittel, url, dato, dokumenttype, tema_treff
       │
       ├──► Jupyter display / st.dataframe()
       ├──► export() → CSV / Excel / Markdown
       └──► bar_chart() / word_cloud() → matplotlib Figure
```

---

## Testing Strategy

Tests live in `tests/` and use `pytest`. HTTP calls are mocked with `unittest.mock.patch` so the test suite runs fully offline.

| Test file | Coverage |
|---|---|
| `test_themes.py` | `count_themes`, `matches_theme`, theme list integrity |
| `test_client.py` | `search()` success and error paths, session headers |
| `test_analysis.py` | `analyze_peace_laws()` with sample data |
| `test_cli.py` | All three CLI sub-commands |
| `test_cache.py` | Cache hit, miss, expiry |
| `test_export.py` | CSV, Excel, Markdown output |

---

## Multi-Paradigm Design

One of the explicit goals of **loven** is to demonstrate multiple programming paradigms in a single readable codebase:

| Paradigm | Where used |
|---|---|
| **Object-oriented** | `LovDataClient`, `AsyncLovDataClient`, `DiskCache` |
| **Functional** | `filter_peace_laws`, `count_themes`, `matches_theme` — pure functions |
| **Declarative** | Pandas DataFrame operations (`sort_values`, column selection) |
| **Imperative** | Structured logging, error handling, CLI argument parsing |
| **Asynchronous** | `AsyncLovDataClient.async_search`, `async_peace_batch_analysis` |
