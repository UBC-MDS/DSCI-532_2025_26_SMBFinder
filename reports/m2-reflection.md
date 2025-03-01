# Reflection - Milestone 2

## Implementation progress
The following components from our original sketch have been successfully implemented:
1) Dropdown Filters (State & County selection)
2) Business Overview Panel (Sidebar with key national metrics)
3) Map
4) Business Density Trend & Median Income Level Plots
5) Three Additional Business Indices (Sellability, Competition, and Hireability)

There are parts we decided not to implement, as well as changes made, which are explained below.

## Deviation from the original plan
- **Changed 'Average Population' to 'Average Microbusiness Density'** (sidebar)\
  Since all three sidebar metrics represent USA-wide values, total population was not as insightful. Instead, average microbusiness density provides a clearer picture of business concentration across the country.
- **Removed scrollbar**\
  Instead of manually scrolling, the map automatically zooms in when a state/county is selected, improving usability.
- **Drop Two plots**
  - Hireability vs. Business Growth Plot: The hireability index already provides a direct measure of workforce availability, making this plot redundant.
  - Microbusiness Density vs. Median Income Scatter Plot: This was removed as it did not provide substantial additional insight and could be misleading without further context.
- **Added a Data Selection Dropdown** (Planned Expansion)\
A new dropdown allows users to select different metrics to display on the heatmap (currently only business density is available). Future iterations will introduce options like median income, enabling more customized analysis.

## Reflection on strength, limitations & potential improvements
**Strength**
- Intuitive Filtering System: Automatic zooming enhances usability.
- Retained Sidebar with Key National-Level Metrics: Provides essential business insights at a glance.
- Provides Additional Business Indices: Offers insights into sellability, competition, and hireability—key factors for entrepreneurs.
  
**Limitations**
- No Side-by-Side Comparisons: Users cannot currently select multiple states/counties for comparison.
- Limited Explanations for Business Indices: While each index has a brief description, users may still need more context or guidance to fully understand their significance and how they should inform decision-making.
  
**Potential improvements**
- Allow multiple state/county selections for direct comparisons.
- Enhance explanations or add interactive tooltips for business indices to provide users with clearer insights on their meaning, relevance, and impact on decision-making.
