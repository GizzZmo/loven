# CLI Reference

The `loven` command-line tool lets you query Lovdata and manage peace themes without opening a Jupyter notebook.

---

## Installation

The `loven` command is available after installing the package:

```bash
pip install -e .
```

---

## Commands

### `loven search`

Search Lovdata and print peace-relevant results to the terminal.

```
loven search <query> [--limit N] [--themes k1,k2,...] [--base-url URL]
```

| Argument | Description |
|---|---|
| `query` | Norwegian search term(s) |
| `--limit N` | Maximum results to request (default: `20`) |
| `--themes k1,k2` | Comma-separated peace-theme keywords (overrides defaults) |
| `--base-url URL` | Override the Lovdata API base URL |

**Examples:**

```bash
loven search "energilov miljø"
loven search "vannressursloven" --limit 10
loven search "energi" --themes "energi,sol,vind"
```

---

### `loven export`

Search Lovdata and save results to a file.

```
loven export <query> --output <file> [--limit N] [--themes k1,k2,...] [--base-url URL]
```

| Argument | Description |
|---|---|
| `query` | Norwegian search term(s) |
| `--output FILE` | Output path. Use `.csv` for CSV or `.xlsx` for Excel *(required)* |
| `--limit N` | Maximum results to request (default: `20`) |
| `--themes k1,k2` | Comma-separated peace-theme keywords (overrides defaults) |
| `--base-url URL` | Override the Lovdata API base URL |

**Examples:**

```bash
loven export "miljøvern" --output results.csv
loven export "etikk Oljefondet" --output results.xlsx --limit 50
```

---

### `loven themes list`

Print all current peace-theme keywords and their English translations.

```
loven themes list
```

**Example output:**

```
Norwegian            English
----------------------------------------
energi               energy
vann                 water
miljø                environment
etikk                ethics
selskap              company / corporation
oppløsning           dissolution
fred                 peace
klima                climate
bolig                housing
arbeidsmiljø         working environment
```

---

## Global help

```bash
loven --help
loven search --help
loven export --help
loven themes --help
```
