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
### PROCESSING
def getRevenue(FILENAME):
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
                entry TEXT,
                category TEXT,
                trans_action TEXT NOT NULL,
                amount REAL NOT NULL
            )
    ;""")
    for i in range(1, len(REVENUE)):
        CURSOR.execute("""
            INSERT INTO
                revenue (
                    entry,
                    category,
                    trans_action,
                    amount
                )
            VALUES (
                ?, ?, ?, ?
            )
        ;""", REVENUE[i])
    CONNECTION.commit()
def comfirmPassword(ASK, PASSWORD):
    """
    Comfirms the password the user has imported
    :param ASK: str
    :return: none
    """
    if ASK == PASSWORD:
        return 1
    else:
        pass
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
    if FIRST_RUN:
        REVENUE = getRevenue("Revenue - Sheet1.csv")
        print(REVENUE)
        setupRevenue(REVENUE)
        PASSWORD = storePass()
    while START == 0:
        CHOICE = choiceLoginOrUpdate()
        if CHOICE == 1:
            ASK = askPassword()
            START = comfirmPassword(ASK, PASSWORD)
        if CHOICE == 2:
            ASK = askPassword()
            PASSWORD = setNewPassword(ASK, PASSWORD)

