# Dataset and Aim

As my broad interest for this course is the influence of women in United States Politics. I first worked to narrow my theme into a dataset that was approachable to build, augment, and analyze for this project. Thus, I decided that my initial dataset would be focused on how that influence by women in U.S. politicians can become more visible through data.

I had chosen the Center for American Women and Politics (CAWP) at Rutgers University as my source for data on female elected state legislators (from the state of Illinois alone for the initial dataset). I selected CAWP as my primary source because it is a widely respected source for scholarly information and data regarding women in U.S. politics.

When analyzing their datasets, I realized that while the institute is great at capturing which women hold political offices in the United States at a national and state level across history, it lacks in highlighting the personal backgrounds and pathways to power that shape how political representation is experienced and reflected.

I felt that the missing data on the personal history of each politician could bring greater insight into the diversity that they bring to office, and moving forward can anchor further research into the political footprint they have left on key issues that are relevant to constituents with regard to their background. For example, being able to review the footprint that a politician with a professional background in education (e.g., having been a teacher before being elected to office) has made on policies regarding education (e.g., formally having written, signed, or passed bills/memos related to education).

Opening up this level of study can enable us to research and answer the larger questions regarding the legislative productivity of women in politics across a plethora of backgrounds and begin cross-analysis with national averages for legislative productivity and that of male politicians. We can even begin to study the interaction (e.g., co-authoring bills, co-signing bills) between female elected officials on the grounds of shared background and the potential impact their collaboration or clashes contribute to political outcomes (e.g., a bill being passed or not).

Overall, at this stage, I am not directly measuring women's political influence in the United States. Instead, I am focused on building a solid foundation by augmenting CAWP's dataset to make women elected officials' backgrounds more visible, which can support later research on how different forms of diversity and professional experience might relate to legislative priorities, representation, and political influence.

---

# Approach

My approach for this stage was to leverage an LLM to augment an existing dataset rather than build one entirely from scratch. I began with a subset of 50 women elected officials from the Illinois state-level data and added three new categories: **immigration visibility**, **highest degree held**, and **professional background**. My goal is not to claim that these categories fully define a politician, but to make visible some dimensions of background that are usually not included in summary political datasets.

**Immigration visibility** was defined as whether a politician has a publicly documented immigration-related background made in explicit statements in public sources. Immigration visibility was categorized with:

- `naturalized_citizen`
- `first_generation_immigrant`
- `child_of_immigrants`
- `no_public_evidence`
- `unclear`

**Professional background** was categorized with:

- `law`
- `education`
- `business`
- `healthcare`
- `nonprofit_advocacy`
- `government_public_service`
- `community_organizing`
- `labor_union`
- `media_communications`
- `science_technology`
- `military`
- `mixed`
- `unclear`

"Mixed" was used when two or more backgrounds were equally prominent, and unclear was used when the public sources were too vague.

---

# Computational Tool Used and Method

I utilized an LLM based workflow to effectively add the mentioned categorical dimensions to the records of the selected female elected officials to better encompass the diversity of representation that they bring. My choice of LLM after testing others including Chat-GPT 5.2 was Google Gemini 3 to aid in researching publicly available biographical information for each politician to consistently categorize them across the dataset.

I prompted the LLM to ground classifications to citable public sources such as official legislative biographies, campaign pages, Ballotpedia, and reputable news coverage, and then return a structured classification for each official.

A key part of the method was the **prompt design**. I made the prompt highly specific so that the augmentation process would be transparent and reproducible. In particular, I added instructions such as:

- "Do not guess."
- "Do not infer immigration-related status from name, race, ethnicity, birthplace alone, or appearance."
- "If there is not enough explicit evidence, use the appropriate fallback label."
- "Preserve all original columns and append the new columns at the end."

These instructions were utilized to reduce the risk of unsupported identity based inferences and force conservative classifications as a false positive classification for a label would be harmful as it misattributes a politician's background while the fallback label labeling uncertainty is safer and enables future research to proceed cautiously. I additionally required Gemini 3 to provide me sources so that I could randomly sample and review sources as a quality assurance measure. I removed this column in the final dataset to maintain the cohesiveness of the dataset and its purpose.

