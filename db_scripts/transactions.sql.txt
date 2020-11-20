CREATE TABLE transactions(
check_number INTEGER,
date TEXT,
description TEXT,
transaction_type TEXT,
debit_amount REAL,
credit_amount REAL,
balance REAL,
memo TEXT,
source TEXT,
category TEXT,
subcategory TEXT,
automatedcategory TEXT,
automatedsubcategory TEXT,
PRIMARY KEY (check_number, date, description, source, debit_amount, credit_amount)
);

