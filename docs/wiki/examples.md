# Examples

Extended code examples and real-world recipes for **loven**.

---

## Basic Search

```python
from loven import LovDataClient, analyze_peace_laws

client = LovDataClient()

# Search for energy laws
df = analyze_peace_laws(client, "energilov", limit=20)
print(df[["tittel", "tema_treff"]].head(10))
```

**Output (sample):**

```
                                    tittel  tema_treff
0          Lov om energiproduksjon (energiloven)       1
1   Lov om produksjon, omforming, overføring...       1
2               Lov om vassdrag og grunnvann        1
```

---

## Batch Analysis

Run multiple queries and combine results into a single ranked DataFrame:

```python
from loven import LovDataClient, batch_analyze

client = LovDataClient()

queries = [
    "energilov fornybar",
    "vannressursloven",
    "miljøvern klimamål",
    "etikk Oljefondet",
    "boliglov nabolag",
]

df = batch_analyze(client, queries, limit=20)

# Sort by relevance score
df = df.sort_values("tema_treff", ascending=False)
print(df[["tittel", "tema_treff", "query"]].head(15))
```

---

## Async Batch Search

Fetch multiple queries in parallel for maximum throughput:

```python
import asyncio
from loven import AsyncLovDataClient

async def main():
    client = AsyncLovDataClient()
    df = await client.async_peace_batch_analysis(
        [
            "energilov fornybar kraft",
            "vannressursloven vassdrag",
            "miljøvern klimagass",
            "etikk varsling korrupsjon",
            "bolig husleie nabolag",
        ],
        limit=25,
    )
    print(f"Total results: {len(df)}")
    print(df[["tittel", "tema_treff"]].head(10))

asyncio.run(main())
```

---

## Filtering by a Custom Theme List

Override the default themes for a single call:

```python
from loven import LovDataClient, analyze_peace_laws

client = LovDataClient()
maritime_themes = ["hav", "sjø", "havrett", "fiske", "skipsfart"]

df = analyze_peace_laws(
    client,
    "havrett sjøfart",
    limit=30,
    themes=maritime_themes,
)
print(df)
```

---

## Synonym Expansion

Widen the search net using the built-in synonym map:

```python
from loven import LovDataClient, analyze_peace_laws
from loven.nlp import expand_themes

client = LovDataClient()

# Expand "energi" to include kraft, strøm, fornybar, vindkraft, ...
expanded = expand_themes(["energi", "klima"])
print("Expanded themes:", expanded)

df = analyze_peace_laws(client, "fornybar energi", themes=expanded)
print(df[["tittel", "tema_treff"]].head(10))
```

---

## Exporting Results

### To CSV

```python
from loven import LovDataClient, analyze_peace_laws, export

client = LovDataClient()
df = analyze_peace_laws(client, "miljøvern")
export(df, "miljøvern_results.csv")
```

### To Excel

```python
export(df, "miljøvern_results.xlsx")
```

### To Markdown

```python
export(df, "miljøvern_results.md")
```

### Using the CLI

```bash
loven export "miljøvern" --output miljøvern_results.csv
loven export "miljøvern" --output miljøvern_results.xlsx
```

---

## Visualisation

### Bar Chart

```python
import matplotlib.pyplot as plt
from loven import LovDataClient, analyze_peace_laws
from loven.viz import bar_chart

client = LovDataClient()
df = analyze_peace_laws(client, "energilov miljø", limit=30)

fig = bar_chart(df, top_n=15)
plt.tight_layout()
plt.savefig("top_laws.png", dpi=150)
plt.show()
```

### Word Cloud

```python
from loven.viz import word_cloud

fig = word_cloud(df)
plt.tight_layout()
plt.savefig("word_cloud.png", dpi=150)
plt.show()
```

---

## Caching

Enable disk caching to avoid redundant API calls during repeated analyses:

```python
from loven import LovDataClient, analyze_peace_laws
from loven.cache import DiskCache

cache = DiskCache(ttl=7200)  # cache for 2 hours
client = LovDataClient(cache=cache)

# First call hits the API
df1 = analyze_peace_laws(client, "energilov")
# Second call returns cached result instantly
df2 = analyze_peace_laws(client, "energilov")

# Clear the cache when needed
cache.clear()
```

---

## CLI Recipes

```bash
# Quick search, print table to terminal
loven search "energilov miljø"

# Search with more results
loven search "vannressursloven" --limit 50

# Save results to CSV
loven export "klimamål" --output klimamål.csv

# Save results to Excel
loven export "klimamål" --output klimamål.xlsx

# List all current peace themes
loven themes list
```

---

## Jupyter Notebook Workflow

The recommended way to run interactive analysis:

```python
# Cell 1 – imports
from loven import LovDataClient, analyze_peace_laws, batch_analyze, PEACE_THEMES
from loven.cache import DiskCache
import pandas as pd

pd.set_option("display.max_colwidth", 80)

# Cell 2 – create client with cache
cache = DiskCache()
client = LovDataClient(cache=cache)

# Cell 3 – single query
df = analyze_peace_laws(client, "energilov miljøvern", limit=20)
display(df.head(10))

# Cell 4 – batch query
queries = ["energilov", "vann", "klimamål", "etikk", "bolig"]
df_batch = batch_analyze(client, queries)
display(df_batch.sort_values("tema_treff", ascending=False).head(20))

# Cell 5 – visualise
from loven.viz import bar_chart
import matplotlib.pyplot as plt

fig = bar_chart(df_batch, top_n=12)
plt.tight_layout()
plt.show()
```

---

## Docker

Run the Streamlit dashboard with a single command:

```bash
docker compose up
# Open http://localhost:8501 in your browser
```

Build a standalone image:

```bash
docker build -t loven .
docker run -p 8501:8501 loven
```

---

## Running the Full Test Suite

```bash
pip install -e ".[dev]"
pytest tests/ -v --cov=src/loven --cov-report=term-missing
```

Expected output:

```
tests/test_analysis.py .....          [ 22%]
tests/test_cache.py ....              [ 38%]
tests/test_cli.py ......              [ 62%]
tests/test_client.py .....            [ 82%]
tests/test_export.py ....             [ 96%]
tests/test_themes.py ..               [100%]
25 passed in 1.8s
```
