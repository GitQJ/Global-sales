#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:11:05 2024

@author: Quentin JONNEAUX
Student Number: R00274704
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "/Users/Quentin/Desktop/Hdip Data Science and Analytics/Year 1/Semester 1/COMP 8060 - Scientific Programming in Python/Assignment/Project_GlobalSales.csv"

# Q1 - Computing and summarising
def main():
    
    # Opening, reading the data frame, and closing file once program exits
    with open(file_path,"r") as sales_file:
        df = pd.read_csv(sales_file)
    
    # Create UnitProfit variable
    unit_profits = []
    for i in range(0, len(df)):
        profit = (df["Profit"][i]) / (df["Quantity"][i])
        unit_profits.append(profit)
    
    df["UnitProfit"] = unit_profits
    
    # Looping in menu until user decides to exit
    has_exit = False
    while not has_exit:
        display_menu()
        option = input("Please enter the option number: ")
        if option =="1":
            # Print a summary of Dataset
            summarise_data(df)
        elif option =="2":
            # Display sales analysis plots
            analyse_sales(df)
        elif option =="3":
            # Display Shipping cost analysis (Correlation matrix and boxplots)
            analyse_shipping_costs(df)
        elif option =="4":
            # Display Country comparison
            country_comparison(df)
        elif option =="5":
            # Display personal insights
            personal_insight(df)
        elif option =="6":
            # Exit pregram
            exit()
            has_exit = True
        else:
            print("Please choose a valid option\n\n")
            
# Create a function to display menu
def display_menu():
    print("Please select one of the following options:",
          "1.Initial Data Summary",
          "2.Sales Analysis",
          "3.Shipping Cost Analysis",
          "4.Country Comparison for Top Product Categories",
          "5.Personal Insights",
          "6.Exit",
          sep="\n   ")

# Create a function to summarise dataset
def summarise_data(df):
    print("\n---------------------------\n")
    # Print all columns in console
    pd.set_option("display.max.columns", None)
    print("Please find the numeric descriptive statistics of the dataframe:\n")
    # Print summary of numeric variables
    print(df.describe())
    print("\nPlease find the non-numeric descriptive statistics of the dataframe:\n")
    # Print summary of categorical variables
    print(df.describe(exclude=np.number))
    print("\nPlease find the first 5 rows of the dataframe:\n")
    # Print first 5 rows
    print(df.head())
    print("\n---------------------------\n")

# Q2 - Sales analysis
def analyse_sales(df):
    # Slicing df
    small_df = df[["Ship.Date","Profit","Quantity","Sales", "ShipY","ShipM"]]

    # Years lineplots
    ship_year_group = small_df.groupby("ShipY")
    lineplot2(ship_year_group, "Sales", "Profit", "Years")
    lineplot(ship_year_group, "Quantity", "Years")
    
    # Months lineplots
    ship_month_group = small_df.groupby("ShipM")
    lineplot2(ship_month_group, "Sales", "Profit", "Months")
    lineplot(ship_month_group, "Quantity", "Months")
    
    # Year and Months barplots
    barplot2(ship_year_group, "Sales", "Profit")
    barplot2(ship_month_group, "Sales", "Profit")

#############Q3 - Shipping Cost Analysis
def analyse_shipping_costs(df):
    # Create a correlation matrix with numerical data
    corrResults = df.corr(numeric_only=True)
    sns.heatmap(corrResults)
    plt.title("Correlation matrix of numeric data of Global Sales")
    plt.show()
    
    # Create boxplot of Shipping cost against Shipping mode
    small_df = df[["Ship.Mode","Shipping.Cost"]]
    small_df.boxplot(by="Ship.Mode", column =['Shipping.Cost'], showfliers=False)
    plt.title('Shipping.Cost by Ship.Mode boxplots')
    plt.suptitle('')
    plt.ylabel("Shipping Costs")
    plt.show()
    
