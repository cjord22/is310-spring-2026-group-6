# Analyzing Redlining's Impact on Chicago
This repo contains 2 datasets, the first, titled "initial-data-set.csv," contains my initial dataset, exploring the Area Descriptions of 64 districts from the Mapping Inequality
The dataset, and combining it with data from the Chicago Health Atlas. The second, titled "final-data-set.csv," contains my final dataset, refining that dataset and expanding it.
There is also a file titled "final-data-essay.ipynb" containing a data essay detailing the process for creating this dataset and my analysis after processing the data. Finally, I
have included the original files I edited to create this data set.


## Initial Data Set Fields
- `District Number` (String) is a unique district label assigned by the HOLC.
- `Current Neighborhood` (String) Neighborhood(s) each HOLC district lies within in modern-day Chicago, as per the City's community boundaries.
- `In City Limit` (Boolean, Y = True, N = False) 'Y' for districts within the city limits and 'N' for those that are not.
- `Class (and Occupation) from 1940s` (String) Includes notes from the HOLC on Class and Occupation in their area descriptions.
- `Neighborhood Median Household Income (2020s)` (String) denotes the median household income for each neighborhood, as recorded by the Chicago Health Atlas.
- `Neighborhood Same Name?`(Boolean, Y = True, N = False) 'Y' if the neighborhood/district has the same name now (2026) as it did when the HOLC compiled these maps.
- `Shifting or Infiltration(1940s)` Notes: "The infiltration of inharmonious racial groups," as defined by the HOLC and Frederick Babcock.


## Final Data Set Fields
- `Name` (String) is the tract name
- `GEOID` (Integer) is a numeric code that uniquely identifies all administrative/legal and statistical geographic areas for which the Census Bureau tabulates data.
- `INC_2020-2024` (String) is the median income for each census tract.
- `INC_2020-2024_moe` (String) is the Margin of Error for Census Tract Median value.
- `properties.area_id` (Integer) is a unique identifier for each area created by the Digital Scholarship Lab.
- `properties.cat` (String) is the assigned category from a redlining map. On standard HOLC City Survey Program maps, the category values are “Best”, “Still Desirable”, “Declining”, or “Hazardous”.
- `properties.grade` (String) is the letter grade used to grade the area. For non-residential areas and most cities that were not part of the City Survey, the value is null.
- `properties.label`(String) is the label from a redlining map. For most HOLC City Survey Program maps, this value is a letter and number, which often corresponds to an area description viewable on the Mapping Inequality website.
- `properties.res` (boolean, true=1, false=0) denotes whether or not an area is labeled explicitly as residential or inferred to be residential.
- `properties.com` (boolean, true=1, false=0) denotes whether or not an area is labeled explicitly as commercial or inferred to be commercial from a redlining map.
- `properties.ind` (boolean, true=1, false=0) denotes whether or not an area is labeled explicitly as industrial, or inferred to be industrial.
- `properties.fill` (string) is a hexadecimal color code for symbology. The value is typically an approximation of the color shown on a redlining map.
- `properties.GISJOIN` (string) is a numeric code for joining tables from NHGIS to spatial data.
- `properties.calc_area` (decimal) the area of the feature in meters.
- `properties.pct_tract` (decimal) the feature's areal percentage of a census tract.


## How To Run
Open final-data-essay.ipynb in Jupyter and run all cells in order. Requires: pandas
```bash
pip install pandas
jupyter notebook final-data-essay.ipynb
```
