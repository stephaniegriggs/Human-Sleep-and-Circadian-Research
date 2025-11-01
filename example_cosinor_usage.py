"""
Example usage of the cosinor analysis module for actigraphy and melatonin data.

This script demonstrates:
1. Single component cosinor analysis
2. Multiple component cosinor analysis
3. Joint analysis of actigraphy and melatonin data
4. Model comparison
"""

import numpy as np
import matplotlib.pyplot as plt
from cosinor_analysis import (
    CosinorAnalysis, 
    analyze_actigraphy_data, 
    analyze_melatonin_data,
    joint_analysis
)


def generate_synthetic_actigraphy_data(n_days: int = 7, noise_level: float = 0.2):
    """
    Generate synthetic actigraphy data with a circadian rhythm.
    
    Parameters:
    -----------
    n_days : int
        Number of days to simulate
    noise_level : float
        Amount of random noise to add (0-1)
    
    Returns:
    --------
    tuple : (time, activity) arrays
    """
    # Create time array (hourly samples over n_days)
    time = np.linspace(0, 24 * n_days, 24 * n_days)
    
    # Generate circadian activity pattern
    # Peak activity around 14:00 (2 PM), low activity at night
    mesor = 100  # baseline activity
    amplitude = 80  # amplitude of variation
    acrophase = 14  # peak at 2 PM
    
    # Activity pattern: high during day, low at night
    activity = mesor + amplitude * np.cos(2 * np.pi * (time - acrophase) / 24)
    
    # Add some noise
    activity += np.random.normal(0, noise_level * amplitude, len(time))
    
    # Activity can't be negative
    activity = np.maximum(activity, 0)
    
    return time, activity


def generate_synthetic_melatonin_data(n_days: int = 7, noise_level: float = 0.15):
    """
    Generate synthetic melatonin data with a circadian rhythm.
    
    Parameters:
    -----------
    n_days : int
        Number of days to simulate
    noise_level : float
        Amount of random noise to add (0-1)
    
    Returns:
    --------
    tuple : (time, melatonin) arrays
    """
    # Create time array (hourly samples over n_days)
    time = np.linspace(0, 24 * n_days, 24 * n_days)
    
    # Generate circadian melatonin pattern
    # Peak around 3:00 AM, low during day
    mesor = 10  # baseline melatonin (pg/mL)
    amplitude = 30  # amplitude of variation
    acrophase = 3  # peak at 3 AM
    
    # Melatonin pattern: high at night, low during day
    melatonin = mesor + amplitude * np.cos(2 * np.pi * (time - acrophase) / 24)
    
    # Add some noise
    melatonin += np.random.normal(0, noise_level * amplitude, len(time))
    
    # Melatonin can't be negative
    melatonin = np.maximum(melatonin, 0.5)
    
    return time, melatonin


def example_single_component_analysis():
    """Demonstrate single component cosinor analysis."""
    print("\n" + "="*70)
    print(" EXAMPLE 1: Single Component Cosinor Analysis")
    print("="*70)
    
    # Generate synthetic data
    time, activity = generate_synthetic_actigraphy_data(n_days=7)
    
    # Perform single component analysis
    print("\nAnalyzing 7 days of actigraphy data...")
    results = analyze_actigraphy_data(time, activity, period=24.0, n_components=1)
    
    return time, activity, results


def example_multiple_component_analysis():
    """Demonstrate multiple component cosinor analysis."""
    print("\n" + "="*70)
    print(" EXAMPLE 2: Multiple Component Cosinor Analysis")
    print("="*70)
    
    # Generate synthetic data with ultradian component
    time = np.linspace(0, 168, 168)  # 7 days, hourly
    
    # Create data with both 24h and 12h components
    mesor = 100
    amp_24h = 50  # circadian component
    amp_12h = 20  # ultradian component (12-hour rhythm)
    
    data = (mesor + 
            amp_24h * np.cos(2 * np.pi * time / 24) +
            amp_12h * np.cos(2 * np.pi * time / 12) +
            np.random.normal(0, 10, len(time)))
    
    # Analyze with multiple components
    print("\nAnalyzing data with circadian and ultradian components...")
    cosinor = CosinorAnalysis(time, data, period=24.0)
    results = cosinor.multiple_component_cosinor(n_components=2)
    cosinor.print_summary('multiple')
    
    return time, data, results


