'''
title: Financial Database Calculator
author: Sean Jin
date-created: 2022-12-14
'''

import sqlite3
import pathlib
import flask



### INPUTS
def choiceLoginOrUpdate():
    """
    Asks user for choice of login into the program, or update a password.
    :return: int
    """
    print("""
    Please select a integer
    1. Login
    2. Update Password
    """)
    CHOICE = input("> ")
    try:
        CHOICE = int(CHOICE)
    except ValueError:
        return choiceLoginOrUpdate()
    if CHOICE == 1 or CHOICE == 2:
        return CHOICE
    else:
        return choiceLoginOrUpdate()
def askPassword():
    """
    Asks for the password. The password is preset.
    :return: str
    """
    print("Current Password:")
    ASK = input("> ")
    return ASK
def storePass():
    """
    Asks the User for the password initially
    :return: str
    """
    print("""
    Set Password: 
    """)
    PASSWORD = input("> ")
    return PASSWORD
def setNewPassword(ASK, PASSWORD):
    """
    Set new password
    :param ASK: str
    :return: str
    """
    if ASK == PASSWORD:
        NEWPASSWORD = input("New password: ")
        PASSWORD = NEWPASSWORD
        return PASSWORD
    else:
        print("Password is incorrect")
### PROCESSING
def getValues(FILENAME):
    """
    Extracts contents of file and put it into 2d array
    :param FILENAME: str
    :return: 2d array
    """
    FILE = open(FILENAME,'r', encoding='utf-8')
    TEXT_LIST = FILE.readlines()
    FILE.close()
    for i in range(len(TEXT_LIST)):
        if TEXT_LIST[i][-1] == "\n":
            TEXT_LIST[i] = TEXT_LIST[i][:-1]
        TEXT_LIST[i] = TEXT_LIST[i].split(',')
        for j in range(len(TEXT_LIST[i])):
            try:
                TEXT_LIST[i][j] = float(TEXT_LIST[i][j])
            except ValueError:
                pass
    return TEXT_LIST
def setupRevenue(REVENUE):
    """
    Sets up the tables of revenue
    :param REVENUE: 2d array
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
        CREATE TABLE
            revenue (
                id INTEGER PRIMARY KEY,
                Entry TEXT,
                Year INTEGER NOT NULL,
                Category TEXT,
                Trans_action TEXT NOT NULL,
                Amount REAL NOT NULL
            )
    ;""")
    for i in range(1, len(REVENUE)):
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
        ;""", REVENUE[i])
    CONNECTION.commit()
def setupSpendings(SPENDINGS):
    """
    Sets up the tables of spendings
    :param SPENDINGS: 2d array
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
        CREATE TABLE
            spendings (
                id INTEGER PRIMARY KEY,
                Entry TEXT,
                Year INTEGER NOT NULL,
                Trans_action TEXT NOT NULL,
                Category TEXT,
                Amount REAL NOT NULL,
                GST REAL NOT NULL
            )
    ;""")
    for i in range(1, len(SPENDINGS)):
        CURSOR.execute("""
            INSERT INTO
                spendings (
                    Entry,
                    Year,
                    Trans_action,
                    Category,
                    Amount,
                    GST
                )
            VALUES (
                ?, ?, ?, ?, ?, ?
            )
        ;""", SPENDINGS[i])
    CONNECTION.commit()
def confirmPassword(ASK, PASSWORD):
    """
    Confirms the password the user has imported
    :param ASK: str
    :return: none
    """
    if ASK == PASSWORD:
        return 1
    else:
        print("Password is incorrect")
def setupRevAndSpend(INFO):
    """
    Sets up the table of revenue vs spendings
    :param INFO: 2d array
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
        CREATE TABLE
            profit (
                id INTEGER PRIMARY KEY,
                Year INTEGER NOT NULL,
                Tot_Spend REAL NOT NULL,
                Tot_Revenue REAL NOT NULL,
                Tot_Profit REAL NOT NULL,
                Amount_Left 
    ;""")
### OUTPUTS

# --- VARIABLES --- #
START = 0
DATABASE_FILE = "Finance.db"
FIRST_RUN = True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False
CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()



if __name__ == "__main__":
    REVENUE = getValues("Revenue - Sheet1.csv")
    print(REVENUE)
    setupRevenue(REVENUE)
    SPENDINGS = getValues("Spendings - Sheet1.csv")
    setupSpendings(SPENDINGS)
    print(SPENDINGS)
    REVENUEVSSPENDINGS = getValues("Revenue vs Spendings - Sheet1.csv")
    setupRevAndSpend(REVENUEVSSPENDINGS)
    print(REVENUEVSSPENDINGS)
    PASSWORD = storePass()
    while START == 0:
        CHOICE = choiceLoginOrUpdate()
        if CHOICE == 1:
            ASK = askPassword()
            START = confirmPassword(ASK, PASSWORD)
        if CHOICE == 2:
            ASK = askPassword()
            PASSWORD = setNewPassword(ASK, PASSWORD)

