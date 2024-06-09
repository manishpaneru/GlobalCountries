# This is my first attempt at cleaning a dataset of global countries! 
# I found it on Kaggle and thought it would be a fun way to practice my Pandas skills.
# Let's see what we can do!

import pandas as pd    # This is the main library I'll use for data cleaning
import numpy as np     # NumPy for some math stuff if I need it
from scipy.stats.mstats import winsorize  # This helps me deal with extreme values, I heard it's important!
from sklearn.preprocessing import StandardScaler, MinMaxScaler  # These are for scaling data, will make it nicer for analysis later

# Let's read in the CSV file
df = pd.read_csv('world-data-2023.csv')

# First, let's take a quick look at the first few rows to get a feel for the data
print("First 5 rows:")
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Hmm, some columns have weird names with newlines. I should fix that later.

# A summary of each column: means, counts, etc.
print("\nSummary Statistics:")
print(df.describe().to_markdown(numalign="left", stralign="left"))

# What types of data do we have in each column? (Numbers, text, etc.)
print("\nColumn Info:")
print(df.info())

# All the column names so I can refer to them easily
print("\nColumn Names:")
print(df.columns)


# Uh oh, some countries are missing data for Birth Rate, Infant mortality, and Life expectancy!
# Let's just remove those rows for now.
df.dropna(subset=['Birth Rate', 'Infant mortality', 'Life expectancy'], inplace=True)

# Let's get rid of rows with any missing values
df.dropna(inplace=True)

# Oops, I just dropped ALL the rows because some columns had a ton of missing values. 
# This isn't the best, but for now, I'll focus on the columns I actually want to use.

# These columns seem unnecessary, so let's drop them
df.drop(columns=['Abbreviation', 'Latitude', 'Longitude'], inplace=True)

# There are '%' signs messing up some of the numbers, gotta get rid of those!
for column in ['Density\n(P/Km2)', 'Agricultural Land( %)', 'Forested Area (%)', 'CPI Change (%)', 'Gross primary education enrollment (%)', 'Gross tertiary education enrollment (%)', 'Population: Labor force participation (%)', 'Tax revenue (%)', 'Total tax rate', 'Unemployment rate']:
    df[column] = df[column].astype(str).str.replace('%', '', regex=False)  # This will take care of the '%' sign
    df[column] = pd.to_numeric(df[column], errors='coerce')   # Now let's make these numbers

print("Data after removing '%' sign:")
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Some columns have '<span class="math-inline">' and commas, which also make them not numeric
for column in \['Land Area\(Km2\)', 'Armed Forces size', 'Co2\-Emissions', 'CPI', 'Gasoline Price', 'GDP', 'Minimum wage', 'Out of pocket health expenditure', 'Population', 'Urban\_population'\]\:
df\[column\] \= df\[column\]\.astype\(str\)\.str\.replace\(r'\[</span>,]', '', regex=True).str.replace('nan', '0', regex=False)  # Replace '<span class="math-inline">', commas, and 'nan'
df\[column\] \= pd\.to\_numeric\(df\[column\], errors\='coerce'\)    \# Convert to numbers
print\("Data after removing '</span>' and ',' sign:")
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Oh no, there are 'N/A' values in the 'Minimum wage' column... let's replace them with NaN
df['Minimum wage'] = df['Minimum wage'].replace('N/A', np.nan) 

# For missing 'Minimum wage' values, I'll use the median for each currency to fill them in
df['Minimum wage'] = df.groupby('Currency-Code')['Minimum wage'].transform(lambda x: x.fillna(x.median()))

# Some commas are messing up 'Out of pocket health expenditure' values, time to fix those!
df['Out of pocket health expenditure'] = df['Out of pocket health expenditure'].astype(str).str.replace(',', '.', regex=False)  # Replace ',' with '.'
df['Out of pocket health expenditure'] = pd.to_numeric(df['Out of pocket health expenditure'], errors='coerce') # Make those numbers!

