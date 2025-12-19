# Age Stratification Quick Reference

## Choose Your Method

| Method | When to Use | Sample Code (R) | Sample Code (Python) |
|--------|-------------|-----------------|----------------------|
| **Equal-Width Bins** | Standard intervals, comparing across studies | `stratify_age_equal_width(age, n_bins=3)` | `stratify_age_equal_width(age, n_bins=3)` |
| **Quartiles** | Balanced groups, maximum statistical power | `stratify_age_quartiles(age)` | `stratify_age_quartiles(age)` |
| **Custom Breaks** | Specific age cutoffs, replicating prior work | `stratify_age_custom(age, breaks=c(40,50,60,70,75))` | `stratify_age_custom(age, breaks=[40,50,60,70,75])` |
| **Median Split** | Simple 2-group comparison | `stratify_age_median_split(age)` | `stratify_age_median_split(age)` |
| **Decades** | Easy communication, epidemiological studies | `stratify_age_decades(age)` | `stratify_age_decades(age)` |

## Quick Start

### R
```r
# 1. Load functions
source("age_stratification.R")

# 2. Use with your data
my_data$age_group <- stratify_age_quartiles(my_data$age)

# 3. Analyze
library(dplyr)
my_data %>% 
  group_by(age_group) %>%
  summarise(mean_outcome = mean(outcome))
```

### Python
```python
# 1. Import functions
from age_stratification import stratify_age_quartiles

# 2. Use with your data
df['age_group'] = stratify_age_quartiles(df['age'])

# 3. Analyze
df.groupby('age_group')['outcome'].mean()
```

## Sample Size Guidelines

| Your N | Recommended Method |
|--------|-------------------|
| < 50 | Median split (2 groups) |
| 50-100 | Tertiles or decades (3-4 groups) |
| 100-200 | Quartiles or decades (4 groups) |
| > 200 | Quartiles or quintiles (4-5 groups) |

## Common Research Scenarios

### Sleep Efficiency Analysis
```r
# Recommended: Quartiles (balanced groups)
data$age_group <- stratify_age_quartiles(data$age)
kruskal.test(sleep_efficiency ~ age_group, data)
```

### Circadian Phase Study
```r
# Recommended: Decades (easy interpretation)
data$age_group <- stratify_age_decades(data$age)
```

### Glucose/Metabolic Research
```r
# Recommended: Custom breaks at key ages
data$age_group <- stratify_age_custom(data$age, 
                                      breaks = c(40, 50, 60, 70, 75))
```

## Reporting Template

> "Participants (N=100, age 40-75 years) were stratified into quartiles: Q1 (40-52 years, n=25, M=46.2, SD=3.4), Q2 (53-59 years, n=25, M=56.1, SD=2.1), Q3 (60-67 years, n=25, M=63.5, SD=2.3), and Q4 (68-75 years, n=25, M=71.2, SD=2.4)."

## Files in This Repository

- **age_stratification.R** / **.py** - Core functions
- **example_sleep_analysis.R** / **.py** - Complete workflow examples
- **AGE_STRATIFICATION_GUIDE.md** - Detailed documentation
- **METHODS_COMPARISON.md** - Method comparisons with examples
- **QUICK_REFERENCE.md** - This file

## Need Help?

1. See **AGE_STRATIFICATION_GUIDE.md** for detailed explanations
2. See **METHODS_COMPARISON.md** for side-by-side comparisons
3. Run **example_sleep_analysis.R** or **.py** for a complete workflow
4. Check **SOLUTION_SUMMARY.md** for an overview
