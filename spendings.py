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
    ENTRY = input("Entry (A brief word regarding the context of the revenue): ")
    YEAR = input("Year (Integer): ")
    YEAR = _checkInt(YEAR)
    TRANSACTION = input("Transaction (Type of transaction): ")
    CATEGORY = input("Category (Donation, Payment, Fee, or other): ")
    AMOUNT = input("Amount (Amount lost before taxes): ")
    AMOUNT = _checkFloat(AMOUNT)
    GST = AMOUNT * 0.05
    SPEND = [ENTRY,YEAR, TRANSACTION, CATEGORY, AMOUNT, GST]
    return SPEND
def askSpendYr():
    """
    Asks for the year of the data the user wants to see
    :return: int
    """
    print("Input the year of the data:")
    YR = input("> ")
    try:
        YR = int(YR)
    except ValueError:
        print("Please input a valid number")
        return askSpendYr()
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