def example_model_comparison():
    """Demonstrate model comparison with different numbers of components."""
    print("\n" + "="*70)
    print(" EXAMPLE 3: Model Comparison")
    print("="*70)
    
    # Generate data with 2 components
    time = np.linspace(0, 168, 168)
    data = (100 + 
            50 * np.cos(2 * np.pi * time / 24) +
            20 * np.cos(2 * np.pi * time / 12) +
            np.random.normal(0, 10, len(time)))
    
    # Compare models
    print("\nComparing models with 1, 2, and 3 components...")
    cosinor = CosinorAnalysis(time, data, period=24.0)
    comparison = cosinor.compare_models(max_components=3)
    
    print("\n" + "="*60)
    print("MODEL COMPARISON RESULTS")
    print("="*60)
    print(f"{'Components':<12} {'R²':<10} {'AIC':<12} {'BIC':<12} {'p-value':<12}")
    print("-" * 60)
    
    for comp in comparison['comparisons']:
        print(f"{comp['n_components']:<12} "
              f"{comp['R_squared']:<10.4f} "
              f"{comp['AIC']:<12.2f} "
              f"{comp['BIC']:<12.2f} "
              f"{comp['p_value']:<12.4e}")
    
    print("\n" + "="*60)
    print(f"Recommended model: {comparison['recommended_components']} components "
          f"(lowest BIC)")
    print("="*60)
    
    return comparison


def example_joint_analysis():
    """Demonstrate joint analysis of actigraphy and melatonin data."""
    print("\n" + "="*70)
    print(" EXAMPLE 4: Joint Actigraphy and Melatonin Analysis")
    print("="*70)
    
    # Generate synthetic data
    time_act, activity = generate_synthetic_actigraphy_data(n_days=7)
    time_mel, melatonin = generate_synthetic_melatonin_data(n_days=7)
    
    # Perform joint analysis
    print("\nPerforming joint analysis...")
    results = joint_analysis(time_act, activity, melatonin, period=24.0)
    
    return time_act, activity, melatonin, results


def plot_results(time, data, fitted_values, title, ylabel):
    """Helper function to plot data and fitted cosinor curve."""
    try:
        plt.figure(figsize=(12, 6))
        
        # Plot first 72 hours for clarity
        mask = time <= 72
        plt.plot(time[mask], data[mask], 'o', alpha=0.5, label='Observed data')
        plt.plot(time[mask], fitted_values[mask], 'r-', linewidth=2, 
                label='Fitted cosinor curve')
        
        plt.xlabel('Time (hours)', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f"/tmp/{title.replace(' ', '_').lower()}.png"
        plt.savefig(filename, dpi=150)
        print(f"\nPlot saved to: {filename}")
        plt.close()
        
    except Exception as e:
        print(f"Note: Could not generate plot - {e}")


def main():
    """Run all examples."""
    print("\n")
    print("="*70)
    print(" COSINOR ANALYSIS EXAMPLES")
    print(" Multiple Component Analysis for Actigraphy and Melatonin Data")
    print("="*70)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Example 1: Single component
    time1, activity1, results1 = example_single_component_analysis()
    if 'fitted_values' in results1:
        plot_results(time1, activity1, results1['fitted_values'],
                    'Single Component Cosinor - Actigraphy',
                    'Activity (counts)')
    
    # Example 2: Multiple components
    time2, data2, results2 = example_multiple_component_analysis()
    if 'fitted_values' in results2:
        plot_results(time2, data2, results2['fitted_values'],
                    'Multiple Component Cosinor - Two Harmonics',
                    'Activity (counts)')
    
    # Example 3: Model comparison
    comparison = example_model_comparison()
    
    # Example 4: Joint analysis
    time4, activity4, melatonin4, results4 = example_joint_analysis()
    
    print("\n" + "="*70)
    print(" ALL EXAMPLES COMPLETED")
    print("="*70)
    print("\nThese examples demonstrate:")
    print("  1. Single component cosinor for simple circadian rhythms")
    print("  2. Multiple component cosinor for complex rhythms")
    print("  3. Model comparison to select optimal number of components")
    print("  4. Joint analysis of actigraphy and melatonin data")
    print("\nFor real data analysis, replace the synthetic data generation")
    print("with your actual actigraphy and melatonin measurements.")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
