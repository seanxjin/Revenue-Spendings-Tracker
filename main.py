'''
title: Financial Database Calculator
author: Sean Jin
date-created: 2022-12-14
'''

import sqlite3
import pathlib
import flask


# --- VARIABLES --- #
START = 0
DATABASE_FILE = "Finance.db"
FIRST_RUN = True
if (pathlib.Path.cwd() / DATABASE_FILE).exists():
    FIRST_RUN = False
CONNECTION = sqlite3.connect(DATABASE_FILE)
CURSOR = CONNECTION.cursor()
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
    print("Password:")
    ASK = input("> ")
    return ASK
### PROCESSING
def comfirmPassword(ASK):
    """
    Comfirms the password the user has imported
    :param ASK: str
    :return: none
    """
    global PASSWORD
    if ASK == PASSWORD:
        return 1
    else:
        pass
def setNewPassword(ASK):
    """
    Set new password
    :param ASK: str
    :return: str
    """
    global PASSWORD
    if ASK == PASSWORD:
        NEWPASSWORD = input("New password: ")
        PASSWORD = NEWPASSWORD
        return PASSWORD
    else:

### OUTPUTS




if __name__ == "__main__":
    if FIRST_RUN:

        while START == 0:
            CHOICE = choiceLoginOrUpdate()
            if CHOICE == 1:
                ASK = askPassword()
                START = comfirmPassword(ASK)
            if CHOICE == 2:
                ASK = askPassword()

