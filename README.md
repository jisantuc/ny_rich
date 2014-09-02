"New York Rich"
=============

[Jordan Weissman](http://www.slate.com/blogs/moneybox/2014/08/29/income_distribution_of_new_york_city_what_does_it_take_to_be_rich.html?wpsrc=fol_fb) made lazy dataviz choices and displayed separate sideways histograms to show the difference between NYC income distribution and the US and San Francisco income distribution and the US. This is unnecessary and can be done better using KDE plots.

Data are the [2012 one-year American Community Survey public use microdata files](http://www2.census.gov/acs2012_1yr/pums/)

Plan is:
- Grab file for each state
- Filter to relevant columns
- Concatenate all states into one big ol' dataset
- Re-estimate the income distributions in each location Weissman showed (possibly with sliders).
