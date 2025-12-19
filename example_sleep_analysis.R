# Example: Age Stratification in Sleep Research
# This script demonstrates how to apply age stratification to sleep and circadian data

# Load the age stratification functions
source("age_stratification.R")

# Load required libraries (install if needed)
# install.packages(c("dplyr", "ggplot2"))
library(dplyr)
library(ggplot2)

# ============================================================================
# STEP 1: Create example sleep and circadian data
# ============================================================================

set.seed(42)
n <- 100

# Create synthetic dataset representing sleep and circadian measures
sleep_data <- data.frame(
  participant_id = 1:n,
  age = round(runif(n, 40, 75)),
  
  # Sleep measures (with age-related trends)
  sleep_efficiency = pmax(50, pmin(100, 88 - 0.15 * (runif(n, 40, 75) - 40) + rnorm(n, 0, 8))),
  total_sleep_time = pmax(300, 420 - 0.8 * (runif(n, 40, 75) - 40) + rnorm(n, 0, 45)),
  waso = pmax(0, 25 + 0.5 * (runif(n, 40, 75) - 40) + abs(rnorm(n, 0, 15))),
  
  # Circadian measures
  circadian_phase = 2.5 + 0.02 * (runif(n, 40, 75) - 40) + rnorm(n, 0, 1.2),
  amplitude = pmax(0.1, 0.8 - 0.006 * (runif(n, 40, 75) - 40) + abs(rnorm(n, 0, 0.15))),
  
  # Biological measures
  fasting_glucose = pmax(70, 92 + 0.3 * (runif(n, 40, 75) - 40) + rnorm(n, 0, 10)),
  cortisol_awakening = pmax(5, 18 - 0.08 * (runif(n, 40, 75) - 40) + rnorm(n, 0, 4))
)

# ============================================================================
# STEP 2: Apply different age stratification methods
# ============================================================================

cat("Age Stratification Analysis for Sleep Research\n")
cat("===============================================\n\n")

# Method 1: Quartiles (recommended for balanced analysis)
sleep_data$age_quartile <- stratify_age_quartiles(sleep_data$age)

# Method 2: Decades (recommended for communication)
sleep_data$age_decade <- stratify_age_decades(sleep_data$age)

# Method 3: Custom groups (example for metabolic research)
sleep_data$age_custom <- stratify_age_custom(sleep_data$age, 
                                              breaks = c(40, 50, 60, 70, 75))

# ============================================================================
# STEP 3: Analyze sleep efficiency by age group (using quartiles)
# ============================================================================

cat("Sleep Efficiency by Age Quartile\n")
cat("---------------------------------\n")

sleep_summary <- sleep_data %>%
  group_by(age_quartile) %>%
  summarise(
    N = n(),
    Mean_Age = round(mean(age), 1),
    SD_Age = round(sd(age), 1),
    Mean_Sleep_Eff = round(mean(sleep_efficiency), 1),
    SD_Sleep_Eff = round(sd(sleep_efficiency), 1),
    Mean_TST = round(mean(total_sleep_time), 0),
    Mean_WASO = round(mean(waso), 1)
  )

print(sleep_summary)
cat("\n")

# Statistical test
kruskal_result <- kruskal.test(sleep_efficiency ~ age_quartile, data = sleep_data)
cat(sprintf("Kruskal-Wallis test: H = %.2f, p = %.4f\n\n", 
            kruskal_result$statistic, kruskal_result$p.value))

# ============================================================================
# STEP 4: Analyze circadian phase by age decade
# ============================================================================

cat("Circadian Phase by Age Decade\n")
cat("------------------------------\n")

circadian_summary <- sleep_data %>%
  group_by(age_decade) %>%
  summarise(
    N = n(),
    Mean_Age = round(mean(age), 1),
    Mean_Phase = round(mean(circadian_phase), 2),
    SD_Phase = round(sd(circadian_phase), 2),
    Mean_Amplitude = round(mean(amplitude), 2)
  )

print(circadian_summary)
cat("\n")

# ============================================================================
# STEP 5: Analyze glucose by custom age groups
# ============================================================================

cat("Fasting Glucose by Custom Age Groups\n")
cat("-------------------------------------\n")

