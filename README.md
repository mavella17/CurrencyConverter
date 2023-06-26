# Currency-API Project for SEO Week 2
![Checkstyle](https://github.com/mavella17/W2_Project/actions/workflows/main.yml/badge.svg)

![Unit Tests](https://github.com/mavella17/W2_Project/actions/workflows/test.yaml/badge.svg)
## Required Libraries:
- SQLAlchemy
- requests
- pandas
No environment variables required
## How To Run:
Simply use ```  python3 capi_main.py ``` in the terminal to run
## How It Works:
**If you are running for the first time, you must use update the database first!**
Runs on a continuous loop.
User is prompted with 4 options:
- "B" to input a base currency and begin a currency exchange lookup
- "U" to update the exchange rate database (should be done at least once daily)
- "V" to view the current exchange rate database
- "L" to list all available currencies and their abbreviations
- "Q" to quit

