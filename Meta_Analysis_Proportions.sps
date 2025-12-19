* ============================================================================.
* META-ANALYSIS OF PROPORTIONS IN SPSS
* Estimating Rhythmic Metabolites Relative to Measured Metabolites
* ============================================================================.
* 
* Purpose: This syntax performs a meta-analysis on proportion data to estimate
*          the pooled proportion of rhythmic metabolites across multiple studies.
*
* Required Variables in Dataset:
*   - Study_ID: Unique study identifier
*   - Study_Name: Name or citation of study
*   - Rhythmic_Metabolites: Number of rhythmic metabolites
*   - Total_Metabolites: Total number of metabolites measured
*   - Sample_Size: Number of participants (optional, for weighting)
*
* Author: Human Sleep and Circadian Research Repository
* Date: December 2025
* ============================================================================.

* -----------------------------------------------------------------------------.
* SECTION 1: DATA INPUT AND PREPARATION
* -----------------------------------------------------------------------------.

* Option A: Enter data directly.
* Uncomment the following section to enter data manually.

/*
DATA LIST FREE /
  Study_ID (F3.0)
  Study_Name (A50)
  Rhythmic_Metabolites (F5.0)
  Total_Metabolites (F5.0)
  Sample_Size (F4.0).
BEGIN DATA
1 "Smith_2020" 45 200 30
2 "Jones_2021" 32 150 25
3 "Brown_2022" 67 300 40
4 "Davis_2021" 28 180 35
5 "Wilson_2023" 52 250 28
6 "Taylor_2022" 41 195 32
7 "Anderson_2023" 38 175 27
8 "Thomas_2021" 55 280 38
END DATA.
EXECUTE.
*/.

* Option B: Import data from Excel/CSV file.
* Adjust file path as needed.

/*
GET DATA
  /TYPE=XLSX
  /FILE='C:\Users\YourName\Documents\MetaAnalysis_Data.xlsx'
  /SHEET=name 'Sheet1'
  /CELLRANGE=FULL
  /READNAMES=ON
  /DATATYPEMIN PERCENTAGE=95.0
  /HIDDEN IGNORE=YES.
CACHE.
EXECUTE.
*/.

* Verify data import.
LIST VARIABLES.
DESCRIPTIVES VARIABLES=Rhythmic_Metabolites Total_Metabolites Sample_Size
  /STATISTICS=MEAN STDDEV MIN MAX.

* -----------------------------------------------------------------------------.
* SECTION 2: CALCULATE BASIC PROPORTIONS AND STATISTICS
* -----------------------------------------------------------------------------.

* Calculate the proportion of rhythmic metabolites for each study.
COMPUTE Proportion = Rhythmic_Metabolites / Total_Metabolites.
EXECUTE.

* Calculate standard error using binomial distribution formula.
COMPUTE SE = SQRT((Proportion * (1 - Proportion)) / Total_Metabolites).
EXECUTE.

* Calculate variance.
COMPUTE Variance = SE ** 2.
EXECUTE.

* Calculate 95% confidence interval for each study (Wald method).
COMPUTE CI_Lower_Study = Proportion - (1.96 * SE).
COMPUTE CI_Upper_Study = Proportion + (1.96 * SE).

* Adjust for boundaries (keep within 0-1).
IF (CI_Lower_Study < 0) CI_Lower_Study = 0.
IF (CI_Upper_Study > 1) CI_Upper_Study = 1.
EXECUTE.

* Display individual study results.
SUMMARIZE
  /TABLES=Study_Name Rhythmic_Metabolites Total_Metabolites Proportion SE CI_Lower_Study CI_Upper_Study
  /FORMAT=LIST NOCASENUM TOTAL
  /TITLE='Individual Study Results'
  /CELLS=NONE.

* -----------------------------------------------------------------------------.
* SECTION 3: FREEMAN-TUKEY DOUBLE ARCSINE TRANSFORMATION
* -----------------------------------------------------------------------------.

* Apply Freeman-Tukey double arcsine transformation to stabilize variance.
* This transformation is particularly useful for proportions near 0 or 1.

COMPUTE FT_Transform = 0.5 * (ARSIN(SQRT(Rhythmic_Metabolites / (Total_Metabolites + 1))) + 
                              ARSIN(SQRT((Rhythmic_Metabolites + 1) / (Total_Metabolites + 1)))).
EXECUTE.

* Calculate sampling variance for transformed values.
COMPUTE FT_Variance = 1 / (4 * Total_Metabolites).
EXECUTE.

* Calculate weight (inverse variance) for each study.
COMPUTE Weight = 1 / FT_Variance.
EXECUTE.

* -----------------------------------------------------------------------------.
* SECTION 4: FIXED-EFFECTS META-ANALYSIS
* -----------------------------------------------------------------------------.

