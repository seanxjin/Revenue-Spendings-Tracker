'''
title: revenue calculator
author: Sean Jin
date-created: 2022-12-26
'''
import sqlite3
import matplotlib
from tabulate import tabulate

# --- VARIABLES --- #
DATABASE_FILE = "Finance.db"
CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()
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
    """)
    CHOICE = input("> ")
    try:
        CHOICE = int(CHOICE)
    except ValueError:
        print("Please enter a valid value")
        return askOption()
    if CHOICE > 0 and CHOICE < 6:
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
def askRevId():
    """
    Displays all revenue data to the user and lets the user choose a primary key to update
    :return: int -- > Primary Key
    """
    INFO = CURSOR.execute("""
        SELECT
            id,
            Entry,
            Year
        FROM
            revenue
        ORDER BY
            Year DESC
    ;""").fetchall()
    HEADER = ["id", "Entry", "Year"]
    print("Please select a id")
    print(tabulate(INFO,HEADER,tablefmt="fancy_outline"))
    CHOICE = input("> ")
    ID = []
    if CHOICE.isnumeric():
        CHOICE = int(CHOICE)
    else:
        print("Please enter a number")
        return askRevId()
    for i in range(len(INFO)):
        ID.append(INFO[i][0])
    if CHOICE not in ID:
        print("Please enter a possible number")
        return askRevId()
    else:
        return CHOICE
### PROCESSING
def updateRev(ID):
    """
    Updates the info on the revenue
    :param INFO: int
    :return: none
    """
    global CURSOR, CONNECTION
    # INPUTS
    INFO = CURSOR.execute("""
        SELECT
            Entry,
            Year,
            Category,
            Trans_action,
            Amount
        FROM
            revenue
        WHERE
            id = ?
    ;""",[ID]).fetchone()
    print("Leave field blank for no changes")
    ENTRY = input(f"Entry: ({INFO[0]}) ")
    YEAR = input(f"Year: ({INFO[1]}) ")
    CATEGORY = input(f"Category: ({INFO[2]}) ")
    TRANSACTION = input(f"Transaction: ({INFO[3]}) ")
    AMOUNT = input(f"Amount: ({INFO[4]}) ")
    NEW = [ENTRY, YEAR, CATEGORY, TRANSACTION, AMOUNT]
    for i in range(len(NEW)):
        if NEW[i] == "":
            NEW[i] = INFO[i]
    try:
        NEW[1] = int(NEW[1])
        NEW[4] = float(NEW[4])
    except:
        print("Please enter valid values")
        return updateRev(ID)
    # PROCESSING
    NEW.append(ID)
    CURSOR.execute("""
        UPDATE
            revenue
        SET
            Entry = ?,
            Year = ?,
            Category = ?,
            Trans_action = ?,
            Amount = ?
        WHERE
            id = ?
    ;""", NEW)
    CONNECTION.commit()
    # OUTPUTS
    print(f"{NEW[5]} was successfully updated!")
def addRevData(INFO):
    """
    Adds the revenue data into the table in sequel
    :param INFO: array
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
        INSERT INTO
            revenue (
                Entry,
                Year,
                Category,
                Trans_action,
                Amount
                )
        VALUES (
            ?, ?, ?, ?, ?
            )
    ;""", INFO)
    CONNECTION.commit()
    print("Data successfully added!")
### OUTPUTS

def displayrevenue():
    """
    Displays the recent 3 inputs of revenue in the table of revenues
    :return: none
    """
    global CURSOR, CONNECTION
    HEADER = ["id", "Entry","Year","Category","Transaction", "Amount"]
    DISPLAY = []
    REVENUE = CURSOR.execute("""
                SELECT 
                    *
                FROM 
                    revenue
                ORDER BY 
                    Year ASC
            ;""").fetchall()
    for i in range(1,4):
        DISPLAY.append(REVENUE[len(REVENUE) - i])
    print("Recent Transactions")
    print(tabulate(DISPLAY,HEADER, tablefmt="fancy_outline", floatfmt=".2f"))
if __name__ == "__main__":
    displayrevenue()