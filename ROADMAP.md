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

## Phase 2 – Testing & Quality

**Goal:** Ensure correctness and enable safe contributions.

- [ ] `tests/` directory with `pytest` suite
  - [ ] `test_themes.py` – unit tests for theme filtering utilities
  - [ ] `test_client.py` – tests for `LovDataClient` (mocked HTTP)
  - [ ] `test_analysis.py` – tests for `analyze_peace_laws()` with sample data
- [ ] GitHub Actions CI workflow (`.github/workflows/ci.yml`)
  - [ ] Runs tests on every push / PR
  - [ ] Linting with `ruff` or `flake8`
- [ ] `pytest-cov` coverage reporting

---

## Phase 3 – CLI Entrypoint

**Goal:** Allow users to query Lovdata from the terminal without Jupyter.

- [ ] `src/loven/cli.py` – `argparse`-based CLI
  - [ ] `loven search <query>` – prints a table of results
  - [ ] `loven export <query> --output results.csv` – saves to CSV
  - [ ] `loven themes list` – shows all current peace themes
- [ ] Entry point registered in `pyproject.toml`
- [ ] `docs/cli_reference.md` – CLI usage guide

---

## Phase 4 – Advanced Features

**Goal:** Richer analysis, caching, and visualisation.

- [ ] **Local caching** – cache API responses to disk (JSON/SQLite) to avoid redundant calls
- [ ] **Export** – save DataFrames to CSV, Excel, and Markdown
- [ ] **Relevance scoring** – score each law by number of matching peace themes (not just a boolean)
- [ ] **Data visualisation** – notebook cells with bar charts and word clouds
  - Tools: `matplotlib`, `wordcloud`
- [ ] **Expanded themes** – add `klima` (climate), `bolig` (housing), `arbeidsmiljø` (work environment)
- [ ] **Norwegian NLP** – keyword synonym expansion using `spacy` (Norwegian model)

---

## Phase 5 – Web Interface

**Goal:** Make the toolkit accessible to non-programmers via a browser.

- [ ] **Streamlit dashboard** (`app/streamlit_app.py`)
  - Search box, results table, theme filter sidebar
  - Visualisation panel
- [ ] **Docker** – `Dockerfile` and `docker-compose.yml` for one-command setup
- [ ] **Deployment guide** – how to run on Render, Railway, or a VPS

---

## Phase 6 – Community & Publishing

**Goal:** Open the project to broader contribution and use.

- [ ] **PyPI package** – publish `loven` so users can `pip install loven`
- [ ] **English summaries** – auto-generate English summaries of Norwegian law titles
- [ ] **Multilingual docs** – English translation of the notebook guide
- [ ] **Issue templates** – GitHub issue templates for new queries and themes
- [ ] **Changelog** – `CHANGELOG.md` following Keep a Changelog format
- [ ] **Code of Conduct** – formal `CODE_OF_CONDUCT.md`

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
