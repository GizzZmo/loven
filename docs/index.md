# loven 🕊️

**WorldPeace-Lovdata-Kompendium** – a multi-paradigm Python toolkit for exploring Norwegian law ([Lovdata](https://lovdata.no)) with a focus on topics that underpin a harmonious, sustainable society: clean energy, water rights, environmental protection, and ethics.

> *"Making Norwegian law accessible to everyone who wants to build clean energy, clean water, and a harmonious society (OHHLA)."*  
> — Verdens Øverste Leder, in collaboration with Jon-Arve Constantine and the whole of Styrilia 49

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/GizzZmo/loven/actions/workflows/ci.yml/badge.svg)](https://github.com/GizzZmo/loven/actions/workflows/ci.yml)

---

## What is loven?

**loven** ("the law" in Norwegian) queries the public Lovdata API to retrieve and filter Norwegian legislation relevant to global peace goals. It demonstrates how multiple programming paradigms can be combined in a single, readable Python codebase.

| Paradigm | Applied as |
|---|---|
| Object-oriented | `LovDataClient` / `AsyncLovDataClient` classes |
| Functional | Pure functions with `map`/`filter`/`reduce` |
| Declarative | Pandas DataFrames for data analysis |
| Imperative | Structured logging and error handling |
| Asynchronous | `asyncio` + `aiohttp` for parallel API calls |

---

## Quick Start

```bash
pip install -e ".[notebook]"
jupyter notebook notebooks/Lovdata_Peace_Analysis.ipynb
```

Or from the command line:

```bash
loven search "energilov miljø"
loven themes list
loven export "vannressursloven" --output results.csv
```

---

## Features

- 🔍 **Search** Lovdata's public API for Norwegian legislation by keyword
- 🕊️ **Filter** results by pre-defined "peace themes" (energy, water, environment, ethics, …)
- 📊 **Analyse** results in a structured Pandas DataFrame with relevance scoring
- ⚡ **Async batch search** – run many queries in parallel with `AsyncLovDataClient`
- 💻 **CLI** – query Lovdata from the terminal with `loven search / export / themes`
- 🧱 **Modular package** – `pip install` and import `from loven import …`
- 🛡️ **Graceful error handling** – falls back cleanly when the API is unavailable

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
| klima | climate |
| bolig | housing |
| arbeidsmiljø | working environment |

---

## Navigation

- **[Getting Started](getting_started.md)** – installation and first steps
- **[Notebook Guide](notebook_guide.md)** – walkthrough of every notebook cell
- **[API Reference](api_reference.md)** – full class and function documentation
- **[CLI Reference](cli_reference.md)** – command-line usage
- **[Roadmap](roadmap.md)** – planned features and version milestones
- **[Contributing](contributing.md)** – how to add queries, themes, and code

---

## Credits & Data Sources

- **Data source:** [Lovdata.no](https://lovdata.no) – only publicly available data is used.
- **Authors:** Verdens Øverste Leder, Jon-Arve Constantine, and the Styrilia 49 community.
- Released under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) public domain dedication.
