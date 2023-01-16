'''
title: Financial Database Calculator
author: Sean Jin
date-created: 2022-12-14
'''
import sqlite3
import pathlib
from revenue import *
from spendings import *
from revenuespendings import *
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
# --------- REVENUE INPUTS -------- #
def askRevId():
    """
    Displays all revenue data to the user and lets the user choose a primary key to update
    :return: int -- > Primary Key
    """
    global CURSOR, CONNECTION
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
# ----------- SPENDINGS INPUTS ------------- #
def askSpendID():
    """
    Displays all spendings data to the user and lets the user choose a primary key to update
    :return:
    """
    global CURSOR, CONNECTION
    INFO = CURSOR.execute("""
        SELECT
            id,
            Entry,
            Year,
            Amount
        FROM
            spendings
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
        return askSpendID()
    for i in range(len(INFO)):
        ID.append(INFO[i][0])
    if CHOICE not in ID:
        print("Please enter a possible number")
        return askSpendID()
    else:
        return CHOICE

### PROCESSING
def checkInt(NUM):
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
        return checkInt(NEW_NUM)
def checkFloat(NUM):
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
        return checkFloat(NEW_NUM)
    return NUM
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
def setupRevAndSpend():
    """
    Sets up the table of revenue vs spendings
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
    CONNECTION.commit()
# -------- REVENUE PROCESSING ------------ #

def queryRev(YR):
    """
    Searches for the info in the database that contains that year
    :param YR: int
    :return: 2d array
    """
    global CURSOR, CONNECTION
    QUERY = CURSOR.execute("""
        SELECT
            *
        FROM 
            revenue
        WHERE
            Year = ?
    ;""",[YR]).fetchall()
    return QUERY
def updateRev(ID):
    """
    Updates the info on the revenue
    :param ID: int
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
    if ENTRY == "":
        ENTRY = INFO[0]
    YEAR = input(f"Year: ({INFO[1]}) ")
    if YEAR == "":
        YEAR = INFO[1]
    try:
        YEAR = int(YEAR)
    except ValueError:
        print("The input for year is not applicable, please enter a valid integer")
        return updateRev(ID)
    CATEGORY = input(f"Category: ({INFO[2]}) ")
    if CATEGORY == "":
        CATEGORY = INFO[2]
    TRANSACTION = input(f"Transaction: ({INFO[3]}) ")
    if TRANSACTION == "":
        TRANSACTION = INFO[3]
    AMOUNT = input(f"Amount: ({INFO[4]}) ")
    if AMOUNT == "":
        AMOUNT = INFO[4]
    try:
        AMOUNT = float(AMOUNT)
    except ValueError:
        print("The input for amount is not applicable, please enter a valid float")
        return updateRev(ID)
    NEW = [ENTRY, YEAR, CATEGORY, TRANSACTION, AMOUNT]
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
def deleteRev(ID):
    """
    Deletes the row of data that the user has chosen to delete
    :param ID: int -- > primary key
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
        DELETE FROM 
            revenue
        WHERE
            id = ?
    """, [ID])
    CONNECTION.commit()
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
def configureRev():
    """
    Configures the data for reveneue, finds the different years, and finds the total from each year and puts it into an array.
    :return: 2d array
    """
    global CURSOR, CONNECTION
    INFO = CURSOR.execute("""
        SELECT
            Year
        FROM
            revenue
    ;""").fetchall()
    print(INFO)
    NEWINFO = []
    for k in range(len(INFO)):
        for j in range(len(INFO)):
            if INFO[k][0] == INFO[j][0]:
                if INFO[j][0] in NEWINFO:
                    pass
                else:
                    NEWINFO.append(INFO[j][0])
    GRAPH = []
    for i in range(len(NEWINFO)):
        TOTAL = CURSOR.execute("""
            SELECT
                Amount
            FROM 
                revenue
            WHERE
                Year = ?
            ;""",[NEWINFO[i]]).fetchall()
        NEWTOTAL = []
        for l in range((len(TOTAL))):
            NEWTOTAL.append(TOTAL[l][0])
        NEWTOTAL = sum(NEWTOTAL)
        GRAPH.append([NEWINFO[i], NEWTOTAL])
    return GRAPH
# ----------- SPENDINGS PROCESSING ------------ #
def addSpendData(INFO):
    """
    Adds the data into the spendings table
    :param INFO: array
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
            INSERT INTO
                spendings (
                    Entry,
                    Year,
                    Category,
                    Trans_action,
                    Amount,
                    GST
                    )
            VALUES (
                ?, ?, ?, ?, ?, ?
                )
        ;""", INFO)
    CONNECTION.commit()
def updateSpend(ID):
    """
    Gets the user information and updates the spendings data into the table
    :param ID: int
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
                Amount,
                GST
            FROM
                spendings
            WHERE
                id = ?
        ;""", [ID]).fetchone()
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
    GST = NEW[4] * 0.05
    NEW.append(GST)
    # PROCESSING
    NEW.append(ID)
    CURSOR.execute("""
            UPDATE
                spendings
            SET
                Entry = ?,
                Year = ?,
                Category = ?,
                Trans_action = ?,
                Amount = ?,
                GST = ?
            WHERE
                id = ?
        ;""", NEW)
    CONNECTION.commit()
def deleteSpend(ID):
    """
    Deletes a row of data in the table of spendings
    :param ID: int
    :return: none
    """
    global CURSOR, CONNECTION
    CURSOR.execute("""
            DELETE FROM 
                spendings
            WHERE
                id = ?
        """, [ID])
    CONNECTION.commit()
    print(f"{ID} successfully deleted!")
def querySpend(YR):
    """
    Searches for the data that has the year in it
    :param YR: int
    :return: 2d array
    """
    global CURSOR, CONNECTION
    QUERY = CURSOR.execute("""
            SELECT
                *
            FROM 
                spendings
            WHERE
                Year = ?
        ;""", [YR]).fetchall()
    return QUERY
def graphSpend():
    """
    Graphs the information of the spendings table
    :return: none
    """
    global CURSOR, CONNECTION
    INFO = CURSOR.execute("""
        SELECT
            Year
        FROM
            spendings
    ;""").fetchall()
    NEWINFO = []
    for k in range(len(INFO)):
        for j in range(len(INFO)):
            if INFO[k][0] == INFO[j][0]:
                if INFO[j][0] in NEWINFO:
                    pass
                else:
                    NEWINFO.append(INFO[j][0])
    GRAPH = []
    for i in range(len(NEWINFO)):
        TOTAL = CURSOR.execute("""
            SELECT
                Amount
            FROM 
                spendings
            WHERE
                Year = ?
            ;""",[NEWINFO[i]]).fetchall()
        NEWTOTAL = []
        for l in range((len(TOTAL))):
            NEWTOTAL.append(TOTAL[l][0])
        NEWTOTAL = sum(NEWTOTAL)
        GRAPH.append([NEWINFO[i], NEWTOTAL])
    X = []
    Y = []
    for t in range(len(GRAPH)):
        X.append(GRAPH[t][0])
        Y.append(GRAPH[t][1])
    plt.figure(figsize=(9, 6))
    plt.ylabel("Total Spendings")
    plt.xlabel("Year")
    plt.suptitle('Total Spendings Yearly')
    plt.plot(X, Y,"r")
    plt.show()
# ------------- Revenue v.s Spendings PROCESSING--------------#
def findProfits(YR):
    """
    Finds the profits of a specific year by adding up all the revenue of that year and all the spendings of that year and subtracting it from each other.
    :param YR: int
    :return: int
    """
    global CURSOR, CONNECTION
    INFOREV = CURSOR.execute("""
        SELECT
            Amount
        FROM
            revenue
        WHERE
            Year = ?
    ;""", [YR]).fetchall()
    if INFOREV == []:
        return None
    else:
        NEWINFOREV = []
        for i in range(len(INFOREV)):
            NEWINFOREV.append(INFOREV[i][0])
        NEWINFOREV = sum(NEWINFOREV)
        INFOSPEND = CURSOR.execute("""
            SELECT
                spendings.Amount
            FROM
                revenue
            JOIN
                spendings
            ON
                revenue.Year = spendings.Year
            WHERE
                revenue.Year = ?
        ;""", [YR]).fetchall()
        REVENUENUMBER = CURSOR.execute("""
            SELECT
                Year
            FROM
                revenue
            WHERE
                Year = ?
        ;""", [YR]).fetchall()
        NEWINFOSPEND = []
        NUM = int(len(INFOSPEND)/len(REVENUENUMBER))
        for i in range(NUM):
            NEWINFOSPEND.append(INFOSPEND[i][0])
        NEWINFOSPEND = sum(NEWINFOSPEND)
        ANSWER = NEWINFOREV - NEWINFOSPEND
        return ANSWER
def displayAllgraph():
    """
    Displays both the graph of the spendings and revenue
    :return: none
    """
    global CURSOR, CONNECTION
    INFO = CURSOR.execute("""
        SELECT
            Year
        FROM
            spendings
    ;""").fetchall()
    NEWINFO = []
    for k in range(len(INFO)):
        for j in range(len(INFO)):
            if INFO[k][0] == INFO[j][0]:
                if INFO[j][0] in NEWINFO:
                    pass
                else:
                    NEWINFO.append(INFO[j][0])
    GRAPH = []
    for i in range(len(NEWINFO)):
        TOTAL = CURSOR.execute("""
            SELECT
                Amount
            FROM 
                spendings
            WHERE
                Year = ?
            ;""",[NEWINFO[i]]).fetchall()
        NEWTOTAL = []
        for l in range((len(TOTAL))):
            NEWTOTAL.append(TOTAL[l][0])
        NEWTOTAL = sum(NEWTOTAL)
        GRAPH.append([NEWINFO[i], NEWTOTAL])
    X = []
    Y = []
    for t in range(len(GRAPH)):
        X.append(GRAPH[t][0])
        Y.append(GRAPH[t][1])
    INFOREV = CURSOR.execute("""
        SELECT
            Year
        FROM
            revenue
    ;""").fetchall()
    NEWINFOREV = []
    for k in range(len(INFOREV)):
        for j in range(len(INFOREV)):
            if INFOREV[k][0] == INFOREV[j][0]:
                if INFOREV[j][0] in NEWINFOREV:
                    pass
                else:
                    NEWINFOREV.append(INFOREV[j][0])
    GRAPHREV = []
    for i in range(len(NEWINFOREV)):
        TOTALREV = CURSOR.execute("""
            SELECT
                Amount
            FROM 
                revenue
            WHERE
                Year = ?
            ;""",[NEWINFOREV[i]]).fetchall()
        NEWTOTALREV = []
        for l in range((len(TOTALREV))):
            NEWTOTALREV.append(TOTALREV[l][0])
        NEWTOTALREV = sum(NEWTOTALREV)
        GRAPHREV.append([NEWINFOREV[i], NEWTOTALREV])
    A = []
    B = []
    for t in range(len(GRAPHREV)):
        A.append(GRAPHREV[t][0])
        B.append(GRAPHREV[t][1])
    plt.figure(figsize=(9, 6))
    plt.ylabel("Total Revenue vs Spendings")
    plt.xlabel("Year")
    plt.suptitle('Total Spendings/Revenue Yearly')
    plt.plot(A, B, label = "Revenue")
    plt.plot(X, Y, label = "Spendings")
    plt.legend()
    plt.show()

### OUTPUTS
# --------- REVENUE OUTPUTS ----------- #
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
# --------- SPENDINGS OUTPUTS ----------- #
def displayspendings():
    """
    Displays the 3 recent spendings in the table of spendings
    :return: none
    """
    HEADER = ["id", "Entry","Year","Category","Transaction", "Amount", "GST"]
    DISPLAY = []
    SPENDINGS = CURSOR.execute("""
                SELECT 
                    *
                FROM 
                    spendings
                ORDER BY 
                    Year ASC
            ;""").fetchall()
    for i in range(1,4):
        DISPLAY.append(SPENDINGS[len(SPENDINGS) - i])
    print("Recent Transactions")
    print(tabulate(DISPLAY,HEADER, tablefmt="fancy_outline", floatfmt=".2f"))



# -------------------------- MAIN PROGRAM CODE --------------------------- #
if __name__ == "__main__":
# Setup Tables/Create a new password
    if FIRST_RUN:
        REVENUE = getValues("Revenue - Sheet1.csv")
        setupRevenue(REVENUE)
        SPENDINGS = getValues("Spendings - Sheet1.csv")
        setupSpendings(SPENDINGS)
        setupRevAndSpend()
        storePass()
# Password Checking
    while START == 0:
        # --- INPUTS --- #
        CHOICE = choiceLoginOrUpdate()
        if CHOICE == 1:
            # INPUT
            ASK = askPassword()
            # PROCESSING
            START = confirmPassword(ASK)
        if CHOICE == 2:
            # INPUT
            ASK = askPassword()
            # PROCESSING
            PASSWORD = setNewPassword(ASK)
    while RUN:
        # INPUT
        CALCULATE = askCalculation()
        if CALCULATE == 1:
            # OUTPUT
            displayrevenue()
            # INPUT
            OPTION = askOption()
            if OPTION == 1:
                # INPUT
                REVINFO = askRevData()
                # PROCESSING
                addRevData(REVINFO)
                # OUTPUT
                print("Data successfully added!")
            if OPTION == 2:
                # INPUT
                ID = askRevId()
                # INPUT/PROCESSING/OUTPUT
                updateRev(ID)
            if OPTION == 3:
                # INPUT
                ID = askRevId()
                # PROCESSING
                deleteRev(ID)
                # OUTPUTS
                print(f"{ID} successfully deleted!")
            if OPTION == 4:
                # INPUT
                YR = askRevYr()
                # PROCESSING
                QUERYREVINFO = queryRev(YR)
                # OUTPUT
                displayqueryRev(QUERYREVINFO)
            if OPTION == 5:
                # PROCESSING
                GRAPH = configureRev()
                # OUTPUT
                graphRev(GRAPH)
            if OPTION == 6:
                pass
        if CALCULATE == 2:
            # OUTPUT
            displayspendings()
            # INPUT
            OPTION = askOption()
            if OPTION == 1:
                # INPUT
                SPENDINFO = askSpendData()
                # PROCESSING
                addSpendData(SPENDINFO)
                # OUTPUT
                print("Data successfully added!")
            if OPTION == 2:
                # INPUT
                SPENDID = askSpendID()
                # INPUT/PROCESSING/OUTPUT
                updateSpend(SPENDID)
            if OPTION == 3:
                SPENDID = askSpendID()
                deleteSpend(SPENDID)
            if OPTION == 4:
                YR = askSpendYr()
                QUERYSPENDINFO = querySpend(YR)
                displayquerySpend(QUERYSPENDINFO)
            if OPTION == 5:
                graphSpend()
            if OPTION == 6:
                pass
        if CALCULATE == 3:
            DECISION = askChoice()
            if DECISION == 1:
                YR = askYr()
                ANSWER = findProfits(YR)
                displayProfit(ANSWER)
            if DECISION == 2:
                displayAllgraph()
            if DECISION == 3:
                pass