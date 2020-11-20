#pip3 install SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import SingletonThreadPool
import json
from os import listdir, rename
from os.path import isfile, join
import time
import pandas as pd

currentyear = "2020"


def query(query):
    connection = get_db_connection()
    try:
        connection.execute(query);
    except Exception as e:
        connection.close()
        print(e)
    else:
        connection.close()
        pass
    pass

def query_and_print(query):
    connection = get_db_connection()
    try:
        result = connection.execute(query);
    except Exception as e:
        connection.close
        print(e)
    else:
        print_results(result)
        resultlist = []
        for row in result:
            resultlist.append(dict(row))
        print(resultlist)
        connection.close()
        return "done"
    return "fail"

def query_results(query):
    print(query)
    connection = get_db_connection()
    try:
        result = connection.execute(query);
    except Exception as e:
        connection.close
        print(e)
    else:
        resultlist = []
        for row in result:
            resultlist.append(dict(row))
        print(resultlist)
        connection.close()
        return resultlist
    return "fail"

def print_results(result):
    for row in result:
        print(row)  # print(row[0], row[1], row[2])
    pass

def get_db_connection():
    engine = create_engine('sqlite:///accounting', poolclass=SingletonThreadPool)
    connection = engine.connect()
    return connection

def add_memos():
    print("Adding memos")
    with open("memomapping.json") as f:
        memomappinglist = json.load(f)
    for memomap in memomappinglist:
        set_memo_to = memomap.get("setmemo")
        account_type = memomap.get("where").get("accounttype")
        debit_amount_check = memomap.get("where").get("debitamount")
        credit_amount_check = memomap.get("where").get("creditamount")

        where_clause = " where "
        if (account_type == "Personal"):
            where_clause += " source like 'Personal' "
        else:
            where_clause += " source not like 'Personal' "
        if (debit_amount_check is not None):
            where_clause += "and debit_amount " + debit_amount_check.get("is") + " " + str(debit_amount_check.get("amount")) + " "
        if (credit_amount_check is not None):
            where_clause += " credit_amount " + credit_amount_check.get("is") + " " + str(credit_amount_check.get("amount")) + " "

        memo_sql = "update transactions set memo = '" + set_memo_to + "'"+ where_clause + ";"
        print(memo_sql)
        query(memo_sql)


def categorize_transactions():
    print("Categorizing Transactions")
    with open('categorymapping.json') as f:
        categorymappinglist = json.load(f)
    for categorymapping in categorymappinglist:
        expectedsource = categorymapping.get("accounttype")
        isexpectedsource = ""
        if expectedsource == "Any":
            isexpectedsource = ""
        else:
            if expectedsource == "Business":
                isexpectedsource = "and source not like 'Personal'"
            else:
                if expectedsource == "Personal":
                    isexpectedsource = "and source like 'Personal'"
        descriptionlist = categorymapping.get("matchon").get("descriptionlikeany")
        if descriptionlist is not None:
            for description in descriptionlist:
                add_category_sql = (
                        "update transactions set " +
                        "automatedcategory='" + categorymapping.get("category") + "', "
                        "automatedsubcategory='" + categorymapping.get("subcategory") + "' "
                        "where description like '%" + description + "%' " +
                        isexpectedsource +
                        ";"
                )
                print(add_category_sql)
                query(add_category_sql)
        memolist = categorymapping.get("matchon").get("memolikeany")
        if memolist is not None:
            for memo in memolist:
                add_category_sql = (
                        "update transactions set " +
                        "automatedcategory='" + categorymapping.get("category") + "', "
                        "automatedsubcategory='" + categorymapping.get("subcategory") + "' "
                        "where memo like '%" + memo + "%' " +
                        isexpectedsource +
                        ";"
                )
                print(add_category_sql)
                query(add_category_sql)


