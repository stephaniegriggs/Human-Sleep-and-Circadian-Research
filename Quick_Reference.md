# Quick Reference: Meta-Analysis in SPSS for Rhythmic Metabolites

## Quick Start Checklist

- [ ] Prepare data with required variables (Study_ID, Rhythmic_Metabolites, Total_Metabolites)
- [ ] Import data into SPSS
- [ ] Run `Meta_Analysis_Proportions.sps` syntax
- [ ] Check heterogeneity statistics (I², Q)
- [ ] Select appropriate model (Fixed vs. Random-Effects)
- [ ] Interpret pooled proportion and confidence intervals
- [ ] Report results

## Required Variables

| Variable | Type | Description |
|----------|------|-------------|
| Study_ID | Numeric | Unique identifier for each study |
| Study_Name | String | Study name or citation |
| Rhythmic_Metabolites | Numeric | Number of rhythmic metabolites |
| Total_Metabolites | Numeric | Total metabolites measured |
| Sample_Size | Numeric | Number of participants (optional) |

## Key SPSS Commands

### Calculate Proportion
```spss
COMPUTE Proportion = Rhythmic_Metabolites / Total_Metabolites.
```

### Freeman-Tukey Transformation
```spss
COMPUTE FT_Transform = 0.5 * (ARSIN(SQRT(Rhythmic_Metabolites / (Total_Metabolites + 1))) + 
                              ARSIN(SQRT((Rhythmic_Metabolites + 1) / (Total_Metabolites + 1)))).
```

### Calculate Weights
```spss
COMPUTE FT_Variance = 1 / (4 * Total_Metabolites).
COMPUTE Weight = 1 / FT_Variance.
```

### Pooled Estimate (Fixed-Effects)
```spss
COMPUTE Pooled_Effect_FE = Sum_Weighted_Effect / Sum_Weight.
COMPUTE Pooled_Proportion_FE = (SIN(Pooled_Effect_FE)) ** 2.
```

### Heterogeneity (Q and I²)
```spss
COMPUTE Q_Statistic = SUM(Weight * ((FT_Transform - Pooled_Effect_FE) ** 2)).
COMPUTE I_Squared = 100 * ((Q_Statistic - DF) / Q_Statistic).
```

### Random-Effects Model
```spss
COMPUTE Tau_Squared = (Q_Statistic - DF) / C.
COMPUTE Weight_RE = 1 / (FT_Variance + Tau_Squared).
COMPUTE Pooled_Effect_RE = Sum_Weighted_Effect_RE / Sum_Weight_RE.
```

## Interpretation Guide

### Heterogeneity Levels
- **I² < 25%**: Low heterogeneity → Use Fixed-Effects
- **I² 25-50%**: Moderate heterogeneity → Consider Random-Effects
- **I² 50-75%**: Substantial heterogeneity → Use Random-Effects
- **I² > 75%**: Considerable heterogeneity → Use Random-Effects + explore sources

### Q-Statistic
- **p < 0.10**: Significant heterogeneity present
- **p ≥ 0.10**: No significant heterogeneity

### Pooled Proportion
- Range: 0 to 1 (0% to 100%)
- Represents overall proportion of rhythmic metabolites across studies
- Example: 0.25 = 25% of metabolites show rhythmicity

### Confidence Interval
- **Narrow CI**: High precision, consistent findings
- **Wide CI**: Low precision, more uncertainty

## Decision Tree

```
Start
  ↓
Calculate I²
  ↓
I² < 25%? ──Yes──> Use Fixed-Effects Model
  │
  No
  ↓
I² ≥ 50%? ──Yes──> Use Random-Effects Model + Explore Heterogeneity
  │
  No
  ↓
Use Random-Effects Model (Conservative Approach)
```

## Common Formulas

### Standard Error (Binomial)
SE = √[p(1-p) / n]

Where:
- p = proportion
- n = total metabolites

### Confidence Interval (95%)
CI = proportion ± 1.96 × SE

### Weight
w = 1 / variance

### Q-Statistic
Q = Σw(θᵢ - θ̄)²

Where:
- w = weight
- θᵢ = individual study effect
- θ̄ = pooled effect

### I² Statistic
I² = 100% × (Q - df) / Q

### Tau-Squared (τ²)
τ² = (Q - df) / C

Where C = Σw - (Σw²/Σw)

## Reporting Template

### Results Statement
"A [fixed/random]-effects meta-analysis of [K] studies measuring [N] total metabolites revealed that [XX.X]% (95% CI: [XX.X]%-[XX.X]%) of metabolites exhibited significant circadian rhythmicity. [Heterogeneity statement]."

### Heterogeneity Statement
**Low heterogeneity**: "There was low heterogeneity between studies (Q = [X.X], df = [X], p = [X.XX]; I² = [X.X]%)."

**Substantial heterogeneity**: "There was substantial heterogeneity between studies (Q = [X.X], df = [X], p < 0.001; I² = [X.X]%; τ² = [X.XX])."

## Troubleshooting

### Problem: Syntax Error
**Solution**: Ensure all variable names match exactly

### Problem: Missing Values
**Solution**: 
```spss
MISSING VALUES Rhythmic_Metabolites Total_Metabolites ().
FILTER OFF.
```

### Problem: Division by Zero
**Solution**: Check for studies with 0 total metabolites

### Problem: Proportions Outside 0-1
**Solution**: Verify data entry; check for negative values

### Problem: Very High I²
**Solution**: 
1. Use random-effects model
2. Perform subgroup analysis
3. Check for outliers
4. Consider meta-regression

## File Locations

- **Full Guide**: `Meta_Analysis_Guide_SPSS.md`
- **SPSS Syntax**: `Meta_Analysis_Proportions.sps`
- **Example Data**: `Example_Data.md`
- **Quick Reference**: This file

## Next Steps After Meta-Analysis

1. **Subgroup Analysis**: Examine by tissue type, method, etc.
2. **Sensitivity Analysis**: Leave-one-out analysis
3. **Publication Bias**: Funnel plot, Egger's test (if ≥10 studies)
4. **Meta-Regression**: Explore continuous moderators
5. **Report**: Follow PRISMA guidelines

## Statistical Software Alternatives

If SPSS is unavailable or insufficient:
- **R**: `metafor` package (most flexible)
- **Comprehensive Meta-Analysis (CMA)**: Commercial GUI software
- **RevMan**: Free from Cochrane Collaboration
- **MetaXL**: Excel-based add-in

## Key References

1. **Barendregt et al. (2013)**: Meta-analysis of prevalence
2. **Freeman & Tukey (1950)**: Arcsine transformation
3. **DerSimonian & Laird (1986)**: Random-effects model
4. **Higgins & Thompson (2002)**: I² statistic

## Contact

For questions or issues, refer to the repository documentation or open an issue on GitHub.

---
*Last Updated: December 2025*
