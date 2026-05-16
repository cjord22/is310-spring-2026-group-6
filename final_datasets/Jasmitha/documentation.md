# Representing Women’s Suffrage as Data: Scaling Historical Newspapers Through Computation

## Introduction

This project explores how women’s suffrage was represented in American newspapers between 1890 and 1920 using the Library of Congress Chronicling America archive. I collected newspaper articles through keyword searches such as “woman suffrage,” “votes for women,” “anti-suffrage,” and “remonstrants,” creating a large computational dataset spanning multiple decades and regions.

The goal was not only to collect suffrage articles, but to examine what happens when culture becomes data. Historical newspapers contain political debates, gender ideologies, and regional perspectives, but once converted into spreadsheets and machine-readable text, interpretive and technical decisions shape what becomes visible and searchable. Through this project, I learned that datasets are not neutral collections of information; they are constructed through archives, algorithms, metadata, and human interpretation.

## Constructing the Dataset

I began by manually exploring suffrage-related newspapers and identifying useful metadata fields such as links, newspaper name, date published, state, headline, tone, type, and justificaiton. At first, it was so tasking to read the articles figure out what type of article it was, if it was for or against suffrage. The readability and OCR-generated text wasn't the best either. The language is also older, so it made it harder to underatand what it was about, so I used AI to help me figure things out. 

This stage showed that transforming culture into data is an interpretive process.

## Scaling Through Computation

After building the initial handcrafted dataset, I recieved some criticism on how to make it better. I wasn't able to expand that dataset even using AI tools. I scraped how I did it and through our assignments on API, I was able to use Chronicling America's API to extract my data. I expanded it computationally using Python with the requests, pandas, and re libraries. My script queried the Chronicling America API across multiple search terms and years between 1890 and 1920, automatically converting results into structured dataset rows.

One major challenge involved extracting city and state information from inconsistent newspaper title formats such as:

* “([Beatrice, Nebraska])”
* “(San Francisco [Calif.])”
* “(Washington, D.C.)”

At first, the location city and state that you can take from the JSON was inaccurate as it sometimes includes where the newspaper publishes to even if it wasn't made in that state. I found city and state in the title, but it was not cleaned. To solve this, I used regular expressions (regex) to identify and standardize publication locations. This process demonstrated that computation is not simply automation, but also interpretation and reconstruction of messy archival systems.

Scaling the dataset changed the nature of the project. In the manual phase, I handpicked each article. Once the dataset expanded into thousands of entries, the focus shifted toward identifying broader patterns across geography, time, and political rhetoric.

## Technical Challenges and Limitations

One of the largest challenges involved OCR (Optical Character Recognition) errors. Because the newspapers were digitized from scans, the machine-generated text often contained distorted spellings and unreadable passages. These errors made keyword searching unreliable and demonstrated how digitization reshapes archival visibility.

Metadata inconsistencies created additional problems. Publication locations were often abbreviated, incomplete, or inaccurate, requiring additional cleaning and regex matching. I also encountered API limitations such as HTTP 429 “Too Many Requests” errors and JSON decoding failures, showing that digital archives are technical infrastructures with constraints rather than neutral repositories. I had to figure what constraints to put on the data so it doens't overwhelm my computer or take 14+ minutes to load. Although it might not be the best in terms of getting the best analysis, it was all I could do with my technologies and this assignment.

## What the Dataset Reveals

The dataset reveals how widely suffrage debates circulated across the United States. Articles appeared in both major newspapers and smaller regional publications, demonstrating that suffrage discourse was nationally distributed rather than isolated to a few urban centers. 

One of the analysis I ran is seeing the most common words in the pro and anti suffrage articles. I first collected the words and then took out common words like "the" and "will" and others. I found out that the pro suffrage articles have women, suffrage, woman, washington, states, national, vote, president, and others. Anti suffrage articles had house, price, sunday, office, women, and suffrage. The pro suffrage had women, woman, and suffrage as the top three words. The anti suffrage had women at 17th and suffrage at 25th. It seems like the anti-suffragist news were buried with regular reporting news, while the pro suffragists focused on it more. Anti-suffrage rhetoric was less centralized and less ideologically unified in newspaper discourse than pro-suffrage organizing. Although we must keep in mind of the small dataset, OCR isn't the best and other factors we may be missing, I still think it's interesting.

New York and Washington dominated as the states with the most articles in my dataset, but third was Nebraska. It's interesting as the 'The Women's Tribune' from Nebraska dominates the early years. With this in mind, you can imagine there's search term bias as Chronicling America collected specifically activist newspapers, so the common words we saw earlier may be biased. 

## What the Dataset Conceals

Although the dataset captures large amounts of information, it also removes much of the original cultural context. Page layouts, advertisements, typography, and surrounding articles are largely absent once newspapers are converted into spreadsheet rows. I also feel that to due time and size constraints, I didn't get to collect as much data as I wanted. It's only 1890-1920, every 3 years, 4 search terms, 1 page from each article. Even though I did get 3000-4000 articles from this, it's not the best dataset to do complex analysis as i'm still missing so much. 

The dataset also cannot fully represent the emotional and rhetorical complexity of the suffrage movement. Articles become simplified into searchable snippets and metadata categories, flattening nuanced historical experiences into machine-readable fields. There's also only so much I can read as the OCR quality isn't the best with multiple words smashed together, missing words, and layouts messing it up. 

Additionally, because the project depends on digitized archives, it reflects institutional decisions about which newspapers were preserved and digitized in the first place.

## Lessons Learned

This project changed how I think about data and computation. I learned that “clean” cultural data rarely exists and that historical archives are inherently messy and incomplete. Titles are wrong, multiple states and cities are listed, terms aren't always what seem to be, and there's tons of metadata. 

Most importantly, I learned how hard it is to be able to do accurate analysis without extracting thousands of articles. I was initally trying to get 3 pages and had 5 search terms and when I stopped it at 14 minutes as it would take too long to get the full dataset. 

## Conclusion

This project demonstrates both the possibilities and limitations of representing culture as data. Computational methods allowed me to scale a small handcrafted dataset into thousands of searchable newspaper entries spanning multiple decades and regions. At the same time, the project revealed the instability of OCR text, metadata systems, and digital archives.

Ultimately, this project showed that computation does not simply uncover history—it reshapes how history becomes visible and interpretable.
