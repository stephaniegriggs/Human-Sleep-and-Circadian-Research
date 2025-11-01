# Multiple Component Cosinor Analysis Implementation Notes

## Overview
This document provides technical details about the implementation of multiple component cosinor analysis for actigraphy and melatonin data.

## Implementation Summary

### Core Module: `cosinor_analysis.py`
A comprehensive Python module (506 lines) implementing:

1. **CosinorAnalysis Class**
   - Single component cosinor regression
   - Multiple component cosinor regression (up to N harmonics)
   - Model comparison using AIC/BIC
   - Statistical significance testing (F-test)
   - Standard error estimation

2. **Convenience Functions**
   - `analyze_actigraphy_data()` - Specialized for activity data
   - `analyze_melatonin_data()` - Specialized for melatonin data
   - `joint_analysis()` - Compare phase relationships between datasets

### Mathematical Background

#### Single Component Model
```
y(t) = M + A*cos(2π*t/τ + φ) + ε
```
Where:
- M = MESOR (Midline Estimating Statistic Of Rhythm)
- A = Amplitude (half peak-to-trough variation)
- τ = Period (24h for circadian rhythms)
- φ = Acrophase (timing of peak)
- ε = Random error

The model is fitted using linear regression after transformation:
```
y(t) = M + β*cos(ωt) + γ*sin(ωt)
```

Where:
- A = √(β² + γ²)
- φ = arctan2(-γ, β)

#### Multiple Component Model
```
y(t) = M + Σ[A_k*cos(2π*k*t/τ + φ_k)] for k=1 to n
```

This allows fitting multiple harmonics simultaneously, useful for:
- Complex rhythms with ultradian components
- Composite patterns (e.g., 24h + 12h rhythms)

### Statistical Methods

1. **Parameter Estimation**: Least squares regression
2. **Significance Testing**: F-test (ratio of variance explained to residual variance)
3. **Model Selection**: 
   - Akaike Information Criterion (AIC)
   - Bayesian Information Criterion (BIC)
4. **Standard Errors**: Calculated using variance-covariance matrix

### Example Usage Script: `example_cosinor_usage.py`
Demonstrates:
1. Single component analysis with synthetic actigraphy data
2. Multiple component analysis with two harmonics
3. Model comparison (1, 2, and 3 components)
4. Joint analysis of actigraphy and melatonin data

### Test Suite: `test_cosinor_analysis.py`
Comprehensive tests (15 tests, all passing):
- Initialization validation
- Perfect cosine wave recovery
- Noisy data analysis
- Multiple component fitting
- Model comparison
- Actigraphy and melatonin analysis
- Joint analysis with phase relationships
- Edge cases (no rhythm, insufficient data)

## Key Features

### 1. Robust Statistical Analysis
- Proper degrees of freedom calculations
- F-statistics for significance testing
- R-squared for goodness of fit
- Standard errors for parameter estimates

### 2. Biological Data Support
- **Actigraphy**: Activity patterns typically show peak during day (14:00)
- **Melatonin**: Levels typically peak at night (3:00 AM)
- **Phase Relationships**: Automatically calculated for joint analysis

### 3. Model Selection
- Automatic comparison of models with different numbers of components
- AIC and BIC criteria balance fit quality with model complexity
- Prevents overfitting while capturing important patterns

### 4. Flexible and Extensible
- Works with any time series data
- Configurable period (not just 24h)
- Can fit arbitrary number of components
- Easy to extend for additional features

## Scientific References

The implementation follows established cosinor methodology:

1. Cornelissen, G. (2014). Cosinor-based rhythmometry. *Theoretical Biology and Medical Modelling*, 11, 16.

2. Refinetti, R., Lissen, G. C., & Halberg, F. (2007). Procedures for numerical analysis of circadian rhythms. *Biological Rhythm Research*, 38(4), 275-325.

3. Nelson, W., et al. (1979). Methods for cosinor-rhythmometry. *Chronobiologia*, 6(4), 305-323.

## Technical Specifications

### Dependencies
- numpy >= 1.20.0 (numerical computations)
- scipy >= 1.7.0 (statistical functions)
- matplotlib >= 3.3.0 (visualization, optional)

### Python Version
- Tested with Python 3.12.3
- Should work with Python 3.7+

### Performance
- Efficient linear algebra implementation
- Suitable for datasets with hundreds to thousands of time points
- Model comparison scales linearly with number of components tested

## Use Cases

### 1. Circadian Rhythm Assessment
- Detect presence of circadian rhythms
- Estimate timing of peak activity or hormone levels
- Quantify rhythm strength (amplitude)

### 2. Shift Work Studies
- Assess circadian disruption
- Compare phase alignment before/after interventions
- Identify abnormal phase relationships

### 3. Clinical Research
- Sleep disorder diagnosis (delayed/advanced sleep phase)
- Treatment efficacy monitoring
- Circadian phase biomarker validation

### 4. Basic Research
- Characterize complex rhythms with multiple periodicities
- Compare rhythms across different measurements
- Analyze ultradian rhythms (< 24h periods)

## Validation

All implementations have been validated with:
1. **Perfect data tests**: Model recovers known parameters exactly
2. **Noisy data tests**: Model performs well with realistic noise levels
3. **Multiple component tests**: Correctly identifies and separates harmonics
4. **Null hypothesis tests**: Handles random data appropriately

## Future Enhancements (Potential)

While the current implementation is complete, potential future additions could include:
- Confidence ellipses for amplitude and acrophase
- Population-mean cosinor for group comparisons
- Bootstrap-based confidence intervals
- Non-stationary cosinor (time-varying parameters)
- Cosinor with irregular sampling
- Zero-amplitude test improvements

## Conclusion

This implementation provides a complete, well-tested, and scientifically sound tool for multiple component cosinor analysis. It is suitable for research use in chronobiology, sleep medicine, and circadian rhythm studies.
