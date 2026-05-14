# Codebook — Pro vs Anti Immigration Law Classification

**Schema version:** `v1`
**Last updated:** 2026-05-02
**Scope:** State-level immigration legislation in IL, CA, AZ, 2008–2026, sourced from the NCSL Immigration Legislation Archived Database.

This codebook defines every field the LLM is asked to extract from a law's full text. It is the methodological reference for the dataset and the source-of-truth definition for the JSON Schema used to constrain LLM outputs.

---

## How extraction works

For each law:

1. The full text of the bill (not a summary) is fetched and stored in `data/bill_texts/{bill_id}.txt`.
2. The bill text is sent to one or more LLMs along with this codebook (or a condensed prompt-friendly form of it) and a JSON Schema.
3. The LLM is forced (via tool-use / structured output) to return a JSON object matching the schema.
4. If two or more models are configured, outputs are reconciled: agreement = consensus, disagreement = `needs_human_review = True`.
5. A stratified sample (default 20%) is hand-validated by the researcher to compute human-vs-LLM agreement.

The pipeline is **modular** — it works with one model or many. Multi-model is a reliability check, not a requirement.

---

## Field reference

All 15 LLM-extracted fields below are **required** in every output. No nulls.

### 1. `stance`


PERSONAL DECISION 

"""The law's overall posture toward immigrants and immigration enforcement.

| Value | Definition |
|---|---|
| `Pro` | Expands rights, protections, access, or due process for immigrants; restricts state cooperation with federal immigration enforcement; limits criminalization of immigration status. |
| `Anti` | Expands enforcement against immigrants; restricts immigrant rights, access, or eligibility; increases penalties tied to immigration status; deepens state cooperation with federal immigration enforcement. |
| `Neutral` | Touches immigration topics procedurally without favoring either direction. Examples: technical definitions, generic appropriations with no substantive immigration provision, baseline humanitarian aid that neither expands nor restricts. |
| `Mixed` | Substantive provisions in **both** directions in the same bill (e.g., funding for victim services bundled with ICE-cooperation funding). Use when neither direction clearly dominates. |

**Decision rule when uncertain:** if a law restricts ICE cooperation OR protects sensitive locations OR expands benefits → `Pro`. If it adds criminal penalties tied to immigration OR expands enforcement powers OR restricts benefits → `Anti`. Use `Mixed` only when both apply with comparable weight."""

### 2. `binding_effect`

| Value | Definition |
|---|---|
| `Binding` | Enacts statute, amends code, allocates enforceable funding, or otherwise has legal force. |
| `Non-binding` | Resolution expressing condemnation, support, or request without changing law. House/Senate Resolutions (HR, SR) are usually non-binding; bills (H, S, A, AB, SB) are usually binding. |

### 3. `enforcement_teeth`

The strongest enforcement mechanism present.

| Value | Definition |
|---|---|
| `None` | Aspirational, symbolic, or declaratory only. |
| `Funding` | Sole mechanism is allocating or withholding money. |
| `Civil` | Civil penalties, private right of action, or agency civil-enforcement authority. |
| `Criminal` | Creates or modifies a criminal offense or criminal penalty. |

If multiple apply, pick the strongest (`Criminal` > `Civil` > `Funding` > `None`).

### 4. `legal_mechanism`

What the law structurally does.

| Value | Definition |
|---|---|
| `Mandate` | Requires an action by an agency, official, or institution. |
| `Prohibition` | Forbids an action. |
| `Funding` | Appropriates or withholds money as the primary lever. |
| `Reporting` | Imposes a reporting / disclosure / data-collection requirement. |
| `Symbolic` | Statement of position with no operative requirement. |

### 5. `primary_policy_area` (single) and 6. `policy_areas[]` (multi)

Both draw from the same controlled vocabulary. `primary_policy_area` is the dominant focus of the bill; `policy_areas` is all areas it materially touches (must include `primary_policy_area`).

Vocabulary:

- `Law Enforcement` — police, sheriffs, ICE cooperation, 287(g), detainers, sanctuary policies
- `Education` — K-12, postsecondary, school enrollment, in-state tuition, school-site enforcement
- `Employment & E-Verify` — work authorization, hiring practices, E-Verify mandates
- `Health & Public Benefits` — Medicaid, public assistance, eligibility for state programs
- `Driver's Licenses & IDs` — driver's licenses, state IDs, REAL ID interactions
- `Detention` — civil immigration detention, detention facility standards, contracts
- `Court & Due Process` — court procedure, evidence rules, public defender access, post-conviction relief
- `Housing` — landlord-tenant, housing discrimination on immigration status
- `Human Trafficking` — trafficking-specific provisions touching immigrants
- `Refugees & Asylum` — refugee resettlement, asylum-seeker support
- `Voting / Civic` — voter ID, citizenship verification, civic participation
- `Appropriations` — budget bills with immigration line-items
- `Symbolic / Resolution` — non-binding resolutions whose subject IS immigration

### 7. `affected_population[]`

Multi-select. Who the law's substantive provisions apply to. Pick all that apply.

- `Undocumented` — people without lawful status
- `DACA/Dreamers` — DACA recipients, undocumented youth specifically
- `Refugees/Asylees` — those with refugee or asylum status
- `Mixed-status families` — households spanning statuses
- `All immigrants` — applies regardless of status (e.g., U-visa holders, LPRs, undocumented all together)
- `Crime victims` — victims/witnesses (often U-visa adjacent)
- `Children/Students` — minors, K-12, postsecondary

