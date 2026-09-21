import pandas as pd
import numpy as np
import numpy as np

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder

from .schemas import (
    TransactionRequest,
    PredictionResponse
)

from .predictor import (
    calculate_prediction,
    alerts_df,
    features_df
)


app = FastAPI(
    title="UPI Fraud Detection API",
    description="API for UPI transaction anomaly and fraud risk detection",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)



def clean_for_json(data):
    if isinstance(data, list):
        return [clean_for_json(item) for item in data]

    if isinstance(data, dict):
        return {
            key: clean_for_json(value)
            for key, value in data.items()
        }

    if isinstance(data, float):
        if not np.isfinite(data):
            return None
        return data

    return data


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "UPI Fraud Detection API"
    }


@app.post(
    "/predict",
    response_model=PredictionResponse
)
def predict_transaction(
    transaction: TransactionRequest
):
    return calculate_prediction(transaction)


@app.get("/alerts")
def get_alerts():
    records = alerts_df.to_dict(orient="records")

    clean_records = []

    for record in records:
        clean_record = {}

        for key, value in record.items():

            # Handle missing values
            if value is None:
                clean_record[key] = None
                continue

            try:
                if pd.isna(value):
                    clean_record[key] = None
                    continue
            except (TypeError, ValueError):
                pass

            # Handle NumPy integer values
            if isinstance(value, np.integer):
                clean_record[key] = int(value)
                continue

            # Handle NumPy and Python floating-point values
            if isinstance(value, (np.floating, float)):
                if np.isfinite(value):
                    clean_record[key] = float(value)
                else:
                    clean_record[key] = None
                continue

            # Handle normal integers
            if isinstance(value, int):
                clean_record[key] = value
                continue

            # Handle normal strings and other JSON-safe values
            clean_record[key] = value

        clean_records.append(clean_record)

    return {
        "total_alerts": len(clean_records),
        "alerts": clean_records
    }


@app.get("/transaction/{transaction_id}")
def get_transaction(
    transaction_id: str
):
    result = features_df[
        features_df["transaction_id"].astype(str)
        == str(transaction_id)
    ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    record = result.iloc[0].to_dict()

    return clean_for_json(jsonable_encoder(record))


@app.get("/")
def root():
    return {
        "message": "UPI Fraud Detection API",
        "docs": "/docs",
        "health": "/health"
    }