* Calculate the weighted mean proportion using fixed-effects model.
AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Sum_Weight = SUM(Weight)
  /Sum_Weighted_Effect = SUM(Weight * FT_Transform)
  /K_Studies = N.

* Calculate pooled effect size (fixed-effects).
COMPUTE Pooled_Effect_FE = Sum_Weighted_Effect / Sum_Weight.
EXECUTE.

* Calculate standard error of pooled effect.
COMPUTE SE_Pooled_FE = SQRT(1 / Sum_Weight).
EXECUTE.

* Calculate 95% confidence interval for pooled effect.
COMPUTE CI_Lower_FE_Trans = Pooled_Effect_FE - (1.96 * SE_Pooled_FE).
COMPUTE CI_Upper_FE_Trans = Pooled_Effect_FE + (1.96 * SE_Pooled_FE).
EXECUTE.

* Back-transform to proportion scale using inverse Freeman-Tukey transformation.
COMPUTE Pooled_Proportion_FE = (SIN(Pooled_Effect_FE)) ** 2.
COMPUTE Proportion_CI_Lower_FE = (SIN(CI_Lower_FE_Trans)) ** 2.
COMPUTE Proportion_CI_Upper_FE = (SIN(CI_Upper_FE_Trans)) ** 2.
EXECUTE.

* -----------------------------------------------------------------------------.
* SECTION 5: HETEROGENEITY ASSESSMENT (Q-STATISTIC AND I²)
* -----------------------------------------------------------------------------.

* Calculate Q-statistic to test for heterogeneity between studies.
COMPUTE Q_Component = Weight * ((FT_Transform - Pooled_Effect_FE) ** 2).
EXECUTE.

AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Q_Statistic = SUM(Q_Component).

* Calculate degrees of freedom for Q-statistic.
COMPUTE DF = K_Studies - 1.
EXECUTE.

* Calculate p-value for Q-statistic (chi-square distribution).
COMPUTE Q_P_Value = 1 - CDF.CHISQ(Q_Statistic, DF).
EXECUTE.

* Calculate I-squared statistic (percentage of variation due to heterogeneity).
* I² = 100% × (Q - df) / Q
COMPUTE I_Squared = 100 * ((Q_Statistic - DF) / Q_Statistic).

* I² cannot be negative; set to 0 if Q ≤ df.
IF (Q_Statistic <= DF) I_Squared = 0.
EXECUTE.

* -----------------------------------------------------------------------------.
* SECTION 6: RANDOM-EFFECTS META-ANALYSIS (DERSIMONIAN-LAIRD METHOD)
* -----------------------------------------------------------------------------.

* Calculate C constant for tau-squared estimation.
AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Sum_Weight_Squared = SUM(Weight ** 2).

COMPUTE C = Sum_Weight - (Sum_Weight_Squared / Sum_Weight).
EXECUTE.

* Calculate between-study variance (tau-squared) using DerSimonian-Laird method.
COMPUTE Tau_Squared = (Q_Statistic - DF) / C.

* Tau-squared cannot be negative; set to 0 if Q ≤ df.
IF (Tau_Squared < 0) Tau_Squared = 0.
EXECUTE.

* Calculate random-effects weight for each study.
COMPUTE Weight_RE = 1 / (FT_Variance + Tau_Squared).
EXECUTE.

* Calculate pooled effect size (random-effects).
AGGREGATE OUTFILE=* MODE=ADDVARIABLES
  /BREAK=
  /Sum_Weight_RE = SUM(Weight_RE)
  /Sum_Weighted_Effect_RE = SUM(Weight_RE * FT_Transform).

COMPUTE Pooled_Effect_RE = Sum_Weighted_Effect_RE / Sum_Weight_RE.
EXECUTE.

* Calculate standard error and confidence interval for random-effects pooled effect.
COMPUTE SE_Pooled_RE = SQRT(1 / Sum_Weight_RE).
COMPUTE CI_Lower_RE_Trans = Pooled_Effect_RE - (1.96 * SE_Pooled_RE).
COMPUTE CI_Upper_RE_Trans = Pooled_Effect_RE + (1.96 * SE_Pooled_RE).
EXECUTE.

* Back-transform to proportion scale.
COMPUTE Pooled_Proportion_RE = (SIN(Pooled_Effect_RE)) ** 2.
COMPUTE Proportion_CI_Lower_RE = (SIN(CI_Lower_RE_Trans)) ** 2.
COMPUTE Proportion_CI_Upper_RE = (SIN(CI_Upper_RE_Trans)) ** 2.
EXECUTE.

* -----------------------------------------------------------------------------.
* SECTION 7: RESULTS SUMMARY AND OUTPUT
* -----------------------------------------------------------------------------.

* Create a summary table of key results.
* Note: This will display one row per case with summary statistics.

