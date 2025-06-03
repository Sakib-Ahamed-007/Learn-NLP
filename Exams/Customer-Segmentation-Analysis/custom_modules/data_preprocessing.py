import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_and_preprocess_data(customer_csv, transaction_csv):
    # Load data
    customers = pd.read_csv(customer_csv)
    transactions = pd.read_csv(transaction_csv)

    # RFM Features
    rfm = transactions.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (pd.to_datetime('2019-01-01') - pd.to_datetime(x).max()).days,
        'InvoiceNo': 'count',
        'TotalAmount': 'sum'
    }).rename(columns={
        'InvoiceDate': 'Recency',
        'InvoiceNo': 'Frequency',
        'TotalAmount': 'Monetary'
    })

    # Normalize RFM values
    scaler = MinMaxScaler()
    rfm_scaled = pd.DataFrame(scaler.fit_transform(rfm), columns=rfm.columns, index=rfm.index)
    
    return rfm_scaled
