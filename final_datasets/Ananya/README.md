# Dataset Overview: Illinois Women Legislators and Bill Sponsorship Activity

## What This Dataset Shows

This dataset tracks the bill sponsorship count of 157 female legislators in the Illinois General Assembly across the 93rd to 104th General Assembly sessions.

Each row shows how many bills a female legislator sponsored as the primary sponsor or co-sponsor within a given General Assembly session. It also includes the overall bill sponsorship count, as well as the number of bills that were healthcare, employment, or children/education related.

Those sub-categories were chosen because they are some of the most significant legislative priorities of female voters. If a female legislator was elected across different sessions, she has a separate row for each session she was elected in so that there is greater visibility into her productivity across and within those sessions.

## Main Question

The main question that founded this dataset was:

**How much legislative “productivity” did Illinois female legislators have in key policy areas for female voters, and what trends can be seen in this productivity across General Assembly sessions?**

The project focuses on three issue areas:

- **Healthcare**
- **Employment**
- **Education / children**

These topics were chosen because they connect to major female voter concerns and are especially relevant to studying how women legislators engage with policy areas that affect families, care work, economic security, and public wellbeing.

## Columns

- `ID`: CAWP identifier for the legislator
- `cawp_name`: Name from the CAWP dataset
- `ilga_name`: Name as found in Illinois General Assembly sponsor reports
- `chamber`: House or Senate
- `general_assembly`: Illinois General Assembly session
- `ilga_all_bills_count`: Total number of bills sponsored or co-sponsored
- `ilga_primary_bills_count`: Number of bills primarily sponsored
- `ilga_cosponsored_bills_count`: Number of bills co-sponsored
- `ilga_healthcare_all_count`: Total healthcare-related bills
- `ilga_employment_all_count`: Total employment-related bills
- `ilga_education_children_all_count`: Total education/children-related bills

## How the Counts Could Be Interpreted

The bill counts are based on Illinois General Assembly sponsor report data.

A higher count means the legislator was listed more often as a sponsor or co-sponsor during that General Assembly. This may suggest that they were more legislatively “productive,” but it cannot be interpreted further as a complete measure of their effectiveness.

For example:

- A high `ilga_primary_bills_count` may suggest more direct bill leadership.
- A high `ilga_cosponsored_bills_count` may suggest coalition-building or public support for many bills.
- A high issue-area count suggests more activity connected to that topic.

## What the Dataset Reveals

This dataset helps show:

- which women legislators had high levels of legislative activity
- how activity changed across General Assemblies
- whether healthcare, employment, or education/children bills were supported by these legislators
- how primary sponsorship compared to co-sponsorship

## What the Dataset Does Not Show

This dataset does **not** show whether a bill passed or the level of impact these prospective bills could have had or did have.

It also does not include every form of political labor, such as:

- committee work
- constituent service
- negotiations
- budget work

## Notes on Method

The dataset was created by matching women legislators from CAWP data to Illinois General Assembly sponsor report records. Bill records were then grouped by legislator, chamber, and General Assembly.

The final topic counts were created by classifying bill titles into healthcare, employment, and education/children categories.

The final dataset is useful for studying trends in women legislators’ bill sponsorship activity over time, especially in policy areas that are of concern for many female voters.
