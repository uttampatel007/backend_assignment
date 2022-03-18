import json
import pandas
from datetime import datetime


class CSVReader:
    """
        CSV Reader class to perform all operations realted to extrating data from CSV
    """

    def __init__(self):
        self.sku_csv_path = '/home/uttam/Documents/projects/assignment_medpay/csv_data/sku_info_csv.csv'
        self.trasaction_csv_path = '/home/uttam/Documents/projects/assignment_medpay/csv_data/transaction_csv.csv'


    def read_sku_csv(self):
        """Return static sku csv info dataframe"""
        sku_info_df = pandas.read_csv(self.sku_csv_path)
        return sku_info_df


    def read_transaction_csv(self):
        """Returns transaction csv dataframe"""
        # parsing string date into datetime object
        dateparse = lambda date: datetime.strptime(date, '%d/%m/%Y')
        
        transactions_df = pandas.read_csv(
                            self.trasaction_csv_path,
                            parse_dates=['transaction_datetime'],
                            date_parser=dateparse
                        )
        return transactions_df


    def get_single_transaction(self,transaction_id):
        """Given the transaction id, returns transaction data in json"""
        transaction_json = {}

        transactions_df = self.read_transaction_csv()
        single_trans_df = transactions_df.loc[transactions_df['transaction_id'] == transaction_id]

        if single_trans_df.empty:
            return transaction_json

        transaction_json = json.loads(single_trans_df.to_json(orient='records'))
        transaction_json = transaction_json[0]

        return transaction_json

    
    def get_single_sku(self,sku_id):
        """Given the sku id of the transaction, returns the sku data in json"""
        sku_json = {}

        sku_df = self.read_sku_csv()
        single_sku_df = sku_df.loc[sku_df['sku_id'] == sku_id]

        if single_sku_df.empty:
            return sku_json

        sku_json = json.loads(single_sku_df.to_json(orient='records'))
        sku_json = sku_json[0]

        return sku_json

### Ideas
# path from env
# sku name from sku hash in transaction api
# requirement.txt file
# adding docker

### Done
# git repo