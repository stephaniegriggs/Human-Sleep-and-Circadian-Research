"""
Example: Age Stratification in Sleep Research
This script demonstrates how to apply age stratification to sleep and circadian data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from age_stratification import (
    stratify_age_quartiles,
    stratify_age_decades,
    stratify_age_custom
)

# Set style for plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ============================================================================
# STEP 1: Create example sleep and circadian data
# ============================================================================

np.random.seed(42)
n = 100

# Create synthetic dataset representing sleep and circadian measures
ages = np.random.uniform(40, 75, n)

sleep_data = pd.DataFrame({
    'participant_id': range(1, n+1),
    'age': np.round(ages),
    
    # Sleep measures (with age-related trends)
    'sleep_efficiency': np.clip(88 - 0.15 * (ages - 40) + np.random.normal(0, 8, n), 50, 100),
    'total_sleep_time': np.clip(420 - 0.8 * (ages - 40) + np.random.normal(0, 45, n), 300, 600),
    'waso': np.clip(25 + 0.5 * (ages - 40) + np.abs(np.random.normal(0, 15, n)), 0, 120),
    
    # Circadian measures
    'circadian_phase': 2.5 + 0.02 * (ages - 40) + np.random.normal(0, 1.2, n),
    'amplitude': np.clip(0.8 - 0.006 * (ages - 40) + np.abs(np.random.normal(0, 0.15, n)), 0.1, 2),
    
    # Biological measures
    'fasting_glucose': np.clip(92 + 0.3 * (ages - 40) + np.random.normal(0, 10, n), 70, 150),
    'cortisol_awakening': np.clip(18 - 0.08 * (ages - 40) + np.random.normal(0, 4, n), 5, 35)
})

# ============================================================================
# STEP 2: Apply different age stratification methods
# ============================================================================

print("Age Stratification Analysis for Sleep Research")
print("=" * 60)
print()

# Method 1: Quartiles (recommended for balanced analysis)
sleep_data['age_quartile'] = stratify_age_quartiles(sleep_data['age'])

# Method 2: Decades (recommended for communication)
sleep_data['age_decade'] = stratify_age_decades(sleep_data['age'])

# Method 3: Custom groups (example for metabolic research)
sleep_data['age_custom'] = stratify_age_custom(sleep_data['age'], 
                                                breaks=[40, 50, 60, 70, 75])

# ============================================================================
# STEP 3: Analyze sleep efficiency by age group (using quartiles)
# ============================================================================

print("Sleep Efficiency by Age Quartile")
print("-" * 60)

sleep_summary = sleep_data.groupby('age_quartile').agg({
    'age': ['count', 'mean', 'std'],
    'sleep_efficiency': ['mean', 'std'],
    'total_sleep_time': 'mean',
    'waso': 'mean'
}).round(1)

print(sleep_summary)
print()

# Statistical test
groups = [group['sleep_efficiency'].values 
          for name, group in sleep_data.groupby('age_quartile')]
h_stat, p_value = stats.kruskal(*groups)
print(f"Kruskal-Wallis test: H = {h_stat:.2f}, p = {p_value:.4f}")
print()

# ============================================================================
# STEP 4: Analyze circadian phase by age decade
# ============================================================================

print("Circadian Phase by Age Decade")
print("-" * 60)

circadian_summary = sleep_data.groupby('age_decade').agg({
    'age': ['count', 'mean'],
    'circadian_phase': ['mean', 'std'],
    'amplitude': 'mean'
}).round(2)

print(circadian_summary)
print()

# ============================================================================
# STEP 5: Analyze glucose by custom age groups
# ============================================================================

print("Fasting Glucose by Custom Age Groups")
print("-" * 60)

glucose_summary = sleep_data.groupby('age_custom').apply(lambda x: pd.Series({
    'N': len(x),
    'Mean_Age': x['age'].mean(),
    'Mean_Glucose': x['fasting_glucose'].mean(),
    'SD_Glucose': x['fasting_glucose'].std(),
    'Above_100': (x['fasting_glucose'] >= 100).sum(),
    'Pct_Above_100': 100 * (x['fasting_glucose'] >= 100).sum() / len(x)
})).round(1)

print(glucose_summary)
print()

# ============================================================================
# STEP 6: Create visualizations
# ============================================================================

print("Creating visualizations...")

# Plot 1: Sleep efficiency by age quartile
fig, ax = plt.subplots(figsize=(10, 6))
sleep_data.boxplot(column='sleep_efficiency', by='age_quartile', ax=ax)
ax.set_xlabel('Age Quartile')
ax.set_ylabel('Sleep Efficiency (%)')
ax.set_title('Sleep Efficiency by Age Quartile')
plt.suptitle('')  # Remove the default title
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('sleep_efficiency_by_age_python.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 2: Circadian phase vs age (with decade coloring)
fig, ax = plt.subplots(figsize=(10, 6))
for decade in sleep_data['age_decade'].unique():
    mask = sleep_data['age_decade'] == decade
    ax.scatter(sleep_data[mask]['age'], 
              sleep_data[mask]['circadian_phase'],
              label=decade, alpha=0.6, s=50)

# Add trend line
z = np.polyfit(sleep_data['age'], sleep_data['circadian_phase'], 1)
p = np.poly1d(z)
ax.plot(sleep_data['age'].sort_values(), 
        p(sleep_data['age'].sort_values()), 
        "k--", alpha=0.5, label='Trend')

ax.set_xlabel('Age (years)')
ax.set_ylabel('Circadian Phase (hours)')
ax.set_title('Circadian Phase vs Age')
ax.legend()
plt.tight_layout()
plt.savefig('circadian_phase_vs_age_python.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 3: Multiple measures by age quartile
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

measures = ['sleep_efficiency', 'total_sleep_time', 'waso']
titles = ['Sleep Efficiency', 'Total Sleep Time', 'WASO']

for ax, measure, title in zip(axes, measures, titles):
    sleep_data.boxplot(column=measure, by='age_quartile', ax=ax)
    ax.set_xlabel('Age Quartile')
    ax.set_ylabel(title)
    ax.set_title(title)
    plt.sca(ax)
    plt.xticks(rotation=45, ha='right')

plt.suptitle('Sleep Measures by Age Quartile')
plt.tight_layout()
plt.savefig('multiple_sleep_measures_python.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 4: Heatmap of correlations
fig, ax = plt.subplots(figsize=(10, 8))
corr_data = sleep_data[['age', 'sleep_efficiency', 'total_sleep_time', 
                        'waso', 'circadian_phase', 'amplitude', 
                        'fasting_glucose', 'cortisol_awakening']]
correlation = corr_data.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, ax=ax)
ax.set_title('Correlation Matrix of Age and Sleep/Circadian Measures')
plt.tight_layout()
plt.savefig('correlation_heatmap_python.png', dpi=300, bbox_inches='tight')
plt.close()

print("Plots saved successfully!")
print()

# ============================================================================
# STEP 7: Export stratified data
# ============================================================================

print("Exporting stratified data...")

# Save data with age stratifications
sleep_data.to_csv('sleep_data_with_age_groups_python.csv', index=False)

print("Data exported to: sleep_data_with_age_groups_python.csv")
print()

# ============================================================================
# STEP 8: Summary report
# ============================================================================

print("Summary Report")
print("=" * 60)
print(f"Total participants: {len(sleep_data)}")
print(f"Age range: {int(sleep_data['age'].min())} - {int(sleep_data['age'].max())} years")
print(f"Mean age: {sleep_data['age'].mean():.1f} (SD = {sleep_data['age'].std():.1f})")
print()

print("Age stratification methods applied:")
print("1. Quartiles - for balanced statistical analysis")
print("2. Decades - for easy interpretation and reporting")
print("3. Custom groups (40-49, 50-59, 60-69, 70-74) - for targeted analysis")
print()

# Calculate key findings
q1_data = sleep_data[sleep_data['age_quartile'] == 'Q1 (Youngest 25%)']
q4_data = sleep_data[sleep_data['age_quartile'] == 'Q4 (Oldest 25%)']
decade_40s = sleep_data[sleep_data['age_decade'] == '40s (40-49)']
decade_70s = sleep_data[sleep_data['age_decade'] == '70s (70-79)']

print("Key findings:")
print(f"- Sleep efficiency decreases with age (Q1: {q1_data['sleep_efficiency'].mean():.1f}%, "
      f"Q4: {q4_data['sleep_efficiency'].mean():.1f}%)")
print(f"- Wake after sleep onset increases with age (Q1: {q1_data['waso'].mean():.1f} min, "
      f"Q4: {q4_data['waso'].mean():.1f} min)")

if len(decade_70s) > 0:
    print(f"- Fasting glucose increases with age (40s: {decade_40s['fasting_glucose'].mean():.1f} mg/dL, "
          f"70s: {decade_70s['fasting_glucose'].mean():.1f} mg/dL)")

print()
print("Analysis complete!")
