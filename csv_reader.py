import pandas
import logging
from datetime import datetime


class CSVReader:
    """
        CSV Reader class to perform all operations realted to extrating data from CSV
    """

    def __init__(self):
        self.trasaction_csv_path = '/home/uttam/Documents/projects/assignment_medpay/csv_data/sku_info_csv.csv'
        self.sku_csv_path = '/home/uttam/Documents/projects/assignment_medpay/csv_data/transaction_csv.csv'


    def read_sku_csv(self):
        sku_info_df = pandas.read_csv(self.trasaction_csv_path)
        return sku_info_df


    def read_transaction_csv(self):
        # parsing string date into datetime object
        dateparse = lambda date: datetime.strptime(date, '%d/%m/%Y')
        
        transactions_df = pandas.read_csv(
                            self.sku_csv_path,
                            parse_dates=['transaction_datetime'],
                            date_parser=dateparse
                        )
        return transactions_df


    def get_single_transaction(self,transaction_id):
        transactions_df = self.read_transaction_csv()

        single_trans_df = transactions_df.loc[transactions_df['transaction_id'] == transaction_id]
        return single_trans_df

    
    def get_single_sku(self,sku_id):
        sku_df = self.read_sku_csv()

        single_sku_df = sku_df.loc[sku_df['sku_id'] == sku_id]
        return single_sku_df

# ideas

# path from env
# sku name from sku hash in transaction api
# git repo