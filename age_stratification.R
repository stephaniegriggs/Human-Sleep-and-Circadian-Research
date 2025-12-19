# Age Stratification Methods for Sleep and Circadian Research
# For age range 40-75 years
# 
# This script provides several methods to stratify participants by age
# for use in sleep and circadian actigraphy and biological data analysis

#' Stratify age into equal-width bins
#' 
#' @param age Numeric vector of ages
#' @param n_bins Number of bins to create (default: 3)
#' @param min_age Minimum age in the range (default: 40)
#' @param max_age Maximum age in the range (default: 75)
#' @return Factor with age stratification labels
#' @examples
#' ages <- c(42, 55, 68, 73, 45, 50, 61)
#' stratify_age_equal_width(ages, n_bins = 3)
stratify_age_equal_width <- function(age, n_bins = 3, min_age = 40, max_age = 75) {
  # Calculate bin width
  bin_width <- (max_age - min_age) / n_bins
  
  # Create breaks
  breaks <- seq(min_age, max_age, by = bin_width)
  
  # Create labels
  labels <- sapply(1:(length(breaks)-1), function(i) {
    sprintf("%.0f-%.0f years", breaks[i], breaks[i+1]-1)
  })
  
  # Cut the ages into bins
  age_strata <- cut(age, 
                    breaks = breaks, 
                    labels = labels,
                    include.lowest = TRUE,
                    right = FALSE)
  
  return(age_strata)
}


#' Stratify age into quartiles
#' 
#' @param age Numeric vector of ages
#' @return Factor with quartile labels (Q1-Q4)
#' @examples
#' ages <- c(42, 55, 68, 73, 45, 50, 61)
#' stratify_age_quartiles(ages)
stratify_age_quartiles <- function(age) {
  quartiles <- quantile(age, probs = c(0, 0.25, 0.5, 0.75, 1), na.rm = TRUE)
  
  labels <- c("Q1 (Youngest 25%)", 
              "Q2 (25-50%)", 
              "Q3 (50-75%)", 
              "Q4 (Oldest 25%)")
  
  age_strata <- cut(age,
                    breaks = quartiles,
                    labels = labels,
                    include.lowest = TRUE)
  
  return(age_strata)
}


#' Stratify age into custom age groups
#' 
#' @param age Numeric vector of ages
#' @param breaks Custom break points for age groups
#' @return Factor with custom age group labels
#' @examples
#' ages <- c(42, 55, 68, 73, 45, 50, 61)
#' stratify_age_custom(ages, breaks = c(40, 50, 60, 70, 75))
stratify_age_custom <- function(age, breaks = c(40, 50, 60, 70, 75)) {
  # Create labels from breaks
  labels <- sapply(1:(length(breaks)-1), function(i) {
    sprintf("%.0f-%.0f years", breaks[i], breaks[i+1]-1)
  })
  
  age_strata <- cut(age,
                    breaks = breaks,
                    labels = labels,
                    include.lowest = TRUE,
                    right = FALSE)
  
  return(age_strata)
}


#' Stratify age into median split
#' 
#' @param age Numeric vector of ages
#' @return Factor with younger/older labels
#' @examples
#' ages <- c(42, 55, 68, 73, 45, 50, 61)
#' stratify_age_median_split(ages)
stratify_age_median_split <- function(age) {
  median_age <- median(age, na.rm = TRUE)
  
  age_strata <- ifelse(age < median_age, 
                       sprintf("Younger (<%.0f years)", median_age),
                       sprintf("Older (≥%.0f years)", median_age))
  
  return(factor(age_strata))
}


#' Stratify age into decades
#' 
#' @param age Numeric vector of ages
#' @return Factor with decade labels
#' @examples
#' ages <- c(42, 55, 68, 73, 45, 50, 61)
#' stratify_age_decades(ages)
stratify_age_decades <- function(age) {
  # For 40-75 range, we have 40s, 50s, 60s, 70s
  breaks <- c(40, 50, 60, 70, 80)
  labels <- c("40s (40-49)", "50s (50-59)", "60s (60-69)", "70s (70-79)")
  
  age_strata <- cut(age,
                    breaks = breaks,
                    labels = labels,
                    include.lowest = TRUE,
                    right = FALSE)
  
  return(age_strata)
}


# Example usage and demonstration
demonstrate_stratification <- function() {
  # Create sample data representing participants aged 40-75
  set.seed(123)
  n_participants <- 100
  sample_ages <- round(runif(n_participants, min = 40, max = 75))
  
  cat("=== Age Stratification Demonstration ===\n\n")
  cat(sprintf("Sample size: %d participants\n", n_participants))
  cat(sprintf("Age range: %d-%d years\n", min(sample_ages), max(sample_ages)))
  cat(sprintf("Mean age: %.1f years (SD = %.1f)\n\n", 
              mean(sample_ages), sd(sample_ages)))
  
  # Method 1: Equal-width bins (tertiles)
  cat("1. EQUAL-WIDTH BINS (3 groups)\n")
  strata1 <- stratify_age_equal_width(sample_ages, n_bins = 3)
  print(table(strata1))
  cat("\n")
  
  # Method 2: Quartiles
  cat("2. QUARTILES (data-driven)\n")
  strata2 <- stratify_age_quartiles(sample_ages)
  print(table(strata2))
  cat("\n")
  
  # Method 3: Custom age groups
  cat("3. CUSTOM AGE GROUPS\n")
  strata3 <- stratify_age_custom(sample_ages, breaks = c(40, 50, 60, 70, 75))
  print(table(strata3))
  cat("\n")
  
  # Method 4: Median split
  cat("4. MEDIAN SPLIT\n")
  strata4 <- stratify_age_median_split(sample_ages)
  print(table(strata4))
  cat("\n")
  
  # Method 5: Decades
  cat("5. DECADES\n")
  strata5 <- stratify_age_decades(sample_ages)
  print(table(strata5))
  cat("\n")
  
  # Return a data frame with all stratifications
  results <- data.frame(
    age = sample_ages,
    equal_width = strata1,
    quartiles = strata2,
    custom = strata3,
    median_split = strata4,
    decades = strata5
  )
  
  return(invisible(results))
}

# Run demonstration when script is sourced
if (!interactive()) {
  demonstrate_stratification()
}
