import pandas as pd
from typing import List
from ..domain.interfaces import IDataProcessor
from ..domain.entities import Transaction


class DataProcessor(IDataProcessor):
    def parse_transactions_from_file(self, file_path: str) -> List[Transaction]:
        df = pd.read_csv(file_path)
        required = {'transaction_id', 'date', 'category', 'amount', 'currency'}
        if not required.issubset(df.columns):
            raise ValueError(f"Missing columns. Required: {required}")

        transactions = []
        for _, row in df.iterrows():
            transactions.append(Transaction(
                str(row['transaction_id']),
                pd.to_datetime(row['date']).date(),
                str(row['category']),
                float(row['amount']),
                str(row['currency'])
            ))
        return transactions