# Meta-Analysis Guide for SPSS: Estimating Rhythmic Metabolites Proportions

## Overview
This guide provides step-by-step instructions for conducting a meta-analysis in SPSS to estimate the proportion of rhythmic metabolites relative to the total number of measured metabolites across multiple studies. This is particularly relevant for circadian rhythm research where researchers want to aggregate findings from multiple metabolomics studies.

## Meta-Analysis Approach for Proportions

When conducting a meta-analysis on proportions (e.g., proportion of rhythmic metabolites), we use specific statistical methods designed for proportion data:

1. **Logit Transformation**: Transforms proportions to handle values near 0 or 1
2. **Freeman-Tukey Double Arcsine Transformation**: Stabilizes variance for proportions
3. **Random-Effects Model**: Accounts for between-study heterogeneity
4. **Fixed-Effects Model**: Assumes a common true effect size across studies

## Data Preparation

### Required Variables

Your SPSS dataset should contain the following variables for each study:

- `Study_ID`: Unique identifier for each study (String)
- `Study_Name`: Name or citation of the study (String)
- `Rhythmic_Metabolites`: Number of metabolites showing significant circadian rhythmicity (Numeric)
- `Total_Metabolites`: Total number of metabolites measured in the study (Numeric)
- `Sample_Size`: Number of participants in the study (Numeric)
- `Tissue_Type`: Type of biological sample (e.g., blood, urine) (String)
- `Analysis_Method`: Statistical method used (e.g., JTK_CYCLE, cosinor) (String)

### Example Data Structure

```
Study_ID | Study_Name          | Rhythmic_Metabolites | Total_Metabolites | Sample_Size | Tissue_Type
---------|---------------------|----------------------|-------------------|-------------|------------
1        | Smith et al. 2020   | 45                   | 200               | 30          | Blood
2        | Jones et al. 2021   | 32                   | 150               | 25          | Urine
3        | Brown et al. 2022   | 67                   | 300               | 40          | Blood
```

## Step-by-Step Procedure in SPSS

### Step 1: Calculate Study-Level Proportions

First, calculate the proportion and its variance for each study:

```spss
* Calculate proportion of rhythmic metabolites.
COMPUTE Proportion = Rhythmic_Metabolites / Total_Metabolites.
EXECUTE.

* Calculate standard error using binomial distribution formula.
COMPUTE SE = SQRT((Proportion * (1 - Proportion)) / Total_Metabolites).
EXECUTE.

* Calculate variance.
COMPUTE Variance = SE ** 2.
EXECUTE.
```

### Step 2: Apply Transformation

For proportions near boundaries (0 or 1), apply the Freeman-Tukey double arcsine transformation:

```spss
* Freeman-Tukey double arcsine transformation.
COMPUTE FT_Transform = 0.5 * (ARSIN(SQRT(Rhythmic_Metabolites / (Total_Metabolites + 1))) + 
                              ARSIN(SQRT((Rhythmic_Metabolites + 1) / (Total_Metabolites + 1)))).
EXECUTE.

* Calculate sampling variance for transformed values.
COMPUTE FT_Variance = 1 / (4 * Total_Metabolites).
EXECUTE.

* Calculate weight (inverse variance).
COMPUTE Weight = 1 / FT_Variance.
EXECUTE.
```

### Step 3: Calculate Pooled Effect Size (Fixed-Effects Model)

```spss
* Calculate weighted mean proportion (Fixed-Effects).
AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Sum_Weight = SUM(Weight)
  /Sum_Weighted_Effect = SUM(Weight * FT_Transform).

COMPUTE Pooled_Effect_FE = Sum_Weighted_Effect / Sum_Weight.
EXECUTE.

* Calculate standard error of pooled effect.
COMPUTE SE_Pooled_FE = SQRT(1 / Sum_Weight).
EXECUTE.

* Calculate 95% confidence interval.
COMPUTE CI_Lower_FE = Pooled_Effect_FE - (1.96 * SE_Pooled_FE).
COMPUTE CI_Upper_FE = Pooled_Effect_FE + (1.96 * SE_Pooled_FE).
EXECUTE.
```

### Step 4: Back-Transform to Proportion Scale

```spss
* Back-transform Freeman-Tukey to proportion.
COMPUTE Pooled_Proportion_FE = (SIN(Pooled_Effect_FE)) ** 2.
COMPUTE Proportion_CI_Lower = (SIN(CI_Lower_FE)) ** 2.
COMPUTE Proportion_CI_Upper = (SIN(CI_Upper_FE)) ** 2.
EXECUTE.
```

### Step 5: Test for Heterogeneity (Q-statistic)

