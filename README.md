# Human-Sleep-and-Circadian-Research

We will save code and syntax here to analyze human sleep and circadian actigraphy and biological data (glucose, circadian phase, and other relevant hormones).

## Meta-Analysis Resources

This repository includes comprehensive resources for conducting meta-analyses in SPSS, specifically designed for estimating the proportion of rhythmic metabolites across multiple studies.

### Available Files

1. **[Meta_Analysis_Guide_SPSS.md](Meta_Analysis_Guide_SPSS.md)** - Complete guide for conducting meta-analysis of proportions in SPSS
   - Detailed methodology for proportion meta-analysis
   - Step-by-step instructions with SPSS commands
   - Interpretation guidelines
   - Subgroup and sensitivity analysis procedures
   - Publication bias assessment

2. **[Meta_Analysis_Proportions.sps](Meta_Analysis_Proportions.sps)** - Ready-to-use SPSS syntax file
   - Complete SPSS syntax for meta-analysis
   - Freeman-Tukey double arcsine transformation
   - Fixed-effects and random-effects models
   - Heterogeneity assessment (Q-statistic, I²)
   - Forest plot data preparation
   - Automated result reporting

3. **[Example_Data.md](Example_Data.md)** - Example dataset and expected results
   - Sample data from 8 hypothetical studies
   - Expected meta-analysis outcomes
   - Instructions for data entry and import
   - Subgroup analysis examples

4. **[Quick_Reference.md](Quick_Reference.md)** - Quick reference guide
   - Essential SPSS commands
   - Interpretation flowchart
   - Troubleshooting tips
   - Reporting templates

### Quick Start

To conduct a meta-analysis on rhythmic metabolites:

1. Prepare your data with the following variables:
   - `Study_ID`: Unique study identifier
   - `Study_Name`: Study name or citation
   - `Rhythmic_Metabolites`: Number of metabolites showing rhythmicity
   - `Total_Metabolites`: Total number of metabolites measured

2. Open SPSS and import your data

3. Run the `Meta_Analysis_Proportions.sps` syntax file

4. Review the output for:
   - Pooled proportion estimate (Fixed and Random-Effects)
   - Heterogeneity statistics (Q, I², τ²)
   - Individual study results
   - Model recommendations

5. Interpret results using the guidelines in `Meta_Analysis_Guide_SPSS.md`

### Key Features

- **Freeman-Tukey Transformation**: Stabilizes variance for proportions near 0 or 1
- **Both Models**: Fixed-effects and random-effects meta-analysis
- **Heterogeneity Assessment**: Q-statistic, I² (I-squared), and tau-squared
- **Automated Decisions**: Recommendations for model selection based on heterogeneity
- **Publication Bias**: Funnel plot and Egger's test
- **Subgroup Analysis**: Framework for analyzing by tissue type, method, etc.

### Use Case

This meta-analysis approach is designed for circadian rhythm and metabolomics research where researchers want to:
- Estimate the overall proportion of rhythmic metabolites across studies
- Account for between-study heterogeneity
- Compare findings across different tissue types or analysis methods
- Synthesize evidence from multiple metabolomics studies

### Citation

When using these resources, please cite the original methodological papers:
- Freeman, M. F., & Tukey, J. W. (1950). Transformations related to the angular and the square root. *The Annals of Mathematical Statistics*, 21(4), 607-611.
- DerSimonian, R., & Laird, N. (1986). Meta-analysis in clinical trials. *Controlled Clinical Trials*, 7(3), 177-188.

### Support

For questions or issues, please refer to the detailed documentation in `Meta_Analysis_Guide_SPSS.md` or open an issue in this repository.
