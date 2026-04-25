# Glossary

Key terms and concepts used throughout the **loven** project.

---

## A

### `analyze_peace_laws()`
The main high-level function in `loven.analysis`. Given a `LovDataClient` and a search query string it:

1. Calls `client.search(query, limit)` to fetch raw results from Lovdata.
2. Passes each result through `count_themes()` to compute a relevance score.
3. Returns a sorted `pandas.DataFrame` with columns: `tittel`, `url`, `dato`, `dokumenttype`, `tema_treff`.

### `AsyncLovDataClient`
An async subclass of `LovDataClient` that adds `async_search()` and `async_peace_batch_analysis()` for parallel, non-blocking API calls using `aiohttp` and `asyncio`.

---

## B

### `batch_analyze()`
A helper in `loven.analysis` that calls `analyze_peace_laws()` for each query in a list and concatenates the results into a single `pandas.DataFrame`. Each row includes a `query` column indicating which search produced it.

---

## C

### Cache
**loven** ships with `loven.cache.DiskCache`, a simple JSON-based disk cache stored in `~/.loven_cache/`. Each cached entry records the API response and a timestamp. Entries older than `ttl` seconds are treated as stale and re-fetched on the next call.

### CLI
The command-line interface registered as the `loven` console script in `pyproject.toml`. Three sub-commands:

| Sub-command | Description |
|---|---|
| `loven search <query>` | Fetch and display results as a terminal table |
| `loven export <query> --output <file>` | Save results to CSV, Excel, or Markdown |
| `loven themes list` | Print all current peace-theme keywords |

### `count_themes()`
A pure function in `loven.themes` that counts how many distinct peace-theme keywords appear (case-insensitively) in a text string. The result is stored in the `tema_treff` column of every results DataFrame.

---

## D

### `DiskCache`
See [Cache](#cache).

### `dokumenttype`
A Lovdata API response field indicating the type of legal document — for example `LOV` (act/statute), `FOR` (regulation), or `RUNDSKRIV` (circular).

---

## E

### Export
`loven.export` provides thin wrappers around `pandas.DataFrame` serialisation:

- `to_csv(df, path)` – comma-separated values
- `to_excel(df, path)` – Excel workbook (requires `openpyxl`)
- `to_markdown(df, path)` – GitHub-flavoured Markdown table
- `export(df, path)` – dispatches based on file extension

---

## F

### `filter_peace_laws()`
A method on `LovDataClient` that takes a raw Lovdata API response dict and returns only the hits that mention at least one peace-theme keyword in their title.

---

## L

### Lovdata
[Lovdata.no](https://lovdata.no) — the Norwegian foundation that maintains the authoritative database of Norwegian legislation, regulations, and court decisions. **loven** uses only the publicly available API endpoints.

### `LovDataClient`
The synchronous HTTP client in `loven.client`. Wraps a persistent `requests.Session` with JSON headers. All network errors are caught internally; callers always receive a dict (possibly `{"error": "…"}`).

---

## M

### `matches_theme()`
A pure function in `loven.themes` that returns `True` if any peace-theme keyword appears in the given text string (case-insensitive substring match).

---

## N

### NLP (Natural Language Processing)
`loven.nlp` provides two synonym-expansion utilities:

- `expand_themes(themes)` – uses the built-in `SYNONYMS` dict; no external dependencies.
- `expand_themes_spacy(themes, nlp)` – uses a loaded spaCy Norwegian model for richer expansion (optional, requires `pip install 'loven[nlp]'`).

---

## P

### Peace Themes
The list of Norwegian keyword strings in `loven.themes.PEACE_THEMES` used to score legal documents. See the [Peace Themes wiki page](peace-themes.md) for the full list and rationale.

### `pyproject.toml`
The PEP 517/518-compliant build configuration file. Defines package metadata, optional dependency groups (`notebook`, `viz`, `nlp`, `dev`, `all`), and the `loven` CLI entry point.

---

## S

### Sample Data
`sample_data/mock_lovdata_response.json` — a bundled JSON snapshot of a real Lovdata API response, used for offline development and in the test suite.

### Streamlit Dashboard
An interactive web UI in `app/streamlit_app.py` with a search box, results table, theme-filter sidebar, visualisation panel, and CSV/Markdown download buttons. Start it with `streamlit run app/streamlit_app.py` or `docker compose up`.

---

## T

### `tema_treff`
Norwegian for "theme hits". The integer relevance score column added to every results DataFrame by `count_themes()`. Higher is more relevant.

### TTL (Time To Live)
The number of seconds a `DiskCache` entry is considered fresh before being re-fetched from the Lovdata API. Default: 3 600 seconds (1 hour).

---

## V

### Visualisation
`loven.viz` provides two charting helpers (require `pip install 'loven[viz]'`):

- `bar_chart(df, top_n)` – horizontal bar chart of the top `n` laws by `tema_treff`, returned as a `matplotlib.figure.Figure`.
- `word_cloud(df)` – word cloud of law titles, returned as a `matplotlib.figure.Figure`.
