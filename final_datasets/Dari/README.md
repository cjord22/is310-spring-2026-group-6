# State Immigration Law Sentiment Analysis

---

## Research Question

Which state — Illinois, California, or Arizona — is the most pro-immigration, and how has each state's legislative stance shifted over time (2009–2026)?

---

## What This Project Does

This project builds a dataset of 589 state immigration laws across Illinois, California, and Arizona and uses a TF-IDF + Logistic Regression classifier to assign each law a pro-immigration probability score (0 = strongly anti-immigration, 1 = strongly pro-immigration).

The researcher manually labeled 30 laws (21 Pro-Immigration, 9 Anti-Immigration) by reading the law text and writing a reasoning note for each. Those labels train the model, which then scores all 589 laws. Leave-One-Out cross-validation on the 30 labeled laws gives an honest accuracy estimate: **80.0% (24/30 correct)**.

---

## Files

### Dataset
- **`dataset/final_dataset.csv`** — 589 laws; 10 columns: State, Year, Law Passed, Law Link, Law Description, my_label, Reasoning, model_label, pro_immigration_score, top_trigger_words
- **`dataset/laws_with_text.csv`** — same laws with full bill text where available (used as richer training input for the classifier)
- **`dataset/State Immigration Laws_Dataset.csv`** — the original 67-law NCSL dataset from the start of the semester (kept for reference)

### Code
- **`IS310_Analysis.ipynb`** — all analysis in one notebook: data overview, manual labeling breakdown, TF-IDF + LR model, LOO cross-validation, feature importance charts, scoring all 589 laws, trend analysis by state, conclusions

### Documentation
- **`documentation/Essay.md`** — the full data essay (9 sections): dataset origins, manual labeling process, computational method, findings, limitations, ethics, scale, lessons learned, situating in scholarship
- **`documentation/Group-Collective-Principles.md`** — Group 6 collective principles document
- **`codebook/ProVsAnti.md`** — the labeling rubric: what counts as Pro-Immigration vs. Anti-Immigration, with worked examples and borderline decision rules

---

## Data Sources

| Source | Rows | Notes |
|--------|------|-------|
| LegiScan API | 337 | Full bill descriptions; IL, CA, AZ; 2009–2026 |
| Arizona Legislature API (azleg.gov) | 183 | Bill titles only — short text, less reliable for TF-IDF |
| NCSL Immigration Legislation Database | 64 | Manually collected; full descriptions |
| State portals via Plural Policy | 5 | Added manually |
| **Total** | **589** | Arizona: 238 · California: 179 · Illinois: 172 |

---

## Key Findings

| State | Avg Score | Assessment |
|-------|-----------|------------|
| Illinois | 0.535 | Highest — driven by explicit post-2019 pro-immigrant language |
| California | 0.527 | Strongly pro-immigration throughout |
| Arizona | 0.508* | Unreliable overall — see note |

*Arizona's model average is not reliable because 183 of its 238 laws came from the Arizona Legislature API and have only 3–7 word titles. TF-IDF cannot score short titles meaningfully. Among the 13 Arizona laws that were manually labeled, 9 are Anti-Immigration — a more accurate picture of Arizona's legislative posture.

---

## How to Run

Open `IS310_Analysis.ipynb` in Jupyter and run all cells in order. Requires: `pandas`, `scikit-learn`, `matplotlib`, `numpy`.

```bash
pip install pandas scikit-learn matplotlib numpy
jupyter notebook IS310_Analysis.ipynb
```