```spss
* Calculate Q-statistic for heterogeneity.
COMPUTE Q_Component = Weight * ((FT_Transform - Pooled_Effect_FE) ** 2).
EXECUTE.

AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Q_Statistic = SUM(Q_Component)
  /K_Studies = N.

* Calculate degrees of freedom.
COMPUTE DF = K_Studies - 1.
EXECUTE.

* Calculate I-squared (percentage of variation due to heterogeneity).
COMPUTE I_Squared = 100 * ((Q_Statistic - DF) / Q_Statistic).
IF (Q_Statistic <= DF) I_Squared = 0.
EXECUTE.

* Calculate p-value for Q-statistic (requires chi-square distribution).
COMPUTE Q_P_Value = 1 - CDF.CHISQ(Q_Statistic, DF).
EXECUTE.
```

### Step 6: Random-Effects Model (DerSimonian-Laird Method)

If heterogeneity is significant (Q p-value < 0.10 or I² > 50%), use random-effects model:

```spss
* First calculate sum of squared weights.
AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Sum_Weight_Squared = SUM(Weight ** 2).

* Calculate between-study variance (tau-squared).
COMPUTE C = Sum_Weight - (Sum_Weight_Squared / Sum_Weight).
COMPUTE Tau_Squared = (Q_Statistic - DF) / C.
IF (Tau_Squared < 0) Tau_Squared = 0.
EXECUTE.

* Calculate random-effects weight.
COMPUTE Weight_RE = 1 / (FT_Variance + Tau_Squared).
EXECUTE.

* Calculate pooled effect (Random-Effects).
AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Sum_Weight_RE = SUM(Weight_RE)
  /Sum_Weighted_Effect_RE = SUM(Weight_RE * FT_Transform).

COMPUTE Pooled_Effect_RE = Sum_Weighted_Effect_RE / Sum_Weight_RE.
EXECUTE.

* Calculate standard error and confidence interval.
COMPUTE SE_Pooled_RE = SQRT(1 / Sum_Weight_RE).
COMPUTE CI_Lower_RE = Pooled_Effect_RE - (1.96 * SE_Pooled_RE).
COMPUTE CI_Upper_RE = Pooled_Effect_RE + (1.96 * SE_Pooled_RE).
EXECUTE.

* Back-transform to proportion scale.
COMPUTE Pooled_Proportion_RE = (SIN(Pooled_Effect_RE)) ** 2.
COMPUTE Proportion_CI_Lower_RE = (SIN(CI_Lower_RE)) ** 2.
COMPUTE Proportion_CI_Upper_RE = (SIN(CI_Upper_RE)) ** 2.
EXECUTE.
```

### Step 7: Create Forest Plot Data

```spss
* Prepare data for forest plot visualization.
SORT CASES BY Proportion (A).

* Label studies for plotting.
STRING Study_Label (A100).
COMPUTE Study_Label = CONCAT(RTRIM(Study_Name), " (", 
                             STRING(Rhythmic_Metabolites, F8.0), "/",
                             STRING(Total_Metabolites, F8.0), ")").
EXECUTE.
```

### Step 8: Generate Summary Statistics Report

```spss
* Generate descriptive statistics.
FREQUENCIES VARIABLES=Proportion
  /FORMAT=NOTABLE
  /STATISTICS=MEAN STDDEV MIN MAX
  /HISTOGRAM.

* Create summary table.
SUMMARIZE
  /TABLES=Study_Name Rhythmic_Metabolites Total_Metabolites Proportion SE
  /FORMAT=LIST NOCASENUM TOTAL
  /TITLE='Individual Study Results'
  /CELLS=NONE.
```

## Interpretation Guidelines

### 1. Pooled Proportion
- **Range**: 0 to 1 (or 0% to 100%)
- **Interpretation**: The overall estimated proportion of rhythmic metabolites across all included studies
- **Example**: If Pooled_Proportion_RE = 0.25, then approximately 25% of measured metabolites show circadian rhythmicity

### 2. Confidence Interval
- **95% CI**: Indicates the precision of the pooled estimate
- **Narrow CI**: High precision, consistent findings across studies
- **Wide CI**: Low precision, more uncertainty in the estimate

### 3. Heterogeneity Statistics

#### Q-Statistic
- **Null Hypothesis**: All studies share a common effect size
- **p < 0.10**: Significant heterogeneity present
- **Interpretation**: Reject null hypothesis if p < 0.10

#### I² Statistic
- **0-25%**: Low heterogeneity (use fixed-effects)
- **25-50%**: Moderate heterogeneity
- **50-75%**: Substantial heterogeneity (use random-effects)
- **75-100%**: Considerable heterogeneity (use random-effects, explore sources)

#### Tau² (τ²)
- **Magnitude**: Variance between studies
- **Zero**: No between-study variance
- **Large values**: Substantial differences between study effects

### 4. Model Selection
- **Fixed-Effects**: Use when I² < 25% and Q is not significant
- **Random-Effects**: Use when I² ≥ 50% or Q is significant (p < 0.10)
- **Default Recommendation**: Random-effects model is generally more conservative

