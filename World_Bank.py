# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:10:55 2018
Author: Arsen Oz

Purpose:
    The purpose of this project is to conduct an explanatory data analysis using
    Python in order to develop a strategy for Southern African countries' from
    2014 World Bank Data.   
    
"""
    
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import seaborn as sns 

###############################################################################   
### 1. Importing and Organizing Data for Analysis
###############################################################################
   
file ='C:/Users/earse/Desktop/MBAN/Python/Project/world_data_hult_regions.xlsx'
global_data = pd.read_excel(file, sheetname = "Sheet1")
 
## Preparing two separate data frames for analysis
SA_group = global_data[global_data['Hult_Team_Regions']=='Southern Africa']
global_data = global_data[global_data['country_name']!='World']
    
SA_final = SA_group.iloc[:,4:] 
global_final = global_data.iloc[:,4:]

###############################################################################
### 2. Visualization of Raw Data
###############################################################################

## Correlation and Heatmap to find relationship between variables
SA_corr = SA_final.corr()
global_corr = global_final.corr()

fig, ax = plt.subplots(figsize = (15,15))
sns.heatmap(global_corr,
            cmap = 'Blues',
            square = True,
            annot = False,
            linecolor = 'black',
            linewidths = 0.5)

plt.show()

## Creating Histograms for visual inspection of data
   
for x in range(1,26): 
    SA_dropped = pd.DataFrame.copy(SA_final)
    global_dropped = pd.DataFrame.copy(global_final)
    
    SA_dropped = SA_dropped.dropna(subset = [SA_dropped.columns[x]]).round(2)
    global_dropped = global_dropped.dropna(subset = [global_dropped.columns[x]]).round(2)
        
    plt.subplots(figsize=(10,5))    
    plt.subplot(1,2,1)
    sns.distplot(SA_dropped.iloc[:,x],
                 bins = 10,
                 color='g',
                 norm_hist = True)
    SA_mean_cols=round(SA_dropped.iloc[:,x].mean(), 2)
    SA_median_cols=round(SA_dropped.iloc[:,x].median(), 2)
    plt.axvline(SA_mean_cols, color = 'red')
    plt.axvline(SA_median_cols, color = 'orange')
    mean_patch = mpatches.Patch(color='red', label=f'Mean:   {SA_mean_cols}')
    median_patch = mpatches.Patch(color='orange', label=f'Median: {SA_median_cols}')
    lgd_1 = plt.legend(handles=[mean_patch, median_patch], bbox_to_anchor = [0.75, -0.15])
    plt.title('Southern Africa')
        
    plt.subplot(1,2,2)
    sns.distplot(global_dropped.iloc[:,x],
                 bins = 10,
                 norm_hist = True)
        
    global_mean_cols=round(global_dropped.iloc[:,x].mean(), 2)
    global_median_cols=round(global_dropped.iloc[:,x].median(), 2)
    plt.axvline(global_mean_cols, color = 'red')
    plt.axvline(global_median_cols, color = 'orange')
    mean_patch = mpatches.Patch(color='red', label=f'Mean:   {global_mean_cols}')
    median_patch = mpatches.Patch(color='orange', label=f'Median: {global_median_cols}')
    lgd_2 = plt.legend(handles=[mean_patch, median_patch], bbox_to_anchor = [0.75, -0.15])
    plt.title('Global')
        
    plt.savefig(f"Dropped Histogram for {SA_dropped.columns[x]}",
                bbox_extra_artists=(lgd_1,lgd_2,), bbox_inches='tight')
    plt.show()

## Creating Boxplots for further visual inspection
for x in range(1,26): 
    
    SA_dropped = pd.DataFrame.copy(SA_final)
    global_dropped = pd.DataFrame.copy(global_final)
    
    SA_dropped = SA_dropped.dropna(subset = [SA_dropped.columns[x]]).round(2)
    global_dropped = global_dropped.dropna(subset = [global_dropped.columns[x]]).round(2)
        
       
    plt.subplots(figsize=(10,5))
    plt.subplot(1,2,1)
    SA_dropped.boxplot(column = SA_dropped.columns[x],
                    meanline = True,
                    showmeans = True)
    plt.title('Southern Africa')
    
    plt.subplot(1,2,2)
    global_dropped.boxplot(column = global_dropped.columns[x],
                    meanline = True,
                    showmeans = True)
    plt.title('Global')
        
    plt.savefig(f"Boxplot for {SA_dropped.columns[x]}")
    plt.show()

###############################################################################
###  3. Selection of Imputation Methods (Mean/Median/Dropping NAs)
###############################################################################
    
# Creating 3 different data frames for Southern Africa and Global data in order
# to try different imputation technics of missing data.    
SA_mean = pd.DataFrame.copy(SA_final)
SA_median = pd.DataFrame.copy(SA_final)
SA_dropped = pd.DataFrame.copy(SA_final)
    
global_mean = pd.DataFrame.copy(global_final)
global_median = pd.DataFrame.copy(global_final)
global_dropped = pd.DataFrame.copy(global_final)

""" Losing significant amount of data with dropna() for both data frames,
    therefore we will not use this method for this case."""   

# Creating lists for columns that will replaced with mean or median
mean_list = ["pct_services_employment",
                "gdp_growth_pct",
                "child_mortality_per_1k",
                "tax_revenue_pct_gdp",
                "unemployment_pct"]

median_list = ["access_to_electricity_pop",
                  "access_to_electricity_rural",
                  "access_to_electricity_urban",
                  "CO2_emissions_per_capita)",
                  "compulsory_edu_yrs",
                  "pct_female_employment",
                  "pct_male_employment",
                  "pct_agriculture_employment",
                  "pct_industry_employment",
                  "exports_pct_gdp",
                  "fdi_pct_gdp",
                  "gdp_usd",
                  "incidence_hiv",
                  "vinternet_usage_pct",
                  "avg_air_pollution",
                  "women_in_parliament",
                  "urban_population_pct",
                  "adult_literacy_pct",
                  "urban_population_growth_pct"]

###############################################################################
###  4. Imputation of Missing Data (With Mean or Median)
###############################################################################

###  Using Mean, Median Imputation
""" Before calculating mean and median to replace 'nan' values, we removed
    outliers from the calculation of mean and median in order to have more
    accurate estimations."""
 
## Southern Africa 
#  Mean
for col in mean_list :
    if SA_mean[col].isnull().any():
        if col != 'income_group':
            Q1_SA = SA_mean[col].quantile(.25)
            Q3_SA = SA_mean[col].quantile(.75)
            IQR_SA = Q3_SA - Q1_SA
            hi_li_SA = Q3_SA + 1.5 * IQR_SA
            low_li_SA = Q1_SA - 1.5 * IQR_SA
            col_mean = SA_mean[col][(SA_mean[col]<= hi_li_SA) &
                              (SA_mean[col] >= low_li_SA)].mean()
            SA_mean[col] = SA_mean[col].fillna(col_mean).round(2)
 
#  Median       
for col in median_list :
    if SA_median[col].isnull().any():
        if col != 'income_group':
            Q1_SA = SA_median[col].quantile(.25)
            Q3_SA = SA_median[col].quantile(.75)
            IQR_SA = Q3_SA - Q1_SA
            hi_li_SA = Q3_SA + 1.5 * IQR_SA
            low_li_SA = Q1_SA - 1.5 * IQR_SA
            col_median = SA_median[col][(SA_median[col]<= hi_li_SA) &
                                        (SA_median[col] >= low_li_SA)].median()
            SA_median[col] = SA_median[col].fillna(col_median).round(2)

## Global Data
#  Mean
for col in mean_list :
    if global_mean[col].isnull().any():
        if col != 'income_group': 
            Q1_global = global_mean[col].quantile(.25)
            Q3_global = global_mean[col].quantile(.75)
            IQR_global = Q3_global - Q1_global
            hi_li_global = Q3_global + 1.5 * IQR_global
            low_li_global = Q1_global - 1.5 * IQR_global
            col_mean = global_mean[col][(global_mean[col]<= hi_li_global) &
                                        (global_mean[col] >= low_li_global)].mean()
            global_mean[col] = global_mean[col].fillna(col_mean).round(2)
 
#  Median           
for col in median_list :
    if global_median[col].isnull().any():
        if col != 'income_group':
            Q1_global = global_median[col].quantile(.25)
            Q3_global = global_median[col].quantile(.75)
            IQR_global = Q3_global - Q1_global
            hi_li_global = Q3_global + 1.5 * IQR_global
            low_li_global = Q1_global - 1.5 * IQR_global
            col_median = global_median[col][(global_median[col]<= hi_li_global) &
                                            (global_median[col] >= low_li_global)].median()
            global_median[col] = global_median[col].fillna(col_median).round(2)

###############################################################################
###  5. Additional Visuals for Key Insights
###############################################################################

""" In this project, further online research has been done in the final version
    (Power Point presentation) in order to explain some of the outliers that are
    spotted in the boxplots and histograms in Chapter 2.
    
    These visuals are created to show those outliers more clearly in the final
    version of this project."""

## CO2 Emission per Capita
fig, ax = plt.subplots(figsize=(8,8))
sns.violinplot(y = 'CO2_emissions_per_capita)',
               data = SA_final,
               orient = 'v',
               inner = None,
               color = 'white')

sns.swarmplot(y = 'CO2_emissions_per_capita)',
              data = SA_final,
              size = 5,
              orient = 'v')

plt.title('CO2 Emission', fontsize=15)
plt.xlabel('Countries in Southern Africa', fontsize=15)
plt.ylabel('CO2 emissions per capita', fontsize=15)
plt.savefig("CO2 emissions per capita')")
plt.show()


## HIV Incidence
fig, ax = plt.subplots(figsize=(8,8))
sns.violinplot(
               y = 'incidence_hiv',
               data = global_final,
               orient = 'v',
               inner = None,
               color = 'white')

sns.swarmplot(
              y = 'incidence_hiv',
              data = global_final,
              size = 5,
              orient = 'v',
              color = 'green')

plt.title('HIV', fontsize=15)
plt.xlabel('Countries', fontsize=15)
plt.ylabel('Incidence HIV', fontsize=15)
plt.savefig("Incidence_hiv", fontsize=15)
plt.show()


## Exports Growth Rate vs. GDP Growth Rate
fig, ax = plt.subplots(figsize=(8,8))
plt.scatter(x = 'exports_pct_gdp',
            y = 'gdp_growth_pct',
            alpha = 0.7,
            color = 'Orange',
            data = SA_final,
            s= 200)

plt.title('Southern Africa GDP', fontsize=15)
plt.xlabel('Exports Growth Rate', fontsize=15)
plt.ylabel('GDP Growth Rate', fontsize=15)
plt.grid(False)
plt.tight_layout()
plt.savefig("SA Exports GDP Stats")
plt.show()


## Internet Usage Percentage vs. Child Mortality Rate
fig, ax = plt.subplots(figsize=(8,8))
plt.scatter(x = 'internet_usage_pct',
            y = 'child_mortality_per_1k',
            alpha = 0.7,
            color = 'grey',
            data = global_final,
            )

plt.scatter(x = 'internet_usage_pct',
            y = 'child_mortality_per_1k',
            alpha = 1,
            color = 'red',
            data = SA_final,
            )

plt.title('Global Data vs. Southern Africa', fontsize=15)
plt.xlabel('Internet_usage_pct', fontsize=15)
plt.ylabel('Child Mortality per 1k', fontsize=15)
plt.grid(False)
plt.tight_layout()
plt.savefig("Child vs. internet")
plt.show()


## Agriculture Employment Percentage vs. Child Mortality Rate
fig, ax = plt.subplots(figsize=(8,8))
plt.scatter(x = 'pct_agriculture_employment',
            y = 'child_mortality_per_1k',
            alpha = 0.7,
            color = 'grey',
            data = global_final,
            )


plt.scatter(x = 'pct_agriculture_employment',
            y = 'child_mortality_per_1k',
            alpha = 1,
            color = 'red',
            data = SA_final,
            )

plt.title('Global Data vs. Southern Africa', fontsize=15)
plt.xlabel('Agriculture Employment', fontsize=15)
plt.ylabel('Child Mortality per 1k', fontsize=15)
plt.grid(False)
plt.tight_layout()
plt.savefig("Child vs. Agriculture")
plt.show()

        
