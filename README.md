Python Data Cleaning: World Data 2023
____________________________________________________________________________
Project Description
This project involves cleaning and preprocessing a dataset containing country-level statistics from the year 2023. The goal of this project is to clean the data and prepare it for exploratory data analysis (EDA) and future visualizations. The focus is on investigating the relationship between education and labor force participation.
________________


Key Features
* Data Cleaning:
   * Renamed columns for clarity and consistency.
   * Removed unnecessary columns to reduce noise.
   * Reformatted values (e.g., removed special characters, standardized data types).
* Exploratory Preparation:
   * Created subsets of the data, such as:
      * Countries with GDP greater than 1 trillion.
      * Top 10 countries by population.
   * Sorted and reset indices for better usability.
________________


Dataset Information
* Data Source: World Data 2023 (CSV file).
* Sample Columns:
   * Country: Name of the country.
   * Population: Total population of the country.
   * GDP: Gross Domestic Product (in USD).
   * density: Population density per square kilometer.
   * Emission_100mt: CO2 emissions (in 100 million metric tons).
Sample Data (Before Cleaning):


Country             Population  GDP              density  Emission_100mt
United Kingdom      67886011    $2,828,640,000  273.1    1,200
United States       331002651   $21,427,700,000 36.5     5,280
	

Sample Data (After Cleaning):

Country             Population    GDP         density   Emission_100mt
United Kingdom      67886011      2828640000  273.1    1200
United States       331002651     21427700000 36.5     5280
	________________


Installation and Usage Instructions
1. Dataset:
   * Place the world-data-2023.csv file in the working directory.
2. Steps to Run:
   * Run the Python script (cleaned.py) to clean the dataset.
   * Check the generated subsets for analysis:
      * Countries with GDP greater than 1 trillion.
      * Top 10 countries by population.
________________


Methodology/Approach
1. Initial Inspection:
   * Checked column names and data types.
   * Cleaned whitespace and reformatted column names.
2. Data Reduction:
   * Removed irrelevant columns like Abbreviation, Latitude, and Longitude.
   * Dropped unnecessary economic and demographic fields.
3. Data Transformation:
   * Removed special characters (e.g., $, ,).
   * Standardized CO2 emissions values for consistency.
4. Data Subsets:
   * Extracted relevant subsets for specific analyses:
      * High-GDP countries.
      * Population-based rankings.
________________


Key Insights/Results
* Prepared a cleaned dataset ready for analysis.
* Identified countries with GDP exceeding 1 trillion USD.
* Created a ranking of countries based on population and GDP.
________________


Dependencies
* Python 3.x
* Libraries:
   * pandas
   * numpy
