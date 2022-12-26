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



### PROCESSING


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
            ;""").fetchall()
    for i in range(1,4):
        DISPLAY.append(REVENUE[len(REVENUE) - i])
    print(tabulate(DISPLAY,HEADER, tablefmt="fancy_outline", floatfmt=".2f"))
if __name__ == "__main__":
    displayrevenue()