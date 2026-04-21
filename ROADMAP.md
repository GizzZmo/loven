# Loven 🕊️ – Development Roadmap

> *Making Norwegian law accessible to everyone who wants to build clean energy, clean water, and a harmonious society.*

This roadmap outlines the planned development of **loven** from its current notebook-based prototype into a well-structured, testable, and extensible Python toolkit.

---

## Current State (April 2026)

- Single Jupyter notebook (`Lovdata_Peace_Analysis.ipynb`) with 4 cells
- Synchronous `LovDataClient` class and `analyze_peace_laws()` function
- Documentation in `docs/` (API reference, notebook guide, contributing guide)
- No package structure, tests, or CI

---

## Phase 1 – Foundation ✅ *(in progress)*

**Goal:** Turn the notebook prototype into a proper, installable Python package.

- [x] `requirements.txt` – pin all dependencies for reproducible installs
- [x] `src/loven/` Python package
  - [x] `themes.py` – `PEACE_THEMES` constant and theme utilities
  - [x] `client.py` – `LovDataClient` + `AsyncLovDataClient` classes
  - [x] `analysis.py` – `analyze_peace_laws()` and DataFrame helpers
  - [x] `__init__.py` – public API surface
- [x] `pyproject.toml` – package metadata and build config
- [x] `sample_data/` – local mock JSON for offline development and testing
- [x] Notebook updated to import from `src/loven` instead of defining classes inline
- [x] Async cells added to notebook (Cells 7–8)

---

## Phase 2 – Testing & Quality ✅

**Goal:** Ensure correctness and enable safe contributions.

- [x] `tests/` directory with `pytest` suite
  - [x] `test_themes.py` – unit tests for theme filtering utilities
  - [x] `test_client.py` – tests for `LovDataClient` (mocked HTTP)
  - [x] `test_analysis.py` – tests for `analyze_peace_laws()` with sample data
- [x] GitHub Actions CI workflow (`.github/workflows/ci.yml`)
  - [x] Runs tests on every push / PR
  - [x] Linting with `ruff` or `flake8`
- [x] `pytest-cov` coverage reporting

---

## Phase 3 – CLI Entrypoint ✅

**Goal:** Allow users to query Lovdata from the terminal without Jupyter.

- [x] `src/loven/cli.py` – `argparse`-based CLI
  - [x] `loven search <query>` – prints a table of results
  - [x] `loven export <query> --output results.csv` – saves to CSV
  - [x] `loven themes list` – shows all current peace themes
- [x] Entry point registered in `pyproject.toml`
- [x] `docs/cli_reference.md` – CLI usage guide

---

## Phase 4 – Advanced Features ✅

**Goal:** Richer analysis, caching, and visualisation.

- [x] **Local caching** – `src/loven/cache.py` – `DiskCache` (JSON, configurable TTL)
- [x] **Export** – `src/loven/export.py` – CSV, Excel, and Markdown via `export()`
- [x] **Relevance scoring** – `count_themes()` scores each law by matching peace themes
- [x] **Data visualisation** – `src/loven/viz.py` – `bar_chart()` and `word_cloud()`
  - Tools: `matplotlib`, `wordcloud` (optional extras: `pip install 'loven[viz]'`)
- [x] **Expanded themes** – `klima`, `bolig`, `arbeidsmiljø` added to `PEACE_THEMES`
- [x] **Norwegian NLP** – `src/loven/nlp.py` – `expand_themes()` with built-in synonym map;
  `expand_themes_spacy()` for spaCy-powered expansion (optional: `pip install 'loven[nlp]'`)

---

## Phase 5 – Web Interface ✅

**Goal:** Make the toolkit accessible to non-programmers via a browser.

- [x] **Streamlit dashboard** (`app/streamlit_app.py`)
  - Search box, results table, theme filter sidebar
  - Visualisation panel, CSV/Markdown download
- [x] **Docker** – `Dockerfile` (multi-stage) and `docker-compose.yml` for one-command setup
- [x] **Deployment guide** – `docs/deployment.md` covering local, Docker, Render, Railway, VPS

---

## Phase 6 – Community & Publishing ✅

**Goal:** Open the project to broader contribution and use.

- [x] **PyPI package** – `pyproject.toml` metadata and classifiers ready for `pip install loven`
- [x] **Multilingual docs** – English translation of the notebook guide (`docs/notebook_guide_en.md`)
- [x] **Issue templates** – `.github/ISSUE_TEMPLATE/` bug report and feature request templates
- [x] **Changelog** – `CHANGELOG.md` following Keep a Changelog format
- [x] **Code of Conduct** – `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1)

---

## Version Milestones

| Version | Phase | Description |
|---|---|---|
| `0.1.0` | Phase 1 | Installable package, async support, sample data |
| `0.2.0` | Phase 2 | Full test suite, CI/CD |
| `0.3.0` | Phase 3 | CLI entrypoint |
| `0.4.0` | Phase 4 | Caching, scoring, visualisation |
| `0.5.0` | Phase 5 | Streamlit dashboard, Docker |
| `1.0.0` | Phase 6 | PyPI release, multilingual, stable API |

---

*This roadmap is a living document. Priorities may shift as community feedback is received.*
