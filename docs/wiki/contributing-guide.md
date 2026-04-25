# Contributing to loven

Thank you for your interest in contributing to **loven**! Contributions of all kinds are welcome — new peace-theme keywords, code improvements, documentation fixes, translations, bug reports, and feature requests.

---

## Code of Conduct

This project follows the [Contributor Covenant 2.1](https://github.com/GizzZmo/loven/blob/main/CODE_OF_CONDUCT.md). All participants are expected to uphold it. Please report unacceptable behaviour to the project maintainers via [GitHub Issues](https://github.com/GizzZmo/loven/issues).

---

## Ways to Contribute

| Type | Where to start |
|---|---|
| 🐛 Bug reports | [Open a GitHub issue](https://github.com/GizzZmo/loven/issues/new) |
| 💡 Feature requests | [Open a GitHub issue](https://github.com/GizzZmo/loven/issues/new) |
| 📝 Documentation | Edit any file in `docs/` and submit a pull request |
| 🌍 Translations | Add a new `docs/notebook_guide_<lang>.md` |
| 🏷️ New peace themes | See [Adding new themes](#adding-new-peace-themes) below |
| 🧪 New tests | Add files to `tests/` and submit a pull request |
| 🔧 Code improvements | Fork → branch → edit → PR |

---

## Development Setup

### 1. Fork and clone

```bash
git clone https://github.com/<your-username>/loven.git
cd loven
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Install in development mode with all extras

```bash
pip install -e ".[dev,notebook,viz,nlp]"
```

### 4. Run the test suite

```bash
pytest tests/ -v --cov=src/loven --cov-report=term-missing
```

All tests must pass before submitting a pull request.

### 5. Lint the code

```bash
ruff check src/ tests/
```

Fix any linting errors before submitting.

---

## Pull Request Checklist

Before opening a PR, please confirm:

- [ ] All existing tests pass (`pytest tests/ -v`)
- [ ] Linting passes (`ruff check src/ tests/`)
- [ ] New functionality is covered by tests
- [ ] Docstrings are updated for changed functions/classes
- [ ] Relevant documentation in `docs/` is updated
- [ ] The PR description explains *what* changed and *why*

---

## Adding New Peace Themes

To add a new peace-theme keyword permanently:

### Step 1 – Edit `src/loven/themes.py`

```python
PEACE_THEMES: list[str] = [
    "energi", "vann", "miljø", "etikk",
    "selskap", "oppløsning", "fred",
    "klima", "bolig", "arbeidsmiljø",
    "havrett",      # ← add new keyword here
]
```

### Step 2 – Add synonyms in `src/loven/nlp.py`

```python
SYNONYMS: dict[str, list[str]] = {
    ...
    "havrett": ["sjørett", "hav", "sjø", "fiske", "skipsfart"],
}
```

### Step 3 – Update documentation

- Add a row to the theme tables in `docs/wiki/peace-themes.md` and `docs/api_reference.md`.
- Update the Peace Themes section of `README.md`.

### Step 4 – Add a test

Add an assertion to `tests/test_themes.py`:

```python
def test_new_theme_present():
    assert "havrett" in PEACE_THEMES
```

### Step 5 – Open a pull request

Commit all changes, push to your fork, and open a PR with a short description of the new keyword and its rationale.

---

## Adding a New Language Translation

Translations of the notebook guide are especially welcome for reaching a global audience.

1. Copy `docs/notebook_guide_en.md` to `docs/notebook_guide_<lang>.md` (e.g. `_de`, `_fr`, `_es`).
2. Translate the content.
3. Add the new file to the `nav` section in `mkdocs.yml`:

```yaml
- Getting Started:
    - Notebook Guide (EN): notebook_guide_en.md
    - Notebook Guide (DE): notebook_guide_de.md   # ← add here
```

4. Open a pull request.

---

## Reporting Bugs

When reporting a bug, please include:

- Your Python version (`python --version`) and operating system
- The exact command or code you ran
- The full error message and traceback
- Whether you can reproduce the issue with the sample data (`sample_data/mock_lovdata_response.json`)

---

## Suggesting Features

Feature requests are welcome. Please open a GitHub issue and describe:

- The problem you are trying to solve
- Your proposed solution or feature
- Any alternatives you have considered

---

## Commit Message Style

Use short, imperative present-tense messages:

```
Add havrett peace theme
Fix async timeout handling
Update FAQ with cache example
```

---

## Questions?

Open an issue on [GitHub](https://github.com/GizzZmo/loven/issues) — there are no silly questions.
