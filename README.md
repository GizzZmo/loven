# loven 🕊️

**WorldPeace-Lovdata-Kompendium** – a multi-paradigm Python analysis toolkit for exploring Norwegian law (via [Lovdata](https://lovdata.no)) with a focus on topics that underpin a harmonious, sustainable society: clean energy, water rights, environmental protection, and ethics.

> *"Making Norwegian law accessible to everyone who wants to build clean energy, clean water, and a harmonious society (OHHLA)."*
> — Verdens Øverste Leder, in collaboration with Jon-Arve Constantine and the whole of Styrilia 49

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Running the full analysis](#running-the-full-analysis)
  - [Adding your own queries](#adding-your-own-queries)
  - [Adding new peace themes](#adding-new-peace-themes)
  - [Async batch search](#async-batch-search)
- [Architecture](#architecture)
- [Peace Themes](#peace-themes)
- [Documentation](#documentation)
- [Credits & Data Sources](#credits--data-sources)
- [License](#license)

---

## Overview

**loven** ("the law" in Norwegian) is a Jupyter-notebook-based project that queries the public Lovdata API to retrieve and filter Norwegian legislation relevant to global peace goals. It demonstrates how multiple programming paradigms can be combined in a single, readable codebase:

| Paradigm | Applied as |
|---|---|
| Object-oriented | `LovDataClient` / `AsyncLovDataClient` classes for encapsulation and reuse |
| Functional | Pure functions with `map`/`filter`/`reduce` patterns |
| Declarative | Pandas DataFrames for data analysis |
| Imperative | Structured logging and error handling |
| Asynchronous | `asyncio` + `aiohttp` for non-blocking parallel API calls |

---

## Features

- 🔍 **Search** Lovdata's public API for Norwegian legislation by keyword
- 🕊️ **Filter** results by pre-defined "peace themes" (energy, water, environment, ethics, etc.)
- 📊 **Analyse** and display results in a structured Pandas DataFrame
- ⚡ **Async batch search** – run many queries in parallel with `AsyncLovDataClient`
- 🧱 **Modular design** – easily extend with new queries or themes
- 🛡️ **Graceful error handling** – falls back cleanly when the API is unavailable

---

## Project Structure

```
loven/
├── notebooks/
│   └── Lovdata_Peace_Analysis.ipynb   # Main analysis notebook
├── docs/
│   ├── notebook_guide.md              # Step-by-step notebook walkthrough
│   ├── api_reference.md               # Class & function reference
│   └── contributing.md               # Contribution guidelines
├── LICENSE                            # CC0 1.0 Universal
└── README.md                          # This file
```

---

## Requirements

- Python **3.10** or higher
- [Jupyter](https://jupyter.org/) (classic Notebook or JupyterLab)
- The following Python packages:

| Package | Purpose |
|---|---|
| `requests` | Synchronous HTTP calls to the Lovdata API |
| `pandas` | Tabular data analysis |
| `aiohttp` | Asynchronous HTTP calls (for `AsyncLovDataClient`) |
| `nest_asyncio` | Allows `asyncio` event loops inside Jupyter notebooks |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GizzZmo/loven.git
cd loven
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install requests pandas jupyter aiohttp nest_asyncio
```

---

## Quick Start

```bash
# Start Jupyter
jupyter notebook notebooks/Lovdata_Peace_Analysis.ipynb
```

Run the cells in order (Cell 1 → Cell 4). Results are displayed as Pandas DataFrames inside the notebook.

---

## Usage

### Running the full analysis

Open the notebook and run all cells sequentially:

1. **Cell 1** – Import libraries and set constants (`BASE_URL`, `PEACE_THEMES`)
2. **Cell 2** – Define the `LovDataClient` class
3. **Cell 3** – Define the `analyze_peace_laws()` function
4. **Cell 4** – Execute example queries and display results

### Adding your own queries

Edit **Cell 4** and extend the `queries` list:

```python
queries = [
    "selskapsloven oppløsning",   # Company dissolution law
    "vannressursloven",           # Water resources act
    "energilov miljø",            # Energy & environment
    "etikk Oljefondet",           # Ethics / Government Pension Fund
    "boliglov nabolag",           # Housing and neighbourhood law  ← add your own
]
```

### Adding new peace themes

Edit the `PEACE_THEMES` constant in **Cell 1**:

```python
PEACE_THEMES = ["energi", "vann", "miljø", "etikk", "selskap", "oppløsning", "fred", "bolig"]
```

### Async batch search

For large-scale analysis, use `AsyncLovDataClient` (add as **Cell 7** in the notebook). It fetches multiple queries in parallel using `asyncio` and `aiohttp`, which is significantly faster than sequential synchronous calls:

```python
# Cell 7: Async API search – non-blocking parallel fetching
import asyncio
import aiohttp
import nest_asyncio

nest_asyncio.apply()  # Required to run asyncio inside Jupyter

class AsyncLovDataClient(LovDataClient):
    """Async extension of LovDataClient for efficient batch fetching."""

    async def async_search(self, session: aiohttp.ClientSession, query: str, **filters) -> Dict:
        """Single async search – returns raw JSON."""
        params = {"q": query, "limit": filters.get("limit", 30)}
        if "doc_type" in filters:
            params["type"] = filters["doc_type"]
        if "department" in filters:
            params["departement"] = filters["department"]
        if "date_from" in filters:
            params["dato_fra"] = filters["date_from"]
        if "date_to" in filters:
            params["dato_til"] = filters["date_to"]

        url = f"{self.base_url}/sok"
        try:
            async with session.get(url, params=params, timeout=15) as resp:
                resp.raise_for_status()
                data = await resp.json()
                logger.info(f"Async search done for '{query}' – {len(data.get('hits', []))} hits.")
                return data
        except Exception as e:
            logger.error(f"Async search failed for '{query}': {e}")
            return {"error": str(e)}

    async def async_peace_batch_analysis(self, queries: List[str], **common_filters) -> pd.DataFrame:
        """Run all queries in parallel and return a combined DataFrame."""
        async with aiohttp.ClientSession() as session:
            tasks = [self.async_search(session, q, **common_filters) for q in queries]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        all_hits = []
        for q, result in zip(queries, results):
            if isinstance(result, dict) and "hits" in result:
                for hit in result["hits"]:
                    hit["query"] = q
                    hit["peace_relevance"] = sum(
                        1 for theme in PEACE_THEMES
                        if theme in str(hit.get("tittel", "")).lower()
                    )
                all_hits.extend(result["hits"])

        df = pd.DataFrame(all_hits)
        if not df.empty:
            df = df.sort_values(by="peace_relevance", ascending=False)
            df = df[["tittel", "url", "peace_relevance", "query"]]
        print(f"Async batch done! {len(queries)} queries → {len(df)} hits.")
        return df
```

**Cell 8 – example run:**

```python
client = AsyncLovDataClient()

peace_queries = [
    "selskapsloven oppløsning",
    "vannressursloven energilov",
    "miljø etikk Oljefondet",
    "kraftforbruk vannforsyning",
    "nabolag bolig miljø Eidsvoll",
]

df_batch = await client.async_peace_batch_analysis(peace_queries, limit=20)
display(df_batch.head(12))
```

**Benefits of the async approach:**

| Benefit | Description |
|---|---|
| Speed | All queries run concurrently instead of one-by-one |
| Scalability | Handles dozens or hundreds of queries without blocking |
| Readable | Fully typed, logged, and commented |

---

## Architecture

```
LovDataClient (synchronous)
│
├── __init__(base_url)          Sets up a requests.Session with JSON headers
│
├── search(query, limit=20)     GET /sok?q=<query>&limit=<limit>
│                               Returns raw JSON dict; logs errors gracefully
│
└── filter_peace_laws(data)     Filters hits by PEACE_THEMES keywords
                                Returns List[Dict]

AsyncLovDataClient (asynchronous, extends LovDataClient)
│
├── async_search(session, query, **filters)
│                               Single async GET with optional filters
│
└── async_peace_batch_analysis(queries, **common_filters)
                                Parallel batch search → sorted pd.DataFrame

analyze_peace_laws(client, query)
    ├── Calls client.search()
    ├── Calls client.filter_peace_laws()
    └── Returns pd.DataFrame with columns: tittel, url, relevans_for_fred
```

See [`docs/api_reference.md`](docs/api_reference.md) for full API documentation.

---

## Peace Themes

The default set of themes used to filter Lovdata results:

| Norwegian | English |
|---|---|
| energi | energy |
| vann | water |
| miljø | environment |
| etikk | ethics |
| selskap | company / corporation |
| oppløsning | dissolution |
| fred | peace |

---

## Documentation

| Document | Description |
|---|---|
| [docs/notebook_guide.md](docs/notebook_guide.md) | Detailed walkthrough of every notebook cell |
| [docs/api_reference.md](docs/api_reference.md) | Full reference for `LovDataClient`, `AsyncLovDataClient`, and `analyze_peace_laws` |
| [docs/contributing.md](docs/contributing.md) | How to contribute queries, themes, and code |

---

## Credits & Data Sources

- **Data source:** [Lovdata.no](https://lovdata.no) (Stiftelsen Lovdata) – only publicly available data is used.
- **Authors:** Verdens Øverste Leder, Jon-Arve Constantine, and the Styrilia 49 community.
- This project is created for Jon-Arve Constantine, Merete Johnsen, and everyone who wants to save the world — one piece of legislation at a time.

---

## License

This project is released under the [CC0 1.0 Universal](LICENSE) public domain dedication.  
You are free to copy, modify, distribute, and use the work — even for commercial purposes — without asking permission.
