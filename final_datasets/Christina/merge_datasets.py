

import csv

MANUAL_FILE = "Jordan Initial Dataset - Sheet1.csv"
COMPUTATIONAL_FILE = "classified_articles.tsv"
OUTPUT_FILE = "final_dataset.tsv"

FIELDNAMES = [
    "snippet_text", "source", "date", "state", "crash_event",
    "media_tone", "mentions_recovery", "mentions_numeric", "mentions_cause",
    "coding_method"
]

def main():
    all_rows = []

    with open(MANUAL_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")  
        for row in reader:
            row.setdefault("state", "")
            row.setdefault("coding_method", "manual")
            clean = {k: row.get(k, "") for k in FIELDNAMES}
            all_rows.append(clean)

    manual_count = len(all_rows)
    print(f"Read {manual_count} manual rows from {MANUAL_FILE}")

    with open(COMPUTATIONAL_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            clean = {k: row.get(k, "") for k in FIELDNAMES}
            all_rows.append(clean)

    computational_count = len(all_rows) - manual_count
    print(f"Read {computational_count} computational rows from {COMPUTATIONAL_FILE}")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter="\t")
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nDone! Final dataset: {len(all_rows)} total rows written to {OUTPUT_FILE}")
    print(f"  — {manual_count} manually coded rows")
    print(f"  — {computational_count} computationally classified rows")


if __name__ == "__main__":
    main()
