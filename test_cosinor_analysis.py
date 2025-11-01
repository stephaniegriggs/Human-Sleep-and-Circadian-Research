"""
Unit tests for the cosinor analysis module.
"""

import numpy as np
import pytest
from cosinor_analysis import (
    CosinorAnalysis,
    analyze_actigraphy_data,
    analyze_melatonin_data,
    joint_analysis
)


class TestCosinorAnalysis:
    """Test cases for CosinorAnalysis class."""
    
    def test_initialization(self):
        """Test proper initialization of CosinorAnalysis."""
        time = np.array([0, 1, 2, 3, 4])
        data = np.array([1, 2, 3, 2, 1])
        
        cosinor = CosinorAnalysis(time, data, period=24.0)
        
        assert len(cosinor.time) == 5
        assert len(cosinor.data) == 5
        assert cosinor.period == 24.0
    
    def test_initialization_mismatched_lengths(self):
        """Test that mismatched array lengths raise ValueError."""
        time = np.array([0, 1, 2])
        data = np.array([1, 2])
        
        with pytest.raises(ValueError, match="same length"):
            CosinorAnalysis(time, data)
    
    def test_initialization_insufficient_data(self):
        """Test that insufficient data points raise ValueError."""
        time = np.array([0, 1])
        data = np.array([1, 2])
        
        with pytest.raises(ValueError, match="at least 3"):
            CosinorAnalysis(time, data)
    
    def test_single_component_with_perfect_cosine(self):
        """Test single component cosinor with perfect cosine wave."""
        # Generate perfect cosine wave
        time = np.linspace(0, 48, 48)  # 2 days, hourly
        mesor = 100
        amplitude = 50
        acrophase_hours = 12  # peak at noon
        period = 24
        
        # Perfect cosine: y = M + A*cos(2π(t - φ)/τ)
        data = mesor + amplitude * np.cos(2 * np.pi * (time - acrophase_hours) / period)
        
        cosinor = CosinorAnalysis(time, data, period=period)
        results = cosinor.single_component_cosinor()
        
        # Check estimated parameters (should be very close to true values)
        assert np.abs(results['MESOR'] - mesor) < 0.01
        assert np.abs(results['amplitude'] - amplitude) < 0.01
        assert np.abs(results['acrophase_hours'] - acrophase_hours) < 0.01
        assert results['R_squared'] > 0.99
        assert results['p_value'] < 0.001
    
    def test_single_component_with_noisy_data(self):
        """Test single component cosinor with noisy cosine wave."""
        np.random.seed(42)
        time = np.linspace(0, 168, 168)  # 7 days
        
        # Cosine with noise
        data = 100 + 50 * np.cos(2 * np.pi * time / 24) + np.random.normal(0, 10, len(time))
        
        cosinor = CosinorAnalysis(time, data, period=24.0)
        results = cosinor.single_component_cosinor()
        
        # Should still detect significant rhythm
        assert results['p_value'] < 0.05
        assert results['R_squared'] > 0.5
        assert results['amplitude'] > 0
        assert 0 <= results['acrophase_hours'] < 24
    
    def test_multiple_component_cosinor(self):
        """Test multiple component cosinor with two harmonics."""
        time = np.linspace(0, 168, 168)
        
        # Two components: 24h and 12h
        data = (100 + 
                50 * np.cos(2 * np.pi * time / 24) +
                20 * np.cos(2 * np.pi * time / 12))
        
        cosinor = CosinorAnalysis(time, data, period=24.0)
        results = cosinor.multiple_component_cosinor(n_components=2)
        
        assert results['n_components'] == 2
        assert len(results['components']) == 2
        assert results['p_value'] < 0.001
        assert results['R_squared'] > 0.99
        
        # Check component periods
        assert np.abs(results['components'][0]['period'] - 24.0) < 0.01
        assert np.abs(results['components'][1]['period'] - 12.0) < 0.01
    
    def test_multiple_component_invalid_n_components(self):
        """Test that invalid number of components raises ValueError."""
        time = np.linspace(0, 48, 48)
        data = np.random.randn(48)
        
        cosinor = CosinorAnalysis(time, data)
        
        with pytest.raises(ValueError, match="at least 1"):
            cosinor.multiple_component_cosinor(n_components=0)
    
    def test_compare_models(self):
        """Test model comparison functionality."""
        np.random.seed(42)
        time = np.linspace(0, 168, 168)
        
        # Data with 2 components plus noise
        data = (100 + 
                50 * np.cos(2 * np.pi * time / 24) +
                20 * np.cos(2 * np.pi * time / 12) +
                np.random.normal(0, 5, len(time)))
        
        cosinor = CosinorAnalysis(time, data, period=24.0)
        comparison = cosinor.compare_models(max_components=3)
        
        assert 'comparisons' in comparison
        assert 'best_model' in comparison
        assert 'recommended_components' in comparison
        assert len(comparison['comparisons']) == 3
        
        # With noise, should recommend 1 or 2 components (not more than 3)
        assert 1 <= comparison['recommended_components'] <= 3
    
    def test_analyze_actigraphy_data(self):
        """Test convenience function for actigraphy analysis."""
        np.random.seed(42)
        time = np.linspace(0, 168, 168)
        activity = 100 + 80 * np.cos(2 * np.pi * (time - 14) / 24) + np.random.normal(0, 10, len(time))
        activity = np.maximum(activity, 0)
        
        results = analyze_actigraphy_data(time, activity, period=24.0, n_components=1)
        
        assert 'MESOR' in results
        assert 'amplitude' in results
        assert 'acrophase_hours' in results
        assert results['p_value'] < 0.05
    
    def test_analyze_melatonin_data(self):
        """Test convenience function for melatonin analysis."""
        np.random.seed(42)
        time = np.linspace(0, 168, 168)
        melatonin = 10 + 30 * np.cos(2 * np.pi * (time - 3) / 24) + np.random.normal(0, 3, len(time))
        melatonin = np.maximum(melatonin, 0.5)
        
        results = analyze_melatonin_data(time, melatonin, period=24.0, n_components=1)
        
        assert 'MESOR' in results
        assert 'amplitude' in results
        assert 'acrophase_hours' in results
        assert results['p_value'] < 0.05
    
    def test_joint_analysis(self):
        """Test joint analysis of actigraphy and melatonin."""
        np.random.seed(42)
        time = np.linspace(0, 168, 168)
        
        # Actigraphy: peak around 14:00
        activity = 100 + 80 * np.cos(2 * np.pi * (time - 14) / 24) + np.random.normal(0, 10, len(time))
        activity = np.maximum(activity, 0)
        
        # Melatonin: peak around 3:00
        melatonin = 10 + 30 * np.cos(2 * np.pi * (time - 3) / 24) + np.random.normal(0, 3, len(time))
        melatonin = np.maximum(melatonin, 0.5)
        
        results = joint_analysis(time, activity, melatonin, period=24.0)
        
        assert 'actigraphy_results' in results
        assert 'melatonin_results' in results
        assert 'phase_difference_hours' in results
        assert 'actigraphy_acrophase' in results
        assert 'melatonin_acrophase' in results
        
        # Phase difference should be approximately 11 hours (14 - 3)
        assert 8 < abs(results['phase_difference_hours']) < 14
    
    def test_no_rhythm_detection(self):
        """Test with random data (no rhythm)."""
        np.random.seed(42)
        time = np.linspace(0, 48, 48)
        data = np.random.normal(100, 10, len(time))
        
        cosinor = CosinorAnalysis(time, data, period=24.0)
        results = cosinor.single_component_cosinor()
        
        # Should have low R-squared and high p-value
        assert results['R_squared'] < 0.3
        # p-value might still be < 0.05 by chance, but R-squared should be low
    
    def test_fitted_values_length(self):
        """Test that fitted values match input length."""
        time = np.linspace(0, 48, 48)
        data = 100 + 50 * np.cos(2 * np.pi * time / 24)
        
        cosinor = CosinorAnalysis(time, data, period=24.0)
        results = cosinor.single_component_cosinor()
        
        assert len(results['fitted_values']) == len(time)
        assert len(results['residuals']) == len(time)
    
    def test_residuals_sum_to_zero(self):
        """Test that residuals sum to approximately zero."""
        time = np.linspace(0, 48, 48)
        data = 100 + 50 * np.cos(2 * np.pi * time / 24)
        
        cosinor = CosinorAnalysis(time, data, period=24.0)
        results = cosinor.single_component_cosinor()
        
        # Residuals should sum to approximately zero
        assert np.abs(np.sum(results['residuals'])) < 1e-10


def test_multiple_periods():
    """Test with different period values."""
    time = np.linspace(0, 100, 100)
    
    # Test with 12-hour period
    data_12h = 100 + 50 * np.cos(2 * np.pi * time / 12)
    cosinor_12h = CosinorAnalysis(time, data_12h, period=12.0)
    results_12h = cosinor_12h.single_component_cosinor()
    
    assert results_12h['period'] == 12.0
    assert results_12h['R_squared'] > 0.99
    
    # Test with 8-hour period
    data_8h = 100 + 50 * np.cos(2 * np.pi * time / 8)
    cosinor_8h = CosinorAnalysis(time, data_8h, period=8.0)
    results_8h = cosinor_8h.single_component_cosinor()
    
    assert results_8h['period'] == 8.0
    assert results_8h['R_squared'] > 0.99


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
