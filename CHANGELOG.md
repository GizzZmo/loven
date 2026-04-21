# Changelog

All notable changes to **loven** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.0.0] – 2026-04-20

### Added
- **PyPI-ready package** – `pyproject.toml` classifiers and metadata polished for `pip install loven`.
- **Multilingual docs** – English translation of the notebook guide (`docs/notebook_guide_en.md`).
- **GitHub issue templates** – bug report and feature request templates in `.github/ISSUE_TEMPLATE/`.
- **Code of Conduct** – `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1).
- **CHANGELOG** – this file, following Keep a Changelog format.

---

## [0.4.0] – 2026-04-20

### Added
- **`loven.cache`** – `DiskCache` class: JSON-based disk cache with configurable TTL for API responses.
- **`loven.export`** – `export()`, `to_csv()`, `to_excel()`, `to_markdown()` helpers.
- **`loven.viz`** – `bar_chart()` and `word_cloud()` visualisation helpers (requires `loven[viz]`).
- **`loven.nlp`** – `expand_themes()` synonym expansion with built-in Norwegian synonym map;
  `expand_themes_spacy()` for spaCy-powered lemma expansion (requires `loven[nlp]`).
- **`LovDataClient(cache=…)`** – optional `DiskCache` integration; cached results avoid redundant network calls.
- **Optional dependency groups** in `pyproject.toml`: `viz`, `nlp`, `all`.
- **Streamlit dashboard** (`app/streamlit_app.py`) with search box, results table, theme filter,
  visualisation panel, and CSV/Markdown download.
- **Docker support** – `Dockerfile` (multi-stage) and `docker-compose.yml` for one-command setup.
- **Deployment guide** (`docs/deployment.md`) for local, Docker, Render, Railway, and VPS.
- 34 new tests (total: 59 passing).

### Changed
- `__version__` bumped to `0.4.0`.
- `__init__.py` public API expanded to include cache, export, and NLP symbols.

---

## [0.3.0] – 2026-04-19

### Added
- **`loven.cli`** – `argparse`-based CLI with `search`, `export`, and `themes list` sub-commands.
- **CLI entry point** registered in `pyproject.toml` (`loven = "loven.cli:main"`).
- **`docs/cli_reference.md`** – full CLI usage guide.

---

## [0.2.0] – 2026-04-18

### Added
- **`tests/`** directory with `pytest` suite: `test_themes.py`, `test_client.py`, `test_analysis.py`.
- **GitHub Actions CI** (`.github/workflows/ci.yml`) – tests on Python 3.10/3.11/3.12, lint with `ruff`.
- **`pytest-cov`** coverage reporting in CI.
- `conftest.py` with shared fixtures.

---

## [0.1.0] – 2026-04-17

### Added
- `src/loven/` Python package: `themes.py`, `client.py`, `analysis.py`, `__init__.py`.
- `LovDataClient` (synchronous) and `AsyncLovDataClient` (asynchronous) API wrappers.
- `analyze_peace_laws()` and `batch_analyze()` high-level analysis functions.
- `PEACE_THEMES` keyword list with `matches_theme()` and `count_themes()` utilities.
- `sample_data/mock_lovdata_response.json` for offline development.
- `pyproject.toml` package metadata and build configuration.
- Jupyter notebook updated to import from `src/loven` and with async cells.
- Documentation: `docs/api_reference.md`, `docs/notebook_guide.md`, `docs/getting_started.md`,
  `docs/contributing.md`.

[Unreleased]: https://github.com/GizzZmo/loven/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/GizzZmo/loven/compare/v0.4.0...v1.0.0
[0.4.0]: https://github.com/GizzZmo/loven/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/GizzZmo/loven/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/GizzZmo/loven/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/GizzZmo/loven/releases/tag/v0.1.0
