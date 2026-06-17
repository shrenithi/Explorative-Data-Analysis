import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create plots directory if it doesn't exist
os.makedirs('plots', exist_ok=True)

# 1. Load the dataset
print("Loading Titanic dataset...")
df = pd.read_csv('Titanic-Dataset.csv')

# 2. Data Cleaning & Imputation
print("Performing data cleaning...")

# Extract Title to help with Age imputation
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)
# Group rare titles
title_mappings = {
    'Mlle': 'Miss', 'Ms': 'Miss', 'Mme': 'Mrs',
    'Lady': 'Rare', 'Countess': 'Rare', 'Capt': 'Rare', 'Col': 'Rare',
    'Don': 'Rare', 'Dr': 'Rare', 'Major': 'Rare', 'Rev': 'Rare',
    'Sir': 'Rare', 'Jonkheer': 'Rare', 'Dona': 'Rare'
}
df['Title'] = df['Title'].replace(title_mappings)

# Impute missing Age based on the median Age for each Title
print("Imputing missing Age values based on passenger titles...")
title_median_ages = df.groupby('Title')['Age'].median()
df['Age'] = df.apply(
    lambda row: title_median_ages[row['Title']] if pd.isnull(row['Age']) else row['Age'],
    axis=1
)

# Impute missing Embarked with the mode ('S')
print("Imputing missing Embarked values with the mode...")
df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])

# Feature engineering: HasCabin (1 if Cabin is recorded, else 0)
df['HasCabin'] = df['Cabin'].apply(lambda x: 0 if pd.isnull(x) else 1)

# Feature engineering: FamilySize and IsAlone
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df['IsAlone'] = df['FamilySize'].apply(lambda x: 1 if x == 1 else 0)

# Drop columns that won't be used in numerical correlation or are highly sparse
# We keep Ticket, Name, PassengerId in df for reference but they won't go in the heatmap.

# 3. Setup Plotting Aesthetics
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['figure.titlesize'] = 16

# Color palette definition for survivors (0: Died, 1: Survived)
surv_palette = {0: "#d9534f", 1: "#5cb85c"}  # Red-ish and Green-ish

print("Generating plots...")

# --- UNIVARIATE PLOTS ---

