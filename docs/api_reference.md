# API Reference

Complete reference for all classes and functions in `Lovdata_Peace_Analysis.ipynb`.

---

## Module-level Constants

### `BASE_URL`

```python
BASE_URL: str = "https://api.lovdata.no"
```

Root URL for all Lovdata API requests. Override by passing a custom `base_url` to `LovDataClient`.

---

### `PEACE_THEMES`

```python
PEACE_THEMES: list[str] = ["energi", "vann", "miljø", "etikk", "selskap", "oppløsning", "fred"]
```

List of Norwegian keywords used by `filter_peace_laws` and `analyze_peace_laws` to decide whether a legal document is relevant to the project's peace-and-sustainability mission.

| Keyword | English translation |
|---|---|
| `energi` | energy |
| `vann` | water |
| `miljø` | environment |
| `etikk` | ethics |
| `selskap` | company / corporation |
| `oppløsning` | dissolution |
| `fred` | peace |

---

## Class: `LovDataClient`

```python
class LovDataClient:
    def __init__(self, base_url: str = BASE_URL) -> None: ...
    def search(self, query: str, limit: int = 20) -> Dict: ...
    def filter_peace_laws(self, data: Dict) -> List[Dict]: ...
```

An object-oriented wrapper around the Lovdata REST API. Uses a persistent `requests.Session` for connection reuse and shared headers.

---

### `LovDataClient.__init__`

```python
def __init__(self, base_url: str = BASE_URL) -> None
```

Initialises the client.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `base_url` | `str` | `"https://api.lovdata.no"` | Base URL for all API requests |

**Side effects**

- Creates `self.session` (`requests.Session`) with `Accept: application/json` header.
- Logs `INFO: LovDataClient initialisert for Global Peace arbeid.`

**Example**

```python
client = LovDataClient()                              # use default URL
client_custom = LovDataClient("https://my-mirror/")  # use custom URL
```

---

### `LovDataClient.search`

```python
def search(self, query: str, limit: int = 20) -> Dict
```

Sends a GET request to the Lovdata search endpoint and returns the parsed JSON response.

**Parameters**

| Name | Type | Default | Description |
|---|---|---|---|
| `query` | `str` | *(required)* | Norwegian search term(s), e.g. `"vannressursloven"` |
| `limit` | `int` | `20` | Maximum number of results to return |

**Returns**

`Dict` – the parsed JSON body. On success this typically contains:

```json
{
  "hits": [
    {
      "tittel": "Lov om ...",
      "url": "https://lovdata.no/...",
      ...
    }
  ]
}
```

On error:

```json
{"error": "<exception message>"}
```

**Raises**

Does not raise. All exceptions are caught internally; the error is logged and `{"error": "..."}` is returned.

**Side effects**

- Logs `INFO: Søkte etter '<query>' – fant <N> treff.` on success.
- Logs `ERROR: API-feil: <e>. Bruk lokal backup-data.` on failure.

**Example**

```python
client = LovDataClient()
result = client.search("energilov", limit=10)
print(result.get("hits", []))
```

---

### `LovDataClient.filter_peace_laws`

```python
def filter_peace_laws(self, data: Dict) -> List[Dict]
```

Filters a search result dict, keeping only hits whose `"tittel"` field contains at least one keyword from `PEACE_THEMES`.

**Parameters**

| Name | Type | Description |
|---|---|---|
| `data` | `Dict` | Raw response dict from `search()`, expected to have a `"hits"` key |

**Returns**

`List[Dict]` – subset of `data["hits"]` matching the peace theme filter. Returns an empty list if `data` has no `"hits"` key or none of the hits match.

**Notes**

- Comparison is case-insensitive (`.lower()` applied to title).
- Uses a list comprehension; does not mutate the input `data`.

**Example**

```python
client = LovDataClient()
raw = client.search("vann")
relevant = client.filter_peace_laws(raw)
for law in relevant:
    print(law["tittel"])
```

---

## Function: `analyze_peace_laws`

```python
def analyze_peace_laws(client: LovDataClient, query: str) -> pd.DataFrame
```

High-level orchestrator function. Runs a search, filters for peace-relevant laws, and returns the results as a Pandas DataFrame.

**Parameters**

| Name | Type | Description |
|---|---|---|
| `client` | `LovDataClient` | An initialised `LovDataClient` instance |
| `query` | `str` | Norwegian search term(s) |

**Returns**

`pd.DataFrame` with the following columns:

| Column | dtype | Description |
|---|---|---|
| `tittel` | `object` (str) | Norwegian title of the legal document |
| `url` | `object` (str) | Direct link to the document on lovdata.no |
| `relevans_for_fred` | `bool` | `True` if the title contains a `PEACE_THEMES` keyword |

Returns an **empty DataFrame** (zero rows) if the search returns no results or the API is unavailable.

**Side effects**

- Prints: `Analysert <N> lover relatert til Global Peace Agreement.`
- Delegates logging to `LovDataClient.search`.

**Example**

```python
client = LovDataClient()
df = analyze_peace_laws(client, "miljølov")
print(df)
```

---

## Logging

All log output uses the standard Python `logging` module under the logger named `__main__`.

| Level | Emitted by | Message |
|---|---|---|
| `INFO` | `LovDataClient.__init__` | Client initialisation |
| `INFO` | `LovDataClient.search` | Successful search with result count |
| `ERROR` | `LovDataClient.search` | Any exception during the HTTP request |

Configure log level in Cell 1:

```python
logging.basicConfig(level=logging.DEBUG)  # more verbose
logging.basicConfig(level=logging.WARNING)  # errors only
```
