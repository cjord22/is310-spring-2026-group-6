# Final dataset documentation

This folder contains **one combined, normalized dataset** of collection records pulled **at scale** from several public museum APIs. Records share a common column layout so rows from different institutions can be analyzed in one table. A small metadata JSON documents **how** the scrape was run (queries, counts, warnings/errors). The Python script reproduces the pipeline.

**What this dataset supports:** examining how “American history” behaves as a **keyword-driven retrieval problem** across museum catalogs and open-access media—not as a neutral or complete historiographic sample.

---

## Contents

| File | Role |
|------|------|
| `final_american_history.jsonl` | Primary dataset (**one JSON object per line**). Best for programmatic use (Python/R). |
| `final_american_history.csv` | Same rows as CSV (**spreadsheet-friendly**). `raw_source` can be very wide. |
| `final_american_history_meta.json` | Run summary: timestamp, query list, per-`source` counts, API warnings/errors. |
| `scrape_american_history_art.py` | Scraper + normalizer + dedupe + export. |
| `requirements.txt` | Python dependencies (`requests`, etc.). |

---

## Data dictionary (column semantics)

| Column | Meaning |
|--------|---------|
| `uid` | UUID generated for this dataset row (not the museum’s native ID). |
| `source` | API origin: `artic`, `met`, `cma`, or `harvard`. |
| `source_object_id` | Museum-native identifier (string). |
| `title` | Title when provided. |
| `artist_display` | Artist/maker string (format varies by museum). |
| `date_display` | Date or date range as a **string** (not normalized to a single year). |
| `medium` | Materials / object type when available. |
| `department` | Department or unit string when available (meaning differs by institution). |
| `image_url` | Image URL when exposed by the API for that record. |
| `iiif_image_id` | Present for some Art Institute rows (IIIF image id used in image URLs). |
| `license_or_rights` | Short rights / access note from the source record (heuristic; verify at `object_url`). |
| `object_url` | Public object page when available. |
| `search_queries` | Which keyword(s) returned this row (format differs slightly between CSV vs JSONL). |
| `raw_source` | JSON/text snapshot of the underlying museum payload (audit + debugging). |

---

## How the dataset was made (computation + scale)

1. **Keyword search** using a shared list of American-history–oriented queries.  
2. **Source-specific retrieval** (some APIs return full records; The Met often requires object-by-object follow-up).  
3. **Normalization** into the shared schema above.  
4. **Deduping + per-source caps** to prevent one index from overwhelming the table.  
5. **Export** to JSONL + CSV + `*_meta.json`.

**Interpretive point:** scale amplifies what is **searchable and digitized**, not what is historically “most important.”

---

## How to reproduce (run the scraper)

### 1) Environment

```bash
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) API keys

| Source | Key required? | How to get access |
|:--|:--|:--|
| **Art Institute of Chicago** | No | Public API. |
| **The Met** | No | Public Collection API. |
| **Cleveland Museum of Art** | No | Open Access API. |
| **Harvard Art Museums** | **Yes** | [Harvard Art Museums API](https://harvardartmuseums.org/collections/api/) |


```bash
export HARVARD_ART_API_KEY="YOUR_KEY_HERE"
```

Harvard harvesting is skipped if this environment variable is not set.

### 3) Run

```bash
python scrape_american_history_art.py \
  --out final_american_history.jsonl \
  --csv-out final_american_history.csv
```

Useful CLI flags:

| Flag | Purpose |
|------|---------|
| `--max-per-source N` | Cap rows retained per institution after dedupe |
| `--per-query-limit N` | Pull more matches per keyword before dedupe/caps |
| `--sleep-met SECONDS` | Pause between Met object-detail requests |
| `--inspect-only` | Print sample response structures (debugging only) |

Show all flags:

```bash
python scrape_american_history_art.py --help
```

### 4) Read outputs (example)

```python
import pandas as pd

df = pd.read_json("final_american_history.jsonl", lines=True)
df.head()
```

---

## Citations & institutional credit

Art Institute of Chicago. (*n.d.*). *Art Institute of Chicago API documentation*. Retrieved from https://api.artic.edu/docs/#quick-start

Metropolitan Museum of Art. (*n.d.*). *The Met Collection API*. Retrieved from https://metmuseum.github.io/

Cleveland Museum of Art. (*n.d.*). *Open Access API*. Retrieved from https://openaccess-api.clevelandart.org/

Harvard Art Museums. (*n.d.*). *Harvard Art Museums API*. Retrieved from https://harvardartmuseums.org/collections/api/

---


