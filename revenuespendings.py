'''
title: Revenue vs Spendings
author: Sean Jin
date-created:2022-12-30
'''



### INPUTS
def askChoice():
    """
    Asks the user what they want to calculate for the revenue vs spendings
    :return: int
    """
    print("""Please choose a integer
    1. Find Profits in a specific year
    2. Graph revenue v.s spendings
    3. Back
    """)
    CHOICE = input("> ")
    try:
        CHOICE = int(CHOICE)
    except ValueError:
        print("Please enter a valid number")
        return askChoice()
    if CHOICE > 0 and CHOICE < 4:
        return CHOICE
    else:
        print("Please enter a valid number")
        return askChoice()
def askYr():
    """
    Asks the user the year they want to calculate
    :return: int
    """
    YEAR = input("Year: ")
    try:
        YEAR = int(YEAR)
    except ValueError:
        print("Please enter a number")
        return askYr()
    return YEAR
### OUTPUTS
def displayProfit(ANSWER):
    """
    Displays the output of the total revenue - total spendings in a given year
    :param: ANSWER: float
    :return: none
    """
    if ANSWER == None:
        print("There is no information in revenue or spendings for the current year.")
    else:
        print(f"The profit is {ANSWER}")