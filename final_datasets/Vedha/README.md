# Final dataset: American-history–oriented artworks (multi-museum aggregation)

This folder contains **one combined, normalized dataset** of collection records pulled **at scale** from several public museum APIs. Records are tied together with a shared column layout so rows from different institutions can be analyzed in one table. A small metadata file documents **how** the scrape was run (queries, counts, errors). The Python script reproduces the pipeline.

**What this dataset is for:** studying how “American history” (as *text search*, not authoritative curation) surfaces through **museum catalog data and open-access images** across institutions—with all the skew that implies.

---

## Contents

| File | Role |
|------|------|
| `final_american_history.jsonl` | **Primary dataset** (one JSON object per line). Best for Python/pandas and strict typing. |
| `final_american_history.csv` | Same rows in tabular form (easy for spreadsheets). Large `raw_source` cells. |
| `final_american_history_meta.json` | **Run summary**: timestamp, keyword list, per-`source` row counts, warnings (e.g. failed API calls). |
| `scrape_american_history_art.py` | Script that queries APIs, normalizes fields, dedupes, caps per source, writes outputs. |
| `requirements.txt` | Python dependencies (`requests`, etc.). |
| `.gitignore` | Keeps local virtualenv junk out of git (if you use one). |

---

## Data dictionary (column semantics)

> **Note on this submission:** `description` and `culture` were **dropped from the released table** because they were **often empty or noisy** after normalization, while other columns carried more reliable signal for our analysis. The full API payloads are still available inside `raw_source` if you need to recover institution-specific fields later.

| Column | Meaning |
|--------|---------|
| `uid` | Random UUID for this row in our dataset (not the museum’s ID). |
| `source` | Which API the row came from: `artic` (Art Institute of Chicago), `met` (Metropolitan Museum), `cma` (Cleveland Museum of Art), `harvard` (Harvard Art Museums). |
| `source_object_id` | The museum’s own identifier for the object (as a string). |
| `title` | Object title when provided. |
| `artist_display` | Creator / maker string when available (format varies by museum). |
| `date_display` | Date or date range as a **display string** (not a normalized year type). |
| `medium` | Materials / object type when available. |
| `department` | Department or unit string when available (semantics differ by museum). |
| `image_url` | Best-effort link to a collection image when the source exposes one. May be empty for rights or missing assets. |
| `iiif_image_id` | Only populated for some Art Institute records (IIIF image identifier used to build IIIF URLs). |
| `license_or_rights` | Short rights note or museum field (e.g. public domain / CC0-style access). **Always verify** at the institution before reuse in publication. |
| `object_url` | Public object page on the museum site when available. |
| `search_queries` | Which keyword(s) from our query list produced this hit (pipe- or list-separated in CSV vs JSONL). |
| `raw_source` | JSON/text snapshot of the **original museum record** (or subset) for auditability and debugging. |

**Deduplication rule in the scraper:** rows are deduped by **(`source`, `source_object_id`)** so the same museum object is not repeated twice *within* a source. The same real-world artwork can still appear **across** museums as separate rows.

---

## How the dataset was made (computation + scale)

1. **Keyword search** across a shared list of American-history–oriented phrases (e.g. “American Revolution,” “Abraham Lincoln,” etc.).  
2. **API-specific retrieval:** some museums return rich objects in one call; others return IDs that require **per-object** follow-up requests (notably The Met).  
3. **Normalization:** map heterogeneous JSON into the shared columns above.  
4. **Deduping + capping:** enforce a maximum number of rows **per `source`** so one institution does not dominate only because its search index is huge.  
5. **Write outputs:** JSONL + CSV + `*_meta.json`.

**What scale does here:** it surfaces *what is easy to index and tag as text* in each catalog, not “the complete universe of American history art.” That gap is interpretive, not just technical.

---

## How to reproduce (run the scraper)

### 1) Environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