### 8. `creates_private_right_of_action` (bool)

True if the law authorizes a private party to bring civil suit for violations. Look for language like "any person aggrieved may bring a civil action," "civil cause of action," "may seek damages."

### 9. `restricts_ice_cooperation` (bool)

True if the law limits state/local cooperation with federal immigration enforcement (ICE, CBP, DHS). Includes detainer prohibitions, 287(g) limits, information-sharing restrictions, sensitive-location protections from federal agents.

### 10. `protects_sensitive_locations` (bool)

True if the law explicitly limits immigration enforcement at schools, hospitals, courthouses, places of worship, or shelters.

### 11. `affects_drivers_licenses` (bool)

True if the law modifies who may obtain a driver's license / state ID, what data is collected, or who that data may be shared with for immigration purposes.

### 12. `affects_public_benefits`

| Value | Definition |
|---|---|
| `Expands` | Broadens eligibility or access for immigrants. |
| `Restricts` | Narrows eligibility or imposes new barriers. |
| `N/A` | Bill does not touch public benefits. |

### 13. `mentions_287g_or_sanctuary` (bool)

True if the bill text references "287(g)," "sanctuary," "sanctuary city/jurisdiction/policy," or substantively addresses such agreements.

### 14. `immigrant_framing`

How the bill linguistically frames immigrants. This is a **textual feature** of the bill's language, separate from `stance`.

| Value | Definition |
|---|---|
| `Victim` | Frames immigrants as victims (of crime, of federal overreach, of trafficking). |
| `Threat` | Frames immigrants as a public-safety, fiscal, or security threat. |
| `Worker` | Frames immigrants primarily through their labor/economic role. |
| `Family` | Frames immigrants through family unity / household. |
| `Neutral` | No clear frame; technical or procedural language. |

### 15. `one_sentence_summary`

Free text, ≤25 words. A plain-language summary of what the law actually does. This is the only free-text LLM-judgment field; it exists for human readability and is **not used** for downstream analysis.

---

## Edge cases

- **Appropriations bills.** A bill that simply lists budget line-items is `Neutral` unless an item materially expands or restricts immigration enforcement / immigrant access. If it funds, e.g., the AZ Department of Emergency and Military Affairs with explicit immigration-enforcement carve-outs → `Anti` with `enforcement_teeth = Funding`.
- **Resolutions condemning federal action.** Non-binding by definition, `binding_effect = Non-binding`, `enforcement_teeth = None`. Stance follows the direction of the condemnation: condemning ICE raids → `Pro`. Condemning a state AG who criticized ICE → `Anti`.
- **"Mixed" stance.** Reserve for laws with comparable provisions in both directions. A bill that's 90% pro with one minor anti carve-out is still `Pro`. Mark mixed only when neither direction clearly dominates.
- **Bills already enacted vs. introduced.** `status` (metadata) tracks this. The codebook fields describe what the bill says, not whether it took effect.

---

## Worked examples (drawn from the existing dataset)

### Example 1 — `CA-2025-A49` (CA A 49 — Schoolsites: Immigration Enforcement)

> "Prohibits school officials from allowing immigration enforcement officers to enter nonpublic areas of school sites without a valid judicial warrant; school officials not allowed to hand over and share information about student immigrants."

| Field | Value |
|---|---|
| `stance` | `Pro` |
| `binding_effect` | `Binding` |
| `enforcement_teeth` | `Civil` |
| `legal_mechanism` | `Prohibition` |
| `primary_policy_area` | `Education` |
| `policy_areas` | `[Education, Law Enforcement]` |
| `affected_population` | `[Children/Students, Undocumented]` |
| `creates_private_right_of_action` | likely `false` (not stated in description) |
| `restricts_ice_cooperation` | `true` |
| `protects_sensitive_locations` | `true` |
| `affects_drivers_licenses` | `false` |
| `affects_public_benefits` | `N/A` |
| `mentions_287g_or_sanctuary` | unknown without full text — `false` if not present |
| `immigrant_framing` | `Family` (children/students as protected family members) |

### Example 2 — `AZ-2026-SR1036` (AZ SR 1036 — Disapproval of AG Statements)

> "Arizona Senate calling out their state's AG for making public statements about resisting ICE; demands retract and resign."

| Field | Value |
|---|---|
| `stance` | `Anti` |
| `binding_effect` | `Non-binding` |
| `enforcement_teeth` | `None` |
| `legal_mechanism` | `Symbolic` |
| `primary_policy_area` | `Symbolic / Resolution` |
| `policy_areas` | `[Symbolic / Resolution, Law Enforcement]` |
| `affected_population` | `[All immigrants]` |
| `creates_private_right_of_action` | `false` |
| `restricts_ice_cooperation` | `false` |
| `protects_sensitive_locations` | `false` |
| `affects_drivers_licenses` | `false` |
| `affects_public_benefits` | `N/A` |
| `mentions_287g_or_sanctuary` | depends on text |
| `immigrant_framing` | `Threat` (resisting ICE framed as public-safety problem) |

---

## Reproducibility

Every extracted row carries provenance:

- `model_used` — exact model id (e.g., `claude-opus-4-7`)
- `schema_version` — bumps when this codebook changes
- `extraction_timestamp`
- `prompt_hash` — hash of the system prompt + user prompt template at time of call

If extraction logic changes mid-project, old rows remain valid under their original `schema_version` and can be re-run on demand.
