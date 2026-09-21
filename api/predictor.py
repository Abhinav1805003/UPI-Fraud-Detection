
import os
import joblib
import pandas as pd


PROJECT_DIR = r"D:\UPI-Fraud-Detection"

MODEL_DIR = r"D:\UPI-Fraud-Detection\models"
DATA_DIR = r"D:\UPI-Fraud-Detection\data\processed"

ISOLATION_MODEL_PATH = (
    r"D:\UPI-Fraud-Detection\models\isolation_forest.pkl"
)

MODEL_METADATA_PATH = (
    r"D:\UPI-Fraud-Detection\models\model_metadata.pkl"
)

IQR_METADATA_PATH = (
    r"D:\UPI-Fraud-Detection\models\iqr_metadata.pkl"
)

FEATURES_PATH = (
    r"D:\UPI-Fraud-Detection\data\processed\features.csv"
)

ALERTS_PATH = (
    r"D:\UPI-Fraud-Detection\data\processed\alerts.csv"
)


isolation_model = joblib.load(
    ISOLATION_MODEL_PATH
)

model_metadata = joblib.load(
    MODEL_METADATA_PATH
)

iqr_metadata = joblib.load(
    IQR_METADATA_PATH
)

features_df = pd.read_csv(
    FEATURES_PATH
)

alerts_df = pd.read_csv(
    ALERTS_PATH
)


MODEL_FEATURES = model_metadata["model_features"]
FINAL_THRESHOLD = model_metadata["final_threshold"]
RISK_WEIGHTS = model_metadata["risk_weights"]

LOWER_BOUND = iqr_metadata["lower_bound"]
UPPER_BOUND = iqr_metadata["upper_bound"]


def calculate_prediction(transaction):
    data = {
        "amount": transaction.amount,
        "amount_deviation": transaction.amount_deviation,
        "transactions_last_1h": transaction.transactions_last_1h,
        "recipient_repeat_count": transaction.recipient_repeat_count,
        "device_changed": transaction.device_changed,
        "location_changed": transaction.location_changed,
        "is_late_night": transaction.is_late_night,
        "is_weekend": transaction.is_weekend
    }

    input_df = pd.DataFrame([data])

    isolation_prediction = isolation_model.predict(
        input_df[MODEL_FEATURES]
    )[0]

    isolation_anomaly = int(
        isolation_prediction == -1
    )

    iqr_anomaly = int(
        transaction.amount < LOWER_BOUND
        or transaction.amount > UPPER_BOUND
    )

    burst_anomaly = int(
        transaction.transactions_last_1h >= 5
    )

    risk_score = (
        iqr_anomaly * RISK_WEIGHTS["iqr_anomaly"]
        + isolation_anomaly * RISK_WEIGHTS["isolation_anomaly"]
        + burst_anomaly * RISK_WEIGHTS["burst_anomaly"]
        + transaction.device_changed * RISK_WEIGHTS["device_changed"]
        + transaction.location_changed * RISK_WEIGHTS["location_changed"]
        + transaction.is_late_night * RISK_WEIGHTS["is_late_night"]
    )

    risk_score = min(risk_score, 100)

    if risk_score < 30:
        risk_level = "Low"
    elif risk_score < 50:
        risk_level = "Medium"
    elif risk_score < 70:
        risk_level = "High"
    else:
        risk_level = "Critical"

    is_suspicious = (
        risk_score >= FINAL_THRESHOLD
    )

    reasons = []

    if iqr_anomaly:
        reasons.append("Unusually high or low transaction amount")

    if isolation_anomaly:
        reasons.append("Isolation Forest detected anomalous behavior")

    if burst_anomaly:
        reasons.append("High transaction frequency within 1 hour")

    if transaction.device_changed:
        reasons.append("New or changed device detected")

    if transaction.location_changed:
        reasons.append("Location change detected")

    if transaction.is_late_night:
        reasons.append("Late-night transaction")

    if not reasons:
        reasons.append("No major suspicious signals detected")

    return {
        "transaction_id": transaction.transaction_id,
        "risk_score": float(risk_score),
        "risk_level": risk_level,
        "is_suspicious": bool(is_suspicious),
        "reasons": reasons,
        "isolation_anomaly": isolation_anomaly,
        "iqr_anomaly": iqr_anomaly,
        "burst_anomaly": burst_anomaly
    }
