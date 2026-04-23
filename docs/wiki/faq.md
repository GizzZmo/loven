# Frequently Asked Questions

---

## General

### What is loven?

**loven** is an open-source Python toolkit for searching and analysing Norwegian legislation via the public [Lovdata](https://lovdata.no) API. It focuses on laws related to peace, sustainability, energy, water, and ethics.

See the [About](../about.md) page for the full background.

---

### Is this an official Lovdata product?

No. **loven** is an independent community project and is not affiliated with or endorsed by Stiftelsen Lovdata.

---

### What data does loven use?

Only publicly available data from the Lovdata API — the same data you can browse on lovdata.no. No authentication is required, no personal data is collected, and no data is stored beyond the optional local disk cache.

---

### Is loven free to use?

Yes. The entire project is released under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) public domain dedication. You can copy, modify, distribute, and use it for any purpose — including commercial purposes — without asking for permission.

---

## Installation

### Which Python versions are supported?

Python **3.10, 3.11, and 3.12**. The GitHub Actions CI runs tests against all three.

---

### I get an ImportError for `loven`. How do I fix it?

Make sure you have installed the package in development mode from the repository root:

```bash
pip install -e .
```

If you are using a virtual environment, make sure it is activated before running `pip install`.

---

### What extras are available?

```bash
pip install -e ".[notebook]"   # Jupyter support
pip install -e ".[viz]"        # matplotlib + wordcloud charts
pip install -e ".[nlp]"        # spaCy Norwegian NLP model
pip install -e ".[dev]"        # pytest, ruff, coverage (for contributors)
pip install -e ".[all]"        # everything above
```

---

## Usage

### The Lovdata API is unreachable. What happens?

`LovDataClient.search()` catches all network exceptions and returns `{"error": "<message>"}` instead of raising. `analyze_peace_laws()` detects this and returns an empty DataFrame. The error is logged at `ERROR` level.

For offline development, point the client at a local mock server or use the bundled `sample_data/mock_lovdata_response.json`:

```python
import json, pathlib
from loven import LovDataClient

# Patch the client to return local data
client = LovDataClient()
mock_path = pathlib.Path("sample_data/mock_lovdata_response.json")
mock_data = json.loads(mock_path.read_text())
client.search = lambda query, **kw: mock_data
```

---

### How do I search for laws in a specific category?

Use keyword combinations. Lovdata's search is a full-text search over Norwegian law. For example:

```python
from loven import LovDataClient, analyze_peace_laws

client = LovDataClient()
df = analyze_peace_laws(client, "energilov fornybar kraft", limit=30)
```

You can also use the CLI:

```bash
loven search "energilov fornybar kraft" --limit 30
```

---

### How do I run multiple queries at once?

Use `batch_analyze()`:

```python
from loven import LovDataClient, batch_analyze

client = LovDataClient()
queries = ["energilov", "vannressursloven", "klimamål"]
df = batch_analyze(client, queries, limit=20)
print(df.sort_values("tema_treff", ascending=False))
```

Or use the async client for parallel fetching:

```python
import asyncio
from loven import AsyncLovDataClient

async def run():
    client = AsyncLovDataClient()
    df = await client.async_peace_batch_analysis(
        ["energilov", "vannressursloven", "klimamål"],
        limit=20,
    )
    print(df)

asyncio.run(run())
```

---

### How do I export results?

**CSV (CLI):**
```bash
loven export "energilov" --output results.csv
```

**Excel (CLI):**
```bash
loven export "energilov" --output results.xlsx
```

**Python:**
```python
from loven import LovDataClient, analyze_peace_laws, export

client = LovDataClient()
df = analyze_peace_laws(client, "energilov")
export(df, "results.csv")
export(df, "results.xlsx")
export(df, "results.md")
```

---

### How does the disk cache work?

When the cache is enabled (default in the Streamlit dashboard), search results are saved to `~/.loven_cache/` as JSON files keyed by a hash of the request parameters. Results are considered fresh for `ttl` seconds (default: 3600). Stale entries are re-fetched automatically.

Clear the cache from Python:

```python
from loven.cache import DiskCache
n = DiskCache().clear()
print(f"Cleared {n} entries.")
```

Or from the Streamlit sidebar, click **Clear cache**.

---

## Contributing

### How do I add a new peace theme keyword?

See the [Peace Themes wiki page](peace-themes.md#adding-new-themes) for a step-by-step guide.

---

### How do I run the tests?

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

---

### How do I lint the code?

```bash
ruff check src/ tests/
```

---

### Where do I report bugs or request features?

Open an issue on [GitHub](https://github.com/GizzZmo/loven/issues). Please include:

- Your Python version and OS
- The exact command or code you ran
- The full error message and traceback
- Any relevant output

---

## Advanced

### Can I use loven with a custom Lovdata mirror or proxy?

Yes. Pass `base_url` to `LovDataClient`:

```python
from loven import LovDataClient

client = LovDataClient(base_url="https://my-mirror.example.com")
```

---

### How do I use spaCy for synonym expansion?

Install the optional NLP extras and the Norwegian model:

```bash
pip install -e ".[nlp]"
python -m spacy download nb_core_news_sm
```

Then use `expand_themes_spacy`:

```python
import spacy
from loven.nlp import expand_themes_spacy

nlp = spacy.load("nb_core_news_sm")
expanded = expand_themes_spacy(["energi", "vann"], nlp)
```

---

### How do I run the Streamlit dashboard locally?

```bash
pip install -e ".[viz]"
streamlit run app/streamlit_app.py
```

Or with Docker:

```bash
docker compose up
```

See [deployment.md](../deployment.md) for production deployment options.