#############Q4 - Country comparison
def country_comparison(df):
    # Display countries available in data to be more user-friendly
    print("Here are the countries where sales have been recorded")
    country_list = sorted(df["Country"].dropna().unique())
    print(country_list)
    
    # Ask for user input with 2 different countries
    country1 = input("Please entry the name of the first country you would like to compare: ").title()
    country2 = input("Please entry the name of the second country you would like to compare: ").title()
    # Error checking for listed countries
    if country1 not in country_list or country2 not in country_list:
        print("Please enter countries from the list")
    # Error checking for same countries
    elif country1==country2:
        print("Please enter 2 different countries")
    else:
        country1_data = df["Country"]==country1
        country1_df = df[country1_data]
        country1_value_counts = country1_df["Sub.Category"].value_counts()
        country1_value_counts.name = country1
        print(country1_value_counts)
        
        country2_data = df["Country"]==country2
        country2_df = df[country2_data]
        country2_value_counts = country2_df["Sub.Category"].value_counts()
        country2_value_counts.name = country2
        print(country2_value_counts)
        
        countries_value_counts = pd.merge(country1_value_counts, country2_value_counts, right_index=True, left_index=True)
        
        if countries_value_counts.empty:
            print(country1 + " and " +  country2 + " cannot be compared as they do not have common subcategories sold")
        else:
            print(countries_value_counts)
            plt.plot(countries_value_counts)
            plt.legend([country1,country2])
            plt.title(country1 + " and " + country2 + " Subcategory records")
            plt.xticks(rotation = 45)
            plt.xlabel("Subcategories")
            plt.ylabel("Counts")
            plt.show()
    
#############Q5 - Personal Insights
def personal_insight(df):
    
    small_df = df[["Shipping.Cost","Category"]]
    small_df.boxplot(by="Category", column =['Shipping.Cost'], showfliers=False)
    plt.title('Shipping.Cost by Category boxplots')
    plt.suptitle('')
    plt.ylabel("Shipping.Cost")
    plt.show()
    plt.show()
    
    small_df = df[["Shipping.Cost","Quantity","Ship.Mode","Market","Category","Region", "Sales", "Profit", "UnitProfit"]]
    scatter_by_cat(small_df, "Shipping.Cost", "Sales") 
    
    scatter_by_cat(small_df, "Shipping.Cost", "Profit")
    
    scatter_by_cat(small_df, "Shipping.Cost", "UnitProfit")
    
    quantity_group = small_df.groupby("Quantity")
    mean_df = quantity_group.mean()
    plt.plot(mean_df["Shipping.Cost"])
    plt.title("Shipping Costs over Quantities lineplot")
    plt.legend(["Shipping Costs"])
    plt.xlabel("Quantities")
    plt.ylabel("Shipping Costs")
    plt.show()
    
    small_df = df[["Profit","Category"]]
    small_df.boxplot(by="Category", column =['Profit'], showfliers=False)
    plt.title('Profit by Category boxplots')
    plt.suptitle('')
    plt.ylabel("Profit")
    plt.show()


    small_df = df[["UnitProfit","Category"]]
    small_df.boxplot(by="Category", column =['UnitProfit'], showfliers=False)
    plt.title('Unit Profit by Category boxplots')
    plt.suptitle('')
    plt.ylabel("Unit Profit")
    plt.show()
    
    small_df = df[["UnitProfit","Market"]]
    small_df.boxplot(by="Market", column =['UnitProfit'], showfliers=False)
    plt.title('Unit Profit by Market boxplots')
    plt.suptitle('')
    plt.ylabel("Unit Profit")
    plt.show()
    
########### Supporting Functions

# Create a lineplot function for one variable
def lineplot(group,var,lab):
    plt.plot(group.mean()[var])
    plt.xlabel(lab)
    plt.ylabel("Amounts")
    plt.title(var + " over " + lab)
    plt.legend(var)
    plt.show()

# Create a lineplot function for two variables
def lineplot2(group,var1,var2, lab):
    plt.plot(group.mean()[var1])
    plt.plot(group.mean()[var2])
    plt.xlabel(lab)
    plt.ylabel("Amounts")
    plt.title(var1 + " and " + var2 + " over " + lab)
    plt.legend([var1,var2])
    plt.show()

# Create a barplot function for one variable
def barplot(group_to_transpose, var):
    group_to_transpose[var].mean().T.plot(kind="bar",stacked=True)
    plt.title(var + " barplot")
    plt.ylabel("Amounts")
    plt.show()

# Create a barplot function for two variables
def barplot2(group_to_transpose, var1, var2):
    group_to_transpose[var1, var2].mean().T.plot(kind="bar",stacked=True)
    plt.title(var1 + "/" + var2 + " barplot")
    plt.ylabel("Amounts")
    plt.show()

# Create a scatterplot function for two variables
def scatter_by_cat(df, numvar1, numvar2):
    small_df = df[[numvar1,numvar2]].dropna()
    plt.scatter(small_df[numvar1], small_df[numvar2])
    plt.title(numvar1 + " against " + numvar2 + " Scatterplot")
    plt.xlabel(numvar1)
    plt.ylabel(numvar2)
    plt.show()

############# Exiting

def exit():
            print("Thank you for having used our program")
            
############# Running Program

        
main()