glucose_summary <- sleep_data %>%
  group_by(age_custom) %>%
  summarise(
    N = n(),
    Mean_Age = round(mean(age), 1),
    Mean_Glucose = round(mean(fasting_glucose), 1),
    SD_Glucose = round(sd(fasting_glucose), 1),
    Above_100 = sum(fasting_glucose >= 100),
    Pct_Above_100 = round(100 * sum(fasting_glucose >= 100) / n(), 1)
  )

print(glucose_summary)
cat("\n")

# ============================================================================
# STEP 6: Create visualizations
# ============================================================================

cat("Creating visualizations...\n")

# Plot 1: Sleep efficiency by age quartile
p1 <- ggplot(sleep_data, aes(x = age_quartile, y = sleep_efficiency)) +
  geom_boxplot(fill = "lightblue", alpha = 0.7) +
  geom_jitter(width = 0.2, alpha = 0.3) +
  labs(title = "Sleep Efficiency by Age Quartile",
       x = "Age Quartile",
       y = "Sleep Efficiency (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Plot 2: Circadian phase by age (with decade coloring)
p2 <- ggplot(sleep_data, aes(x = age, y = circadian_phase, color = age_decade)) +
  geom_point(alpha = 0.6, size = 2) +
  geom_smooth(method = "lm", se = TRUE, color = "black", linetype = "dashed") +
  labs(title = "Circadian Phase vs Age",
       x = "Age (years)",
       y = "Circadian Phase (hours)",
       color = "Age Decade") +
  theme_minimal()

# Plot 3: Multiple measures by age quartile
sleep_long <- sleep_data %>%
  select(age_quartile, sleep_efficiency, total_sleep_time, waso) %>%
  tidyr::pivot_longer(cols = c(sleep_efficiency, total_sleep_time, waso),
                     names_to = "measure",
                     values_to = "value")

p3 <- ggplot(sleep_long, aes(x = age_quartile, y = value)) +
  geom_boxplot(fill = "lightgreen", alpha = 0.7) +
  facet_wrap(~ measure, scales = "free_y") +
  labs(title = "Sleep Measures by Age Quartile",
       x = "Age Quartile",
       y = "Value") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Save plots
ggsave("sleep_efficiency_by_age.png", p1, width = 8, height = 6)
ggsave("circadian_phase_vs_age.png", p2, width = 8, height = 6)
ggsave("multiple_sleep_measures.png", p3, width = 10, height = 6)

cat("Plots saved successfully!\n\n")

# ============================================================================
# STEP 7: Export stratified data
# ============================================================================

cat("Exporting stratified data...\n")

# Save data with age stratifications
write.csv(sleep_data, "sleep_data_with_age_groups.csv", row.names = FALSE)

cat("Data exported to: sleep_data_with_age_groups.csv\n\n")

# ============================================================================
# STEP 8: Summary report
# ============================================================================

cat("Summary Report\n")
cat("==============\n")
cat(sprintf("Total participants: %d\n", nrow(sleep_data)))
cat(sprintf("Age range: %d - %d years\n", min(sleep_data$age), max(sleep_data$age)))
cat(sprintf("Mean age: %.1f (SD = %.1f)\n\n", mean(sleep_data$age), sd(sleep_data$age)))

cat("Age stratification methods applied:\n")
cat("1. Quartiles - for balanced statistical analysis\n")
cat("2. Decades - for easy interpretation and reporting\n")
cat("3. Custom groups (40-49, 50-59, 60-69, 70-74) - for targeted analysis\n\n")

cat("Key findings:\n")
cat(sprintf("- Sleep efficiency decreases with age (Q1: %.1f%%, Q4: %.1f%%)\n",
            mean(sleep_data$sleep_efficiency[sleep_data$age_quartile == "Q1 (Youngest 25%)"]),
            mean(sleep_data$sleep_efficiency[sleep_data$age_quartile == "Q4 (Oldest 25%)"])))

cat(sprintf("- Wake after sleep onset increases with age (Q1: %.1f min, Q4: %.1f min)\n",
            mean(sleep_data$waso[sleep_data$age_quartile == "Q1 (Youngest 25%)"]),
            mean(sleep_data$waso[sleep_data$age_quartile == "Q4 (Oldest 25%)"])))

cat(sprintf("- Fasting glucose increases with age (40s: %.1f mg/dL, 70s: %.1f mg/dL)\n",
            mean(sleep_data$fasting_glucose[sleep_data$age_decade == "40s (40-49)"]),
            mean(sleep_data$fasting_glucose[sleep_data$age_decade == "70s (70-79)"])))

cat("\nAnalysis complete!\n")
