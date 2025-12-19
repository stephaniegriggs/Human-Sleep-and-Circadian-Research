"""
Age Stratification Methods for Sleep and Circadian Research
For age range 40-75 years

This module provides several methods to stratify participants by age
for use in sleep and circadian actigraphy and biological data analysis
"""

import numpy as np
import pandas as pd
from typing import Union, List, Optional


def stratify_age_equal_width(
    age: Union[np.ndarray, pd.Series, list],
    n_bins: int = 3,
    min_age: float = 40,
    max_age: float = 75
) -> pd.Series:
    """
    Stratify age into equal-width bins
    
    Parameters
    ----------
    age : array-like
        Numeric array of ages
    n_bins : int, default=3
        Number of bins to create
    min_age : float, default=40
        Minimum age in the range
    max_age : float, default=75
        Maximum age in the range
        
    Returns
    -------
    pd.Series
        Categorical series with age stratification labels
        
    Examples
    --------
    >>> ages = [42, 55, 68, 73, 45, 50, 61]
    >>> stratify_age_equal_width(ages, n_bins=3)
    """
    age_array = np.array(age)
    
    # Calculate bin width
    bin_width = (max_age - min_age) / n_bins
    
    # Create breaks
    breaks = [min_age + i * bin_width for i in range(n_bins + 1)]
    
    # Create labels
    labels = [f"{int(breaks[i])}-{int(breaks[i+1]-1)} years" 
              for i in range(len(breaks)-1)]
    
    # Cut the ages into bins
    age_strata = pd.cut(age_array, bins=breaks, labels=labels, 
                        include_lowest=True, right=False)
    
    return age_strata


def stratify_age_quartiles(age: Union[np.ndarray, pd.Series, list]) -> pd.Series:
    """
    Stratify age into quartiles
    
    Parameters
    ----------
    age : array-like
        Numeric array of ages
        
    Returns
    -------
    pd.Series
        Categorical series with quartile labels (Q1-Q4)
        
    Examples
    --------
    >>> ages = [42, 55, 68, 73, 45, 50, 61]
    >>> stratify_age_quartiles(ages)
    """
    age_array = np.array(age)
    
    # Calculate quartiles
    quartiles = np.percentile(age_array, [0, 25, 50, 75, 100])
    
    labels = [
        "Q1 (Youngest 25%)",
        "Q2 (25-50%)",
        "Q3 (50-75%)",
        "Q4 (Oldest 25%)"
    ]
    
    age_strata = pd.cut(age_array, bins=quartiles, labels=labels, 
                        include_lowest=True)
    
    return age_strata


def stratify_age_custom(
    age: Union[np.ndarray, pd.Series, list],
    breaks: Optional[List[float]] = None
) -> pd.Series:
    """
    Stratify age into custom age groups
    
    Parameters
    ----------
    age : array-like
        Numeric array of ages
    breaks : list of float, optional
        Custom break points for age groups
        Default is [40, 50, 60, 70, 75]
        
    Returns
    -------
    pd.Series
        Categorical series with custom age group labels
        
    Examples
    --------
    >>> ages = [42, 55, 68, 73, 45, 50, 61]
    >>> stratify_age_custom(ages, breaks=[40, 50, 60, 70, 75])
    """
    if breaks is None:
        breaks = [40, 50, 60, 70, 75]
    
    age_array = np.array(age)
    
    # Create labels from breaks
    labels = [f"{int(breaks[i])}-{int(breaks[i+1]-1)} years" 
              for i in range(len(breaks)-1)]
    
    age_strata = pd.cut(age_array, bins=breaks, labels=labels,
                        include_lowest=True, right=False)
    
    return age_strata


def stratify_age_median_split(age: Union[np.ndarray, pd.Series, list]) -> pd.Series:
    """
    Stratify age into median split
    
    Parameters
    ----------
    age : array-like
        Numeric array of ages
        
    Returns
    -------
    pd.Series
        Categorical series with younger/older labels
        
    Examples
    --------
    >>> ages = [42, 55, 68, 73, 45, 50, 61]
    >>> stratify_age_median_split(ages)
    """
    age_array = np.array(age)
    median_age = np.median(age_array)
    
    age_strata = np.where(
        age_array < median_age,
        f"Younger (<{median_age:.0f} years)",
        f"Older (≥{median_age:.0f} years)"
    )
    
    return pd.Categorical(age_strata)


def stratify_age_decades(age: Union[np.ndarray, pd.Series, list]) -> pd.Series:
    """
    Stratify age into decades
    
    Parameters
    ----------
    age : array-like
        Numeric array of ages
        
    Returns
    -------
    pd.Series
        Categorical series with decade labels
        
    Examples
    --------
    >>> ages = [42, 55, 68, 73, 45, 50, 61]
    >>> stratify_age_decades(ages)
    """
    age_array = np.array(age)
    
    # For 40-75 range, we have 40s, 50s, 60s, 70s
    breaks = [40, 50, 60, 70, 80]
    labels = ["40s (40-49)", "50s (50-59)", "60s (60-69)", "70s (70-79)"]
    
    age_strata = pd.cut(age_array, bins=breaks, labels=labels,
                        include_lowest=True, right=False)
    
    return age_strata


def demonstrate_stratification():
    """
    Demonstrate all stratification methods with sample data
    """
    # Create sample data representing participants aged 40-75
    np.random.seed(123)
    n_participants = 100
    sample_ages = np.random.uniform(low=40, high=75, size=n_participants)
    sample_ages = np.round(sample_ages)
    
    print("=== Age Stratification Demonstration ===\n")
    print(f"Sample size: {n_participants} participants")
    print(f"Age range: {int(sample_ages.min())}-{int(sample_ages.max())} years")
    print(f"Mean age: {sample_ages.mean():.1f} years (SD = {sample_ages.std():.1f})\n")
    
    # Method 1: Equal-width bins (tertiles)
    print("1. EQUAL-WIDTH BINS (3 groups)")
    strata1 = stratify_age_equal_width(sample_ages, n_bins=3)
    print(strata1.value_counts().sort_index())
    print()
    
    # Method 2: Quartiles
    print("2. QUARTILES (data-driven)")
    strata2 = stratify_age_quartiles(sample_ages)
    print(strata2.value_counts().sort_index())
    print()
    
    # Method 3: Custom age groups
    print("3. CUSTOM AGE GROUPS")
    strata3 = stratify_age_custom(sample_ages, breaks=[40, 50, 60, 70, 75])
    print(strata3.value_counts().sort_index())
    print()
    
    # Method 4: Median split
    print("4. MEDIAN SPLIT")
    strata4 = stratify_age_median_split(sample_ages)
    print(pd.Series(strata4).value_counts().sort_index())
    print()
    
    # Method 5: Decades
    print("5. DECADES")
    strata5 = stratify_age_decades(sample_ages)
    print(strata5.value_counts().sort_index())
    print()
    
    # Return a data frame with all stratifications
    results = pd.DataFrame({
        'age': sample_ages,
        'equal_width': strata1,
        'quartiles': strata2,
        'custom': strata3,
        'median_split': strata4,
        'decades': strata5
    })
    
    return results


if __name__ == "__main__":
    # Run demonstration when script is executed
    demonstrate_stratification()
