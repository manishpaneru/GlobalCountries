#!/usr/bin/env python
# coding: utf-8

# In[85]:


# This is a data-cleaning project. We have a CSV file with the data of countries and their various data. We are gonna clean them now and use it to analysis.
# we are gonna clean it now and we will perform an explorative analysis in this data
# The objective of this data analysis project is to find the relationship between education, and labor force participation, so this data cleaning focus on that.


# In[86]:


# First let's import the libraries and dependecies
import pandas as pd
import numpy as np


# In[87]:


df = pd.read_csv("world-data-2023.csv")
# let's have a look at the data first
df


# In[88]:


# let's have a look at column names in the dataframe
print(df.columns)


# In[89]:


# let's have a look at the data types  in the data
print(df.dtypes)


# In[90]:


# Thats a lots of columns. Let's only use column that are relevant to our projects objectives. soo we aren't gonna need much columns
# First let's do something absolutely basic data cleaning steps, first let's clear white space from the data.
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df


# In[91]:


# Dang it! it deleted 50% of the data
# let's clean the rows name and data types.
# Let's rename the population density table as it has some formatting error while importing the data from excel


# In[92]:


df.rename(
    columns={"Density\n(P/Km2)": "density"}, inplace=True
)  # This code supposedly will change the columns name from something crazy to density
df  # let's check the dataframe to see if it worked


# In[93]:


# AS we have no use of the abbreviation of the countries name in the column as does Agricultural land , land Area(%) , Land Area(Km2), Also Birth rate
# And calling code of the country
df.drop(
    columns=[
        "Abbreviation",
        "Agricultural Land( %)",
        "Land Area(Km2)",
        "Armed Forces size",
        "Birth Rate",
        "Calling Code",
    ],
    inplace=True,
)
# This code should delete all the useless columns
df  # let's check the data


# In[94]:


# We also don't have any use of latitude and longitude
df.drop(
    columns=["Latitude", "Longitude"], inplace=True
)  # This should delete the unnecassary columns
df  # let's check it out


# In[95]:


# There is some issue of Co2 cmission , we dont know the unit of Co2 emmision, let's first see a country's Co2 emmissions and then google it
print(df.loc[df["Country"] == "United Kingdom", "Co2-Emissions"])
# Let's see UK's co2 emissions and compare it to googles answer
# Seems like the value is in 100mt to 1 , so let's change that


# In[96]:


# This code should rename the Co2-Emissions, to emissions_100mt
df.rename(
    columns={"Co2-Emissions": "Emission_100mt"}, inplace=True
)  # This shall rename it
df  # let's check it out


# In[102]:


# Now that we are done with that , we need to delete fertility rate , Forested Area , out of pocket health expenditure , physician per thousand
# infant mortality , Maternal Mortality Ratio , official languages , Currency-Code. There are many columns so first create a list of the columns
# Corrected list of column names to be removed
columns = [
    "Fertility Rate",
    "Forested Area (%)",
    "Out of pocket health expenditure",
    "Physicians per thousand",
    "Infant mortality",
    "Maternal mortality ratio",
    "Official language",
    "Currency-Code",
]

# Remove the specified columns from the DataFrame
df.drop(columns=columns, inplace=True)

# Display the DataFrame after removing the specified columns
print(df)


# In[104]:


# Now that we have all the columns that we need let's change the data types and format them properly
# Let's first remove '$' from the entire data frame also commas from the dataframe  as they will be an obstacle when we convert the data type to int
df = df.replace(
    {"\$": ""}, regex=True
)  # This should remove all the '$' signs from the data frame.
df = df.replace(
    {",": ""}, regex=True
)  # This should remove all the ',' from the data frame
# let's check them out
df


# In[105]:


# Now that we are done with data cleaning, Let's create new dataframes that we can use for visualizations.


# In[106]:


# Let's create a data frame with data of the countries with just data of countries with GDP more than 1 trillion.
developed_nations = df[df["GDP"].astype(float) > 10**12]
developed_nations


# In[107]:


# let's reset the table index.
developed_nations.reset_index(
    drop=True, inplace=True
)  # This should reset the index in the developed nation data frame
developed_nations  # looks like it worked


# In[111]:


# Now that that's sorted out let's Sort the data based on GDP
developed_nations = developed_nations.sort_values(
    by="GDP", ascending=True
)  # This should sort the data
developed_nations  # let's check if hte code worked


# In[114]:


# Now that'e , we can use it later for data visualization and analysis, let's see the original dataframe and then know what to do with the data
df
# let's create a new table with countries with top 10 largest population and then sort it according to populations
# First let's srot our entire dataframe according to the population
df_sorted = df.sort_values(by="Population", ascending=False)
# Now let's creaet a new data frame with population of top 10 countries
population = df_sorted.head(
    10
)  # This code should find the top 10 from the sorted dataframe
population = population.sort_values(
    by="Population", ascending=False
)  # Now it sorts the new created table according to population
population.reset_index(
    drop=True, inplace=True
)  # This should reset the index of the table
population


# In[115]:


# now that we have 3 tables we can continue on analysis part


# In[ ]:


# I ma gonna upload it to GitHub and , So this is the data cleaning part and I can move on to analysis in python part.
