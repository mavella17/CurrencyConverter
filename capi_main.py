import requests
import pprint
import pandas as pd
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.sql import text as sa_text



engine = db.create_engine('sqlite:///currency.db')


def updateDB():
    listofCurr = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json'
    currList = requests.get(listofCurr)
    currList = currList.json().keys()
    url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/"
    first = True
    for currency in currList:
        r = requests.get(url + currency + ".json")
        rates = r.json()[currency]
        firstColumn = {'Currency':currency, 'Date Updated':r.json()['date']}
        firstColumn.update(rates)
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
    listofCurr = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json'
    currList = requests.get(listofCurr)
    pprint.pprint(currList.json())
    return True

def base_exchange():
    base = input("What base currency would you like to start with: ")
    exchange = input("What currency would you like to exchange to: ")
    sql = "Select " + exchange +  " FROM exchange WHERE " + base + " = 1;" 
    df = pd.read_sql(sql, con=engine).iat[0,0]
    print(f"{base} to {exchange} has an exchange rate of: {df} {exchange} for 1 {base}")

def main():
    while True:
        print("---------")
        print("Commands:")
        print("---------")
        print("Input B to input a base currency")
        print("Input U to update the exchange rate database")
        print("Inpuy V to view the exchange rate database")
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