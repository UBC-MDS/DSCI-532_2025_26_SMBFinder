# Milestone 4 Reflection

## Feedback Implementation

### Larger Feedback Items

1. **Layout issue with line charts**
   - **Action Taken**: We modified the card layout to prevent wrapping or unwanted row shifts.

2. **Performance Issues on Render**
   - **Action Taken**:
     - Caching does not improve performance.
     - Weirdly, when we added cache to the maps, the performance actually became slower. For example, below is an implementation of general cache in Plotly:
     
     ```python
      from flask_caching import Cache
      cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})

      @cache.cached(timeout=300)
      def some_map_function():
         print("Cache miss - computing now")
         # Your logic here
         return result
     ```
     
     - While in theory, this cache could speed up the workflow, from user behavior, we find that if the user selects states/counties to compare, they generally don't select the same combination again. Furthermore, this process degraded the performance because it meant the app would have to perform a cache operation every time a map is loaded.
     - Additionally, this is actually an interesting permutation problem, where at any given time, a user could either select 3 states or 3 counties within a state. Since there are 50 states and ~3100 counties, even if we set our cache to the size of 1,000, our hit rate (user using the same cache again) would be around 0.05%, and 0.5% if the cache size is 10,000. Therefore, we would benefit if we were not to have a cache component in our map function.


### Smaller Feedback Items
1. **Change color scale to be more intuitive**:
   - **Action Taken**: Adjusted the color scale so that lighter shades indicate higher index values.

2. **Button for About info instead of at the bottom**:
   - **Action Taken**: We added GitHub and About info beside the title.

3. **Cards in the same style/color and title also**:
   - **Action Taken**: Unified the design of cards (sidebar) and title with a light blue background.

4. **Remove "filtered data" label**:
   - **Action Taken**: We removed it.

5. **Add units to all cards**:
   - **Action Taken**: Units have been added to "Avg. Microbusiness Density"

6. **Align input filters**:
   - **Action Taken**: The filters were previously misaligned; they have now been adjusted.

7. **Consider cards for lines chart**:
   - **Action Taken**: Placed line charts inside cards for a more cohesive layout.

8. **Consider if zero should be in the y-axis for line charts**:
   - **Action Taken**: Previously, the y-axis for both line charts started from zero. Now, they dynamically adjust based on the selected filter values.

---

## Reflection on Dashboard Development

### Insights and Feedback
Feedback from Joel and peers was invaluable in refining our dashboard. Suggestions regarding map scaling, adding layout for line charts, and ensuring data consistency significantly enhanced the usability and clarity of our app.

### Strengths and Limitations
- **Strengths**:
  - Intuitive and user-friendly interface.
  - Comprehensive visualizations (maps, bar charts, and line charts).
  - Effective use of interactivity to explore data.

- **Limitations**:
  - Limited to data from 2018-2022.
  - Performance issues with large datasets.

### Future Improvements
If we had more time, we would:
- Expand the dataset to include more recent years.
- Optimize performance for large datasets.
- Add advanced interactivity features (e.g., drill-down capabilities).

---

## Conclusion
Overall, we are proud of the progress made on our SMBFinder dashboard and believe it effectively communicates critical insights about microbusiness trends in the U.S. The feedback from Joel and peers was instrumental in refining the app, and we look forward to continuing to improve it in the future.
