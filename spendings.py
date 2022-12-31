'''
Title: Spendings calculator
author: Sean
date-created: 2022-12-30
'''
from tabulate import tabulate
### INPUTS
def askSpendData():
    """
    Asks the user for the information they want to add to the spendings database
    :return: array
    """
    ENTRY = input("Entry: ")
    YEAR = input("Year: ")
    TRANSACTION = input("Transaction: ")
    CATEGORY = input("Category: ")
    AMOUNT = input("Amount: ")
    try:
        YEAR = int(YEAR)
        AMOUNT = float(AMOUNT)
    except ValueError:
        print("Please enter valid values")
        return askSpendData()
    GST = AMOUNT * 0.05
    SPEND = [ENTRY,YEAR, TRANSACTION, CATEGORY, AMOUNT, GST]
    return SPEND
def askSpendYr():
    """
    Asks for the year of the data the user wants to see
    :return: int
    """
    print("Input Year:")
    YR = input("> ")
    try:
        YR = int(YR)
    except ValueError:
        print("Please input a valid number")
        return askSpendYr()
    return YR
### OUTPUTS
def displayquerySpend(QUERYINFO):
    """
    Displays the info from the year the user has inputted
    :param QUERYINFO: 2d array
    :return: none
    """
    HEADER = ["id", "Entry", "Year", "Category", "Transaction", "Amount", "GST"]
    if QUERYINFO == []:
        print("There is no existing information in this year")
    else:
        print(f"""Available Info
{tabulate(QUERYINFO, HEADER, tablefmt="fancy_outline")}""")
        if input("To proceed, press any button") == "r":
            pass
        else:
            pass