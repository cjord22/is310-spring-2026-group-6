# Project Changelog — IS310 Group 6 Immigration Laws Dataset
**Daria Meshcheriakova | UIUC Spring 2026**

---

## Early Work (Pre-Feedback)

- Identified research question: *"What is the most pro-immigration state and how has each state's stance shifted over time?"*
- Selected three states: **Illinois** (home state), **Arizona** (most politically volatile), **California** (consistently pro-immigration)
- Sourced data from the **NCSL Immigration Legislation Archived Database** (2008–2026)
- Dropped initial idea of correlating immigration laws with unemployment rates — too broad, unclear outcome
- Manually built Excel spreadsheet with two sheets: main data (state, year, law name, key description, sentiment) + AI answers sheet
- Populated database with bills from 2009–2026 using Claude Code and Claude Browser
- Used Gemini and Claude Browser on the same prompt per law to generate 1-sentence summaries
- Ran summaries through own judgment to assign **Pro** or **Anti** sentiment label with written reasoning
- Documented all prompts used in `Daria/Documentation.md`

---

## Instructor Feedback Received

Feedback from Jesse Frye on the initial dataset submission (`Daria/Feedback.txt`):

- ❌ Sentiment was being run on **LLM-generated summaries**, not the actual law text — effectively studying the LLM's sentiment, not the law
- ❌ No explicit rubric for what counts as Pro vs Anti — only a few labels had written justifications
- ❌ LLM comparison creates **two research questions** (immigration stance + LLM performance), which dilutes both
- ❌ No scaling plan — manual data entry is not feasible for hundreds of laws

---

## 05/02 — Pipeline Build

- Shifted from spreadsheet-only workflow to a **structured extraction pipeline**
- Built `codebook/ProVsAnti.md` — full 15-field rubric with controlled vocabularies, worked examples, edge cases; this is the methodological source-of-truth
- Built `schema/schema.py` — `LawFeatures` dataclass + `validate()` + `json_schema()`, stdlib-only so tests run without API keys
- Built full pipeline in order:
  - `pipeline/seed_bills.py` — converts original CSV into `data/bills.csv`
  - `pipeline/fetch_bill_text.py` — downloads full bill text per bill ID
  - `pipeline/extract_features.py` — sends full text + codebook to LLM, writes per-model CSV
  - `pipeline/reconcile.py` — merges outputs across models, flags disagreements for human review
  - `analysis/run_analysis.py` — produces summary tables (stance by state, by year, policy area frequency)
- Built provider-agnostic LLM layer (`pipeline/providers/`) — supports `mock`, `claude_sonnet`, `claude_opus`, `gemini_pro`; adding a new model = one new file
- All 30 tests written, stdlib-only, all passing
- Schema version set to `v1`
- Addressed instructor feedback:
  - ✅ Sentiment now runs on **full bill text**, not summaries
  - ✅ Explicit rubric (`codebook/ProVsAnti.md`) enforced via JSON Schema
  - ✅ Scaling plan = the pipeline (hundreds of bills, <$100 at current API pricing)
  - 🟡 Two-research-questions framing still needs to be addressed in the writeup

---

## 2026-05-04 — Removed AI Stance Classification; Added Rule-Based Derivation

**Decision:** AI should not decide Pro/Anti — that introduces AI political bias and is a black box. Instead, AI extracts only **objective facts**, and stance is derived from a transparent researcher-controlled rule.

- Removed `stance` field from `LawFeatures` dataclass, JSON schema, and LLM system prompt — AI is no longer asked to classify
- Added `derive_stance()` function in `schema/schema.py` with an explicit rule:
  - **Pro signals:** `restricts_ice_cooperation = True`, `protects_sensitive_locations = True`, `affects_public_benefits = "Expands"`
  - **Anti signals:** `affects_public_benefits = "Restricts"`
  - More Pro than Anti → `Pro`; more Anti → `Anti`; both → `Mixed`; neither → `Neutral` (flagged for human review)
- `restricts_ice_cooperation` and `protects_sensitive_locations` intentionally carry no Anti weight — they are structural facts, not value judgments
- `enforcement_teeth` and `mentions_287g_or_sanctuary` excluded from the rule — not directional on their own
- Updated `pipeline/reconcile.py` to call `derive_stance()` after reconciling all extracted fields; stance is written to the output CSV as a derived column
- Bumped `SCHEMA_VERSION` `v1` → `v2` — forces re-extraction so no v1 rows (which carry an AI-assigned stance) pollute new runs
- Updated tests in `test_schema.py`, `test_providers.py`, `test_reconcile.py`, `test_seed_and_extract.py`
- All **37 tests** passing

**Why this matters for the writeup:** Every Pro/Anti classification can now be explained in one sentence citing specific bill provisions — no AI black box. Bills with no clear signal come out `Neutral` and get flagged for manual review, which is more rigorous than letting the model guess.

---

## 2026-05-05 — Session Notes

- *(no recorded activity — placeholder created by Stop hook)*

---

## 2026-05-11 — Session Notes

- Reviewed `TestingCode.ipynb` — identified that scraper only retrieved text for 10/67 rows
- Decided to use `Law Description` as the feature column for logistic regression
- Discussed and confirmed final deliverable: Jupyter notebook + analysis writeup
- Confirmed primary research goal: trend analysis over time per state

---

## 2026-05-12 — Session Notes

- Pivoted final analysis approach: replaced fragile bill-text scraper (only worked for 10/67 rows) with TF-IDF on `Law Description` column (66/66 rows covered)
- Built `IS310_Analysis.ipynb` — clean 5-section notebook: EDA, model, LOO CV, trend charts, conclusions
- Installed `scikit-learn` 1.8.0 into system Python 3.14 (was missing)
- Model results: **84.85% LOO accuracy** (56/66 correct); CA avg 0.637, IL 0.636, AZ 0.540
- Created `Essay-outline.md` with 9-section outline + group collective principles doc questions
- Set up rolling conversation log system: `conversation-log.md` + `/log-session` custom command + updated Stop hook
