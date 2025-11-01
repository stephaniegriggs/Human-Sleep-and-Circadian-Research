"""
Multiple Component Cosinor Analysis for Circadian Rhythm Research

This module provides tools for analyzing circadian rhythms in actigraphy and 
melatonin data using single and multiple component cosinor regression.

Cosinor analysis is a statistical method for fitting cosine curves to time series
data to characterize circadian rhythms. It estimates the MESOR (Midline Estimating 
Statistic Of Rhythm), amplitude, and acrophase (peak time) of periodic patterns.

Multiple component cosinor extends this to fit multiple harmonics, useful for
modeling complex rhythms with multiple periodicities.
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional


class CosinorAnalysis:
    """
    Implements single and multiple component cosinor analysis for circadian research.
    
    Methods follow standard cosinor methodology as described in:
    - Cornelissen, G. (2014). Cosinor-based rhythmometry. Theoretical Biology 
      and Medical Modelling, 11, 16.
    - Refinetti, R., et al. (2007). Procedures for numerical analysis of 
      circadian rhythms. Biological Rhythm Research, 38(4), 275-325.
    """
    
    def __init__(self, time: np.ndarray, data: np.ndarray, period: float = 24.0):
        """
        Initialize cosinor analysis.
        
        Parameters:
        -----------
        time : np.ndarray
            Time points (in hours)
        data : np.ndarray
            Measured values (e.g., activity counts, melatonin levels)
        period : float
            Expected period of the rhythm in hours (default: 24.0 for circadian)
        """
        self.time = np.asarray(time)
        self.data = np.asarray(data)
        self.period = period
        self.results = {}
        
        if len(self.time) != len(self.data):
            raise ValueError("Time and data arrays must have the same length")
        
        if len(self.time) < 3:
            raise ValueError("Need at least 3 data points for cosinor analysis")
    
    def single_component_cosinor(self) -> Dict:
        """
        Perform single component cosinor analysis.
        
        Fits the model: y(t) = M + A*cos(2π*t/τ + φ)
        where:
        - M is the MESOR (Midline Estimating Statistic Of Rhythm)
        - A is the amplitude
        - τ is the period
        - φ is the acrophase (phase angle)
        
        Returns:
        --------
        dict : Contains MESOR, amplitude, acrophase, R-squared, p-value, and statistics
        """
        # Convert to radians
        omega = 2 * np.pi / self.period
        
        # Create design matrix for linear regression
        # y = M + β*cos(ωt) + γ*sin(ωt)
        X = np.column_stack([
            np.ones_like(self.time),
            np.cos(omega * self.time),
            np.sin(omega * self.time)
        ])
        
        # Least squares regression
        beta, residuals, rank, s = np.linalg.lstsq(X, self.data, rcond=None)
        
        M = beta[0]  # MESOR
        beta_cos = beta[1]
        gamma_sin = beta[2]
        
        # Calculate amplitude and acrophase
        amplitude = np.sqrt(beta_cos**2 + gamma_sin**2)
        acrophase = np.arctan2(-gamma_sin, beta_cos)  # in radians
        acrophase_hours = (acrophase * self.period / (2 * np.pi)) % self.period
        
        # Calculate statistics
        y_pred = X @ beta
        ss_res = np.sum((self.data - y_pred)**2)
        ss_tot = np.sum((self.data - np.mean(self.data))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # F-test for significance of rhythm
        n = len(self.data)
        df_model = 2  # β and γ
        df_residual = n - 3
        
        if df_residual > 0 and ss_res > 0:
            ms_model = (ss_tot - ss_res) / df_model
            ms_residual = ss_res / df_residual
            f_statistic = ms_model / ms_residual
            p_value = 1 - stats.f.cdf(f_statistic, df_model, df_residual)
        else:
            f_statistic = np.nan
            p_value = np.nan
        
        # Standard errors
        if df_residual > 0:
            mse = ss_res / df_residual
            var_covar = mse * np.linalg.pinv(X.T @ X)
            se_M = np.sqrt(var_covar[0, 0])
            
            # Standard error of amplitude using delta method
            if amplitude > 0:
                se_amplitude = np.sqrt(
                    (beta_cos**2 * var_covar[1, 1] + 
                     gamma_sin**2 * var_covar[2, 2] + 
                     2 * beta_cos * gamma_sin * var_covar[1, 2]) / amplitude**2
                )
            else:
                se_amplitude = np.nan
        else:
            se_M = np.nan
            se_amplitude = np.nan
        
        self.results['single'] = {
            'MESOR': M,
            'amplitude': amplitude,
            'acrophase': acrophase,
            'acrophase_hours': acrophase_hours,
            'period': self.period,
            'R_squared': r_squared,
            'p_value': p_value,
            'F_statistic': f_statistic,
            'SE_MESOR': se_M,
            'SE_amplitude': se_amplitude,
            'n_observations': n,
            'fitted_values': y_pred,
            'residuals': self.data - y_pred
        }
        
        return self.results['single']
    
    def multiple_component_cosinor(self, n_components: int = 2) -> Dict:
        """
        Perform multiple component cosinor analysis.
        
        Fits the model: y(t) = M + Σ[A_k*cos(2π*k*t/τ + φ_k)] for k=1 to n_components
        
        This allows modeling of complex rhythms with multiple harmonics, such as:
        - Ultradian rhythms (periods shorter than 24h)
        - Higher-order harmonics of circadian rhythms
        
        Parameters:
        -----------
        n_components : int
            Number of harmonic components to fit (default: 2)
        
        Returns:
        --------
        dict : Contains MESOR, amplitudes, acrophases for each component, 
               and overall statistics
        """
        if n_components < 1:
            raise ValueError("Number of components must be at least 1")
        
        omega = 2 * np.pi / self.period
        
        # Create design matrix with multiple harmonics
        # y = M + Σ[β_k*cos(k*ωt) + γ_k*sin(k*ωt)]
        X_list = [np.ones_like(self.time)]
        
        for k in range(1, n_components + 1):
            X_list.append(np.cos(k * omega * self.time))
            X_list.append(np.sin(k * omega * self.time))
        
        X = np.column_stack(X_list)
        
        # Least squares regression
        beta, residuals, rank, s = np.linalg.lstsq(X, self.data, rcond=None)
        
        M = beta[0]  # MESOR
        
        # Extract amplitudes and acrophases for each component
        components = []
        for k in range(1, n_components + 1):
            idx_cos = 2 * k - 1
            idx_sin = 2 * k
            
            beta_cos = beta[idx_cos]
            gamma_sin = beta[idx_sin]
            
            amplitude = np.sqrt(beta_cos**2 + gamma_sin**2)
            acrophase = np.arctan2(-gamma_sin, beta_cos)
            acrophase_hours = (acrophase * self.period / (2 * np.pi * k)) % (self.period / k)
            
            components.append({
                'component': k,
                'period': self.period / k,
                'amplitude': amplitude,
                'acrophase': acrophase,
                'acrophase_hours': acrophase_hours
            })
        
        # Calculate statistics
        y_pred = X @ beta
        ss_res = np.sum((self.data - y_pred)**2)
        ss_tot = np.sum((self.data - np.mean(self.data))**2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # F-test for significance
        n = len(self.data)
        df_model = 2 * n_components  # pairs of β and γ for each component
        df_residual = n - (2 * n_components + 1)
        
        if df_residual > 0 and ss_res > 0:
            ms_model = (ss_tot - ss_res) / df_model
            ms_residual = ss_res / df_residual
            f_statistic = ms_model / ms_residual
            p_value = 1 - stats.f.cdf(f_statistic, df_model, df_residual)
        else:
            f_statistic = np.nan
            p_value = np.nan
        
        self.results['multiple'] = {
            'MESOR': M,
            'n_components': n_components,
            'components': components,
            'R_squared': r_squared,
            'p_value': p_value,
            'F_statistic': f_statistic,
            'n_observations': n,
            'fitted_values': y_pred,
            'residuals': self.data - y_pred
        }
        
        return self.results['multiple']
    
    def compare_models(self, max_components: int = 3) -> Dict:
        """
        Compare multiple cosinor models with different numbers of components.
        
        Uses F-test and information criteria (AIC, BIC) to determine the optimal
        number of components.
        
        Parameters:
        -----------
        max_components : int
            Maximum number of components to test (default: 3)
        
        Returns:
        --------
        dict : Comparison statistics and recommended model
        """
        comparisons = []
        n = len(self.data)
        
        for k in range(1, max_components + 1):
            result = self.multiple_component_cosinor(n_components=k)
            
            ss_res = np.sum(result['residuals']**2)
            n_params = 2 * k + 1  # MESOR + 2 params per component
            
            # Calculate AIC and BIC
            if ss_res > 0:
                log_likelihood = -n/2 * np.log(2*np.pi*ss_res/n) - n/2
                aic = 2 * n_params - 2 * log_likelihood
                bic = n_params * np.log(n) - 2 * log_likelihood
            else:
                aic = np.inf
                bic = np.inf
            
            comparisons.append({
                'n_components': k,
                'R_squared': result['R_squared'],
                'p_value': result['p_value'],
                'AIC': aic,
                'BIC': bic,
                'n_parameters': n_params
            })
        
        # Find best model by BIC (lower is better)
        best_idx = np.argmin([c['BIC'] for c in comparisons])
        
        return {
            'comparisons': comparisons,
            'best_model': comparisons[best_idx],
            'recommended_components': comparisons[best_idx]['n_components']
        }
    
    def print_summary(self, model_type: str = 'single'):
        """
        Print a summary of the cosinor analysis results.
        
        Parameters:
        -----------
        model_type : str
            'single' or 'multiple' to specify which results to print
        """
        if model_type not in self.results:
            print(f"No {model_type} component analysis has been performed yet.")
            return
        
        result = self.results[model_type]
        
        print(f"\n{'='*60}")
        print(f"{'COSINOR ANALYSIS SUMMARY':^60}")
        print(f"{'='*60}\n")
        
        if model_type == 'single':
            print(f"Single Component Cosinor Analysis")
            print(f"Period: {self.period:.2f} hours")
            print(f"\nParameters:")
            print(f"  MESOR:              {result['MESOR']:.4f} ± {result['SE_MESOR']:.4f}")
            print(f"  Amplitude:          {result['amplitude']:.4f} ± {result['SE_amplitude']:.4f}")
            print(f"  Acrophase:          {result['acrophase_hours']:.2f} hours")
            print(f"                      ({result['acrophase']:.4f} radians)")
            
        elif model_type == 'multiple':
            print(f"Multiple Component Cosinor Analysis")
            print(f"Number of components: {result['n_components']}")
            print(f"Base period: {self.period:.2f} hours")
            print(f"\nParameters:")
            print(f"  MESOR:              {result['MESOR']:.4f}")
            print(f"\nComponents:")
            for comp in result['components']:
                print(f"  Component {comp['component']}:")
                print(f"    Period:           {comp['period']:.2f} hours")
                print(f"    Amplitude:        {comp['amplitude']:.4f}")
                print(f"    Acrophase:        {comp['acrophase_hours']:.2f} hours")
        
        print(f"\nModel Statistics:")
        print(f"  R-squared:          {result['R_squared']:.4f}")
        print(f"  F-statistic:        {result['F_statistic']:.4f}")
        print(f"  p-value:            {result['p_value']:.4e}")
        print(f"  N observations:     {result['n_observations']}")
        
        if result['p_value'] < 0.05:
            print(f"\n  *** Significant rhythm detected (p < 0.05) ***")
        else:
            print(f"\n  No significant rhythm detected (p >= 0.05)")
        
        print(f"\n{'='*60}\n")


def analyze_actigraphy_data(time: np.ndarray, activity: np.ndarray, 
                            period: float = 24.0, 
                            n_components: int = 1) -> Dict:
    """
    Analyze actigraphy data using cosinor analysis.
    
    Actigraphy measures physical activity levels over time, typically showing
    strong circadian rhythms with peak activity during the day and low activity
    at night.
    
    Parameters:
    -----------
    time : np.ndarray
        Time points in hours (e.g., 0-24 for one day, 0-168 for one week)
    activity : np.ndarray
        Activity counts at each time point
    period : float
        Expected period in hours (default: 24.0 for circadian rhythm)
    n_components : int
        Number of components for cosinor analysis (default: 1)
    
    Returns:
    --------
    dict : Cosinor analysis results
    """
    cosinor = CosinorAnalysis(time, activity, period)
    
    if n_components == 1:
        results = cosinor.single_component_cosinor()
    else:
        results = cosinor.multiple_component_cosinor(n_components)
    
    cosinor.print_summary('single' if n_components == 1 else 'multiple')
    
    return results


def analyze_melatonin_data(time: np.ndarray, melatonin: np.ndarray, 
                           period: float = 24.0,
                           n_components: int = 1) -> Dict:
    """
    Analyze melatonin data using cosinor analysis.
    
    Melatonin is a hormone that shows strong circadian rhythms, with levels
    rising in the evening, peaking at night, and declining in the morning.
    Dim Light Melatonin Onset (DLMO) is a key circadian phase marker.
    
    Parameters:
    -----------
    time : np.ndarray
        Time points in hours
    melatonin : np.ndarray
        Melatonin concentrations (e.g., pg/mL or pmol/L)
    period : float
        Expected period in hours (default: 24.0 for circadian rhythm)
    n_components : int
        Number of components for cosinor analysis (default: 1)
    
    Returns:
    --------
    dict : Cosinor analysis results including estimated peak melatonin time
    """
    cosinor = CosinorAnalysis(time, melatonin, period)
    
    if n_components == 1:
        results = cosinor.single_component_cosinor()
    else:
        results = cosinor.multiple_component_cosinor(n_components)
    
    cosinor.print_summary('single' if n_components == 1 else 'multiple')
    
    # Add interpretation for melatonin
    if n_components == 1:
        acrophase_hours = results['acrophase_hours']
        print(f"Estimated peak melatonin time: {acrophase_hours:.2f} hours")
        print(f"(Note: DLMO typically occurs ~2-3 hours before peak)")
    
    return results


def joint_analysis(time: np.ndarray, 
                  actigraphy: np.ndarray, 
                  melatonin: np.ndarray,
                  period: float = 24.0) -> Dict:
    """
    Perform joint analysis of actigraphy and melatonin data.
    
    Compares circadian phase markers from both data types to assess:
    - Phase relationship between activity and melatonin rhythms
    - Circadian alignment or misalignment
    
    Parameters:
    -----------
    time : np.ndarray
        Time points in hours (must be same for both datasets)
    actigraphy : np.ndarray
        Activity counts
    melatonin : np.ndarray
        Melatonin concentrations
    period : float
        Expected period in hours (default: 24.0)
    
    Returns:
    --------
    dict : Joint analysis results including phase relationships
    """
    print("\n" + "="*60)
    print("JOINT ACTIGRAPHY AND MELATONIN ANALYSIS")
    print("="*60 + "\n")
    
    # Analyze actigraphy
    print("Actigraphy Analysis:")
    print("-" * 40)
    act_results = analyze_actigraphy_data(time, actigraphy, period)
    
    # Analyze melatonin
    print("\nMelatonin Analysis:")
    print("-" * 40)
    mel_results = analyze_melatonin_data(time, melatonin, period)
    
    # Calculate phase relationship
    act_acrophase = act_results['acrophase_hours']
    mel_acrophase = mel_results['acrophase_hours']
    
    phase_difference = act_acrophase - mel_acrophase
    # Adjust for circular nature of time
    if phase_difference > period / 2:
        phase_difference -= period
    elif phase_difference < -period / 2:
        phase_difference += period
    
    print("\n" + "="*60)
    print("PHASE RELATIONSHIP")
    print("="*60)
    print(f"\nActivity peak time:     {act_acrophase:.2f} hours")
    print(f"Melatonin peak time:    {mel_acrophase:.2f} hours")
    print(f"Phase difference:       {phase_difference:.2f} hours")
    print(f"\nInterpretation:")
    if abs(phase_difference) < 2:
        print("  Normal phase relationship")
    elif phase_difference < -2:
        print("  Activity peak precedes melatonin peak (possible phase advance)")
    else:
        print("  Melatonin peak precedes activity peak (possible phase delay)")
    print("="*60 + "\n")
    
    return {
        'actigraphy_results': act_results,
        'melatonin_results': mel_results,
        'phase_difference_hours': phase_difference,
        'actigraphy_acrophase': act_acrophase,
        'melatonin_acrophase': mel_acrophase
    }
