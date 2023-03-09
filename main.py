'''
title: Financial Database Calculator
author: Sean Jin
date-created: 2022-12-14
'''
import sqlite3
import pathlib
import matplotlib.pyplot as plt
from tabulate import tabulate
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
### INPUTS
def choiceLoginOrUpdate():
    """
    Asks user for choice of login into the program, update a password, or exit.
    :return: int
    """
    print("""
    Please select one of the options
    1. Login
    2. Update Password
    3. Exit
    """)
    CHOICE = input("> ")
    try:
        CHOICE = int(CHOICE)
    except ValueError:
        return choiceLoginOrUpdate()
    if CHOICE == 1 or CHOICE == 2 or CHOICE == 3:
        return CHOICE
    else:
        return choiceLoginOrUpdate()
def askPassword():
    """
    Asks for the password.
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
    Please set a password for the Finance Calculator
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
    Welcome to the Financial Calculator, please select an option from below
        
    1. Revenue 
    2. Spending
    3. Revenue vs Spending
    4. Exit
    """)
    CHOICE = input("> ")
    try:
        CHOICE = int(CHOICE)
    except ValueError:
        print("Please input possible integer")
        return askCalculation()
    if CHOICE == 1 or CHOICE == 2 or CHOICE == 3 or CHOICE == 4:
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
    ENTRY = input("Entry/Context: ")
    YEAR = input("Year: ")
    YEAR = checkInt(YEAR)
    CATEGORY = input("Category Payment/Other: ")
    TRANSACTION = input("Transaction: ")
    checkTransaction(TRANSACTION)
    AMOUNT = input("Amount: ")
    AMOUNT = checkFloat(AMOUNT)

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
    HEADER = ["id", "Entry", "Year","Amount"]
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
def askSpendData():
    """
    Asks the user for the information they want to add to the spendings database
    :return: array
    """
    ENTRY = input("Entry (A brief word regarding the context of the revenue): ")
    YEAR = input("Year (Integer): ")
    YEAR = checkInt(YEAR)
    TRANSACTION = input("Transaction (Type of transaction): ")
    checkTransaction(TRANSACTION)
    CATEGORY = input("Category (Donation, Payment, Fee, or other): ")
    AMOUNT = input("Amount (Amount lost before taxes): ")
    AMOUNT = checkFloat(AMOUNT)
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
# ---- REVENUE V.S SPENDINGS INPUTS ---- #
def askChoice():
    """
    Asks the user what they want to calculate for the revenue vs spendings
    :return: int
    """
    print("""Please select a calculation
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
def checkTransaction(NUM):
    """
    A recursive function that checks if the transaction input is null, and if it is, the function will ask for a proper input.
    :param NUM: str
    :return: str
    """
    if NUM == "":
        print("Type of transaction must be identified, please fill out this area")
        NEW_TRANSACTION = input("> ")
        return checkTransaction((NEW_TRANSACTION))
    else:
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
    Displays all current data for revenue, and user will input new information in the place of the chosen revenue spot, and then the system will update.
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
    Configures the data for revenue, finds the different years, and finds the total from each year and puts it into an array.
    :return: 2d array
    """
    global CURSOR, CONNECTION
    INFO = CURSOR.execute("""
        SELECT
            Year
        FROM
            revenue
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
    if ENTRY == "":
        ENTRY = INFO[0]
    YEAR = input(f"Year: ({INFO[1]}) ")
    if YEAR == "":
        YEAR = INFO[1]
    try:
        YEAR = int(YEAR)
    except ValueError:
        print("The input for year is not applicable, please enter a valid integer")
        return updateSpend(ID)
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
        return updateSpend(ID)
    NEW = [ENTRY, YEAR, CATEGORY, TRANSACTION, AMOUNT]
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
def getInfoSpend():
    """
    Configures the information for the graph, grabs the total amounts from each year and adds them up.
    :return: list --> array
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
    return X, Y
# ------------- Revenue v.s Spendings PROCESSING--------------#
def findProfits(YR):
    """
    Finds the profits of a specific year by adding up all the revenue of that year and all the spendings of that year and subtracting it from each other.
    :param: YR: int
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
        INFOREV = 0
        INFOSPEND = CURSOR.execute("""
            SELECT
                AMOUNT
            FROM 
                spendings
            WHERE
                Year = ?
        ;""", [YR]).fetchall()
        if INFOSPEND == []:
            return None
        else:
            NEWINFOSPEND = []
            for i in range(len(INFOSPEND)):
                for j in range(len(INFOSPEND[i])):
                    NEWINFOSPEND.append(INFOSPEND[i][j])
            NEWINFOSPEND = sum(NEWINFOSPEND)
            ANSWER = INFOREV - NEWINFOSPEND
            ANSWER = round(ANSWER, 2)
            return ANSWER
    else:
        INFOSPEND = CURSOR.execute("""
                SELECT
                    spendings.Amount,
                    spendings.GST
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
        NEWINFOREV = []
        for i in range(len(INFOREV)):
            NEWINFOREV.append(INFOREV[i][0])
        NEWINFOREV = sum(NEWINFOREV)
        if INFOSPEND == []:
            NEWINFOSPEND = 0
        else:
            NEWINFOSPEND = []
            NUM = int(len(INFOSPEND)/len(REVENUENUMBER))
            for i in range(NUM):
                for j in range(2):
                    NEWINFOSPEND.append(INFOSPEND[i][j])
            NEWINFOSPEND = sum(NEWINFOSPEND)
        ANSWER = NEWINFOREV - NEWINFOSPEND
        ANSWER = round(ANSWER, 2)
        return ANSWER
def getInfoAll():
    """
    Gets the info from all the different years and find the total amount from each specific year in both revenue and spending.
    :return: array
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
               ;""", [NEWINFO[i]]).fetchall()
        NEWTOTAL = []
        for l in range((len(TOTAL))):
            NEWTOTAL.append(TOTAL[l][0])
        NEWTOTAL = sum(NEWTOTAL)
        GRAPH.append([NEWINFO[i], NEWTOTAL])
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
                ;""", [NEWINFOREV[i]]).fetchall()
        NEWTOTALREV = []
        for l in range((len(TOTALREV))):
            NEWTOTALREV.append(TOTALREV[l][0])
        NEWTOTALREV = sum(NEWTOTALREV)
        GRAPHREV.append([NEWINFOREV[i], NEWTOTALREV])
    return GRAPH, GRAPHREV
def displayAllgraph(GRAPHSPEND, GRAPHREV):
    """
    Displays both the graph of the spendings and revenue
    :param: GRAPH: array
    :return: none
    """
    X = []
    Y = []
    for t in range(len(GRAPHSPEND)):
        X.append(GRAPHSPEND[t][0])
        Y.append(GRAPHSPEND[t][1])
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
def graphRev(GRAPH):
    """
    Graphs all the current information using matplotlib
    :param GRAPH: 2d array
    :return: none
    """
    X = []
    Y = []
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
def graphSpend(X, Y):
    """
    Graphs the information of the spendings table
    :param: X: array
    :param Y: array
    :return: none
    """
    plt.figure(figsize=(9, 6))
    plt.ylabel("Total Spendings")
    plt.xlabel("Year")
    plt.suptitle('Total Spendings Yearly')
    plt.plot(X, Y,"r")
    plt.show()
# ------------ REVENUE V.S SPENDINGS OUTPUTS -------- #
def displayProfit(ANSWER):
    """
    Displays the output of the total revenue - total spendings in a given year
    :param: ANSWER: float
    :return: none
    """
    if ANSWER == None:
        print("There is no information in revenue or spendings for the current year.")
    else:
        print(f"The profit is ${ANSWER}")
# -------------------------- MAIN PROGRAM CODE --------------------------- #
if __name__ == "__main__":
# Setup Tables/Create a new password
    if FIRST_RUN:
        REVENUE = getValues("Revenue - Sheet1.csv")
        setupRevenue(REVENUE)
        SPENDINGS = getValues("Spendings - Sheet1.csv")
        setupSpendings(SPENDINGS)
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
        if CHOICE == 3:
            exit()
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
                REVID = askRevId()
                # INPUT/PROCESSING
                updateRev(REVID)
                # OUTPUTS
                print("Information successfully updated!")
            if OPTION == 3:
                # INPUT
                REVID = askRevId()
                # PROCESSING
                deleteRev(REVID)
                # OUTPUTS
                print(f"{REVID} successfully deleted!")
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
                # INPUT/PROCESSING
                updateSpend(SPENDID)
                # OUTPUT
                print("Information successfully updated!")
            if OPTION == 3:
                # INPUT
                SPENDID = askSpendID()
                # PROCESSING
                deleteSpend(SPENDID)
                # OUTPUT
                print(f"{SPENDID} successfully deleted!")
            if OPTION == 4:
                # INPUT
                YR = askSpendYr()
                # PROCESSING
                QUERYSPENDINFO = querySpend(YR)
                # OUTPUT
                displayquerySpend(QUERYSPENDINFO)
            if OPTION == 5:
                # PROCESSING
                XSPEND, YSPEND = getInfoSpend()
                # OUTPUT
                graphSpend(XSPEND, YSPEND)
            if OPTION == 6:
                pass
        if CALCULATE == 3:
            # INPUT
            DECISION = askChoice()
            if DECISION == 1:
                # INPUT
                YR = askYr()
                # PROCESSING
                ANSWER = findProfits(YR)
                # OUTPUT
                displayProfit(ANSWER)
            if DECISION == 2:
                # PROCESSING
                GRAPHSPEND, GRAPHREV = getInfoAll()
                # OUTPUT
                displayAllgraph(GRAPHSPEND, GRAPHREV)
            if DECISION == 3:
                pass
        if CALCULATE == 4:
            exit()