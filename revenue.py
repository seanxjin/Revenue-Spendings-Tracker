'''
title: revenue calculator
author: Sean Jin
date-created: 2022-12-26
'''
import sqlite3
import matplotlib.pyplot as plt
from tabulate import tabulate
### INPUTS
def askOption():
    """
    Asks the user which of the following calculations they want to do for revenue
    :return: int
    """
    print("""Please Choose a Integer
    1. Add new data
    2. Update data
    3. Delete existing data
    4. Search for a dataset
    5. Graphing
    6. Back
    """)
    CHOICE = input("> ")
    try:
        CHOICE = int(CHOICE)
    except ValueError:
        print("Please enter a valid value")
        return askOption()
    if CHOICE > 0 and CHOICE < 7:
        return CHOICE
    else:
        print("Please enter a valid value")
        return askOption()
def askRevData():
    """
    Asks the user for the revenue data that is about to be inputted
    :return: Array
    """
    ENTRY = input("Entry: ")
    YEAR = input("Year: ")
    CATEGORY = input("Category: ")
    TRANSACTION = input("Transaction: ")
    AMOUNT = input("Amount: ")
    try:
        YEAR = int(YEAR)
        AMOUNT = float(AMOUNT)
    except:
        print("Please enter valid values")
        return askRevData()
    REV = [ENTRY, YEAR, CATEGORY, TRANSACTION, AMOUNT]
    return REV
def askRevYr():
    """
    Asks the year from the user, and uses that info to query the database
    :return: int
    """
    print("Input Year:")
    YR = input("> ")
    try:
        YR = int(YR)
    except ValueError:
        print("Please input a valid number")
        return askRevYr()
    return YR
### PROCESSING

### OUTPUTS


def displayqueryRev(QUERYINFO):
    """
    Displays the info from the year the user has inputted
    :param QUERYINFO: 2d array
    :return: none
    """
    HEADER = ["id", "Entry", "Year", "Category", "Transaction", "Amount"]
    if QUERYINFO == []:
        print("There is no existing information in this year")
    else:
        print(f"""Available Info
{tabulate(QUERYINFO,HEADER,tablefmt="fancy_outline" )}""")
        if input("To proceed, press any button") == "r":
            pass
        else:
            pass
# --- VARIABLES --- #



if __name__ == "__main__":
    displayrevenue()