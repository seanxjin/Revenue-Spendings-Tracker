'''
title: revenue calculator
author: Sean Jin
date-created: 2022-12-26
'''
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
    ENTRY = input("Entry (A brief word regarding the context of the revenue): ")
    YEAR = input("Year (Integer): ")
    YEAR = _checkInt(YEAR)
    CATEGORY = input("Category (Donation, Payment, Fee, or other): ")
    TRANSACTION = input("Transaction (Type of transaction): ")
    AMOUNT = input("Amount (Total gained): ")
    AMOUNT = _checkFloat(AMOUNT)
    REV = [ENTRY, YEAR, CATEGORY, TRANSACTION, AMOUNT]
    return REV
def askRevYr():
    """
    Asks the year from the user, and uses that info to query the database
    :return: int
    """
    print("Input the year of the data:")
    YR = input("> ")
    try:
        YR = int(YR)
    except ValueError:
        print("Please input a valid number")
        return askRevYr()
    return YR
### PROCESSING
def _checkInt(NUM):
    """
    A recursive function that checks the added input is an int
    :param: NUM: str
    :return: int
    """
    try:
        NUM = int(NUM)
        return NUM
    except ValueError:
        print("Please enter a possible value")
        NEW_NUM = input("> ")
        return _checkInt(NEW_NUM)
def _checkFloat(NUM):
    """
    A recursive function that checks the added input is a float
    :param NUM: str
    :return: float
    """
    try:
        NUM = float(NUM)
    except ValueError:
        print("Please enter a possible value")
        NEW_NUM = input("> ")
        return _checkFloat(NEW_NUM)
    return NUM
### OUTPUTS
def graphRev(GRAPH):
    """
    Graphs all the current information using matplotlib
    :param GRAPH: 2d array
    :return: none
    """
    X = []
    Y = []
    print(GRAPH)
    for t in range(len(GRAPH)):
        X.append(GRAPH[t][0])
        Y.append(GRAPH[t][1])
    plt.figure(figsize=(9, 6))
    plt.ylabel("Total Revenue")
    plt.xlabel("Year")
    plt.suptitle('Total Revenue Yearly')
    plt.plot(X, Y,"r")
    plt.show()
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



