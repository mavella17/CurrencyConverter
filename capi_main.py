import requests
import pprint
import pandas as pd
import sqlalchemy as db
from sqlalchemy import delete
from sqlalchemy.sql import text as sa_text



engine = db.create_engine('sqlite:///currency.db')


def buildDB():
    listofCurr = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json'
    currList = requests.get(listofCurr)
    currList = currList.json().keys()
    url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/"
    for currency in currList: 
        r = requests.get(url + currency + ".json")
        rates = r.json()[currency]
        firstColumn = {'Currency':currency}
        firstColumn.update(rates)
        d = pd.DataFrame(firstColumn, index=[0]) 
        d.to_sql('exchange', con=engine, if_exists='append', index=False)
 
def printDB():
    with engine.connect() as connection:
        query_result = connection.execute(db.text("""SELECT * FROM
        exchange;""")).fetchall()
        print(pd.DataFrame(query_result))

def main():
    while True:
        base = input("Enter Your Base Currency, or LIST to view all currencies: ")
        if base.upper() == "LIST":
            listofCurr = 'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies.json'
            currList = requests.get(listofCurr)
            pprint.pprint(currList.json())

        
        

if __name__ == "__main__":
    main()