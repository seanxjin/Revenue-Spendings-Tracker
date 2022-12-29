'''
title: Financial Database Calculator
author: Sean Jin
date-created: 2022-12-14
'''

import sqlite3
import pathlib
import matplotlib.pyplot as plt
from revenue import *
# --- VARIABLES --- #
START = 0
RUN = True
DATABASE_FILE = "Finance.db"
FIRST_RUN = True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False
    CONNECTION = sqlite3.connect(DATABASE_FILE)
    CURSOR = CONNECTION.cursor()
else:
    CONNECTION = sqlite3.connect(DATABASE_FILE)
    CURSOR = CONNECTION.cursor()
START = 0
RUN = True
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
    global CURSOR, CONNECTION
    print("""
    Set Password: 
    """)
    PASSWORD = input("> ")
    CURSOR.execute("""
        CREATE TABLE
            password (
                password TEXT PRIMARY KEY
            )
    ;""")
    CURSOR.execute("""
        INSERT INTO
            password
        VALUES (
            ?
        )
    ;""", [PASSWORD])
    CONNECTION.commit()
def setNewPassword(ASK):
    """
    Set new password
    :param ASK: str
    :return: str
    """
    global CURSOR, CONNECTION
    PASSWORD = CURSOR.execute("""
        SELECT 
            password
        FROM 
            password
    ;""").fetchone()
    PASSWORD = PASSWORD[0]
    if ASK == PASSWORD:
        NEWPASSWORD = input("New password: ")
        CURSOR.execute("""
            UPDATE
                password
            SET
                password = ?
        ;""", [NEWPASSWORD])
        CONNECTION.commit()
    else:
        print("Password is incorrect")
def askCalculation():
    """
    Asks which calculation to do. Revenue, Spendings, or Revenue vs Spendings.
    :return: int
    """
    print("""
    Please Select an Calculation. Input an Integer
    
    1. Revenue 
    2. Spendings
    3. Revenue vs Spendings
    """)
    CHOICE = input("> ")
    try:
        CHOICE = int(CHOICE)
    except ValueError:
        print("Please input possible integer")
        return askCalculation()
    if CHOICE == 1 or CHOICE == 2 or CHOICE == 3:
        return CHOICE
    else:
        print("Please input possible integer")
        return askCalculation()
### PROCESSING
def createGraphs():
    """
    Creates databases for the graphing part of the functions
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
        CREATE TABLE
            revenuegraph (
                Year,
                Amount
            )
    ;""")
    CONNECTION.commit()
    CURSOR.execute("""
        CREATE TABLE 
            spendingsgraph (
                Year,
                Amount
            )
        ;""")
    CONNECTION.commit()
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
def confirmPassword(ASK):
    """
    Confirms the password the user has imported
    :param ASK: str
    :return: none
    """
    global CURSOR
    PASSWORD = CURSOR.execute("""
        SELECT
            password
        FROM 
            password
    ;""").fetchone()
    PASSWORD = PASSWORD[0]
    if ASK == PASSWORD:
        return 1
    else:
        print("Password is incorrect")
        return 0
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
                Amount_Left REAL NOT NULL
                )
    ;""")

    for i in range(1, len(INFO)):
        CURSOR.execute("""
            INSERT INTO
                profit (
                    Year,
                    Tot_Spend,
                    Tot_Revenue,
                    Tot_Profit,
                    Amount_Left
                )
            VALUES (
                ?, ?, ?, ?, ?
                )
        ;""", INFO[i])
    CONNECTION.commit()
### OUTPUTS





if __name__ == "__main__":
    if FIRST_RUN:
        REVENUE = getValues("Revenue - Sheet1.csv")
        print(REVENUE)
        setupRevenue(REVENUE)
        SPENDINGS = getValues("Spendings - Sheet1.csv")
        setupSpendings(SPENDINGS)
        print(SPENDINGS)
        REVENUEVSSPENDINGS = getValues("Revenue vs Spendings - Sheet1.csv")
        setupRevAndSpend(REVENUEVSSPENDINGS)
        print(REVENUEVSSPENDINGS)
        createGraphs()
        storePass()
    while START == 0:
        CHOICE = choiceLoginOrUpdate()
        if CHOICE == 1:
            ASK = askPassword()
            START = confirmPassword(ASK)
        if CHOICE == 2:
            ASK = askPassword()
            PASSWORD = setNewPassword(ASK)
    while RUN:
        CALCULATE = askCalculation()
        if CALCULATE == 1:
            displayrevenue()
            OPTION = askOption()
            if OPTION == 1:
                REVINFO = askRevData()
                addRevData(REVINFO)
            if OPTION == 2:
                ID = askRevId()
                updateRev(ID)
            if OPTION == 3:
                ID = askRevId()
                deleteRev(ID)
            if OPTION == 4:
                YR = askRevYr()
                QUERYINFO = queryRev(YR)
                displayquery(QUERYINFO)
            if OPTION == 5:
                CHOICEGRAPH = askTypeGraph()
                graphRev(CHOICEGRAPH)
        if CALCULATE == 2:
            pass
        if CALCULATE == 3:
            pass
