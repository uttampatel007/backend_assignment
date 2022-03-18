import json
from loguru import logger
from datetime import datetime, timedelta
from app.csv_reader import CSVReader


csv_reader = CSVReader()


def process_single_transaction(transaction_id):
    """Given transaction id, create & return single transaction response"""
    try:
        payload = {}

        transaction_json = csv_reader.get_single_transaction(transaction_id)
        
        # in case of no transaction found for requested id
        if not transaction_json:
            payload = {
                "description":"Item not found"
            }
            return payload, 404

        # converting transaction datetime interger to datetime obj 
        # datetime integer example - 1643328000000
        transaction_date = datetime.fromtimestamp(
            transaction_json.get("transaction_datetime") / 1e3).strftime('%d/%m/%Y')
        
        # getting single sku data from sku id
        sku_id = transaction_json.get("sku_id")
        sku_json = csv_reader.get_single_sku(sku_id)
        if not sku_json:
            payload = {
                "description":"Item not found"
            }
            return payload, 404

        sku_name = sku_json.get("sku_name")

        payload = {
            "transaction_id":transaction_json.get("transaction_id"),
            "sku_name":sku_name,
            "sku_price":transaction_json.get("sku_price"),
            "transaction_datetime":transaction_date
        }
        return payload, 200
        
    except Exception as e:
        logger.exception(e)
        payload = {"description": "Internal error"}
        return payload, 500


def get_n_day_before_date(last_n_days):
    """Given last n days, return datetime object of nth day from today"""
    today = datetime.now()

    # to get midnight time
    today = datetime.combine(today, datetime.min.time())
    
    nth_date = timedelta(days = last_n_days)
    nth_day_date = today - nth_date
    
    return nth_day_date


def get_sku_total_hash(n_day_trans_json):
    """
    Given transactions json, return sku id and total price hash
    example : {1: 202.11, 2: 21.2, 4: 200.0, 3: 100.0}
    """
    sku_total_hash = {}
    for obj in n_day_trans_json:

        sku_id = obj.get("sku_id")
        sku_price = obj.get("sku_price")
        if sku_id not in sku_total_hash:
            sku_total_hash[sku_id] = sku_price
        else:
            sku_total_hash[sku_id] += sku_price

    return sku_total_hash


def get_sku_hash():
    """
    Return a hash of sku id and name from static sku csv
    example: {1: 'S1', 2: 'S2', 3: 'S3'}
    """
    sku_df = csv_reader.read_sku_csv()
    sku_json = json.loads(sku_df.to_json(orient='records'))

    sku_hash = {}
    for obj in sku_json:
        sku_id = obj.get("sku_id")
        sku_name = obj.get("sku_name")
        sku_hash[sku_id] = sku_name
    
    return sku_hash


def get_n_day_transactions(last_n_days):
    """
    Given last n days value, 
    return data of transactions happens in last n days in json
    """
    nth_day_date = get_n_day_before_date(last_n_days)

    # get transaction dataframe
    all_trans_df = csv_reader.read_transaction_csv()
    
    # get transaction of last n days
    n_day_trans_df = all_trans_df.loc[all_trans_df['transaction_datetime'] > nth_day_date]
    n_day_trans_df = n_day_trans_df.to_json(orient='records')
    n_day_trans_json = json.loads(n_day_trans_df)

    return n_day_trans_json


def process_transaction_summary_by_sku(last_n_days):
    """Given last n days, return summary by sku"""
    try:
        n_day_trans_json = get_n_day_transactions(last_n_days)

        # get sku total hash
        sku_total_hash = get_sku_total_hash(n_day_trans_json)

        # get sku hash
        sku_hash = get_sku_hash()

        summary = []
        for sku_id,sku_total_price in sku_total_hash.items():
            summary.append({
                "sku_name":sku_hash.get(sku_id),
                "total_amount":sku_total_price
            })
        
        payload = {
            "summary":summary
        }

        return payload, 200
    except Exception as e:
        logger.exception(e)
        payload = {"description": "Internal error"}
        return payload, 500
        

def get_sku_id_category_hash():
    """
    Return a hash of sku id and sku category from static sku csv
    example: {1: 'C1', 2: 'C1', 3: 'C2', 4: 'C2', 5: 'C1'}
    """
    sku_df = csv_reader.read_sku_csv()
    sku_json = json.loads(sku_df.to_json(orient='records'))
    
    cat_id_hash = {}   
    for obj in sku_json:
        sku_id = obj.get("sku_id")
        sku_category = obj.get("sku_category")
        cat_id_hash[sku_id] = sku_category
    
    return cat_id_hash


def process_transaction_summary_by_category(last_n_days):
    """Given last n days, return summary by category"""
    try:
        n_day_trans_json = get_n_day_transactions(last_n_days)

        cat_id_hash = get_sku_id_category_hash()

        # hash to store category id wise total amount
        category_price_hash = {}

        for obj in n_day_trans_json:
            sku_id = obj.get("sku_id")
            sku_price = obj.get("sku_price")

            sku_category = cat_id_hash.get(sku_id)

            if sku_category not in category_price_hash:
                category_price_hash[sku_category] = sku_price
            else:
                category_price_hash[sku_category] += sku_price

        summary = []
        for category_name,category_total in category_price_hash.items():
            summary.append({
                "sku_category":category_name,
                "total_amount":category_total
            })

        payload = {"summary":summary}
        return payload, 200

    except Exception as e:
        logger.exception(e)
        payload = {"description": "Internal error"}
        return payload, 500