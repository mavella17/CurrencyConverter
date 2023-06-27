import requests
import pprint
import pandas as pd
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text
engine = db.create_engine('sqlite:///currency.db')
currencies = None


def updateDB():
    url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
    url += 'currency-api@1/latest/currencies.json'
    currList = requests.get(url).json()
    currList.pop("1inch")
    currList = currList.keys()
    url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
    url += 'currency-api@1/latest/currencies/'
    first = True
    for currency in currList:
        r = requests.get(url + currency + ".json")
        rates = r.json()[currency]
        firstColumn = {'Currency': currency, 'Date Updated': r.json()['date']}
        firstColumn.update(rates)
        firstColumn.pop('1inch')
        d = pd.DataFrame(firstColumn, index=[0])
        if first:
            d.to_sql('exchange', con=engine, if_exists='replace', index=False)
            first = False
        else:
            d.to_sql('exchange', con=engine, if_exists='append', index=False)
    return True


def printDB():
    with engine.connect() as connection:
        query_result = connection.execute(db.text("""SELECT * FROM
        exchange;""")).fetchall()
        print(pd.DataFrame(query_result))
        return True
    return False


def getList():
    url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/'
    url += 'currency-api@1/latest/currencies.json'
    currList = requests.get(url).json()
    currList.pop('1inch')
    pprint.pprint(currList)
    return True


def base_exchange(b=None, e=None, a=None):  # parameters are only for testing
    if not b:
        b = input("What base currency would you like to start with: ").lower()
    else:
        b = b.lower()
    while not checkValidCurrency(b) or b.lower() == 'all':
        b = input("Not a valid currency, please try again: ").lower()
    if not e:
        print("What currency would you like to exchange to?")
        e = input("Input \"ALL\" for conversions in every currency: ").lower()
    else:
        e = e.lower()
    while not checkValidCurrency(e):
        e = input("Not a valid currency, please try again: ").lower()

    if not a and e != 'all':
        while True:
            try:
                a = float(input(f"Enter an amount of {b} to convert to {e}: "))
                break
            except ValueError:
                print("Please only input numbers")
                continue

    if e == 'all':
        sql = "Select * FROM exchange WHERE " + b + " = 1;"
        df = pd.read_sql(sql, con=engine)
        res = df.loc[df['Currency'] == b]
        print(res)
        return res
    else:
        sql = "Select " + e + " FROM exchange WHERE " + b + " = 1;"
        df = pd.read_sql(sql, con=engine).iat[0, 0]
        print(f"{a} {b} converted to {e} would be {a * df} {e}")
        return df * a


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
        print("Input Q to quit")
        print("Input L to list all currencies and their acronyms")
        base = input("Type command here: ")
        base = base.upper()
        if base == "L":
            getList()
        elif base == "Q":
            print("Quitting!")
            break
        elif base == "U":
            updateDB()
            printDB()
        elif base == "V":
            printDB()
        elif base == "B":
            base_exchange()
        else:
            print("Invalid Command, Try Again!")


if __name__ == "__main__":
    main()
