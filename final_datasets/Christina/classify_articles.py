"""
STEP 2: Classify articles using keyword-based rules
-----------------------------------------------------
This script reads raw_articles.tsv (output of fetch_articles.py)
and adds four annotation columns using rule-based keyword matching:

    media_tone        — Positive / Neutral / Negative
    mentions_recovery — Yes / No
    mentions_numeric  — Yes / No
    mentions_cause    — Yes / No

The rules replicate the manual judgments made during bespoke data creation.
This approach is fully transparent: every classification decision is
traceable to an explicit rule in this file.

HOW TO RUN:
    python classify_articles.py

INPUT:  raw_articles.tsv
OUTPUT: classified_articles.tsv
"""

import csv
import re

# ----------------------------------------------------------------
# CLASSIFICATION RULES
# These keyword lists were derived from patterns observed during
# manual coding of the 60-item bespoke dataset.
# ----------------------------------------------------------------

# --- media_tone ---
# Negative: language of loss, blame, suffering, crisis, death
NEGATIVE_KEYWORDS = [
    "suicide", "dead", "death", "killed", "bankrupt", "bankruptcy",
    "ruin", "ruined", "disaster", "catastrophe", "panic", "panicky",
    "crisis", "collapse", "depression", "unemployment", "unemployed",
    "destitute", "wiped out", "devastating", "devastating", "loss",
    "losses", "decline", "slump", "fell", "dropped", "plunged",
    "suffering", "hardship", "starving", "starvation", "evicted",
    "predatory", "fraud", "gambling", "speculation", "misrepresentation",
    "charged", "blamed", "responsibility", "guilty", "wrong",
    "fear", "alarm", "worried", "concern", "danger", "threat",
]

# Positive: language of recovery, reassurance, resilience, opportunity
POSITIVE_KEYWORDS = [
    "recovery", "recover", "recovered", "improving", "improvement",
    "optimistic", "optimism", "confidence", "confident", "sound",
    "stable", "stability", "reassured", "reassurance", "nothing to worry",
    "bounced back", "rebound", "upturn", "growth", "prosper",
    "surplus", "profit", "gain", "gains", "stronger", "strength",
    "opportunity", "invest", "buying opportunity", "foundation",
    "resilient", "resilience", "overcome", "better", "brighter",
]

# --- mentions_recovery ---
# Explicit forward-looking or confirmed recovery language
RECOVERY_KEYWORDS = [
    "recovery", "recover", "recovered", "recovering",
    "unemployment on the mend", "conditions improving",
    "business improving", "will disappear", "passed",
    "bounce back", "rebound", "upturn", "stabilize",
    "return to normal", "getting better", "mend",
    "restored confidence", "confidence restored",
]

# --- mentions_numeric ---
# Dollar amounts, percentages, specific figures
# We use a regex pattern to catch numbers like $10,000,000 or 30 per cent
NUMERIC_PATTERN = re.compile(
    r'(\$[\d,]+)|'           # dollar amounts like $10,000,000
    r'(\d+[\.,]\d+\s*(per cent|percent|%))|'  # percentages
    r'(\d{1,3}(,\d{3})+)',   # large numbers with commas like 416,770
)

# --- mentions_cause ---
# Explicit causal attribution language
CAUSE_KEYWORDS = [
    "caused by", "cause of", "result of", "resulted from",
    "due to", "because of", "responsible for", "precipitated by",
    "brought about by", "direct result", "principal cause",
    "led to", "contributing factor", "primarily", "fundamentally",
    "overproduction", "speculation", "speculative", "federal reserve",
    "foreign liquidation", "predatory", "gambling with",
    "contradictions", "over-production", "credit",
    "engineered", "drove", "triggered",
]

# ----------------------------------------------------------------
# CLASSIFICATION FUNCTIONS
# ----------------------------------------------------------------

def classify_tone(text):
    """
    Returns Positive, Negative, or Neutral based on keyword presence.
    If both positive and negative keywords appear, Negative wins
    (consistent with manual coding: content trumps framing).
    """
    text_lower = text.lower()
    has_negative = any(kw in text_lower for kw in NEGATIVE_KEYWORDS)
    has_positive = any(kw in text_lower for kw in POSITIVE_KEYWORDS)

    if has_negative:
        return "Negative"
    elif has_positive:
        return "Positive"
    else:
        return "Neutral"


def classify_recovery(text):
    """Returns Yes if the snippet mentions recovery, No otherwise."""
    text_lower = text.lower()
    return "Yes" if any(kw in text_lower for kw in RECOVERY_KEYWORDS) else "No"


def classify_numeric(text):
    """Returns Yes if the snippet contains specific numeric figures."""
    return "Yes" if NUMERIC_PATTERN.search(text) else "No"


def classify_cause(text):
    """Returns Yes if the snippet explicitly attributes a cause to the crash."""
    text_lower = text.lower()
    return "Yes" if any(kw in text_lower for kw in CAUSE_KEYWORDS) else "No"


# ----------------------------------------------------------------
# MAIN: read raw TSV, classify each row, write output TSV
# ----------------------------------------------------------------

def main():
    input_file = "raw_articles.tsv"
    output_file = "classified_articles.tsv"

    rows_read = 0
    rows_written = 0

    input_fieldnames = ["snippet_text", "source", "date", "state", "crash_event"]
    output_fieldnames = input_fieldnames + [
        "media_tone", "mentions_recovery", "mentions_numeric", "mentions_cause",
        "coding_method"  # flags whether row was manually or computationally coded
    ]

    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile, delimiter="\t")
        writer = csv.DictWriter(outfile, fieldnames=output_fieldnames, delimiter="\t")
        writer.writeheader()

        for row in reader:
            rows_read += 1
            text = row.get("snippet_text", "")

            row["media_tone"] = classify_tone(text)
            row["mentions_recovery"] = classify_recovery(text)
            row["mentions_numeric"] = classify_numeric(text)
            row["mentions_cause"] = classify_cause(text)
            row["coding_method"] = "computational"  # mark as auto-classified

            writer.writerow(row)
            rows_written += 1

    print(f"Done! Read {rows_read} rows, wrote {rows_written} rows to {output_file}")
    print("Next step: run merge_datasets.py to combine with your manual 60-row dataset.")


if __name__ == "__main__":
    main()
