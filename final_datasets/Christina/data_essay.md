# Culture as Data Essay
## Stock Market Crash Media Coverage Dataset
**Christina Jordan**
**May 15, 2026**

---

## Introduction

This essay tells the story of a dataset I built over the course of a semester: a structured collection of newspaper snippets documenting how American print media covered stock market crashes across three historical periods — the 1929 Black Thursday crash, the 1937 recession crash, and the 1962 Flash Crash. The dataset began as 60 rows of carefully hand-coded material drawn from the Library of Congress's Chronicling America archive and grew, through computational augmentation, to 660 rows. What follows is an account of how I made it, what it represents, what it reveals, and — just as importantly — what it conceals.

---

## The Cultural Material and Why It Matters

The primary source material is the American newspaper article, accessed through Chronicling America's full-text search interface. Specifically, the dataset is built from OCR-extracted text snippets returned when querying the phrase "stock market crash." These are not full articles. They are fragments — roughly 100 to 500 characters of body text surrounding the search term — and that fragmentary quality is itself a feature of the archive worth understanding.

I chose newspapers as my cultural material because they are not neutral records of financial events. They frame crises, assign blame, express anxiety or reassurance, and shape how ordinary readers come to understand economic catastrophe. A newspaper does not simply report that the market crashed; it tells readers how to feel about it, who is responsible, and whether to expect recovery. Studying this framing at scale — across years, papers, and crash events — opens up questions that neither economic history nor close literary reading can fully answer on their own. What was the emotional register of crash coverage? Did media tone shift between the moment of crisis and retrospective reporting? Whose voices dominated the explanation of what happened?

The decision to focus on stock market crashes as a recurring cultural form, rather than any single event, reflects a theoretical bet: that the crash is not just an economic event but a cultural script that American media has replayed and revised across the twentieth century. The 1937 coverage already invokes 1929. The 1962 coverage calls back to Black Thursday. Each crash is understood through the ones that came before it.

---

## Approach: Creating Data from Scratch

I took a create-from-scratch approach. Chronicling America is an existing archive, but no structured dataset of crash-related newspaper coverage with interpretive annotations — tone, framing, causal attribution — existed. I created that structure myself, first through manual close reading and then through computational scaling.

This choice came with real costs. Every decision I made about what to capture, how to name columns, and how to define categories was mine alone, which means the dataset embeds my interpretive assumptions at every level. A different researcher asking the same questions might have built a meaningfully different dataset. That is not a flaw unique to this project; it is a condition of all data work that usually goes undocumented. Part of what this project tries to do is make those assumptions visible.

---

## How Computation Shaped the Dataset

### Phase One: Bespoke Manual Creation

The first 60 rows were coded entirely by hand. I pasted Chronicling America search results into a working document, read each snippet, and made judgment calls about tone, causal framing, and the presence of recovery language or numeric figures. This process was slow and often ambiguous. What counts as "mentioning recovery" — a politician's prediction that things will improve? A confirmed statistic? A reader's letter expressing hope? I resolved these questions one snippet at a time, developing tacit rules that I could not fully articulate until I had to automate them.

