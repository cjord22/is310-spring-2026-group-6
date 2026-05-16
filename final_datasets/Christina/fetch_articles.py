

import requests
import time
import csv
import sys

CRASH_PERIODS = [
    {"label": "1929", "date_start": "1929-01-01", "date_end": "1932-12-31"},
    {"label": "1937", "date_start": "1937-01-01", "date_end": "1939-12-31"},
    {"label": "1962", "date_start": "1962-01-01", "date_end": "1963-12-31"},
]

RESULTS_PER_PERIOD = 300

API_BASE = "https://www.loc.gov/collections/chronicling-america/"

HEADERS = {
    "User-Agent": "student research project"
}

def fetch_page(crash_label, date_start, date_end, page_number):
    params = {
        "q": "stock market crash",
        "dl": "page",
        "start_date": date_start,
        "end_date": date_end,
        "fo": "json",
        "c": 100,             
        "sp": page_number,      
        "at": "results,pagination",
    }

    try:
        response = requests.get(API_BASE, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"  ERROR on page {page_number}: {e}")
        return [], False

    results_list = data.get("results", [])
    pagination = data.get("pagination", {})
    has_more = pagination.get("next", None) is not None

    results = []
    for item in results_list:
        description = item.get("description", [])
        if isinstance(description, list):
            ocr_text = " ".join(description)
        else:
            ocr_text = str(description)

        ocr_text = " ".join(ocr_text.split())

        if len(ocr_text) < 30:
            continue

        source = ""
        title = item.get("title", "")
        if isinstance(title, list):
            source = " ".join(title)
        else:
            source = str(title)


        date = item.get("date", "")

        location = item.get("location_city", [])
        state = location[0] if location else ""

        results.append({
            "snippet_text": ocr_text[:500],
            "source": source,
            "date": date,
            "state": state,
            "crash_event": crash_label,
        })

    return results, has_more


def main():
    all_articles = []

    for period in CRASH_PERIODS:
        label = period["label"]
        print(f"\nFetching articles for crash period: {label}")

        period_articles = []
        page = 1

        while len(period_articles) < RESULTS_PER_PERIOD:
            print(f"  Fetching page {page}... ", end="")
            sys.stdout.flush()

            articles, has_more = fetch_page(
                label, period["date_start"], period["date_end"], page
            )

            if not articles:
                print("no results, stopping.")
                break

            period_articles.extend(articles)
            print(f"got {len(articles)} (total: {len(period_articles)})")

            if not has_more:
                print("  No more pages available.")
                break

            page += 1
            time.sleep(1)

        period_articles = period_articles[:RESULTS_PER_PERIOD]
        all_articles.extend(period_articles)
        print(f"  Collected {len(period_articles)} articles for {label}.")

    output_file = "raw_articles.tsv"
    fieldnames = ["snippet_text", "source", "date", "state", "crash_event"]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(all_articles)

    print(f"\nDone! Wrote {len(all_articles)} articles to {output_file}")


if __name__ == "__main__":
    main()
