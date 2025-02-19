# -- coding: utf-8 --
"""
Created on Fri Nov  8 18:10:53 2024

@author: kate
"""

import pandas as pd
import numpy as np

# Step 1: Load the existing trial data file "Consistency Report.csv"
df = pd.read_csv('Consistency Report.csv')

# Check the first few rows to confirm the data format
print("Loaded Data:\n", df.head())

# Step 2: Define the week labels for 2024 (Wk 43 to Wk 46)
week_labels_2024 = ['Wk 43', 'Wk 44', 'Wk 45', 'Wk 46']

# Step 3: Calculate the mean and standard deviation of sales for Wk 43 to Wk 46 for each store
df['mean_2024'] = df[week_labels_2024].mean(axis=1)  # Mean of Wk 43 to Wk 46 for 2024
df['std_dev_2024'] = df[week_labels_2024].std(axis=1)  # Standard deviation of Wk 43 to Wk 46 for 2024

# Step 4: Add columns for Ave Wk 2024 and Peak Wk 2024 from the dataset
# Assuming these columns are already present in the dataset
df['mean_2024_benchmark'] = df['Ave Wk 2024']  # Average sales for 2024 for each store
df['peak_2024_benchmark'] = df['Peak Wk 2024']  # Peak sales for 2024 for each store

# Step 5: Flag stores based on their 2024 sales for weeks 43-46 and the benchmark data
def flag_inconsistent_2024(row):
    inconsistent = False
    
    # Flag if any sales in weeks Wk 43 to Wk 46 exceed the peak for 2024 or fall below 75% of the 2024 average
    for week in week_labels_2024:
        if row[week] > row['peak_2024_benchmark']:  # Sales exceed peak
            inconsistent = True
        if row[week] < row['mean_2024_benchmark'] * 0.75:  # Sales below 75% of the average
            inconsistent = True

    if inconsistent:
        return 'Inconsistent (Based on 2024 Ave & Peak)'
    else:
        return 'Consistent (Based on 2024 Ave & Peak)'

df['Flag_2024'] = df.apply(flag_inconsistent_2024, axis=1)

# Step 6: Week-over-week sales consistency check
def week_over_week_check(row):
    for i in range(1, len(week_labels_2024)):
        # Calculate the sales difference from the previous week
        sales_diff = abs(row[week_labels_2024[i]] - row[week_labels_2024[i-1]])
        sales_avg = (row[week_labels_2024[i]] + row[week_labels_2024[i-1]]) / 2
        
        # Define a threshold for significant difference (e.g., ±30% difference from previous week)
        if sales_diff > sales_avg * 0.30:  # 30% change threshold
            return 'Inconsistent (Week-over-Week Change Too High)'
    
    return 'Consistent (Week-over-Week)'

df['Flag_Week_Over_Week'] = df.apply(week_over_week_check, axis=1)

# Step 7: Combine the flags
def combine_flags(row):
    if 'Inconsistent' in row['Flag_2024'] or 'Inconsistent' in row['Flag_Week_Over_Week']:
        return 'Inconsistent (Ave/Peak or Week-over-Week)'
    else:
        return 'Consistent'

df['Final_Flag'] = df.apply(combine_flags, axis=1)

# Step 8: Add the "Good" column for increasing sales (Wk 46 > Wk 45)
def flag_good_sales(row):
    # Check if sales in Wk 46 are higher than sales in Wk 45
    if row['Wk 46'] > row['Wk 45']:
        return 'Good'
    else:
        return 'Not Good'

df['Good'] = df.apply(flag_good_sales, axis=1)

# Step 9: Add the "Increasing" column for increasing sales over the weeks
def flag_increasing_sales(row):
    # Check if sales are consistently increasing from Wk 43 to Wk 46
    for i in range(1, len(week_labels_2024)):
        if row[week_labels_2024[i]] <= row[week_labels_2024[i-1]]:  # If sales are not increasing
            return 'Not Increasing'
    
    return 'Increasing'

df['Increasing'] = df.apply(flag_increasing_sales, axis=1)

# Step 12: Add a new column for the sales difference between Wk 46 and Wk 45
df['Wk 46 vs Wk 45 Difference'] = df['Wk 46'] - df['Wk 45']

# Step 13: Add a new column for the percentage difference between Wk 46 and Wk 43
df['Wk 46 vs Wk 45 Percentage Change'] = (df['Wk 46'] - df['Wk 45']) / df['Wk 45'] * 100

# Step 10: Display results for the first few stores (to ensure it's working)
print("Analysis Results (first few rows):\n", df[['Store', 'mean_2024', 'std_dev_2024', 'Flag_2024', 'Flag_Week_Over_Week', 'Final_Flag', 'Good', 'Increasing', 'Wk 46 vs Wk 45 Difference', 'Wk 46 vs Wk 45 Percentage Change']].head())

# Step 11: Save the analysis results to a new CSV file
df.to_csv('sales_analysis_with_good_and_increasing_flag.csv', index=False)
print("\nAnalysis results saved to 'sales_analysis_with_good_and_increasing_flag.csv'.")