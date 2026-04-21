# Notebook Guide (English)

This guide explains how to use the **loven** Jupyter notebook to explore Norwegian law with a focus on peace, energy, water, and environment themes.

---

## Prerequisites

Install loven and Jupyter:

```bash
pip install -e ".[notebook]"
```

---

## Opening the Notebook

```bash
jupyter lab
```

Then open `notebooks/Lovdata_Peace_Analysis.ipynb` from the file browser.

---

## Running the Cells

### Cell 1 – Imports

Imports the `loven` package and sets up logging.

```python
from loven import LovDataClient, analyze_peace_laws, PEACE_THEMES
```

### Cell 2 – Create the Client

Creates a synchronous API client pointing at the Lovdata REST API.
Pass `cache=DiskCache()` to enable on-disk response caching.

```python
from loven.cache import DiskCache
client = LovDataClient(cache=DiskCache())
```

### Cell 3 – Analyse Peace Laws

Runs a search query, filters results by peace themes, and returns a DataFrame.

```python
df = analyze_peace_laws(client, "energilov miljoe", limit=20)
df.head()
```

The DataFrame columns are:

| Column | Description |
|---|---|
| `tittel` | Norwegian law title |
| `url` | Link to the Lovdata document |
| `dato` | Publication date |
| `dokumenttype` | Document type (e.g. `lov`, `forskrift`) |
| `relevans_for_fred` | `True` if at least one peace theme matches |
| `tema_treff` | Number of matching peace themes |

### Cell 4 – Display Results

```python
with pd.option_context("display.max_colwidth", 80):
    display(df[["tittel", "tema_treff", "url"]])
```

---

## Async Batch Analysis (Cells 7–8)

Run multiple queries in parallel for faster results:

```python
import asyncio, nest_asyncio
nest_asyncio.apply()

from loven import AsyncLovDataClient

async_client = AsyncLovDataClient()
queries = ["energilov", "vannressursloven", "klimamaal", "miljoevern"]
df_batch = asyncio.run(async_client.async_peace_batch_analysis(queries, limit=10))
df_batch.head(20)
```

---

## Exporting Results

```python
from loven.export import export
export(df, "results.csv")          # CSV
export(df, "results.xlsx")         # Excel
export(df, "results.md")           # Markdown table
```

---

## Visualisation

```python
from loven.viz import bar_chart, word_cloud, save_figure
fig = bar_chart(df)
save_figure(fig, "chart.png")
```

> **Note:** Install visualisation extras first: `pip install 'loven[viz]'`
