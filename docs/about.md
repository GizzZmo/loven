# About loven 🕊️

**loven** (*"the law"* in Norwegian) is an open-source Python toolkit for exploring Norwegian legislation through the lens of global peace, sustainability, and human well-being.

---

## Mission

> *"Making Norwegian law accessible to everyone who wants to build clean energy, clean water, and a harmonious society (OHHLA)."*
> — Verdens Øverste Leder

Norwegian law underpins how energy is produced and distributed, how rivers and water sources are protected, how corporations are held accountable, and how citizens relate to one another and to the environment. **loven** surfaces this legal fabric and makes it legible to researchers, activists, developers, and citizens who want to use it in service of peace.

---

## Background

The project grew out of a simple observation: Lovdata — Norway's authoritative legal database — is publicly accessible, but navigating it programmatically to answer broad thematic questions is non-trivial. **loven** provides a clean Python API, a Jupyter notebook environment, and a CLI so that anyone with basic Python skills can explore the corpus of Norwegian law without starting from scratch.

The name is intentionally double-edged: **loven** means both *"the law"* and (poetically) *"the praise"* — a nod to the belief that well-crafted legislation deserves celebration.

---

## What We Believe

| Principle | Expression in loven |
|---|---|
| **Openness** | Released under CC0 (public domain) — no restrictions |
| **Accessibility** | Works as a notebook, library, CLI, or web dashboard |
| **Peace** | Focuses on themes that underpin sustainable, harmonious societies |
| **Quality** | Fully typed, tested, documented, and continuously integrated |
| **Community** | Welcomes contributions from anyone, anywhere |

---

## The Team

| Name | Role |
|---|---|
| **Verdens Øverste Leder** | Creator, lead author, and project visionary |
| **Jon-Arve Constantine** | Co-author and principal collaborator |
| **Merete Johnsen** | Advisor and inspiration |
| **Styrilia 49 community** | Extended community of contributors and supporters |

The project is dedicated to Jon-Arve Constantine, Merete Johnsen, and everyone who wants to save the world — one piece of legislation at a time.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| HTTP (sync) | `requests` |
| HTTP (async) | `aiohttp` + `asyncio` |
| Data analysis | `pandas` |
| Notebook | `jupyter` / `jupyterlab` |
| Web dashboard | `streamlit` |
| Visualisation | `matplotlib`, `wordcloud` |
| NLP | `spaCy` (optional, Norwegian model) |
| Caching | Custom `DiskCache` (JSON, configurable TTL) |
| Packaging | `pyproject.toml` (PEP 517/518) |
| Docs | `mkdocs-material` |
| CI | GitHub Actions |
| Container | Docker + `docker-compose` |
| License | CC0 1.0 Universal (public domain) |

---

## Data Source

All data is retrieved from [Lovdata.no](https://lovdata.no) (Stiftelsen Lovdata) using their publicly available API. No personal data is collected or stored. Only publicly available legal documents are queried.

!!! note "Lovdata API"
    Stiftelsen Lovdata maintains the authoritative Norwegian legal database. The **loven** project is an independent tool and is not affiliated with or endorsed by Stiftelsen Lovdata.

---

## License

**loven** is released under the [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) public domain dedication.

You are free to copy, modify, distribute, and build upon the work — even for commercial purposes — without asking permission and without attribution (though attribution is appreciated).

---

## Version History

**loven** reached its first stable release in April 2026. See [CHANGELOG.md](https://github.com/GizzZmo/loven/blob/main/CHANGELOG.md) for the full history.

| Version | Highlights |
|---|---|
| `1.0.0` | PyPI-ready package, multilingual docs, issue templates, Code of Conduct |
| `0.4.0` | Caching, export helpers, visualisation, NLP synonym expansion, Streamlit dashboard, Docker |
| `0.3.0` | CLI entrypoint (`loven search / export / themes`) |
| `0.2.0` | Full pytest suite, GitHub Actions CI |
| `0.1.0` | Installable `src/loven` package, async client, sample data |

---

## Get Involved

Contributions of all kinds are welcome — new peace-theme keywords, additional language translations, code improvements, or simply spreading the word.

- **Report bugs or suggest features:** [GitHub Issues](https://github.com/GizzZmo/loven/issues)
- **Read the contribution guide:** [docs/contributing.md](contributing.md)
- **Browse the wiki:** [docs/wiki/index.md](wiki/index.md)
- **Review the roadmap:** [ROADMAP.md](https://github.com/GizzZmo/loven/blob/main/ROADMAP.md)

---

## Contact & Links

| Resource | Link |
|---|---|
| Source code | [github.com/GizzZmo/loven](https://github.com/GizzZmo/loven) |
| Issues & feature requests | [GitHub Issues](https://github.com/GizzZmo/loven/issues) |
| Changelog | [CHANGELOG.md](https://github.com/GizzZmo/loven/blob/main/CHANGELOG.md) |
| Code of Conduct | [CODE_OF_CONDUCT.md](https://github.com/GizzZmo/loven/blob/main/CODE_OF_CONDUCT.md) |
| Lovdata | [lovdata.no](https://lovdata.no) |