TITLE 'META-ANALYSIS RESULTS SUMMARY'.

* Format output for readability.
FORMATS 
  Pooled_Proportion_FE Proportion_CI_Lower_FE Proportion_CI_Upper_FE
  Pooled_Proportion_RE Proportion_CI_Lower_RE Proportion_CI_Upper_RE
  Proportion (F8.4)
  Q_Statistic Tau_Squared (F10.4)
  Q_P_Value (F10.6)
  I_Squared (F8.2)
  K_Studies (F3.0).

* Display Fixed-Effects Results.
COMPUTE Model = 1.
VARIABLE LABELS Model 'Analysis Model (1=FE, 2=RE)'.
VALUE LABELS Model 1 'Fixed-Effects' 2 'Random-Effects'.

SUMMARIZE
  /TABLES=Model K_Studies Pooled_Proportion_FE Proportion_CI_Lower_FE Proportion_CI_Upper_FE
  /FORMAT=LIST NOCASENUM NOTOTAL LIMIT=1
  /TITLE='Fixed-Effects Model Results'
  /FOOTNOTE='Pooled proportion with 95% confidence interval'
  /CELLS=NONE.

* Display Random-Effects Results.
COMPUTE Model = 2.
SUMMARIZE
  /TABLES=Model K_Studies Pooled_Proportion_RE Proportion_CI_Lower_RE Proportion_CI_Upper_RE
  /FORMAT=LIST NOCASENUM NOTOTAL LIMIT=1
  /TITLE='Random-Effects Model Results'
  /FOOTNOTE='Pooled proportion with 95% confidence interval'
  /CELLS=NONE.

* Display Heterogeneity Statistics.
SUMMARIZE
  /TABLES=Q_Statistic DF Q_P_Value I_Squared Tau_Squared
  /FORMAT=LIST NOCASENUM NOTOTAL LIMIT=1
  /TITLE='Heterogeneity Statistics'
  /FOOTNOTE='Q = Cochran Q statistic; I² = I-squared; τ² = Tau-squared'
  /CELLS=NONE.

* -----------------------------------------------------------------------------.
* SECTION 8: INTERPRETATION GUIDE
* -----------------------------------------------------------------------------.

* Decision rule for model selection based on heterogeneity.
STRING Model_Recommendation (A50).
IF (I_Squared < 25) Model_Recommendation = 'Use Fixed-Effects Model'.
IF (I_Squared >= 25 AND I_Squared < 50) Model_Recommendation = 'Consider Random-Effects Model'.
IF (I_Squared >= 50) Model_Recommendation = 'Use Random-Effects Model (Substantial Heterogeneity)'.
EXECUTE.

STRING Heterogeneity_Level (A30).
IF (I_Squared < 25) Heterogeneity_Level = 'Low'.
IF (I_Squared >= 25 AND I_Squared < 50) Heterogeneity_Level = 'Moderate'.
IF (I_Squared >= 50 AND I_Squared < 75) Heterogeneity_Level = 'Substantial'.
IF (I_Squared >= 75) Heterogeneity_Level = 'Considerable'.
EXECUTE.

SUMMARIZE
  /TABLES=Heterogeneity_Level Model_Recommendation
  /FORMAT=LIST NOCASENUM NOTOTAL LIMIT=1
  /TITLE='Model Selection Recommendation'
  /CELLS=NONE.

* -----------------------------------------------------------------------------.
* SECTION 9: CREATE FOREST PLOT DATA
* -----------------------------------------------------------------------------.

* Sort studies by proportion for better visualization.
SORT CASES BY Proportion (A).

* Create formatted study labels for forest plot.
STRING Study_Label (A100).
COMPUTE Study_Label = CONCAT(RTRIM(Study_Name), " (", 
                             STRING(Rhythmic_Metabolites, F8.0), "/",
                             STRING(Total_Metabolites, F8.0), ")").
EXECUTE.

* Calculate percentage for easier interpretation.
COMPUTE Proportion_Percent = Proportion * 100.
COMPUTE CI_Lower_Percent = CI_Lower_Study * 100.
COMPUTE CI_Upper_Percent = CI_Upper_Study * 100.
EXECUTE.

* Display forest plot data.
SUMMARIZE
  /TABLES=Study_Label Proportion_Percent CI_Lower_Percent CI_Upper_Percent Weight_RE
  /FORMAT=LIST NOCASENUM TOTAL
  /TITLE='Forest Plot Data (Studies Sorted by Proportion)'
  /FOOTNOTE='Use this data to create a forest plot in SPSS Chart Builder or external software'
  /CELLS=NONE.

* -----------------------------------------------------------------------------.
* SECTION 10: SUBGROUP ANALYSIS (OPTIONAL)
* -----------------------------------------------------------------------------.

