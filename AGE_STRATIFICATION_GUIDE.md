# Age Stratification Guide

## Overview
This guide provides methods for stratifying participants by age in the 40-75 year range for sleep and circadian research.

## Available Methods

### 1. Equal-Width Bins
Divides the age range into equal-width intervals.

**When to use:**
- When you want equally-sized age intervals
- For reporting that requires standardized age brackets
- When age distribution is relatively uniform

**Example:**
```r
source("age_stratification.R")
ages <- c(42, 55, 68, 73, 45, 50, 61)

# Create 3 equal bins: 40-51, 52-63, 64-75
strata <- stratify_age_equal_width(ages, n_bins = 3)
table(strata)
```

### 2. Quartiles
Divides participants into four groups based on age distribution in your dataset.

**When to use:**
- When you want equal sample sizes in each group
- For statistical analyses requiring balanced groups
- When your age distribution is skewed

**Example:**
```r
strata <- stratify_age_quartiles(ages)
table(strata)
```

### 3. Custom Age Groups
Allows you to define specific age boundaries based on research needs.

**When to use:**
- When you have specific age cutoffs based on prior research
- For replicating previous studies
- When biological/clinical considerations dictate specific ages

**Example:**
```r
# Common age groups for middle-age and older adults
strata <- stratify_age_custom(ages, breaks = c(40, 50, 60, 70, 75))
table(strata)
```

### 4. Median Split
Divides participants into younger and older groups based on the median age.

**When to use:**
- For simple binary comparisons
- When you have limited sample size
- For exploratory analyses

**Example:**
```r
strata <- stratify_age_median_split(ages)
table(strata)
```

### 5. Decades
Groups participants by decade of life.

**When to use:**
- For easy interpretation and communication
- When comparing across different life stages
- For epidemiological studies

**Example:**
```r
strata <- stratify_age_decades(ages)
table(strata)
```

## Choosing the Right Method

### Sample Size Considerations
- **Small samples (n < 50):** Use median split or 2-3 bins
- **Medium samples (50-200):** Use tertiles, quartiles, or decades
- **Large samples (n > 200):** Can use quartiles, quintiles, or more fine-grained bins

### Research Question Considerations
- **Dose-response relationship:** Use quartiles or quintiles for even distribution
- **Comparing age groups:** Use equal-width bins or decades
- **Replicating prior work:** Use custom breaks matching previous studies
- **Maximum statistical power:** Use median split (if assuming linear effects)

## Example Workflow

```r
# Load the script
source("age_stratification.R")

# Your data
participant_data <- data.frame(
  id = 1:100,
  age = round(runif(100, 40, 75)),
  sleep_efficiency = rnorm(100, 85, 10),
  circadian_phase = rnorm(100, 2, 1.5)
)

# Choose stratification method based on your needs
participant_data$age_group <- stratify_age_quartiles(participant_data$age)

# Analyze by age group
library(dplyr)
participant_data %>%
  group_by(age_group) %>%
  summarize(
    n = n(),
    mean_sleep_efficiency = mean(sleep_efficiency),
    mean_circadian_phase = mean(circadian_phase)
  )
```

## Running the Demonstration

To see all methods in action:

```r
source("age_stratification.R")
demonstrate_stratification()
```

Or from command line:
```bash
Rscript age_stratification.R
```

## Reporting Age Stratification

When reporting in publications, include:
1. The stratification method used
2. The age range and cutoffs
3. Sample size in each stratum
4. Mean age (and SD) in each stratum

**Example:**
> "Participants (N=100, age 40-75 years) were stratified into quartiles based on age distribution: Q1 (40-52 years, n=25, M=46.2, SD=3.4), Q2 (53-59 years, n=25, M=56.1, SD=2.1), Q3 (60-67 years, n=25, M=63.5, SD=2.3), and Q4 (68-75 years, n=25, M=71.2, SD=2.4)."

## Statistical Considerations

### Power Analysis
- More strata = more comparisons = need for multiple comparison corrections
- Fewer strata = less granularity but more power per comparison

### Assumptions
- Equal-width bins assume uniform distribution of biological effects across age
- Quartiles ensure balanced groups but may have unequal age intervals
- Choose based on whether you expect linear vs. threshold effects of age

## Additional Resources

For circadian and sleep research:
- Age effects on sleep architecture typically show gradual changes (favor quartiles/quintiles)
- Circadian phase shifts may show threshold effects at certain ages (favor custom bins)
- Glucose regulation often changes around age 60 (consider custom breaks at key ages)
