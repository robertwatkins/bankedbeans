# bankedbeans
A personal accounting system to import bank account transactions and automatically categorize spending based on customized rules.


## What is this?

This system is a custom accounting system with a few basic goals:
 - Import banking transactions from all sources for business and personal use
 - Generate end of year expenses for business purposes by business entity
 - Automate as much as possible the categorization of transactions
 - Allow for custom memo entries for transactions to aid in automatically categorizing transactions.

## Prerequisites
 - Python 3.x should be installed (you can check by typing ```python3 --version``` in a terminal session)
 - SQLAlchemy Library for python (type ```pip3 install SQLAlchemy``` in terminal)
 - CherryPy Library for python (type ```pip3 install CherryPy``` in terminal)
 - Also install pandas by typing ```pip3 install pandas``` in terminal
 - You'll need to create a database once (type ```sqlite3 accounting < db_scripts/new_accounting_db.sql``` in a terminal session at the root of this project)
 
 
## Starting up 
Type the following in a terminal window.

``
python3 app.py
``

Open the URL [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

## Usage
The site has basic functionality
 - Update memo fields for transactions with no category
 - View category summary by Account
 - View category details by Account
 
## Using Demo Data
Copy the demo data to the 'importfiles' folder by typing 
```
cp importfiles/processed/personal_account_sample.csv importfiles
```

## Importing new data
This is a work in progress
- the data files must have the following columns 'Check Number,Date,Description,Transaction Type,Debit Amount,Credit Amount,Balance'
- export the data files in csv format for each account
- put the files in the 'importfiles' directory
- run from the terminal 'python3 process.py'
- this will process each of the data files and import the transactions to the db

# Reviewing the categorization rules
The file 'categorymapping.json' describes how the transactions are categorized. 

Each categorization is for 'Peronal', 'Business' or 'Any' type of account.

The categorization is based on the 'description' and 'memo' fields based on text matching.

## Troubleshooting
| Issue                           | Resolution                                 |
| ------------------------------- | ------------------------------------------ |
| Errors loading data from bank   | Check that there are no overlapping dates  | 
| Data isn't categorized properly | `It's possible there is a conflict between`| 
|                                 | `rules. Check the rule being applied and ` |
|                                 | `adjust the 'categorymapping.json' file `  |

## Architecture
The data store is in a local sqlite db. The structure is in the 'transactions.sql.txt' file

The logic is in the 'process.py' file. It is typically called manually to import data or referenced from the website.

The Website is controlled by the 'app.py' file. 

http://asciiflow.com diagram

```
+-----------------+   +-----------------+  +----------------+
|                 |   |                 |  |                |
|   sqlite db     |   |   python        |  |   CherryPy     |
|                 +-->+   functions     +->+   web interface|
|                 |   |                 |  |                |
+-----------------+   +-----------------+  +----------------+

```

The REST services available are:

| Endpoint  | Supported Verbs | description |
| --------- | ---------------- | ----------- |
| `/memobyid`                      | POST | update memo field based on the transaction unique id.         |
|                                  |      | `Example:`                                                    |
|                                  |      | `[ `                                                          |
|                                  |      | `  {`                                                         |
|                                  |      | `     "id": 15", `                                            |
|                                  |      | `     "memo": "misc" `                                        |
|                                  |      | `  },`                                                        |
|                                  |      | `  {`                                                         |
|                                  |      | `     "id": 85", `                                            |
|                                  |      | `     "memo": "grocery" `                                     |
|                                  |      | `  },`                                                        |
|                                  |      | `]`                                                           |
| `/categorytotals/<year>`         | GET  | get list of category totals by year (default to current year) |
|                                  |      | `Example:`                                                    |
|                                  |      | `[ `                                                          |
|                                  |      | `  {`                                                         |
|                                  |      | `     "source": "Personal", `                                 |
|                                  |      | `     "category": "taxes", `                                  |
|                                  |      | `     "sum-debits": 500", `                                   |
|                                  |      | `     "sum-credits": "" `                                     |
|                                  |      | `  },`                                                        |
|                                  |      | `  {`                                                         |
|                                  |      | `     "source": "Personal", `                                 |
|                                  |      | `     "category": "grocery", `                                |
|                                  |      | `     "sum-debits": 1500", `                                  |
|                                  |      | `     "sum-credits": "" `                                     |
|                                  |      | `   }`                                                        |
|                                  |      | `]`                                                           |
| `/transactions/<source>/<year>/<category>/<subcategory>` | GET  | get transactions by values provided.  |
|                                  |      | `Example:`                                                    |
|                                  |      | `[`                                                           |
|                                  |      | `  {`                                                         |
|                                  |      | `     "id": "340", `                                          |
|                                  |      | `     "checknumber": "1500", `                                |
|                                  |      | `     "description": "SEVEN ELEVEN", `                        |
|                                  |      | `     "type": "POS", `                                        |
|                                  |      | `     "debit_amount": "15.59", `                              |
|                                  |      | `     "credit_amount": "", `                                  |
|                                  |      | `     "balance": 1500", `                                     |
|                                  |      | `     "memo": "" `                                            |
|                                  |      | `   }`                                                        |
|                                  |      | `]`                                                           |

## Oddities
 - The 'automatedcategory' and 'automatedsubcategory' columns were intended to be the default values
 - The 'category' and 'subcategory' columns were intended for overrides. That override functionality has not been implemented. There are bits of code that rename 'automatedcategory' to 'category' for readability.
 
 