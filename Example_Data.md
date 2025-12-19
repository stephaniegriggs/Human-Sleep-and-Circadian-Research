# Example Dataset for Meta-Analysis of Rhythmic Metabolites

## Overview
This file provides example data that can be used with the SPSS syntax files for conducting a meta-analysis on the proportion of rhythmic metabolites.

## Data Structure

The data includes 8 hypothetical studies examining circadian rhythmicity in metabolites:

| Study_ID | Study_Name | Rhythmic_Metabolites | Total_Metabolites | Sample_Size | Tissue_Type | Analysis_Method | Year |
|----------|------------|----------------------|-------------------|-------------|-------------|-----------------|------|
| 1 | Smith et al. | 45 | 200 | 30 | Blood | JTK_CYCLE | 2020 |
| 2 | Jones et al. | 32 | 150 | 25 | Urine | Cosinor | 2021 |
| 3 | Brown et al. | 67 | 300 | 40 | Blood | JTK_CYCLE | 2022 |
| 4 | Davis et al. | 28 | 180 | 35 | Saliva | RAIN | 2021 |
| 5 | Wilson et al. | 52 | 250 | 28 | Blood | JTK_CYCLE | 2023 |
| 6 | Taylor et al. | 41 | 195 | 32 | Urine | Cosinor | 2022 |
| 7 | Anderson et al. | 38 | 175 | 27 | Saliva | RAIN | 2023 |
| 8 | Thomas et al. | 55 | 280 | 38 | Blood | MetaCycle | 2021 |

## Calculated Proportions

Based on the above data:

| Study_Name | Proportion | Percentage |
|------------|-----------|------------|
| Smith et al. | 0.225 | 22.5% |
| Jones et al. | 0.213 | 21.3% |
| Brown et al. | 0.223 | 22.3% |
| Davis et al. | 0.156 | 15.6% |
| Wilson et al. | 0.208 | 20.8% |
| Taylor et al. | 0.210 | 21.0% |
| Anderson et al. | 0.217 | 21.7% |
| Thomas et al. | 0.196 | 19.6% |

## Expected Meta-Analysis Results

Using these example data, you should expect:

### Fixed-Effects Model
- **Pooled Proportion**: ~0.210 (21.0%)
- **95% CI**: ~0.195 - 0.225

### Random-Effects Model
- **Pooled Proportion**: ~0.209 (20.9%)
- **95% CI**: ~0.185 - 0.234

### Heterogeneity Statistics
- **Q-statistic**: ~8-10 (df = 7)
- **I²**: ~20-30% (Low to Moderate heterogeneity)
- **Recommendation**: Either model acceptable; Fixed-Effects preferred for low heterogeneity

## How to Use This Data

### Option 1: Manual Entry in SPSS
1. Open SPSS
2. Go to Variable View and create the variables listed above
3. Switch to Data View
4. Enter the data manually

### Option 2: Copy-Paste from CSV
Save the following as a CSV file and import into SPSS:

```
Study_ID,Study_Name,Rhythmic_Metabolites,Total_Metabolites,Sample_Size,Tissue_Type,Analysis_Method,Year
1,Smith_2020,45,200,30,Blood,JTK_CYCLE,2020
2,Jones_2021,32,150,25,Urine,Cosinor,2021
3,Brown_2022,67,300,40,Blood,JTK_CYCLE,2022
4,Davis_2021,28,180,35,Saliva,RAIN,2021
5,Wilson_2023,52,250,28,Blood,JTK_CYCLE,2023
6,Taylor_2022,41,195,32,Urine,Cosinor,2022
7,Anderson_2023,38,175,27,Saliva,RAIN,2023
8,Thomas_2021,55,280,38,Blood,MetaCycle,2021
```

### Option 3: Use Built-in Data in Syntax
The data is already included in the SPSS syntax file (`Meta_Analysis_Proportions.sps`) in the DATA LIST section. Simply uncomment that section to use it.

## Subgroup Analysis Example

With this dataset, you can perform subgroup analyses:

### By Tissue Type
- **Blood** (4 studies): Studies 1, 3, 5, 8
- **Urine** (2 studies): Studies 2, 6
- **Saliva** (2 studies): Studies 4, 7

### By Analysis Method
- **JTK_CYCLE** (3 studies): Studies 1, 3, 5
- **Cosinor** (2 studies): Studies 2, 6
- **RAIN** (2 studies): Studies 4, 7
- **MetaCycle** (1 study): Study 8

## Real-World Application

When using this meta-analysis approach with real data:

1. **Search Literature**: Conduct systematic literature search for relevant studies
2. **Inclusion Criteria**: Define clear criteria for study inclusion
3. **Data Extraction**: Extract the number of rhythmic and total metabolites from each study
4. **Quality Assessment**: Evaluate study quality and consider as covariate
5. **Run Analysis**: Use the provided SPSS syntax
6. **Interpret Results**: Consider heterogeneity, subgroups, and publication bias
7. **Report Findings**: Follow PRISMA guidelines for meta-analysis reporting

## Common Issues and Solutions

### Issue 1: Zero or 100% Proportions
**Solution**: Add 0.5 to both rhythmic and total metabolites (continuity correction)
```spss
IF (Rhythmic_Metabolites = 0 OR Rhythmic_Metabolites = Total_Metabolites) Rhythmic_Metabolites = Rhythmic_Metabolites + 0.5.
IF (Rhythmic_Metabolites = 0 OR Rhythmic_Metabolites = Total_Metabolites) Total_Metabolites = Total_Metabolites + 1.
```

### Issue 2: Small Number of Studies
**Solution**: Interpret with caution; meta-analysis with < 5 studies has limited power

### Issue 3: High Heterogeneity
**Solution**: 
- Use random-effects model
- Perform subgroup analysis
- Conduct meta-regression to explore sources of heterogeneity

## Additional Variables for Extended Analysis

Consider collecting these additional variables for more comprehensive analysis:

- **Study_Quality**: Quality score (e.g., 1-5)
- **Significance_Threshold**: p-value or q-value cutoff used
- **Circadian_Period**: Period range tested (e.g., 20-28 hours)
- **Sampling_Frequency**: How often samples were collected
- **Duration_Hours**: Length of study in hours
- **Age_Mean**: Mean age of participants
- **Sex_Distribution**: Percentage of female participants
- **Publication_Type**: Peer-reviewed journal, preprint, etc.

## References

These example data are hypothetical and created for instructional purposes. For real meta-analyses, always use data from published studies with proper citations.

## Next Steps

1. Review the `Meta_Analysis_Guide_SPSS.md` for detailed methodology
2. Run the `Meta_Analysis_Proportions.sps` syntax with this example data
3. Verify you can reproduce the expected results
4. Adapt the syntax for your own research data
