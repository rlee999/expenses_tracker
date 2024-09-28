# expenses_tracker

### App structure
1. Import + edit master + settings
2. Analyse

### Data Structure
Define local working folder in import page.

Local working folder should be on onedrive or google drive to ensure data is 
synced.

Maser_AT.csv (all transactions): contains all transactions years 2021-current.
Trimmed transactions for years before 2024
Columns: transaction name, date, 

Backups of Master_transaction: Confirmation of each import should create a new 
csv called AT_yyyy-mm-dd.csv


### Import page
Define working local file directory. can select and save defaults (surface default, big pc
default, s24+).

Local working folder should be on onedrive or google drive to ensure data is 
synced.

Import function: takes csv from goodbudget or commbank.
Allows user to view columns and tell app which master column it corresponds to.

Confirmation of each import should create a new 
csv called AT_yyyy-mm-dd.csv

### Draft monthly workflow
1. export transactions from CBA as csv
2. import CBA csv transactions into goodbudget to allocate categories and fill envelopes etc. 
3. export goodbudget csv transactions to streamlit to save master_hx and further analysis 
4. optional subcategory allocation in streamlit (to save to master, and for further analysis)
5. (master_AT is saved on onedrive/googld drive, and is uploaded in streamlit each use)

### Draft monthly workflow (without streamlit)
monthly categories: Rent, Utilities, Groceries, Leisure (other), Eating out, Petrol/travel, Necessary,
Sports
annual categories: Holidays

(eating out)
(leisure includes: shopping, games, netflix)
(necessary includes: work related, insurances, home food, educational, furniture shopping)
