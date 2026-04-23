# Peace Themes

This page explains the **peace theme** system at the heart of **loven** — how it works, what each keyword means, why it was chosen, and how to extend it.

---

## What Is a Peace Theme?

A *peace theme* is a Norwegian keyword that indicates a legal document may be relevant to the project's mission of building a harmonious, sustainable society.

When **loven** retrieves search results from Lovdata it scores each document by counting how many distinct peace-theme keywords appear in its title. Documents with a score of zero are filtered out; documents with higher scores appear first.

---

## Default Theme Keywords

| Keyword | English | Rationale |
|---|---|---|
| `energi` | energy | Clean, renewable energy is foundational to a sustainable future |
| `vann` | water | Water access and water-quality law are basic human-rights issues |
| `miljø` | environment | Environmental protection underpins long-term habitability of the planet |
| `etikk` | ethics | Ethical regulation of government, finance, and AI is central to peace |
| `selskap` | company / corporation | Corporate law governs how economic power is structured and dissolved |
| `oppløsning` | dissolution | Orderly dissolution of entities prevents conflict and injustice |
| `fred` | peace | Direct keyword — legislation that mentions peace explicitly |
| `klima` | climate | Climate legislation shapes long-term environmental outcomes |
| `bolig` | housing | Housing law affects social equity and community stability |
| `arbeidsmiljø` | working environment | Labour and workplace law protects human dignity |

---

## How Scoring Works

```python
# From src/loven/themes.py
def count_themes(text: str, themes: list[str] = PEACE_THEMES) -> int:
    """Return number of distinct themes found in text (case-insensitive)."""
    lowered = text.lower()
    return sum(1 for theme in themes if theme in lowered)
```

Each document's `tema_treff` column value is the count of matching keywords in its title. A document titled *"Lov om energiproduksjon og miljøvern"* would score **2** (both `energi` and `miljø` match).

---

## Synonym Expansion

The default keywords are simple substring matches. For richer recall, you can expand the theme list with synonyms using `loven.nlp`:

```python
from loven.nlp import expand_themes, SYNONYMS

# Built-in synonym map (no external dependencies)
expanded = expand_themes(["energi", "vann"])
print(expanded)
# ['energi', 'vann', 'kraft', 'strøm', 'fornybar', 'vannressurs', 'drikkevann', ...]
```

The `SYNONYMS` dictionary maps each theme to a list of related Norwegian terms:

| Theme | Built-in synonyms |
|---|---|
| `energi` | `kraft`, `strøm`, `fornybar`, `vindkraft`, `solkraft`, `vannkraft` |
| `vann` | `vannressurs`, `drikkevann`, `vannforsyning`, `vassdrag` |
| `miljø` | `naturvern`, `forurensning`, `biologisk mangfold`, `natur` |
| `etikk` | `integritet`, `korrupsjon`, `åpenhet`, `varsling` |
| `klima` | `klimamål`, `klimagass`, `CO2`, `utslipp`, `bærekraft` |
| `bolig` | `husleie`, `leietaker`, `nabolag`, `plan og bygg` |
| `arbeidsmiljø` | `arbeidstaker`, `arbeidsrett`, `HMS`, `diskriminering` |

---

## Adding New Themes

### Option A – Temporary (single session)

Pass a custom theme list to any function:

```python
from loven import LovDataClient, analyze_peace_laws

client = LovDataClient()
my_themes = ["energi", "vann", "havrett", "naturvern"]
df = analyze_peace_laws(client, "havrett", themes=my_themes)
```

### Option B – Permanent (edit the source)

Edit `src/loven/themes.py`:

```python
PEACE_THEMES: list[str] = [
    "energi", "vann", "miljø", "etikk",
    "selskap", "oppløsning", "fred",
    "klima", "bolig", "arbeidsmiljø",
    "havrett",      # ← maritime law
    "naturvern",    # ← nature conservation
    "bærekraft",    # ← sustainability
]
```

Then add corresponding synonyms to `SYNONYMS` in `src/loven/nlp.py` and update the theme table in this page and in `docs/api_reference.md`.

---

## Choosing Good Theme Keywords

Good theme keywords for **loven** share these properties:

1. **Specificity** — they appear in legal document titles when the document genuinely concerns the theme (low false-positive rate).
2. **Norwegian** — Lovdata titles are in Norwegian; English keywords rarely match.
3. **Root form** — Norwegian is an inflected language; prefer root forms that match both singular and plural, e.g. `energi` matches `energiloven`, `energilovgivning`, `energiproduksjon`.
4. **Broad enough to be useful** — a keyword that matches zero documents is not helpful.

If you are unsure whether a keyword is useful, test it with:

```bash
loven search "<keyword>" | head -20
```

and check whether the returned titles are genuinely relevant.

---

## Peace Themes and the UN Sustainable Development Goals

The **loven** theme system loosely maps to the following [UN SDGs](https://sdgs.un.org/goals):

| Theme | Primary SDG |
|---|---|
| `energi` | SDG 7 – Affordable and Clean Energy |
| `vann` | SDG 6 – Clean Water and Sanitation |
| `miljø` / `klima` | SDG 13 – Climate Action, SDG 15 – Life on Land |
| `etikk` | SDG 16 – Peace, Justice and Strong Institutions |
| `bolig` | SDG 11 – Sustainable Cities and Communities |
| `arbeidsmiljø` | SDG 8 – Decent Work and Economic Growth |
| `fred` | SDG 16 – Peace, Justice and Strong Institutions |
