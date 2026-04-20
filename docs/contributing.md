# Contributing

Thank you for your interest in contributing to **loven**! Every query, theme keyword, or code improvement that helps make Norwegian law more accessible is welcome.

---

## Table of Contents

- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Adding Peace Themes](#adding-peace-themes)
- [Adding Queries](#adding-queries)
- [Code Style](#code-style)
- [Submitting a Pull Request](#submitting-a-pull-request)
- [Code of Conduct](#code-of-conduct)

---

## Ways to Contribute

| Type | Examples |
|---|---|
| **New queries** | Add Norwegian legal terms relevant to sustainability, housing, or social justice |
| **New peace themes** | Expand the keyword list with new thematic areas |
| **Bug fixes** | Fix error handling, edge cases, or API compatibility |
| **Documentation** | Improve guides, add translations, or add usage examples |
| **Notebook improvements** | New cells, better visualisations, or richer analysis |

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/loven.git
   cd loven
   ```
3. **Create a branch** for your contribution:
   ```bash
   git checkout -b feature/my-improvement
   ```
4. **Install dependencies**:
   ```bash
   pip install requests pandas jupyter
   ```
5. Make your changes, then **open a pull request** against `main`.

---

## Adding Peace Themes

Peace themes are the Norwegian keywords used to filter Lovdata search results. They live in `PEACE_THEMES` in **Cell 1** of the notebook.

1. Open `notebooks/Lovdata_Peace_Analysis.ipynb`.
2. In Cell 1, add your keyword to `PEACE_THEMES`:
   ```python
   PEACE_THEMES = [
       "energi", "vann", "miljø", "etikk",
       "selskap", "oppløsning", "fred",
       "bolig",    # ← your new theme (housing)
       "klima",    # ← your new theme (climate)
   ]
   ```
3. Update the [API Reference](api_reference.md) table to document the new keyword.
4. Run all cells and verify the output looks correct.

---

## Adding Queries

Example queries live in **Cell 4**. To add your own:

1. Extend the `queries` list in Cell 4:
   ```python
   queries = [
       "selskapsloven oppløsning",
       "vannressursloven",
       "energilov miljø",
       "etikk Oljefondet",
       "boliglov nabolag",    # ← your new query
   ]
   ```
2. Run Cell 4 and verify the output.
3. Include a brief comment (in English or Norwegian) explaining the relevance of the query.

---

## Code Style

- Follow **PEP 8** for Python code (4-space indentation, meaningful variable names).
- Use **type hints** (`Dict`, `List`, `Optional`, etc.) consistent with the existing codebase.
- Add a **docstring** to any new class or function.
- Keep notebook cells **self-contained** and ordered: a fresh `Kernel → Restart & Run All` must complete without errors.
- Write **log messages** at the appropriate level (`INFO` for normal operations, `ERROR` for failures).

---

## Submitting a Pull Request

1. Ensure all notebook cells run without error (`Kernel → Restart & Run All`).
2. Commit your changes with a clear message:
   ```bash
   git add .
   git commit -m "feat: add klima theme and climate-change queries"
   ```
3. Push to your fork:
   ```bash
   git push origin feature/my-improvement
   ```
4. Open a pull request on GitHub. In the description, briefly explain:
   - **What** you changed
   - **Why** it is useful for the project's peace and sustainability goals
   - Any relevant Lovdata document links or sources

---

## Code of Conduct

This project exists to make Norwegian law accessible in service of a more harmonious, sustainable world. All contributors are expected to:

- Be respectful and constructive in all communications.
- Give proper credit to data sources (Lovdata.no).
- Use only publicly available data.
- Follow Norwegian and international law when using the Lovdata API.

Contributions that are disrespectful, harmful, or violate the above principles will not be accepted.

---

*For questions, open an issue on GitHub or reach out to the project maintainers.*
