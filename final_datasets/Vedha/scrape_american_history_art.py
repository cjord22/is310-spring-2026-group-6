#!/usr/bin/env python3
"""
Aggregate open / open-access museum APIs into one normalized dataset, focused on
American-history-related keywords.

Sources:
  - Art Institute of Chicago (AIC):   https://api.artic.edu/docs/
  - The Met Collection:                https://metmuseum.github.io/
  - Cleveland Museum of Art:          https://openaccess-api.clevelandart.org/
  - Harvard Art Museums:              https://harvardartmuseums.org/collections/api (apikey required)

Examples
  pip install -r requirements.txt
  export HARVARD_ART_API_KEY=...   # optional; Harvard is skipped without it

  # See what each API returns (keys, types, small samples)
  python scrape_american_history_art.py --inspect-only

  # Build a combined JSONL file (deduped per source + id)
  python scrape_american_history_art.py --out combined_american_history.jsonl

  # Tighter scrape (faster)
  python scrape_american_history_art.py --max-per-source 40 --sleep-met 0.15
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

import requests

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "american-history-art-aggregator/1.0 (educational research; contact: local script)",
        "Accept": "application/json",
    }
)

# --- American history oriented search phrases (expand / edit freely) ---
DEFAULT_QUERIES = [
    "American history",
    "United States",
    "George Washington",
    "American Revolution",
    "Abraham Lincoln",
    "American Civil War",
    "Colonial America",
    "American West",
]


@dataclass
class NormalizedWork:
    """Single cross-museum row."""

    uid: str
    source: str
    source_object_id: str
    title: str | None
    artist_display: str | None
    date_display: str | None
    medium: str | None
    culture: str | None
    department: str | None
    description: str | None
    image_url: str | None
    iiif_image_id: str | None
    license_or_rights: str | None
    object_url: str | None
    search_queries: list[str] = field(default_factory=list)
    raw_source: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Debugging: show "what does this API give us?"
# ---------------------------------------------------------------------------

def _type_name(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        return "list"
    if isinstance(v, dict):
        return "dict"
    return type(v).__name__


def summarize_json(label: str, obj: Any, max_depth: int = 5, _depth: int = 0) -> list[str]:
    """Return human-readable lines describing structure (keys, types, list lengths)."""
    lines: list[str] = []
    pad = "  " * _depth
    if _depth == 0:
        lines.append(f"=== {label} ===")

    if _depth >= max_depth:
        lines.append(f"{pad}… (max_depth {max_depth})")
        return lines

    if isinstance(obj, Mapping):
        lines.append(f"{pad}dict with {len(obj)} keys: {sorted(obj.keys())[:40]}{' …' if len(obj) > 40 else ''}")
        for k in sorted(obj.keys())[:25]:
            v = obj[k]
            lines.append(f"{pad}  [{k}] {_type_name(v)}")
            if isinstance(v, Mapping):
                lines.extend(summarize_json("", v, max_depth, _depth + 2)[1:])
            elif isinstance(v, Sequence) and not isinstance(v, (str, bytes)):
                lines.append(f"{pad}    list len={len(v)}")
                if v and isinstance(v[0], Mapping):
                    lines.extend(summarize_json("first_item", v[0], max_depth, _depth + 3)[1:])
        if len(obj) > 25:
            lines.append(f"{pad}  … ({len(obj) - 25} more keys omitted)")
        return lines

    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
        lines.append(f"{pad}list len={len(obj)}")
        if obj:
            lines.append(f"{pad}  first element: {_type_name(obj[0])}")
            if isinstance(obj[0], Mapping):
                lines.extend(summarize_json("first_element", obj[0], max_depth, _depth + 2)[1:])
        return lines

    lines.append(f"{pad}scalar {_type_name(obj)} sample: {repr(obj)[:120]}")
    return lines


def print_json_sample(label: str, obj: Any, max_chars: int = 2500) -> None:
    try:
        s = json.dumps(obj, indent=2, ensure_ascii=False)[:max_chars]
    except (TypeError, ValueError):
        s = repr(obj)[:max_chars]
    print(f"\n--- {label} (JSON sample, truncated) ---\n{s}\n")


def print_normalized_table_preview(rows: list[NormalizedWork], limit: int = 8) -> None:
    """Tabular preview of the normalized columns."""
    cols = [
        "source",
        "source_object_id",
        "title",
        "artist_display",
        "date_display",
        "image_url",
        "object_url",
        "license_or_rights",
    ]
    print("\n=== Normalized column preview (first rows) ===")
    print(" | ".join(cols))
    for r in rows[:limit]:
        d = asdict(r)
        print(" | ".join([(d.get(c) or "")[:80] for c in cols]))


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def http_get_json(url: str, params: dict[str, Any] | None = None) -> Any:
    r = SESSION.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Fetchers → NormalizedWork
# ---------------------------------------------------------------------------

def artic_search(
    query: str,
    limit: int,
    *,
    only_public_domain: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """https://api.artic.edu/api/v1/artworks/search"""
    url = "https://api.artic.edu/api/v1/artworks/search"
    params: dict[str, Any] = {
        "q": query,
        "limit": limit,
        # Search hits are sparse unless you ask for fields (see api.artic.edu docs).
        "fields": ",".join(
            [
                "id",
                "title",
                "artist_display",
                "date_display",
                "image_id",
                "is_public_domain",
                "medium_display",
                "department_title",
                "thumbnail_alt_text",
                "artwork_type_title",
            ]
        ),
    }
    if only_public_domain:
        # Bracket syntax from AIC docs, e.g.
        # .../search?q=cats&query[term][is_public_domain]=true
        params["query[term][is_public_domain]"] = "true"
    data = http_get_json(url, params=params)
    artworks = data.get("data") or []
    return artworks, data