## Subgroup Analysis

To examine whether the proportion varies by study characteristics (e.g., tissue type):

```spss
* Subgroup analysis by tissue type.
SORT CASES BY Tissue_Type.
SPLIT FILE BY Tissue_Type.

* Repeat meta-analysis calculations for each subgroup.
* [Insert Steps 3-6 here for each subgroup]

SPLIT FILE OFF.
```

## Sensitivity Analysis

### 1. Leave-One-Out Analysis
Test robustness by removing each study sequentially:

```spss
* This requires looping through each study.
* Temporarily filter out one study, recalculate pooled effect, restore study.
* Compare results to identify influential studies.
```

### 2. Influence Analysis
Identify studies with disproportionate influence on pooled estimate.

## Publication Bias Assessment

### Funnel Plot (Visual)
Plot effect size (proportion) vs. standard error to detect asymmetry.

### Egger's Test (Statistical)
Tests for funnel plot asymmetry:

```spss
* Calculate standardized effect and precision.
COMPUTE Standardized_Effect = FT_Transform / SQRT(FT_Variance).
COMPUTE Precision = 1 / SQRT(FT_Variance).
EXECUTE.

* Regression of standardized effect on precision.
* A significant intercept (p < 0.10) suggests publication bias.
REGRESSION
  /STATISTICS COEFF OUTS R ANOVA
  /DEPENDENT Standardized_Effect
  /METHOD=ENTER Precision
  /SAVE PRED RESID.

* Note: Check the coefficient table in the output.
* If the intercept p-value < 0.10, there is evidence of publication bias.
```

Interpret the intercept from the coefficient table: A significant intercept (p < 0.10) suggests publication bias.

## Reporting Results

### Required Information

1. **Number of studies included**: K studies with N total metabolites measured
2. **Pooled proportion**: Point estimate with 95% CI
3. **Model used**: Fixed-effects or random-effects with justification
4. **Heterogeneity statistics**: Q-statistic (p-value), I², τ²
5. **Individual study results**: Table or forest plot
6. **Subgroup analyses**: If performed
7. **Publication bias assessment**: If performed
8. **Sensitivity analyses**: If performed

### Example Results Statement

> "A random-effects meta-analysis of K studies measuring N total metabolites revealed that 25.3% (95% CI: 18.7%-32.4%) of metabolites exhibited significant circadian rhythmicity. There was substantial heterogeneity between studies (Q = 45.2, df = 7, p < 0.001; I² = 72.3%; τ² = 0.043). Subgroup analysis by tissue type showed higher proportions in blood samples (32.1%, 95% CI: 24.5%-40.2%) compared to urine samples (18.5%, 95% CI: 12.3%-26.1%)."

## Limitations and Considerations

1. **Small Sample Sizes**: Meta-analysis with < 5 studies may have limited power
2. **Zero or 100% Proportions**: Require continuity correction (add 0.5 to cells)
3. **Study Quality**: Consider quality assessment and sensitivity analysis excluding low-quality studies
4. **Different Methods**: Studies using different rhythmicity detection methods may not be directly comparable
5. **Circadian Parameters**: Studies may use different significance thresholds (e.g., q < 0.05 vs. p < 0.01)
6. **Tissue Differences**: Metabolite rhythmicity varies substantially by tissue type

## References and Resources

### Key References for Meta-Analysis of Proportions
1. Barendregt, J. J., Doi, S. A., Lee, Y. Y., Norman, R. E., & Vos, T. (2013). Meta-analysis of prevalence. *Journal of Epidemiology and Community Health*, 67(11), 974-978.
2. Freeman, M. F., & Tukey, J. W. (1950). Transformations related to the angular and the square root. *The Annals of Mathematical Statistics*, 21(4), 607-611.
3. DerSimonian, R., & Laird, N. (1986). Meta-analysis in clinical trials. *Controlled Clinical Trials*, 7(3), 177-188.
4. Higgins, J. P., & Thompson, S. G. (2002). Quantifying heterogeneity in a meta-analysis. *Statistics in Medicine*, 21(11), 1539-1558.

### SPSS Resources
- IBM SPSS Statistics Documentation: https://www.ibm.com/docs/en/spss-statistics/
- Meta-analysis extensions and macros for SPSS

### Alternative Software
For more comprehensive meta-analysis features, consider:
- **R**: metafor package, meta package
- **Comprehensive Meta-Analysis (CMA)**: Commercial software with GUI
- **RevMan**: Free software from Cochrane Collaboration
- **MetaXL**: Excel-based meta-analysis tool

## Appendix: Complete SPSS Syntax File

See the accompanying file `Meta_Analysis_Proportions.sps` for complete, ready-to-use SPSS syntax.

## Contact and Contributions

For questions or contributions to this guide, please refer to the repository documentation.
