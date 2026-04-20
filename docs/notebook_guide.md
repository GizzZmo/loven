# Notebook Guide – Lovdata_Peace_Analysis.ipynb

This guide walks through every cell of the notebook in detail.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Opening the Notebook](#opening-the-notebook)
- [Cell 1 – Imports and Setup](#cell-1--imports-and-setup)
- [Cell 2 – LovDataClient Class](#cell-2--lovdataclient-class)
- [Cell 3 – analyze_peace_laws Function](#cell-3--analyze_peace_laws-function)
- [Cell 4 – Example Queries](#cell-4--example-queries)
- [Understanding the Output](#understanding-the-output)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before opening the notebook, ensure you have installed all required packages:

```bash
pip install requests pandas jupyter
```

See [Getting Started](getting_started.md) for the full installation guide.

---

## Opening the Notebook

```bash
cd loven
jupyter notebook notebooks/Lovdata_Peace_Analysis.ipynb
```

Or with JupyterLab:

```bash
jupyter lab notebooks/Lovdata_Peace_Analysis.ipynb
```

Always run cells **in order** (top to bottom). Later cells depend on definitions made in earlier ones.

---

## Cell 1 – Imports and Setup

```python
import requests
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.lovdata.no"
PEACE_THEMES = ["energi", "vann", "miljø", "etikk", "selskap", "oppløsning", "fred"]
```

### What it does

| Line | Purpose |
|---|---|
| `import requests` | Makes HTTP calls to the Lovdata REST API |
| `import pandas as pd` | Stores and displays results as structured tables |
| `import logging` | Produces informational and error messages during execution |
| `logging.basicConfig(level=logging.INFO)` | Configures logs to be printed at INFO level and above |
| `BASE_URL` | Root URL for all Lovdata API requests |
| `PEACE_THEMES` | Keyword list used to filter search results |

### Customisation

- Add keywords to `PEACE_THEMES` to broaden the filter (e.g., `"bolig"` for housing, `"klima"` for climate).
- Change `level=logging.INFO` to `logging.DEBUG` for more verbose output during development.

---

## Cell 2 – LovDataClient Class

```python
class LovDataClient:
    def __init__(self, base_url: str = BASE_URL): ...
    def search(self, query: str, limit: int = 20) -> Dict: ...
    def filter_peace_laws(self, data: Dict) -> List[Dict]: ...
```

### What it does

`LovDataClient` is an **object-oriented wrapper** around the Lovdata public API.

#### `__init__(base_url)`

- Creates a persistent `requests.Session` (connection reuse, shared headers).
- Sets the `Accept: application/json` header so the API returns JSON.
- Logs an INFO message confirming initialisation.

#### `search(query, limit=20)`

- Constructs the URL: `GET https://api.lovdata.no/sok?q=<query>&limit=<limit>`
- Returns a `dict` with a `"hits"` key containing a list of matching laws.
- On any exception (network error, non-200 status), logs the error and returns `{"error": "..."}`.

> **Note:** The Lovdata API may require authentication for some endpoints. If you receive 401/403 errors, check [Lovdata Developer documentation](https://lovdata.no) for API key requirements.

#### `filter_peace_laws(data)`

- Accepts the raw dict from `search()`.
- Uses a **list comprehension** (functional style) to keep only hits whose `"tittel"` (title) contains at least one `PEACE_THEMES` keyword.
- Returns a `List[Dict]`.

### Example

```python
client = LovDataClient()
raw = client.search("vannressursloven", limit=5)
filtered = client.filter_peace_laws(raw)
print(filtered)
```

---

## Cell 3 – analyze_peace_laws Function

```python
def analyze_peace_laws(client: LovDataClient, query: str) -> pd.DataFrame:
    raw_data = client.search(query)
    peace_hits = client.filter_peace_laws(raw_data)
    df = pd.DataFrame([{
        "tittel": hit.get("tittel"),
        "url": hit.get("url"),
        "relevans_for_fred": any(theme in str(hit.get("tittel", "")).lower()
                                 for theme in PEACE_THEMES)
    } for hit in peace_hits])
    print(f"Analysert {len(df)} lover relatert til Global Peace Agreement.")
    return df
```

### What it does

This **top-level function** orchestrates the full pipeline:

1. Calls `client.search(query)` to retrieve raw hits.
2. Calls `client.filter_peace_laws(raw_data)` to narrow to peace-relevant laws.
3. Builds a Pandas `DataFrame` with three columns:

| Column | Type | Description |
|---|---|---|
| `tittel` | `str` | Norwegian title of the legal document |
| `url` | `str` | Direct link to the document on Lovdata |
| `relevans_for_fred` | `bool` | Whether the title matches a peace theme |

4. Prints a summary count and returns the DataFrame.

### Extending the DataFrame

To add more columns (e.g., publication date or document type), update the dict comprehension:

```python
df = pd.DataFrame([{
    "tittel": hit.get("tittel"),
    "url": hit.get("url"),
    "dato": hit.get("dato"),           # publication date if available
    "type": hit.get("dokumenttype"),   # document type if available
    "relevans_for_fred": any(theme in str(hit.get("tittel", "")).lower()
                             for theme in PEACE_THEMES)
} for hit in peace_hits])
```

---

## Cell 4 – Example Queries

```python
client = LovDataClient()

queries = [
    "selskapsloven oppløsning",
    "vannressursloven",
    "energilov miljø",
    "etikk Oljefondet"
]

for q in queries:
    df = analyze_peace_laws(client, q)
    display(df.head())
```

### What it does

- Instantiates one `LovDataClient` (shared session across all queries).
- Iterates over a list of Norwegian legal search terms.
- For each query, displays the first few rows of the resulting DataFrame using `display()`.

### Adding your own queries

Replace or extend `queries` with any Norwegian legal term, for example:

```python
queries = [
    "boliglov nabolag",      # Housing and neighbourhood
    "klimaendring utslipp",  # Climate change emissions
    "barnehage oppvekst",    # Child care
    "arbeidsmiljø",          # Working environment
]
```

---

## Understanding the Output

A successful query produces a DataFrame like:

| tittel | url | relevans_for_fred |
|---|---|---|
| Lov om vannressurser (vannressursloven) | https://lovdata.no/... | True |
| Forskrift om drikkevann | https://lovdata.no/... | True |

- **tittel** – the official name of the Norwegian law or regulation.
- **url** – click to read the full text on lovdata.no.
- **relevans_for_fred** – `True` if the title contains a peace theme keyword.

If the API is unavailable, the DataFrame will be empty and you will see an error logged:

```
ERROR:__main__:API-feil: <error message>. Bruk lokal backup-data.
```

---

## Troubleshooting

| Problem | Likely cause | Solution |
|---|---|---|
| Empty DataFrame | API returned no results | Try a broader query or check Lovdata status |
| `401 Unauthorized` | API requires authentication | Check if an API key is needed |
| `ConnectionError` | No internet access | Verify network; consider using cached/local data |
| `ModuleNotFoundError` | Missing package | Run `pip install requests pandas` |
| `NameError: name 'display' is not defined` | Running outside Jupyter | Replace `display(df.head())` with `print(df.head())` |
