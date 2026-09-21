
from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction ID")
    amount: float = Field(..., gt=0)
    amount_deviation: float = Field(..., ge=0)
    transactions_last_1h: int = Field(..., ge=0)
    recipient_repeat_count: int = Field(..., ge=0)
    device_changed: int = Field(..., ge=0, le=1)
    location_changed: int = Field(..., ge=0, le=1)
    is_late_night: int = Field(..., ge=0, le=1)
    is_weekend: int = Field(..., ge=0, le=1)


class PredictionResponse(BaseModel):
    transaction_id: str
    risk_score: float
    risk_level: str
    is_suspicious: bool
    reasons: list[str]
    isolation_anomaly: int
    iqr_anomaly: int
    burst_anomaly: int