# Same trick for filling in missing values, using the mean for each currency
df['Out of pocket health expenditure'] = df.groupby('Currency-Code')['Out of pocket health expenditure'].transform(lambda x: x.fillna(x.mean()))

# Making a new column to group countries by income level (low, middle, high) based on GDP per capita
df['Income Level'] = pd.qcut(df['GDP per capita'], q=4, labels=['Low', 'Lower-Middle', 'Upper-Middle', 'High'])

# Filling in any remaining blanks with "Missing" - gotta be tidy!
df['Abbreviation'] = df['Abbreviation'].fillna('Missing')
df['Capital/Major City'] = df['Capital/Major City'].fillna('Missing')
df['Currency-Code'] = df['Currency-Code'].fillna('Missing')
df['Official language'] = df['Official language'].fillna('Missing')

# Some countries have extra stuff after the name, let's clean those up
df['Country'] = df['Country'].astype(str).str.split(',').str[0]  

# Same issue with city names, sometimes extra info after "and"
df['Largest city'] = df['Largest city'].astype(str).str.split(' and').str[0] 

# These columns should be categories, not just regular text
df['Calling Code'] = df['Calling Code'].astype('category')  
df['Currency-Code'] = df['Currency-Code'].astype('category')
df['Official language'] = df['Official language'].astype('category')

# Missing Density? Let's just use the median for now...
median_density = df['Density\n(P/Km2)'].median()
df['Density\n(P/Km2)'].fillna(median_density, inplace=True)

# Same idea for missing Agricultural Land data
mean_agricultural_land = df['Agricultural Land( %)'].mean()
df['Agricultural Land( %)'].fillna(mean_agricultural_land, inplace=True)

# Let's calculate GDP per capita by dividing GDP by Population
df['GDP per capita'] = df['GDP'] / df['Population']

# Drop rows with missing GDP per capita values (if any)
df.dropna(subset=['GDP per capita'], inplace=True)

# Trying out this fancy "Winsorization" thing to deal with extreme Co2 emissions
df['Co2-Emissions'] = winsorize(df['Co2-Emissions'], limits=[0, 0.05]) 

# Scaling CPI to be between 0 and 1
scaler = MinMaxScaler()
df['CPI'] = scaler.fit_transform(df[['CPI']])  

print("Cleaned data:")
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Creating a binary flag to indicate high-income countries
df['High_Income'] = df['Income Level'].apply(lambda x: 1 if x == 'High' else 0)

# Standardizing Birth Rate
scaler = StandardScaler()
df['Birth Rate'] = scaler.fit_transform(df[['Birth Rate']]) 

# Quick check of how the 'GDP per capita' is distributed (skewed or normal-ish?)
print("\nGDP per capita Stats:")
print(f"Skewness of GDP per capita: {df['GDP per capita'].skew()}") 
print(f"Kurtosis of GDP per capita: {df['GDP per capita'].kurtosis()}") 

# This looks pretty skewed, so I'll have to be careful with analysis!
print("\nThe GDP per capita distribution is highly right-skewed and has heavy tails. This suggests there are some outlier countries with really high GDP per capita, and most countries are clumped together with lower values.")



# I've heard outliers can mess up analysis, so let's try to remove them 
columns_to_check = ['Density\n(P/Km2)', 'Agricultural Land( %)', 'Land Area(Km2)', 'Armed Forces size', 'Co2-Emissions', 'CPI', 'Forested Area (%)', 'Gasoline Price', 'Gross primary education enrollment (%)', 'Gross tertiary education enrollment (%)', 'Infant mortality', 'Life expectancy', 'Maternal mortality ratio', 'Minimum wage', 'Out of

# Iterate through each column
for col in columns_to_check:
    # Calculate Q1, Q3, and IQR
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    # Define bounds
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

    # Replace outliers with median
    median_value = df[col].median()
    df.loc[outliers.index, col] = median_value

    # Print results
    print(f"Column '{col}': {len(outliers)} outliers replaced with median {median_value}")
