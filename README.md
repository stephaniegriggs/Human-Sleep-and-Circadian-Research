# Human-Sleep-and-Circadian-Research

We will save code and syntax here to analyze human sleep and circadian actigraphy and biological data (glucose, circadian phase, and other relevant hormones)

## Age Stratification

This repository includes comprehensive tools for stratifying participants by age in the 40-75 year range, which is critical for analyzing age-related effects in sleep and circadian research.

### Available Tools

1. **R Implementation**: `age_stratification.R`
   - Five different stratification methods
   - Built-in demonstration function
   - No additional packages required

2. **Python Implementation**: `age_stratification.py`
   - Five different stratification methods
   - Built-in demonstration function
   - Requires: numpy, pandas

3. **Comprehensive Guide**: `AGE_STRATIFICATION_GUIDE.md`
   - Detailed explanation of each method
   - When to use each approach
   - Sample size considerations
   - Reporting guidelines

### Quick Start

#### R
```r
# Source the script
source("age_stratification.R")

# View demonstration
demonstrate_stratification()

# Use with your data
ages <- c(42, 55, 68, 73, 45, 50, 61)
age_groups <- stratify_age_quartiles(ages)
```

#### Python
```python
# Install dependencies
pip install -r requirements.txt

# Import the module
from age_stratification import stratify_age_quartiles

# Use with your data
ages = [42, 55, 68, 73, 45, 50, 61]
age_groups = stratify_age_quartiles(ages)
```

### Stratification Methods

1. **Equal-Width Bins**: Divides age range into equal intervals
2. **Quartiles**: Data-driven groups with equal sample sizes
3. **Custom Breaks**: User-defined age boundaries
4. **Median Split**: Simple binary younger/older division
5. **Decades**: Groups by decade of life (40s, 50s, 60s, 70s)

See `AGE_STRATIFICATION_GUIDE.md` for detailed information on choosing the right method for your research.

