import requests
import pprint
import pandas as pd
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text
engine = db.create_engine('sqlite:///currency.db')
currencies = None


# Updates the database with the latest currencies. Should be run once daily
def updateDB():
    url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
    url += 'currency-api@1/latest/currencies.json'
    currList = requests.get(url).json()
    currList.pop("1inch")  # excluded because of several issues
    currList = currList.keys()
    url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
    url += 'currency-api@1/latest/currencies/'
    first = True
    for currency in currList:
        r = requests.get(url + currency + ".json")
        rates = r.json()[currency]
        firstColumn = {'Currency': currency, 'Date Updated': r.json()['date']}
        firstColumn.update(rates)
        firstColumn.pop('1inch')  # not liked by sql for some reason
        d = pd.DataFrame(firstColumn, index=[0])
        if first:
            d.to_sql('exchange', con=engine, if_exists='replace', index=False)
            first = False
        else:
            d.to_sql('exchange', con=engine, if_exists='append', index=False)
    return True


# Prints the current database
def printDB():
    with engine.connect() as connection:
        query_result = connection.execute(db.text("""SELECT * FROM
        exchange;""")).fetchall()
        print(pd.DataFrame(query_result))
        return True


# Gets a list of active currencies
def getList():
    url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
    url += 'currency-api@1/latest/currencies.json'
    currList = requests.get(url).json()
    currList.pop('1inch')
    pprint.pprint(currList)
    return True


# Main code, allows currency lookups,convert base currency to exchange currency
def base_exchange(baseCurr=None, exCurr=None, amount=None):
    if not baseCurr:
        baseCurr = input("Input base currency: ").lower()
    else:
        baseCurr = baseCurr.lower()
    while not checkValidCurrency(baseCurr) or baseCurr.lower() == 'all':
        baseCurr = input("Not a valid currency, please try again: ").lower()
    if not exCurr:
        print("What currency would you like to exchange to?")
        exCurr = input("Input \"ALL\" for all excahnge rates: ").lower()
    else:
        exCurr = exCurr.lower()
    while not checkValidCurrency(exCurr):
        exCurr = input("Not a valid currency, please try again: ").lower()

    if not amount and exCurr != 'all':
        while True:
            try:
                amount = float(input(f"Enter an amount of {baseCurr}: "))
                break
            except ValueError:
                print("Please only input numbers")
                continue

    if exCurr == 'all':
        sql = "Select * FROM exchange WHERE " + baseCurr + " = 1;"
        df = pd.read_sql(sql, con=engine)
        res = df.loc[df['Currency'] == baseCurr]
        res = res.transpose()
        range = 17
        acceptable_inputs = ["yes", "y", "no", "n"]
        print(res[0:range])
        while not(range > len(res) - 15):
            range += 15
            ans = input("Print next 15 rows? (Yes/No): ").lower()
            while ans not in acceptable_inputs:
                ans = input("Please enter valid input (Yes/No): ").lower()
            if ans in acceptable_inputs[0:2]:
                print(res[range - 15: range])
            elif ans in acceptable_inputs[2:4]:
                break
        if len(res) - 15 < range:
            ans = input("Print remaining rows? (Yes/No): ").lower()
            while ans not in acceptable_inputs:
                ans = input("Please enter valid input (yes or no): ").lower()
            if ans in acceptable_inputs[0:2]:
                print(res[range:])
        return True
    else:
        sql = "Select " + exCurr + " FROM exchange WHERE " + baseCurr + " = 1;"
        rate = pd.read_sql(sql, con=engine).iat[0, 0]
        res = rate * amount
        print(f"{amount} {baseCurr} converted to {exCurr} is {res} {exCurr}")
        return rate * amount


# determines if currency acronym is valid
def checkValidCurrency(curr):
    global currencies
    if not currencies:
        url = 'https://cdn.jsdelivr.net/gh/fawazahm'
        url += 'ed0/currency-api@1/latest/currencies.json'
        currencies = requests.get(url).json()
        currencies.pop('1inch')
    curr = curr.lower()
    if curr in currencies or curr.upper() == 'ALL':
        return True
    return False


def main():
    while True:
        print("---------")
        print("Commands:")
        print("---------")
        print("Input B to input a base currency")
        print("Input U to update the exchange rate database")
        print("Input V to view the exchange rate database")
        print("Input L to list all currencies and their acronyms")
        print("Input Q to quit")
        base = input("Type command here: ")
        base = base.upper()
        match base:
            case "L":
                getList()
            case "Q":
                print("Quitting!")
                break
            case "U":
                updateDB()
                printDB()
            case "V":
                printDB()
            case "B":
                base_exchange()
            case _:
                print("Invalid Command, Try Again!")


if __name__ == "__main__":
    main()