* If you have a grouping variable (e.g., Tissue_Type, Analysis_Method),
* you can perform subgroup analysis.

* Example: Subgroup analysis by tissue type.
* Uncomment and modify as needed.

/*
SORT CASES BY Tissue_Type.
SPLIT FILE BY Tissue_Type.

* Repeat calculations for each subgroup.
* [You would repeat Sections 3-7 here for each subgroup]

* Compare subgroups.
SUMMARIZE
  /TABLES=Tissue_Type Pooled_Proportion_RE Proportion_CI_Lower_RE Proportion_CI_Upper_RE I_Squared
  /FORMAT=LIST NOCASENUM TOTAL
  /TITLE='Subgroup Analysis Results'
  /CELLS=NONE.

SPLIT FILE OFF.
*/.

* -----------------------------------------------------------------------------.
* SECTION 11: PUBLICATION BIAS ASSESSMENT (OPTIONAL)
* -----------------------------------------------------------------------------.

* Funnel plot data: Plot effect size vs. standard error.
* Visual asymmetry suggests publication bias.

* Calculate standardized effect for funnel plot.
COMPUTE Standardized_Effect = FT_Transform / SQRT(FT_Variance).
COMPUTE Precision = 1 / SQRT(FT_Variance).
EXECUTE.

* Egger's regression test for funnel plot asymmetry.
* Test if intercept is significantly different from zero.

REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS R ANOVA
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN 
  /DEPENDENT Standardized_Effect
  /METHOD=ENTER Precision
  /SAVE PRED RESID.

* Note: A significant intercept (p < 0.10) suggests funnel plot asymmetry,
*       which may indicate publication bias.

* -----------------------------------------------------------------------------.
* SECTION 12: SENSITIVITY ANALYSIS (OPTIONAL)
* -----------------------------------------------------------------------------.

* Leave-one-out analysis: Remove each study sequentially and recalculate.
* This identifies influential studies that heavily impact the pooled estimate.

* Manual approach: Use SELECT IF to exclude one study at a time, then re-run analysis.

/*
* Example: Exclude Study 1.
TEMPORARY.
SELECT IF (Study_ID ~= 1).
* [Re-run Sections 3-7 to recalculate pooled estimate]
*/.

* -----------------------------------------------------------------------------.
* SECTION 13: EXPORT RESULTS (OPTIONAL)
* -----------------------------------------------------------------------------.

* Save key results to a new dataset for further analysis or reporting.
* Uncomment to export results.

/*
SAVE OUTFILE='C:\Users\YourName\Documents\MetaAnalysis_Results.sav'
  /KEEP Study_ID Study_Name Study_Label 
       Rhythmic_Metabolites Total_Metabolites Proportion SE CI_Lower_Study CI_Upper_Study
       FT_Transform FT_Variance Weight Weight_RE
       Pooled_Proportion_FE Proportion_CI_Lower_FE Proportion_CI_Upper_FE
       Pooled_Proportion_RE Proportion_CI_Lower_RE Proportion_CI_Upper_RE
       Q_Statistic DF Q_P_Value I_Squared Tau_Squared
       Heterogeneity_Level Model_Recommendation
  /COMPRESSED.
*/.

* Export results to Excel.
/*
SAVE TRANSLATE OUTFILE='C:\Users\YourName\Documents\MetaAnalysis_Results.xlsx'
  /TYPE=XLS
  /VERSION=12
  /MAP
  /REPLACE
  /FIELDNAMES
  /CELLS=VALUES.
*/.

* -----------------------------------------------------------------------------.
* SECTION 14: CREATE VISUALIZATIONS
* -----------------------------------------------------------------------------.

* Generate histogram of study proportions.
GRAPH
  /HISTOGRAM=Proportion
  /TITLE='Distribution of Proportions Across Studies'.

* Generate bar chart comparing fixed-effects vs. random-effects estimates.
* Note: This requires data restructuring for proper visualization.

* Generate scatter plot for funnel plot (effect size vs. SE).
GRAPH
  /SCATTERPLOT(BIVAR)=SE WITH Proportion
  /TITLE='Funnel Plot: Proportion vs. Standard Error'
  /MISSING=LISTWISE.

* -----------------------------------------------------------------------------.
* END OF SYNTAX
* -----------------------------------------------------------------------------.

* Final Note: 
* 1. Review heterogeneity statistics to choose between fixed and random-effects models.
* 2. If I² > 50% or Q p-value < 0.10, use random-effects model results.
* 3. Interpret the pooled proportion in the context of your research question.
* 4. Consider subgroup and sensitivity analyses if substantial heterogeneity exists.
* 5. Assess publication bias if number of studies ≥ 10.

* For questions or issues, consult the accompanying Meta_Analysis_Guide_SPSS.md document.

* ============================================================================.