Additionally, as mentioned before I provided thorough definitions for the categories in the prompt to promote consistency in categorization by the model. For example, for immigration visibility, I defined the column as whether a politician had a publicly documented immigration-related background based only on explicit statements in reliable public sources. I narrowed the allowed values to:

- `naturalized_citizen`
- `first_generation_immigrant`
- `child_of_immigrants`
- `no_public_evidence`
- `unclear`

For the **highest degree held** category, I asked the model to classify only the highest degree that was explicitly supported by reliable public sources. If a biography mentioned school attendance or education generally without clearly stating the degree, the fallback category was "unclear."

For my **professional background**, I grouped careers into broad categories such as law, education, business, healthcare, nonprofit/advocacy, and government/public service. I chose broad categories because they made comparison possible across the dataset, even though they flatten some individual nuance.

## Limitations of Tools Used

The main limitation of using an LLM is the risk of hallucination, overconfident classification, or unsupported inference. This was especially important for a category like immigration visibility, since that kind of information is not always publicly documented and would be easy to handle irresponsibly.

For that reason, I designed the prompt to prioritize low false positives. I would rather mark a row as `no_public_evidence` or `unclear` than misclassify. This means the dataset may undercount some backgrounds, but that tradeoff is more responsible than overstating what the public record supports.

Another limitation I saw initially was that the LLM was quite slow in responding due to the intensity of conducting and citing research to support classification for 3 categories across 50 politicians. This leads me to believe that as the classification needs expand beyond 50 politicians there may be a barrier in successfully processing this labeling task through the browser versions of LLMs.

---

# Core Decisions

I made a few significant decisions on what to include and exclude in my dataset.

First, I narrowed my scope to 50 women elected for state legislature in Illinois. This made the project manageable and allowed me to have greater ability to discern the quality of my outputs as I have interned twice at the state legislature level and know background characteristics on a few state legislatures that are encompassed in this dataset.

Second, I selected only three augmentation categories for this first stage:

- **Immigration visibility**
- **Highest degree held**
- **Professional background**

I considered adding more categories, but I decided that doing so would reduce consistency and increase the chance of weak classifications.

Third, as mentioned before I decided that categorizations should be made conservatively provided solid documented public evidence.

These core decisions improve the confidence that this data can be leveraged to conduct the various deeper research that I had highlighted in my introduction.

---

# Next Steps

Beyond this initial dataset, I would like to scale this project beyond Illinois officials. The most direct pathway would be to expand the augmentation process to more state datasets from CAWP and potentially to a broader national set of women state legislators or women elected officials at multiple levels of government. As mentioned, to label this data at a larger scale, I would need to transition from my current browser-based LLM workflow to an API-based one. This would ensure that I could process hundreds of rows more systematically and maintain a reproducible structure for classification outputs.

At scale, I would continue using LLMs with the added caution of ensuring that verifiable citations can be leveraged post generation to validate the accuracy of categorization along with rationale to the categorization.

## What Will Change

The biggest change at scale is that interpretive decisions that felt manageable at 50 rows might become more unstable and risky at 500-1,000+ items. A category like professional background may remain relatively reliable, but a category like immigration visibility which may hinge on snippets from one off but reputable news articles and campaigns may become harder to manage since the public documentation is uneven and lack of evidence for the LLM may not be accurately reflective of the landscape.

For now I am confident that interpretive decisions for categories such as highest education can be reliably automated while categories that may be more unstable at scale may need to remain smaller and more carefully verified annotations.

---

# Broader Direction

In a larger version of this project, I would like to connect background variables to political behavior and issue engagement. For example, I could examine whether women with backgrounds in education are more active in education-related legislation, or whether publicly documented immigration-related background corresponds to greater engagement with immigration policy. That kind of question would require merging this augmented dataset with legislative data such as sponsorship, voting records, and issue-tagged bills.
