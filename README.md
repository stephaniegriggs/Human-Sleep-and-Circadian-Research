# Human Sleep and Circadian Research

This repository contains tools and code for analyzing human sleep and circadian rhythms using actigraphy and biological data (melatonin, glucose, circadian phase markers, and other relevant hormones).

## Features

### Multiple Component Cosinor Analysis

The repository includes a comprehensive implementation of cosinor analysis for circadian rhythm research:

- **Single Component Cosinor Analysis**: Fits a single cosine curve to identify circadian rhythms
- **Multiple Component Cosinor Analysis**: Fits multiple harmonics to model complex rhythms with ultradian components
- **Actigraphy Data Analysis**: Specialized functions for analyzing activity patterns
- **Melatonin Data Analysis**: Tools for analyzing melatonin rhythms and estimating circadian phase
- **Joint Analysis**: Compare phase relationships between actigraphy and melatonin data
- **Model Comparison**: Statistical tools to select the optimal number of components

## Installation

1. Clone this repository:
```bash
git clone https://github.com/stephaniegriggs/Human-Sleep-and-Circadian-Research.git
cd Human-Sleep-and-Circadian-Research
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Example

```python
import numpy as np
from cosinor_analysis import analyze_actigraphy_data, analyze_melatonin_data

# Example with actigraphy data
time = np.linspace(0, 168, 168)  # 7 days, hourly sampling
# Load your activity counts data (e.g., from CSV file)
# activity = np.loadtxt('actigraphy_data.csv')
# Or use synthetic data for testing:
activity = 100 + 80 * np.cos(2 * np.pi * (time - 14) / 24) + np.random.normal(0, 10, len(time))

results = analyze_actigraphy_data(time, activity, period=24.0, n_components=1)
print(f"Activity peak at: {results['acrophase_hours']:.2f} hours")
```

### Running Examples

Run the example script to see demonstrations of all features:

```bash
python example_cosinor_usage.py
```

This will demonstrate:
1. Single component cosinor analysis
2. Multiple component cosinor analysis
3. Model comparison with different numbers of components
4. Joint analysis of actigraphy and melatonin data

### Advanced Usage

#### Multiple Component Analysis

```python
from cosinor_analysis import CosinorAnalysis

# Initialize with your data
cosinor = CosinorAnalysis(time, data, period=24.0)

# Fit multiple components (e.g., 24h and 12h rhythms)
results = cosinor.multiple_component_cosinor(n_components=2)
cosinor.print_summary('multiple')
```

#### Model Comparison

```python
# Compare models with 1, 2, and 3 components
comparison = cosinor.compare_models(max_components=3)
print(f"Best model: {comparison['recommended_components']} components")
```

#### Joint Analysis

```python
from cosinor_analysis import joint_analysis

# Analyze both actigraphy and melatonin together
results = joint_analysis(time, actigraphy_data, melatonin_data, period=24.0)
print(f"Phase difference: {results['phase_difference_hours']:.2f} hours")
```

## Cosinor Analysis Background

Cosinor analysis is a statistical method used to characterize rhythmic patterns in biological time series data. It fits cosine curves to the data and estimates:

- **MESOR** (Midline Estimating Statistic Of Rhythm): The rhythm-adjusted mean
- **Amplitude**: Half the peak-to-trough distance of the fitted curve
- **Acrophase**: The time of peak in the fitted curve (phase marker)

Multiple component cosinor extends this to fit multiple harmonics, allowing for the analysis of complex rhythms with multiple periodicities (e.g., circadian + ultradian rhythms).

## References

- Cornelissen, G. (2014). Cosinor-based rhythmometry. *Theoretical Biology and Medical Modelling*, 11, 16.
- Refinetti, R., Lissen, G. C., & Halberg, F. (2007). Procedures for numerical analysis of circadian rhythms. *Biological Rhythm Research*, 38(4), 275-325.
- Nelson, W., et al. (1979). Methods for cosinor-rhythmometry. *Chronobiologia*, 6(4), 305-323.

## License

This project is open source and available for research purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