def artic_build_iiif_url(config: Mapping[str, Any], image_id: str | None) -> str | None:
    if not image_id:
        return None
    base = (config.get("iiif_url") or "").rstrip("/") + "/"
    if not base:
        return None
    # IIIF Image API 2 request; tweak size if you want max res.
    return f"{base}{image_id}/full/!2000,2000/0/default.jpg"


def normalize_artic_records(
    payload: Mapping[str, Any], query: str
) -> list[NormalizedWork]:
    config = payload.get("config") or {}
    out: list[NormalizedWork] = []
    for aw in payload.get("data") or []:
        if not isinstance(aw, Mapping):
            continue
        aw_id = aw.get("id")
        image_id = aw.get("image_id")
        title = aw.get("title")
        nw = NormalizedWork(
            uid=str(uuid.uuid4()),
            source="artic",
            source_object_id=str(aw_id) if aw_id is not None else "",
            title=title,
            artist_display=aw.get("artist_display"),
            date_display=aw.get("date_display"),
            medium=aw.get("medium_display") or aw.get("artwork_type_title"),
            culture=None,
            department=aw.get("department_title"),
            description=aw.get("thumbnail_alt_text"),
            image_url=artic_build_iiif_url(config, image_id) if isinstance(image_id, str) else None,
            iiif_image_id=image_id if isinstance(image_id, str) else None,
            license_or_rights="public_domain" if aw.get("is_public_domain") else None,
            object_url=f"https://www.artic.edu/artworks/{aw_id}" if aw_id is not None else None,
            search_queries=[query],
            raw_source=dict(aw),
        )
        out.append(nw)
    return out


def met_search_ids(query: str, limit: int) -> tuple[list[int], dict[str, Any]]:
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    data = http_get_json(url, {"q": query, "hasImages": True})
    ids = list(data.get("objectIDs") or [])[:limit]
    return ids, data


def met_object(object_id: int) -> dict[str, Any]:
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    data = http_get_json(url)
    if not isinstance(data, dict):
        return {}
    return data


def normalize_met_objects(ids: Sequence[int], query: str, sleep_s: float) -> list[NormalizedWork]:
    out: list[NormalizedWork] = []
    for oid in ids:
        time.sleep(sleep_s)
        try:
            ob = met_object(int(oid))
        except requests.HTTPError:
            continue
        if ob.get("message") == "Not a valid object":
            continue
        nw = NormalizedWork(
            uid=str(uuid.uuid4()),
            source="met",
            source_object_id=str(ob.get("objectID", oid)),
            title=ob.get("title"),
            artist_display=ob.get("artistDisplayName"),
            date_display=ob.get("objectDate"),
            medium=ob.get("medium"),
            culture=ob.get("culture"),
            department=ob.get("department"),
            description=None,
            image_url=ob.get("primaryImage") or ob.get("primaryImageSmall"),
            iiif_image_id=None,
            license_or_rights="CC0 / Met Open Access" if ob.get("isPublicDomain") else ob.get("rightsAndReproduction"),
            object_url=ob.get("objectURL"),
            search_queries=[query],
            raw_source=ob,
        )
        out.append(nw)
    return out


