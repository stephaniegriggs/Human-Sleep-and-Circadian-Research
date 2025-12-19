# Age Stratification Methods Comparison

## Sample Dataset
- **N**: 100 participants
- **Age Range**: 40-75 years
- **Mean Age**: 57.5 years (SD = 9.5)

## Method Comparison

### 1. Equal-Width Bins (3 groups)
Creates age groups with equal intervals across the age range.

| Age Group | N | Percentage |
|-----------|---|------------|
| 40-51 years | 33 | 33% |
| 52-63 years | 35 | 35% |
| 64-75 years | 32 | 32% |

**Advantages:**
- Standardized age intervals
- Easy to interpret and compare across studies
- Good for examining linear trends

**Disadvantages:**
- Groups may have unequal sample sizes
- May not account for non-uniform age distribution

---

### 2. Quartiles (Data-Driven)
Divides participants into four equal groups based on age distribution.

| Quartile | Age Range | N | Percentage |
|----------|-----------|---|------------|
| Q1 (Youngest 25%) | 40-52 years | 25 | 25% |
| Q2 (25-50%) | 53-59 years | 25 | 25% |
| Q3 (50-75%) | 60-66 years | 25 | 25% |
| Q4 (Oldest 25%) | 67-75 years | 25 | 25% |

**Advantages:**
- Equal sample sizes in each group
- Maximizes statistical power
- Adapts to your data distribution

**Disadvantages:**
- Age ranges vary between groups
- Less comparable across different studies
- Specific to your dataset

---

### 3. Custom Age Groups
User-defined age boundaries based on research needs.

Example: Using breaks at 40, 50, 60, 70, 75

| Age Group | N | Percentage |
|-----------|---|------------|
| 40-49 years | 27 | 27% |
| 50-59 years | 30 | 30% |
| 60-69 years | 28 | 28% |
| 70-74 years | 15 | 15% |

**Advantages:**
- Matches clinical or biological stages
- Replicates previous study designs
- Meaningful age boundaries

**Disadvantages:**
- May result in unequal group sizes
- Arbitrary if not based on theory
- Less flexible to data distribution

---

### 4. Median Split
Divides participants into younger and older groups at the median.

| Group | Age Range | N | Percentage |
|-------|-----------|---|------------|
| Younger (<58 years) | 40-57 years | 50 | 50% |
| Older (≥58 years) | 58-75 years | 50 | 50% |

**Advantages:**
- Simple and straightforward
- Equal group sizes
- Good for exploratory analyses
- Maximizes power for two-group comparisons

**Disadvantages:**
- Loses information about age gradient
- Median varies by dataset
- May not capture non-linear effects

---

### 5. Decades
Groups by decade of life.

| Decade | N | Percentage |
|--------|---|------------|
| 40s (40-49) | 27 | 27% |
| 50s (50-59) | 30 | 30% |
| 60s (60-69) | 28 | 28% |
| 70s (70-79) | 15 | 15% |

**Advantages:**
- Intuitive and easy to communicate
- Commonly used in epidemiology
- Recognizable life stages
- Good for cross-study comparisons

**Disadvantages:**
- Arbitrary decade boundaries
- May have unequal sample sizes
- Last group (70s) only partially represented

---

## Recommendations by Research Context

### Sleep Architecture Analysis
**Recommended:** Quartiles or Decades
- Sleep architecture changes gradually with age
- Quartiles ensure sufficient power in each group
- Decades facilitate comparison with existing literature

### Circadian Phase Studies
**Recommended:** Custom breaks or Equal-width bins
- Consider breaks at biologically meaningful ages (e.g., 45, 55, 65)
- Circadian changes may show threshold effects
- Equal-width bins good for testing linear trends

### Glucose Regulation Research
**Recommended:** Custom breaks
- Use breaks around ages where metabolic changes occur (e.g., 50, 60)
- Consider menopause age for sex-stratified analyses
- Align with diabetes risk stratification

### Hormone Studies
**Recommended:** Custom breaks or Decades
- Align with known hormonal transition periods
- Decades facilitate clinical interpretation
- Custom breaks for sex-specific analyses

### Exploratory Analyses
**Recommended:** Median split or Quartiles
- Median split for initial two-group comparisons
- Quartiles for more nuanced exploration
- Can refine approach based on initial findings

---

## Statistical Power Considerations

| Sample Size | Recommended Number of Groups |
|-------------|------------------------------|
| < 50 | 2 groups (median split) |
| 50-100 | 2-3 groups (median split or tertiles) |
| 100-200 | 3-4 groups (tertiles, quartiles, or decades) |
| > 200 | 4-5 groups (quartiles, quintiles, or decades) |

**Note:** More groups = more comparisons = need for multiple comparison corrections

---

## Example Analysis Code

### R
```r
# Load your data
data <- read.csv("your_data.csv")

# Choose stratification method
data$age_group <- stratify_age_quartiles(data$age)

# Analyze sleep efficiency by age group
library(dplyr)
data %>%
  group_by(age_group) %>%
  summarize(
    n = n(),
    mean_age = mean(age),
    sd_age = sd(age),
    mean_sleep_eff = mean(sleep_efficiency),
    se_sleep_eff = sd(sleep_efficiency) / sqrt(n())
  )

# Statistical test
kruskal.test(sleep_efficiency ~ age_group, data = data)
```

### Python
```python
import pandas as pd
from age_stratification import stratify_age_quartiles
from scipy import stats

# Load your data
data = pd.read_csv("your_data.csv")

# Choose stratification method
data['age_group'] = stratify_age_quartiles(data['age'])

# Analyze sleep efficiency by age group
summary = data.groupby('age_group').agg({
    'age': ['count', 'mean', 'std'],
    'sleep_efficiency': ['mean', 'std']
})
print(summary)

# Statistical test
groups = [group['sleep_efficiency'].values 
          for name, group in data.groupby('age_group')]
stats.kruskal(*groups)
```
