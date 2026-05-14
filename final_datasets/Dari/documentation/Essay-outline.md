# Final Data Essay — Outline & Questions

## Introduction
*Set up the problem and your contribution.*

- What is the cultural phenomenon you're studying, and why do immigration laws qualify as "cultural data"?
- What is your central research question? *(State it clearly as ONE question: "Which state — Illinois, California, or Arizona — is most pro-immigration, and how has each state's stance shifted over time (2009–2026)?")*
- Why did you choose these three states specifically? *(You have a great personal answer for Illinois — use it. Explain California vs. Arizona as a contrast pair.)*

---

## Section 1: What Is the Dataset and Where Did It Come From?
*Tell the story of the source and your selection decisions.*

- What is the NCSL Immigration Legislation Archived Database, and who creates it? What makes it a credible source?
- What were your inclusion criteria — what kinds of laws got in and what got left out? *(Why only laws that mention immigration enforcement, protections, or status? What about budget-only bills like AZ H 2862?)*
- Why 2009–2026? Why Illinois, California, and Arizona and not other states?
- How many laws are in the final dataset and how are they distributed across states and years?

---

## Section 2: How You Made It — The Manual Labeling Process
*This is where you address instructor critique #2 directly.*

- Walk through your exact workflow: how did you read a law, decide its sentiment, and write the description and reasoning?
- How did you define "Pro-Immigration" vs. "Anti-Immigration"? What is your rubric? *(Give 2–3 concrete examples of borderline cases and how you decided.)*
- Why did you choose to label based on the **intent and effect** of the law rather than just its language?
- What role did LLM summaries (Claude, Gemini) play — were they a drafting tool, a check, or something else? *(Address critique #1: be clear that final labels are yours, not the model's.)*
- What was the hardest law to label and why?

---

## Section 3: How Computation Played a Role
*This is a required essay component and also addresses critique #4 directly.*

- What is TF-IDF, and why is it an appropriate feature representation for short law descriptions?
- What is Logistic Regression, and why is it more appropriate for this task than a black-box model?
- What does "Leave-One-Out cross-validation" mean and why was it necessary for a 66-law dataset?
- What did **84.85% LOO accuracy** tell you? What does it validate about your manual labels?
- What did the model's feature importance (top terms) reveal about what language distinguishes pro- vs. anti-immigration laws in your dataset?
- Where did the model **disagree** with your labels, and what does that tell you?

---

## Section 4: What the Data Reveals
*The actual findings — answer your research question.*

- Which state is most pro-immigration, and by how much? *(CA: 0.637, IL: 0.636, AZ: 0.540)*
- Describe Arizona's trajectory — what happened in 2009–2011 (SB 1070 era) and how did it compare to 2022–2026?
- Describe California's pattern — consistent, or are there peaks? What years had the most activity and why?
- Describe Illinois — why does all its activity cluster in recent years (2019–2026)? What does that suggest about the state's political engagement with immigration?
- What is the overall legislative trend across all three states from 2009 to 2026?

---

## Section 5: What the Data Conceals — Limitations
*Required component. Also addresses critique #3 on two research questions.*

- Your descriptions are short (1–2 sentences you wrote). What nuance is lost between your summary and the actual 20-page bill?
- The model scores some AZ anti-immigration laws above 0.5 — why? What does that say about the gap between text features and policy intent?
- **Arizona Legislature API mismatch:** The AZ Legislature API returns only short bill titles (e.g., "immigration; law enforcement; repeal"), not full descriptions. TF-IDF requires vocabulary to work — with 4–6 word titles, the model has almost nothing to learn from and assigns near-coin-flip scores (0.50–0.54) to almost every AZ Legislature bill, making 89% of them "Pro-Immigration" by a hair. This is a methodological mismatch, not a data quality error: the source is fine, but the text is too short for this method to function. Explain why those bills are kept in the dataset for completeness but excluded from the model's state-level scoring.
- What laws are **not** in this dataset? Laws that failed, were vetoed, or never reached a vote — what would those add?
- Is your dataset a representative sample of immigration legislation in these states, or a curated selection? What's the difference?
- The pro/anti binary label — what are the cases where a law is partially both? What gets lost in that simplification?

---

## Section 6: Ethical and Privacy Considerations
*Required component — don't skip this even though it seems obvious for laws.*

- Government laws are public records, but what about the people affected by them? Are there any privacy implications in how you framed or described the laws?
- Is there any researcher bias in how you labeled? *(Be honest — you are from Ukraine, you live in Illinois, you have a perspective. How did you try to mitigate it?)*
- What are the risks of misreading a model's classification as "objective"? Who might misuse a chart that says "Arizona is anti-immigration"?

---

## Section 7: How Scale Shaped the Data Over the Semester
*Required component — tells the story of intellectual growth.*

- What did your dataset look like at the initial submission? How was it different?
- What changed when you moved from manually reading every law one-by-one to using the logistic regression pipeline?
- How did scale change what questions you could ask? What became possible that wasn't before?
- What did you have to give up or simplify to scale? *(e.g., you dropped full bill text scraping and used descriptions instead)*

---

## Section 8: Lessons Learned
*Required component — personal and methodological reflection.*

- What would you do differently if you started over?
- What surprised you most — about the data, about the computation, or about immigration law itself?
- What would the "next version" of this project look like if you had a full year?

---

## Section 9: Situating the Work in Scholarship
*Required component — peer-reviewed citations.*

You'll need at least 3–4 academic sources. Suggested areas to look into:

- **Computational text analysis on legislation** — there is published work on using NLP to classify bills
- **Immigration law and state politics** — political science literature on SB 1070 and state immigration enforcement
- **Sentiment analysis limitations** — critical data studies work on the limits of binary classification
- **Data as cultural artifact** — the theoretical framing of the course itself (ask your professor for the core reading)

Questions to answer:

- How does published scholarship describe the relationship between state immigration law and federal policy?
- What does existing NLP/computational research say about analyzing legal text?
- Where does your work fit — does it confirm, complicate, or extend what scholars have found?

---

## For the Group Collective Principles Document (5%)
*This is separate from your individual essay. Your group collectively answers:*

- What should someone know before they try to represent immigration law as data?
- What did you learn about the difference between what a law says and what it does?
- What principles emerged for handling binary classification of political documents?
- How did each group member's approach differ, and what can future researchers learn from that contrast?

---

## Priority for 3 Days

1. **Day 1** — Sections 1–3 (the "how I made it" backbone)
2. **Day 2** — Sections 4–6 (findings + limitations) + find 3–4 academic sources
3. **Day 3** — Sections 7–9 + polish + group doc
