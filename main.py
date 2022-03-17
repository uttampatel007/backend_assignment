import logging
from fastapi import FastAPI
from processer import (
    process_single_transaction,
    process_transaction_summary_by_sku,
    process_transaction_summary_by_category
)
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/transaction/{transaction_id}")
def get_transaction(transaction_id:int):
    payload = process_single_transaction(transaction_id)
    return payload


@app.get("/transaction-summary-bySKU/{last_n_days}")
def get_transaction_summary_by_sku(last_n_days:int):
    payload = process_transaction_summary_by_sku(last_n_days)
    return payload


@app.get('/transaction-summary-bycategory/{last_n_days}')
def get_transaction_summary_by_category(last_n_days:int):
    payload = process_transaction_summary_by_category(last_n_days)
    return payload