def show_transactions(source, year=currentyear, category=None, subcategory=None):
    if source is not None:
        source = sanitize(source)
    if category is not None:
        category = sanitize(category)
    if subcategory is not None:
        subcategory = sanitize(subcategory)
    if year is not None:
        year = sanitize(year)
    else:
        year = currentyear
    if year == "currentyear":
        year = currentyear
    if year == "prevousyear":
        year = str(int(currentyear)-1)

    transactions_sql = "select rowid as id, * from transactions "
    where_clause = "where source = '" + source + "'"
    if source is not None:
        if source.lower() == "any":
            where_clause = "where source is not null"
        if source.lower() == "personal":
            where_clause = "where source like 'Personal'"
        if source.lower() == "business":
            where_clause = "where source not like 'Personal'"
    else:
        where_clause = "where source like '%'"
    transactions_sql += where_clause
    if category is not None:
        if category.lower() == "nocategory":
            transactions_sql += " and automatedcategory is null"
        else:
            if category.lower() != "any":
                transactions_sql += " and automatedcategory = '" + category + "'"
    if subcategory is not None:
        transactions_sql += " and automatedsubcategory = '" + subcategory + "'"
    transactions_sql += " and date like '%" + year + "'"
    transactions_sql += " order by automatedcategory, automatedsubcategory, description, date;"
    results = query_results(transactions_sql)

    return results


def show_annual_category_totals(year = currentyear):
    annual_category_totals_sql = "select source, automatedcategory, sum(debit_amount),sum(credit_amount)\
                                  from transactions\
                                  where date like '%" + year + "' \
                                  group by source, automatedcategory\
                                  order by source, automatedcategory;"
    results = query_results(annual_category_totals_sql)

    return results


def sanitize(input):
    return input.encode("utf8").decode("utf8").replace("'","`")


def update_memo_by_id(memos_by_ids):
    memotext = memos_by_ids
    print(memotext)
    memolist = json.loads(memotext.replace("'", "\""))

    for memoline in memolist:
        print(memoline)
        memotext = sanitize(memoline.get("memo"))
        memoid = sanitize(memoline.get("id"))
        memo_update_sql = "update transactions set memo='" + memotext + "' where rowid = " + memoid + ";"
        print(memo_update_sql)
        query(memo_update_sql)
    categorize_transactions()
    pass

def download_transactions():
    print("Download Transactions - Not Implemented")
    pass

def import_transactions():
    print("Importing Transactions")
    importpath = "importfiles/"
    processedpath = "importfiles/processed/"
    onlyfiles = [f for f in listdir(importpath) if isfile(join(importpath, f))]
    for file in onlyfiles:
        print(file)
        csv_file_path = importpath + file
        seconds = time.time()
        processed_csv_file_path = processedpath + file + str(seconds)
        #with open(csv_file_path, 'r') as f:
        #    conn = get_db_connection()
        #    cursor = conn.cursor()
        #    cmd = 'COPY transactions(check_number, date, description, transaction_type, debit_amount, credit amount, balance) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
        #    cursor.copy_expert(cmd, f)
        #    conn.commit()
        Base = declarative_base()
        df = pd.read_csv(csv_file_path)
        df = df.rename(columns={'Check Number':'check_number', 'Date':'date', 'Description':'description', 'Transaction Type':'transaction_type', 'Debit Amount':'debit_amount', 'Credit Amount':'credit_amount', 'Balance':'balance'})
        conn = get_db_connection()
        df.to_sql("transactions", con=conn, if_exists='append', index=False)
        conn.close()
        set_source_sql = ""
        import_file_name = file.title().capitalize().upper()
        if import_file_name.startswith("ROBERT AND MARIA"):
            set_source_sql = "update transactions set source='Personal' where source is NULL;"
        else:
            source = file[:file.find("(")]
            set_source_sql = "update transactions set source='" + source + "' where source is NULL;"
        print(set_source_sql)
        query(set_source_sql)
        rename(csv_file_path, processed_csv_file_path)
    pass



def main():
    download_transactions()
    import_transactions()
    add_memos()
    categorize_transactions()
    print(show_transactions("Any", "nocategory", ""))
    show_annual_category_totals("2020")

if __name__ == "__main__":
    main()