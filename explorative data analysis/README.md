# Exploratory Data Analysis (EDA)

## 📌 Overview

This project focuses on Exploratory Data Analysis (EDA), a crucial step in the data science workflow. The goal is to understand the dataset by cleaning the data, analyzing its structure, identifying patterns, detecting outliers, and visualizing relationships between variables.

## 🚀 Features

- Load and inspect datasets
- Handle missing values
- Remove duplicate records
- Perform statistical analysis
- Detect outliers
- Visualize data using charts and graphs
- Explore correlations between variables
- Generate meaningful insights

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## 📂 Project Structure

- `Titanic-Dataset.csv` - The raw passenger data.
- `eda.py` - Python analysis and visualization script.
- `titanic_eda_report.md` - Structured analysis report presenting statistical summaries and insights.
- `plots/` - Folder containing all generated visualization charts:
  - `survival_rate.png` - Overall survival distribution.
  - `pclass_distribution.png` - Distribution of passenger classes.
  - `sex_distribution.png` - Distribution of passenger genders.
  - `age_distribution.png` - Overall age distribution.
  - `fare_distribution.png` - Distribution of ticket prices.
  - `survival_by_sex.png` - Survival rates for males vs. females.
  - `survival_by_pclass.png` - Survival rates by ticket class.
  - `survival_by_age.png` - Age distribution compared between survivors and deceased.
  - `survival_by_family.png` - Impact of family size on survival.
  - `survival_by_title.png` - Survival rates grouped by passenger social titles.
  - `survival_by_sex_pclass.png` - Multivariate analysis of survival by gender and class.
  - `correlation_heatmap.png` - Pearson correlation matrix of numerical and encoded features.

## ⚙️ How to Run

1. Install the required libraries:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
2. Run the analysis script to regenerate the plots:
   ```bash
   python eda.py
   ```
3. Open `titanic_eda_report.md` to view the comprehensive findings.
