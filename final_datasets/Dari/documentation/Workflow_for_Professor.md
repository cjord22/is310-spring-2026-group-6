# Revised Workflow & Approach — Response to Feedback
**IS310 Group 6 | Daria Meshcheriakova | Spring 2026**

---

## Primary Research Question

> *"What is the most pro-immigration state, and how has each state's stance toward immigration shifted over time (2008–2026)?"*

States studied: **Illinois, California, Arizona**
Source: NCSL Immigration Legislation Archived Database

---

## Response to Each Feedback Point

---

### 1. "Are you performing sentiment analysis on the LLM summary or the law itself?"

**Previous approach:** I was running the prompt on short summaries that the LLM generated, which meant I was measuring the LLM's language, not the law's content.

**Revised approach:**
- Step 1: Retrieve the **full text** of each bill from the NCSL source URL
- Step 2: Send the full text directly to the model — no pre-summarization step
- Step 3: The model reads the actual legislative language and extracts structured features from it
- The summary the model produces is stored separately and is only used for human readability — it does **not** drive any classification

---

### 2. "How are you labeling pro- vs. anti-immigration? The rubric is not clear."

**Previous approach:** Labels were assigned case-by-case with informal reasoning notes. No consistent rule was applied.

**Revised approach — transparent, rule-based classification:**

The label **Pro/Anti/Mixed/Neutral** is now derived from four objective facts extracted from the bill text:

| Fact extracted from bill | What it signals |
|---|---|
| Does the bill restrict ICE cooperation? | Pro |
| Does the bill protect sensitive locations (schools, hospitals, churches)? | Pro |
| Does the bill expand access to public benefits for immigrants? | Pro |
| Does the bill restrict access to public benefits? | Anti |

**Decision rule:**
- More Pro signals than Anti → **Pro**
- More Anti signals than Pro → **Anti**
- Both signals present equally → **Mixed**
- No signals → **Neutral** (flagged for my manual review)

This rule is written explicitly in the codebase and applies identically to every bill. The AI does not decide the label — it only extracts the objective facts above, and the rule does the rest.

---

### 3. "Emphasis on LLMs creates two research questions — immigration AND LLM performance."

**Previous approach:** I was comparing Claude vs. Gemini outputs and treating model agreement as a finding in itself, which split the focus.

**Revised approach — one primary question, one reliability check:**

- **Primary question (the research):** Which state passes the most pro-immigration laws, and has that changed over time?
- **Reliability check (the method):** I optionally run extraction through two models. If they extract the same facts from the same bill, that confirms the extraction is reliable. If they disagree, I flag the bill for my own manual review.

The multi-model comparison is **not a separate research question** — it is a quality-control mechanism, the same way a researcher might re-code a sample of their data to check inter-rater reliability. It validates my method; it is not what I am studying.

---

### 4. "You need a clear plan for scaling. Manual data entry is not feasible."

**Previous approach:** I was copying and pasting law lists into Claude and asking it to fill in spreadsheet rows — not scalable.

**Revised approach — automated pipeline:**

The project now runs as a pipeline with five steps:

```
Step 1 — seed_bills
    Input:  State Immigration Laws_Dataset.csv (original NCSL export)
    Output: data/bills.csv (standardized list of all bills with IDs)

Step 2 — fetch_bill_text
    Input:  data/bills.csv
    Action: Downloads the full text of each bill from its source URL
    Output: data/bill_texts/{bill_id}.txt (one file per bill)

Step 3 — extract_features
    Input:  Full bill text + structured codebook
    Action: Sends text to LLM; model fills in 14 objective fields per bill
    Output: data/extracted/{model}.csv

Step 4 — reconcile
    Input:  Extracted CSVs (one or more models)
    Action: Merges results; derives Pro/Anti label using the rule above;
            flags any bill where models disagreed for my manual review
    Output: data/reconciled.csv

Step 5 — analysis
    Input:  data/reconciled.csv
    Action: Produces stance counts by state and by year
    Output: Summary tables answering the research question
```

**Scalability:** The pipeline processes each bill automatically. Running it across all 64+ bills in the dataset requires no manual data entry. Cost estimate: hundreds of bills < $100 at current API pricing.

**Source note:** The NCSL archived database pages are public and linkable. The pipeline uses the source URLs already in the original dataset to retrieve the full text of each law.

---

## Summary of What the AI Does and Does Not Do

| Task | Who does it |
|---|---|
| Read the full bill text | AI |
| Extract objective facts (ICE cooperation, benefits, etc.) | AI |
| Write a plain-language summary (for my reference only) | AI |
| Decide if a bill is Pro or Anti | **Me** (via explicit rule) |
| Review flagged/ambiguous bills | **Me** (manual) |
| Interpret trends across states and years | **Me** |

The AI is a research assistant that reads documents quickly and consistently. Every classification decision traces back to a rule I wrote, which I can explain and defend.

---

## Open Item

The writeup will frame the research question as:

> *Primary question:* What is the most pro-immigration state?
> *Method validation:* Multi-model agreement is reported as a reliability metric (like inter-rater reliability), not as a standalone finding.

I will update the documentation to make this framing explicit.