One significant error occurred early in the process. When I first asked Claude (Anthropic's AI assistant) to help structure the data, it generated plausible-sounding but entirely fabricated headlines for each row. None of these headlines existed. A simple Google search returned zero results for them, which is how the fabrication was discovered. The dataset had to be rebuilt from scratch using only verbatim OCR text from the search results. This incident became one of the most instructive moments of the semester: LLMs fill gaps confidently rather than flagging uncertainty. They produce outputs that look like data without being data. Human verification is not optional.

The column `snippet_text` — not `headline_text` — is a direct consequence of this lesson. Renaming the column was a methodological decision: it forces any future user of this dataset to understand that they are reading a fragment of body text, not an editorial title. The name is honest about what the data actually contains.

### Phase Two: Computational Scaling

After the manual phase, I used two tools to scale the dataset to 660 rows.

**Chronicling America API (loc.gov):** I wrote a Python script to query the Library of Congress's JSON API for "stock market crash" across each crash period, paginating through results and extracting snippet text, source title, date, and state metadata automatically. This process surfaced 600 additional rows with no manual reading required. The API is public and requires no authentication.

One technical complication arose: the legacy Chronicling America API (chroniclingamerica.loc.gov) was retired in 2025 and replaced by a new endpoint (www.loc.gov/collections/chronicling-america/). The original script failed with 404 errors until the URL and parameter structure were updated. This kind of infrastructure change — an archive silently retiring its API — is exactly the type of technical fragility that is invisible when you download a dataset someone else made but highly visible when you build your own.

**Keyword-based rule classifier:** Rather than using a paid LLM API for classification, I wrote a Python script that applies explicit keyword rules to each snippet to assign values for `media_tone`, `mentions_recovery`, `mentions_numeric`, and `mentions_cause`. For example, a snippet containing words like "suicide," "panic," "ruin," or "predatory" is classified as Negative; one containing "recovery," "confidence," or "stable" is classified as Positive. The full keyword lists are documented in `classify_articles.py` and are entirely transparent — every classification decision is traceable to an explicit rule.

This approach has real advantages for a project concerned with methodological transparency. Unlike an LLM classifier, the keyword rules do not change between runs, do not hallucinate, and can be audited by anyone. Their limitation is that they are brittle: they cannot detect irony, cannot distinguish a denial from an assertion ("the crash was not caused by speculation" would incorrectly flag `mentions_cause` as Yes), and cannot handle context. These are known tradeoffs documented in the dataset.

The final dataset includes a `coding_method` column that flags each row as either `manual` or `computational`, making the two phases of production traceable throughout.

---

## Key Decisions, Exclusions, and Tensions

### What I Included and Excluded

I included any snippet where "stock market crash" appeared in a context that revealed something about how the crash was being framed, explained, or responded to. I excluded snippets where the phrase appeared purely incidentally — a weather article that compared a cold snap to the crash, for instance — and snippets too fragmentary to code any column reliably.

One inclusion I flagged as borderline: a Provident Mutual Life Insurance advertisement from the Evening Star (November 26, 1929) using "STOCK MARKET CRASH!" as a headline. I kept it because it demonstrates how the crash was immediately mobilized for commercial purposes — a real cultural finding — but it is not journalism, and a downstream researcher treating all rows as news articles would be misled.

### The Tone Classification Problem

`media_tone` was the most contested column. The hardest cases were snippets describing suicides or financial ruin in a flat, matter-of-fact register — neutral in tone but deeply negative in content. I coded by content rather than rhetorical register, which means my Negative category mixes genuine alarm with clinical reportage. A more refined schema might separate *event valence* from *authorial tone*, but doing so consistently across 660 rows would have required more granular rules than I could reliably apply or automate.

### The Ethics of Suicide as a Data Point

Multiple rows in this dataset record suicides — people who died by suicide after losing money in the crash. In the dataset, these appear as rows with `media_tone: Negative`, `mentions_cause: No`, `mentions_recovery: No`. The act of coding a person's death as a data point is not neutral. It reduces a human life to a categorical observation. I have not resolved this tension, but I want to name it explicitly: the dataset contains human suffering that the schema does not adequately represent, and any analysis that treats these rows purely as instances of a category is doing something ethically incomplete.

---

## What the Data Reveals

Even at 660 rows, several patterns emerge that would not have been visible through close reading of individual articles.

**Tone distribution:** Of the 660 rows, 315 (47.7%) were classified as Neutral, 214 (32.4%) as Negative, and 131 (19.8%) as Positive. The relatively high Neutral proportion reflects the limits of keyword classification — many snippets are descriptive without being evaluative, and the classifier defaults to Neutral when neither keyword list fires. Among the manually coded rows, Negative is more dominant, which suggests the keyword rules may be undercounting negativity in the computational rows.

**Causal attribution is rare but contested:** Only 94 rows (14.2%) were classified as explicitly mentioning a cause. Among those that do, the causes named are strikingly fragmented: the Federal Reserve, Democratic party chairman Raskob, foreign investors liquidating American securities, speculative excess, and systemic overproduction all appear as explanations — often in the same week, in competing papers. This fragmentation of blame is itself a cultural finding. It suggests that the meaning of a financial crash is not settled by the event itself but is actively constructed through a competitive interpretive process in the press.

**Recovery mentions are scarce:** Only 47 rows (7.1%) mention recovery. The concentration of these rows in early 1930 — the brief window when officials like Secretary of Commerce Lamont were insisting the worst had passed — and in 1962 post-crash commentary, suggests that recovery framing is temporally specific and politically motivated rather than evenly distributed across coverage.

**Source diversity is limited:** The Evening Star (Washington, D.C.) dominates the dataset, particularly in the computational rows. This reflects the archive's digitization priorities, not the actual distribution of American newspaper coverage. The Daily Worker (Chicago) is a notable outlier — its snippets consistently frame the crash as evidence of systemic capitalism failing workers, a framing that is invisible if you analyze only tone but becomes significant when reading `mentions_cause` alongside `source`. A dataset that did not preserve source information would lose this entirely.

---

## What the Data Conceals

The dataset's limitations are as important as its findings.

**The archive's structural absences:** Chronicling America's digitized collection is not a representative sample of American newspaper coverage. It overrepresents large urban dailies and underrepresents the Black press, Spanish-language papers, rural weeklies, and labor papers. Scaling within this archive scales those absences. A researcher using this dataset to make claims about "American newspaper coverage" would be making claims about a particular subset of that coverage — predominantly white, urban, and English-language.

**Post-1963 crashes are missing:** The Chronicling America archive ends around 1963, which means the 1987 Black Monday crash, the 2000 dot-com collapse, the 2008 financial crisis, and the 2020 COVID crash are not represented. The dataset's scope is therefore limited to a period before the digitization of the daily press, which is also a period before television and the internet transformed financial news. Any comparison of tone across crash events must account for the fact that the media landscape itself changed fundamentally between 1929 and 2008.

**OCR errors are uncorrected:** The snippet text contains OCR artifacts — broken words, garbled characters, missing spaces — that are features of the archive's digitization process, not the original newspaper. Some of these errors may affect classification: a snippet where "recovery" appears as "recov ery" due to OCR splitting would not be caught by the keyword classifier.

**Scale flattens close reading:** The most important thing lost in scaling from 60 to 660 rows is the ability to read each snippet carefully. The insurance advertisement, the suicide reports, the ideological specificity of the Daily Worker — these became visible only through close reading. Automated classification treats all 660 rows equivalently. What gets lost is precisely the kind of interpretive attention that makes cultural data analysis different from counting.

---

## Situating This Work in Broader Scholarship

This project sits at the intersection of several scholarly conversations.

The foundational insight driving the schema design — that newspapers do not merely report events but frame them, assign blame, and construct meaning — draws on the tradition of framing analysis in media studies, most influentially Robert Entman's 1993 essay "Framing: Toward Clarification of a Fractured Paradigm," which argues that frames "define problems, diagnose causes, make moral judgments, and suggest remedies." The columns `mentions_cause` and `media_tone` are direct operationalizations of Entman's frame components.

The approach to data documentation follows the principles articulated by the Responsible Datasets in Context project, which argues that "data cannot be analyzed responsibly without deep knowledge of its social and historical context, provenance, and limitations." This essay is an attempt to produce exactly that kind of documentation — not just a data dictionary, but an account of the interpretive labor that produced each column.

The problem of scaling qualitative judgment through computational means is addressed in Ted Underwood's *Distant Horizons: Digital Evidence and Literary Change* (2019), which grapples directly with what is gained and lost when literary interpretation is automated. Underwood argues that distant reading does not replace close reading but creates a different kind of knowledge — one that trades interpretive depth for breadth and pattern visibility. This project's dual-phase structure, preserving both the 60-row manual dataset and the 600-row computational augmentation with explicit `coding_method` labeling, is an attempt to hold both modes in productive tension rather than treating one as superior.

Finally, the ethical question raised by suicide rows — what it means to reduce human suffering to a data point — connects to Safiya Umoja Noble's work on the ethics of algorithmic systems and Catherine D'Ignazio and Lauren Klein's *Data Feminism* (2020), which argues that "data are not neutral or objective" and that the choices embedded in data collection and categorization always reflect and reproduce social values. The fact that the deaths of real people appear in this dataset as instances of `media_tone: Negative` is not a problem I can fully solve within the schema, but it is one I can — and should — name.

---

## Lessons Learned

The most important lesson of this semester is that data work is interpretive work. Every column name, every inclusion decision, every classification rule embeds an assumption about what matters and what counts. Those assumptions do not disappear when the process is automated — they get encoded into the automation and applied at scale, often invisibly. Making those assumptions explicit, as this documentation attempts to do, is not a supplement to data work. It is data work.

The second lesson is that computation is a collaborator, not a solution. The Python scripts that fetched and classified 600 rows did not eliminate interpretive labor; they displaced it upstream, into the design of keyword lists and query parameters that themselves required careful judgment. And the LLM that hallucinated plausible headlines reminded me that tools which look like they are solving problems can be generating new ones just as fluently.

The third lesson is that the archive is never neutral. Chronicling America is a magnificent resource, but it is also a particular set of choices about what to digitize, what to preserve, and what to make searchable. Every dataset built from it inherits those choices. The Evening Star's dominance in my dataset is not a fact about American newspaper coverage; it is a fact about digitization priorities. Responsible data work requires naming that difference.

---

*Dataset file: `final_dataset.tsv`*
*Scripts: `fetch_articles.py`, `classify_articles.py`, `merge_datasets.py`*
*Initial documentation: `documentation.md`*