def cma_search(query: str, limit: int, *, cc0_only: bool = True) -> dict[str, Any]:
    url = "https://openaccess-api.clevelandart.org/api/artworks/"
    params: dict[str, Any] = {"q": query, "limit": limit, "skip": 0}
    if cc0_only:
        params["cc0"] = "1"
    return http_get_json(url, params=params)


def normalize_cma_payload(payload: Mapping[str, Any], query: str) -> list[NormalizedWork]:
    out: list[NormalizedWork] = []
    for row in payload.get("data") or []:
        if not isinstance(row, Mapping):
            continue
        creators = row.get("creators") or []
        artist_bits: list[str] = []
        if isinstance(creators, list):
            for c in creators:
                if isinstance(c, Mapping) and c.get("description"):
                    artist_bits.append(str(c["description"]))
        images = row.get("images") or {}
        img_url = None
        if isinstance(images, Mapping):
            web = images.get("web")
            if isinstance(web, Mapping) and web.get("url"):
                img_url = web["url"]
            elif isinstance(images.get("print"), Mapping):
                img_url = images["print"].get("url")
        cul = row.get("culture")
        culture_s = None
        if isinstance(cul, list) and cul:
            culture_s = "; ".join(str(x) for x in cul[:5])
        elif isinstance(cul, str):
            culture_s = cul

        rid = row.get("id")
        nw = NormalizedWork(
            uid=str(uuid.uuid4()),
            source="cma",
            source_object_id=str(rid) if rid is not None else "",
            title=row.get("title"),
            artist_display="; ".join(artist_bits) if artist_bits else None,
            date_display=row.get("creation_date"),
            medium=row.get("technique"),
            culture=culture_s,
            department=row.get("department"),
            description=row.get("tombstone"),
            image_url=img_url,
            iiif_image_id=None,
            license_or_rights=row.get("share_license_status") or row.get("copyright"),
            object_url=row.get("url"),
            search_queries=[query],
            raw_source=dict(row),
        )
        out.append(nw)
    return out


def harvard_search(
    apikey: str,
    keyword: str,
    size: int,
    *,
    has_image: bool = True,
) -> dict[str, Any]:
    url = "https://api.harvardartmuseums.org/object"
    params: dict[str, Any] = {
        "apikey": apikey,
        "keyword": keyword,
        "size": min(max(size, 1), 100),
        "page": 1,
        # Ask for usable columns in the list response to avoid N detail calls when possible.
        "fields": (
            "objectid,id,title,people,dated,medium,culture,department,"
            "primaryimageurl,url,copyright,description,commentary"
        ),
    }
    if has_image:
        params["hasimage"] = 1
    return http_get_json(url, params=params)


def harvard_object_detail(apikey: str, object_id: int) -> dict[str, Any]:
    url = f"https://api.harvardartmuseums.org/object/{int(object_id)}"
    return http_get_json(url, {"apikey": apikey})


def normalize_harvard_records(
    payload: Mapping[str, Any],
    query: str,
    apikey: str,
    *,
    fetch_full: bool,
    skip_detail: bool,
    sleep_s: float,
) -> list[NormalizedWork]:
    out: list[NormalizedWork] = []
    for rec in payload.get("records") or []:
        if not isinstance(rec, Mapping):
            continue
        oid = rec.get("objectid") or rec.get("id")
        if oid is None:
            continue

        need_detail = (not skip_detail) and (fetch_full or not rec.get("title"))
        src: Mapping[str, Any] = rec
        if need_detail:
            time.sleep(sleep_s)
            try:
                src = harvard_object_detail(apikey, int(oid))
            except requests.HTTPError:
                src = rec

        people = src.get("people") or []
        names: list[str] = []
        if isinstance(people, list):
            for p in people:
                if isinstance(p, Mapping):
                    nm = p.get("displayname") or p.get("name")
                    if nm:
                        names.append(str(nm))

        title = src.get("title")
        nw = NormalizedWork(
            uid=str(uuid.uuid4()),
            source="harvard",
            source_object_id=str(oid),
            title=title if isinstance(title, str) else None,
            artist_display="; ".join(names) if names else None,
            date_display=src.get("dated"),
            medium=src.get("medium"),
            culture=src.get("culture"),
            department=src.get("department"),
            description=(src.get("description") or src.get("commentary") or None),
            image_url=src.get("primaryimageurl"),
            iiif_image_id=None,
            license_or_rights=src.get("copyright"),
            object_url=src.get("url"),
            search_queries=[query],
            raw_source=dict(src) if isinstance(src, Mapping) else {},
        )
        out.append(nw)
    return out


