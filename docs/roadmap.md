# Roadmap

This page mirrors [`ROADMAP.md`](https://github.com/GizzZmo/loven/blob/main/ROADMAP.md) in the repository root.

---

## Current State (April 2026)

- Single Jupyter notebook (`Lovdata_Peace_Analysis.ipynb`) with 6 cells
- `LovDataClient` (sync) + `AsyncLovDataClient` (async) in `src/loven/`
- `analyze_peace_laws()` and `batch_analyze()` helpers
- `loven` CLI with `search`, `export`, and `themes list` sub-commands
- 25-test pytest suite with mocked HTTP
- GitHub Actions CI (Python 3.10 / 3.11 / 3.12)
- GitHub Pages documentation site

---

## Phase 1 – Foundation ✅ *(complete)*

- [x] `requirements.txt` – pinned dependencies
- [x] `src/loven/` Python package (`themes`, `client`, `analysis`, `cli`)
- [x] `pyproject.toml` – installable package with extras
- [x] `sample_data/` – mock JSON for offline testing
- [x] Notebook updated to import from the package; async cells added
- [x] GitHub Pages documentation site (MkDocs Material)

---

## Phase 2 – Testing & Quality ✅ *(complete)*

- [x] `tests/` with pytest suite (25 tests)
- [x] GitHub Actions CI workflow
- [x] `ruff` linting

---

## Phase 3 – CLI Entrypoint ✅ *(complete)*

- [x] `loven search <query>`
- [x] `loven export <query> --output file.csv`
- [x] `loven themes list`

---

## Phase 4 – Advanced Features

- [ ] **Local caching** – cache API responses to disk (JSON/SQLite)
- [ ] **Export to Excel** – `openpyxl` integration
- [ ] **Data visualisation** – bar charts and word clouds in notebook
- [ ] **Expanded themes** – `naturvern`, `havrett`, `bærekraft`
- [ ] **Norwegian NLP** – keyword synonym expansion with `spacy` (Norwegian model)

---

## Phase 5 – Web Interface

- [ ] **Streamlit dashboard** – search box, results table, theme filter sidebar
- [ ] **Docker** – `Dockerfile` + `docker-compose.yml`
- [ ] **Deployment guide** – Render, Railway, or VPS

---

## Phase 6 – Community & Publishing

- [ ] **PyPI package** – `pip install loven`
- [ ] **English summaries** – auto-translate Norwegian law titles
- [ ] **Multilingual docs** – English translation of notebook guide
- [ ] **Changelog** – `CHANGELOG.md` (Keep a Changelog format)

---

## Version Milestones

| Version | Phase | Description |
|---|---|---|
| `0.1.0` | Phase 1–3 | Installable package, async support, CLI, docs site |
| `0.2.0` | Phase 4 | Caching, scoring, visualisation |
| `0.3.0` | Phase 5 | Streamlit dashboard, Docker |
| `1.0.0` | Phase 6 | PyPI release, multilingual, stable API |