# Plot 1: Survival Rate (Survived)
plt.figure()
sns.countplot(data=df, x='Survived', palette=surv_palette, hue='Survived', legend=False)
plt.title("Distribution of Survival (0 = Deceased, 1 = Survived)")
plt.xlabel("Survival Status")
plt.ylabel("Passenger Count")
plt.xticks([0, 1], ['Deceased', 'Survived'])
plt.savefig('plots/survival_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 2: Passenger Class (Pclass) Distribution
plt.figure()
sns.countplot(data=df, x='Pclass', palette="Blues_r", hue='Pclass', legend=False)
plt.title("Distribution of Passengers by Class")
plt.xlabel("Passenger Class (Pclass)")
plt.ylabel("Passenger Count")
plt.xticks([0, 1, 2], ['1st Class', '2nd Class', '3rd Class'])
plt.savefig('plots/pclass_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 3: Gender (Sex) Distribution
plt.figure()
sns.countplot(data=df, x='Sex', palette="pastel", hue='Sex', legend=False)
plt.title("Distribution of Passengers by Gender")
plt.xlabel("Gender")
plt.ylabel("Passenger Count")
plt.savefig('plots/sex_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 4: Age Distribution (Histogram + KDE)
plt.figure()
sns.histplot(data=df, x='Age', kde=True, color='#2b5c8f', bins=30)
plt.title("Passenger Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.savefig('plots/age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 5: Fare Distribution (Histogram + KDE)
plt.figure()
sns.histplot(data=df, x='Fare', kde=True, color='#8884d8', bins=40)
plt.title("Passenger Ticket Fare Distribution")
plt.xlabel("Fare (in GBP)")
plt.ylabel("Frequency")
plt.savefig('plots/fare_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# --- BIVARIATE PLOTS ---

# Plot 6: Survival by Gender
plt.figure()
sns.barplot(data=df, x='Sex', y='Survived', errorbar=None, palette="pastel", hue='Sex', legend=False)
plt.title("Survival Rate by Gender")
plt.xlabel("Gender")
plt.ylabel("Survival Rate")
plt.ylim(0, 1)
# Add data labels
ax = plt.gca()
for p in ax.patches:
    ax.annotate(f"{p.get_height()*100:.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() - 0.08),
                ha='center', va='center', color='white', fontweight='bold', xytext=(0, 0), textcoords='offset points')
plt.savefig('plots/survival_by_sex.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 7: Survival by Pclass
plt.figure()
sns.barplot(data=df, x='Pclass', y='Survived', errorbar=None, palette="Blues_r", hue='Pclass', legend=False)
plt.title("Survival Rate by Passenger Class")
plt.xlabel("Passenger Class")
plt.ylabel("Survival Rate")
plt.xticks([0, 1, 2], ['1st Class', '2nd Class', '3rd Class'])
plt.ylim(0, 1)
ax = plt.gca()
for p in ax.patches:
    ax.annotate(f"{p.get_height()*100:.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() - 0.08),
                ha='center', va='center', color='white', fontweight='bold', xytext=(0, 0), textcoords='offset points')
plt.savefig('plots/survival_by_pclass.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 8: Survival by Age (KDE Split)
plt.figure()
sns.kdeplot(data=df[df['Survived'] == 0], x='Age', fill=True, color='#d9534f', label='Deceased', alpha=0.5)
sns.kdeplot(data=df[df['Survived'] == 1], x='Age', fill=True, color='#5cb85c', label='Survived', alpha=0.5)
plt.title("Age Distribution by Survival Status")
plt.xlabel("Age")
plt.ylabel("Density")
plt.legend()
plt.savefig('plots/survival_by_age.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 9: Survival by Family Size
plt.figure()
sns.barplot(data=df, x='FamilySize', y='Survived', errorbar=None, color='#5bc0de')
plt.title("Survival Rate by Family Size (SibSp + Parch + 1)")
plt.xlabel("Family Size")
plt.ylabel("Survival Rate")
plt.ylim(0, 1)
plt.savefig('plots/survival_by_family.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 10: Survival by Title
plt.figure()
sns.barplot(data=df, x='Title', y='Survived', errorbar=None, palette="Set2", hue='Title', legend=False)
plt.title("Survival Rate by Title")
plt.xlabel("Title")
plt.ylabel("Survival Rate")
plt.ylim(0, 1)
ax = plt.gca()
for p in ax.patches:
    if p.get_height() > 0:
        ax.annotate(f"{p.get_height()*100:.1f}%", (p.get_x() + p.get_width() / 2., p.get_height() - 0.08),
                    ha='center', va='center', color='white', fontweight='bold', xytext=(0, 0), textcoords='offset points')
plt.savefig('plots/survival_by_title.png', dpi=300, bbox_inches='tight')
plt.close()

# Plot 11: Survival by Sex and Passenger Class (Multivariate)
plt.figure()
sns.pointplot(data=df, x='Pclass', y='Survived', hue='Sex', palette="pastel", markers=["o", "s"], linestyles=["-", "--"])
plt.title("Survival Probability by Passenger Class and Sex")
plt.xlabel("Passenger Class")
plt.ylabel("Survival Probability")
plt.xticks([0, 1, 2], ['1st Class', '2nd Class', '3rd Class'])
plt.ylim(0, 1)
plt.savefig('plots/survival_by_sex_pclass.png', dpi=300, bbox_inches='tight')
plt.close()

# --- CORRELATION HEATMAP ---
# Encode Sex and Embarked for correlation analysis
df_encoded = df.copy()
df_encoded['Sex_encoded'] = df_encoded['Sex'].map({'male': 0, 'female': 1})
df_encoded['Embarked_encoded'] = df_encoded['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

# Select numerical columns for correlation
corr_cols = ['Survived', 'Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'HasCabin', 'FamilySize', 'IsAlone', 'Sex_encoded', 'Embarked_encoded']
corr_matrix = df_encoded[corr_cols].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
plt.title("Correlation Matrix Heatmap")
plt.savefig('plots/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("All plots generated successfully inside 'plots/' folder.")

# Print some useful statistics to console
print("\n--- STATISTICS SUMMARY FOR REPORT ---")
print(f"Overall Survival Rate: {df['Survived'].mean()*100:.2f}%")
print("\nSurvival Rate by Gender:")
print(df.groupby('Sex')['Survived'].mean() * 100)
print("\nSurvival Rate by Class:")
print(df.groupby('Pclass')['Survived'].mean() * 100)
print("\nSurvival Rate by Title:")
print(df.groupby('Title')['Survived'].mean() * 100)
print("\nSurvival Rate by Having Cabin:")
print(df.groupby('HasCabin')['Survived'].mean() * 100)
print("\nSurvival Rate by Family Size:")
print(df.groupby('FamilySize')['Survived'].mean() * 100)