# ---------------------------------------------------------------------------
# Inspect-only: one small call per API
# ---------------------------------------------------------------------------

def run_inspect(harvard_key: str | None) -> None:
    print("\n*** INSPECT MODE: one sample request per API ***\n")

    # --- AIC ---
    try:
        artworks, artic_payload = artic_search("George Washington", limit=1)
        print("\n".join(summarize_json("artic /artworks/search root", artic_payload, max_depth=4)))
        if artworks:
            print("\n".join(summarize_json("artic first artwork", artworks[0], max_depth=5)))
        print_json_sample("artic full search payload", artic_payload)
    except requests.RequestException as e:
        print(f"[artic] request failed: {e}", file=sys.stderr)

    # --- Met ---
    try:
        ids, met_search_payload = met_search_ids("american history", limit=5)
        print("\n".join(summarize_json("met /search root", met_search_payload, max_depth=4)))
        if ids:
            ob = met_object(ids[0])
            print("\n".join(summarize_json("met first object detail", ob, max_depth=4)))
            print_json_sample("met object detail", ob)
        else:
            print("[met] search returned no IDs for sample query.")
    except requests.RequestException as e:
        print(f"[met] request failed: {e}", file=sys.stderr)

    # --- Cleveland ---
    try:
        cma_payload = cma_search("America", limit=1)
        print("\n".join(summarize_json("cma /api/artworks root", cma_payload, max_depth=4)))
        rows = cma_payload.get("data") or []
        if rows:
            print("\n".join(summarize_json("cma first artwork", rows[0], max_depth=5)))
        print_json_sample("cma full payload", cma_payload)
    except requests.RequestException as e:
        print(f"[cma] request failed: {e}", file=sys.stderr)

    # --- Harvard ---
    if not harvard_key:
        print("\n[harvard] skipped (set HARVARD_ART_API_KEY or pass --harvard-key).")
    else:
        try:
            hpayload = harvard_search(harvard_key, "American history", size=3)
            print("\n".join(summarize_json("harvard /object root", hpayload, max_depth=4)))
            recs = hpayload.get("records") or []
            if recs:
                print("\n".join(summarize_json("harvard first list record", recs[0], max_depth=5)))
                oid = recs[0].get("objectid") or recs[0].get("id")
                if oid:
                    detail = harvard_object_detail(harvard_key, int(oid))
                    print("\n".join(summarize_json("harvard object detail", detail, max_depth=4)))
                    print_json_sample("harvard object detail", detail)
            else:
                print_json_sample("harvard list payload", hpayload)
        except requests.RequestException as e:
            print(f"[harvard] request failed: {e}", file=sys.stderr)


def dedupe(rows: list[NormalizedWork]) -> list[NormalizedWork]:
    seen: set[tuple[str, str]] = set()
    out: list[NormalizedWork] = []
    for r in rows:
        key = (r.source, r.source_object_id)
        if key in seen or not r.source_object_id:
            continue
        seen.add(key)
        out.append(r)
    return out


