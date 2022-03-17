import json
import logging
from unicodedata import category
from csv_reader import CSVReader
from datetime import datetime, timedelta


csv_reader = CSVReader()


def process_single_transaction(transaction_id):
    try:
        transaction_df = csv_reader.get_single_transaction(transaction_id)
        transaction_json = json.loads(transaction_df.to_json(orient='records'))
        transaction_json = transaction_json[0]
        transaction_date = datetime.fromtimestamp(
            transaction_json.get("transaction_datetime") / 1e3).strftime('%d/%m/%Y')

        sku_id = transaction_json.get("sku_id")
        sku_df = csv_reader.get_single_sku(sku_id)
        sku_json = json.loads(sku_df.to_json(orient='records'))
        sku_json = sku_json[0]
        sku_name = sku_json.get("sku_name")

        payload = {
            "transaction_id":transaction_json.get("transaction_id"),
            "sku_name":sku_name,
            "sku_price":transaction_json.get("sku_price"),
            "transaction_datetime":transaction_date
        }
        return payload
        
    except Exception as e:
        logging.exception(e)


def get_n_day_before_date(last_n_days):
    try:
        # get date for n days before from current date
        today = datetime.now()
        
        # to get midnight time
        today = datetime.combine(today, datetime.min.time())
        
        date = timedelta(days = last_n_days)
        
        nth_day_date = today - date
        
        return nth_day_date
    except:
        pass


def get_sku_total_hash(rslt_date_json):
    try:
        # creating sku id and sku total hash
        # example : {1: 202.11, 2: 21.2, 4: 200.0, 3: 100.0}
        
        sku_total_hash = {}
        for obj in rslt_date_json:

            sku_id = obj.get("sku_id")
            sku_price = obj.get("sku_price")
            if sku_id not in sku_total_hash:
                sku_total_hash[sku_id] = sku_price
            else:
                sku_total_hash[sku_id] += sku_price

        return sku_total_hash
    except:
        pass


def get_sku_hash():
    try:
        sku_df = csv_reader.read_sku_csv()
        sku_json = json.loads(sku_df.to_json(orient='records'))

        sku_hash = {}
        for obj in sku_json:
            sku_id = obj.get("sku_id")
            sku_name = obj.get("sku_name")
            sku_hash[sku_id] = sku_name

        return sku_hash
    except:
        pass


def process_transaction_summary_by_sku(last_n_days):
    try:
        nth_day_date = get_n_day_before_date(last_n_days)

        # get transaction dataframe
        transactions_df = csv_reader.read_transaction_csv()

        # get transaction of last n days
        transactions_df = transactions_df.loc[transactions_df['transaction_datetime'] > nth_day_date]
        transactions_df = transactions_df.to_json(orient='records')
        transactions_json = json.loads(transactions_df)

        # get sku total hash
        sku_total_hash = get_sku_total_hash(transactions_json)

        # get sku hash
        sku_hash = get_sku_hash()

        # creating response
        summary = []
        for sku_id,sku_total_price in sku_total_hash.items():
            summary.append({
                "sku_name":sku_hash.get(sku_id),
                "total_amount":sku_total_price
            })
        
        payload = {
            "summary":summary
        }

        return payload
    except Exception as e:
        pass

"""
GET API /transaction-summary-bycategory/{last_n_days}
Response format: JSON
{"summary":[{"sku_category":"C1", "total_amount": 2080.30}]}
"""

def get_category_hash():
    """
    {'S1': 'C1','S2': 'C1','S3': 'C2','S4': 'C2','S5': 'C1','S6': 'C3','S7': 'C3'}
    """
    try:
        sku_df = csv_reader.read_sku_csv()
        sku_json = json.loads(sku_df.to_json(orient='records'))
        category_hash = {}
        for obj in sku_json:
            sku_name = obj.get("sku_name")
            sku_category = obj.get("sku_category")
            category_hash[sku_name] = sku_category

        return category_hash

        pass
    except:
        pass

def get_sku_id_category_hash():
    try:
        
        sku_df = csv_reader.read_sku_csv()
        sku_json = json.loads(sku_df.to_json(orient='records'))

        cat_id_hash = {}
        for obj in sku_json:
            sku_id = obj.get("sku_id")
            sku_category = obj.get("sku_category")
            cat_id_hash[sku_id] = sku_category
    except:
        pass

def process_transaction_summary_by_category(last_n_days):
    try:
        nth_day_date = get_n_day_before_date(last_n_days)

        # get transaction dataframe
        transactions_df = csv_reader.read_transaction_csv()


        pass
    except:
        pass


def process_transaction_summary_by_category(last_n_days):
    try:
        nth_day_date = get_n_day_before_date(last_n_days)
        
        # get transaction dataframe
        transactions_df = csv_reader.read_transaction_csv()

        # get transaction of last n days
        transactions_df = transactions_df.loc[transactions_df['transaction_datetime'] > nth_day_date]
        transactions_df = transactions_df.to_json(orient='records')
        transactions_json = json.loads(transactions_df)

        # get sku total hash
        sku_total_hash = get_sku_total_hash(transactions_json)

        # get category hash
        category_hash = get_category_hash()

        # get sku hash
        sku_hash = get_sku_hash()

        sku_name_total_hash = {}
        for sku_id,sku_total_price in sku_total_hash.items():
            sku_name = sku_hash.get(sku_id)
            sku_name_total_hash[sku_name] = sku_total_price

        # 
        category_total_hash = {}
        for sku_name,sku_total_price in sku_name_total_hash.items():
            cat = category_hash.get(sku_name)
            if not cat in category_total_hash:
                category_total_hash[cat] = sku_total_price
            else:
                category_total_hash[cat] += sku_total_price

        summary = []
        for category_name,category_total in category_total_hash.items():
            summary.append({
                "sku_category":category_name,
                "total_amount":category_total
            })
        
        payload = {"summary":summary}
        return payload
    except:
        pass
        