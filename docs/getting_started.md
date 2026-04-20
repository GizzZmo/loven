# Getting Started

This guide covers installation and your first query in three ways: as a Jupyter notebook, as a Python library, and as a command-line tool.

---

## Requirements

- Python **3.10** or higher
- Internet access to reach `api.lovdata.no`

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
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. Install the package

```bash
# Core library + CLI
pip install -e .

# Core + Jupyter notebook support
pip install -e ".[notebook]"

# Core + development tools (tests, linting)
pip install -e ".[dev]"
```

---

## Option A – Jupyter Notebook

```bash
jupyter notebook notebooks/Lovdata_Peace_Analysis.ipynb
```

Run the cells in order (Cell 1 → Cell 6). Results are displayed as Pandas DataFrames inside the notebook.

See the [Notebook Guide](notebook_guide.md) for a detailed walkthrough of every cell.

---

## Option B – Python Library

```python
from loven import LovDataClient, analyze_peace_laws

client = LovDataClient()
df = analyze_peace_laws(client, "energilov miljø", limit=20)
print(df[["tittel", "tema_treff"]])
```

**Async batch search:**

```python
import asyncio
from loven import AsyncLovDataClient

async def main():
    client = AsyncLovDataClient()
    df = await client.async_peace_batch_analysis(
        ["energilov", "vannressursloven", "miljøvern"],
        limit=20,
    )
    print(df)

asyncio.run(main())
```

See the [API Reference](api_reference.md) for the full interface.

---

## Option C – Command Line

```bash
# Search and print results
loven search "energilov miljø"

# Search with custom result limit
loven search "vannressursloven" --limit 10

# Export results to CSV
loven export "miljøvern" --output results.csv

# Export to Excel
loven export "etikk Oljefondet" --output results.xlsx

# List current peace themes
loven themes list
```

See the [CLI Reference](cli_reference.md) for all options.

---

## Offline / Testing

The repository ships with `sample_data/mock_lovdata_response.json` — a local snapshot of a Lovdata API response. You can point the client at any URL, including a local mock server, by passing `base_url`:

```python
from loven import LovDataClient

# Use a local test server or custom mirror
client = LovDataClient(base_url="http://localhost:8000")
```