def write_jsonl(path: str, rows: Sequence[NormalizedWork]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            d = asdict(r)
            if isinstance(d.get("raw_source"), dict):
                # Keep JSON serializable (Harvard dates etc.)
                d["raw_source"] = json.loads(json.dumps(d["raw_source"], default=str))
            f.write(json.dumps(d, ensure_ascii=False) + "\n")


def write_csv(path: str, rows: Sequence[NormalizedWork]) -> None:
    cols = list(NormalizedWork.__dataclass_fields__.keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            d = asdict(r)
            d["search_queries"] = "|".join(d["search_queries"])
            d["raw_source"] = json.dumps(d["raw_source"], ensure_ascii=False, default=str)
            w.writerow(d)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--inspect-only", action="store_true", help="Print API shapes + samples, no full scrape.")
    ap.add_argument("--out", default="combined_american_history.jsonl", help="Output JSONL path.")
    ap.add_argument("--csv-out", default=None, help="Optional CSV path (raw JSON in raw_source column).")
    ap.add_argument("--queries", nargs="*", default=DEFAULT_QUERIES, help="Search strings (per source).")
    ap.add_argument(
        "--max-per-source",
        type=int,
        default=200,
        help="Max records to keep per museum after dedupe (Artic, Met, CMA, Harvard each capped here).",
    )
    ap.add_argument(
        "--per-query-limit",
        type=int,
        default=60,
        help="Hits to request per query & source (raise if a source ends under --max-per-source after dedupe).",
    )
    ap.add_argument(
        "--sleep-met",
        type=float,
        default=0.25,
        help="Delay between Met object detail fetches (seconds); higher is friendlier when pulling many IDs.",
    )
    ap.add_argument("--harvard-fetch-full", action="store_true", help="Always GET /object/{id} for Harvard (slow, richest fields).")
    ap.add_argument(
        "--harvard-no-detail",
        action="store_true",
        help="Use Harvard list rows only (no per-object detail calls; may omit some titles).",
    )
    ap.add_argument("--harvard-sleep", type=float, default=0.15, help="Delay for Harvard detail fetches.")
    ap.add_argument("--harvard-key", default=os.environ.get("HARVARD_ART_API_KEY"), help="Harvard apikey (or env HARVARD_ART_API_KEY).")
    ap.add_argument("--include-artic-non-pd", action="store_true", help="Disable is_public_domain filter for AIC.")
    ap.add_argument("--cma-no-cc0-filter", action="store_true", help="Do not restrict Cleveland to cc0=1.")
    args = ap.parse_args()

    hkey: str | None = args.harvard_key

    if args.inspect_only:
        run_inspect(hkey)
        return

    merged: list[NormalizedWork] = []
    errors: list[str] = []

    # AIC — one search per query, cap total later
    for q in args.queries:
        try:
            _, payload = artic_search(
                q,
                args.per_query_limit,
                only_public_domain=not args.include_artic_non_pd,
            )
            merged.extend(normalize_artic_records(payload, q))
        except requests.RequestException as e:
            errors.append(f"artic[{q}]: {e}")

    # Met — search returns IDs; detail per object
    for q in args.queries:
        try:
            ids, _sp = met_search_ids(q, args.per_query_limit)
            merged.extend(normalize_met_objects(ids, q, args.sleep_met))
        except requests.RequestException as e:
            errors.append(f"met[{q}]: {e}")

    # Cleveland
    for q in args.queries:
        try:
            payload = cma_search(q, args.per_query_limit, cc0_only=not args.cma_no_cc0_filter)
            merged.extend(normalize_cma_payload(payload, q))
        except requests.RequestException as e:
            errors.append(f"cma[{q}]: {e}")

    # Harvard
    if hkey:
        for q in args.queries:
            try:
                payload = harvard_search(hkey, q, size=args.per_query_limit)
                merged.extend(
                    normalize_harvard_records(
                        payload,
                        q,
                        hkey,
                        fetch_full=args.harvard_fetch_full,
                        skip_detail=args.harvard_no_detail,
                        sleep_s=args.harvard_sleep,
                    )
                )
            except requests.RequestException as e:
                errors.append(f"harvard[{q}]: {e}")
    else:
        errors.append("harvard: skipped (no API key)")

    # Dedupe + cap per source
    merged = dedupe(merged)
    per_source: dict[str, list[NormalizedWork]] = {}
    for r in merged:
        per_source.setdefault(r.source, []).append(r)

    trimmed: list[NormalizedWork] = []
    for src, lst in per_source.items():
        trimmed.extend(lst[: args.max_per_source])

    trimmed = dedupe(trimmed)
    trimmed.sort(key=lambda x: (x.source, x.source_object_id))

    write_jsonl(args.out, trimmed)
    if args.csv_out:
        write_csv(args.csv_out, trimmed)

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "queries": args.queries,
        "record_count": len(trimmed),
        "per_source_counts": {s: sum(1 for r in trimmed if r.source == s) for s in sorted({r.source for r in trimmed})},
        "errors": errors,
        "outputs": {"jsonl": os.path.abspath(args.out), "csv": os.path.abspath(args.csv_out) if args.csv_out else None},
    }
    meta_path = args.out.replace(".jsonl", "_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    print(f"Wrote {len(trimmed)} rows → {args.out}")
    print(f"Meta → {meta_path}")
    if errors:
        print("Warnings:")
        for e in errors:
            print(f"  - {e}")

    print_normalized_table_preview(trimmed)


if __name__ == "__main__":
    main()
