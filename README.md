# UPI Fraud Detection & Risk Monitoring System

An end-to-end machine learning system for detecting suspicious UPI transactions using behavioral anomaly detection, risk scoring, and a real-time monitoring dashboard.

## Project Overview

Digital payment systems process a large number of transactions, making automated detection of unusual transaction behavior important for fraud monitoring.

This project analyzes UPI transaction behavior and assigns each transaction a risk score based on multiple signals, including:

* Unusual transaction amount
* Transaction frequency
* Recipient repetition
* Device changes
* Location changes
* Late-night activity
* Time-based behavioral anomalies

The system combines statistical anomaly detection, machine learning, and rule-based behavioral signals into a unified risk score.

## System Architecture

```text
UPI Transaction Data
        │
        ▼
Data Preprocessing
        │
        ▼
Feature Engineering
        │
        ├───────────────┐
        ▼               ▼
   IQR Detection   Isolation Forest
        │               │
        └───────┬───────┘
                ▼
       Behavioral Signals
                │
                ▼
          Risk Scoring
                │
                ▼
        Fraud Alert Engine
                │
        ┌───────┴────────┐
        ▼                ▼
   FastAPI Backend    Dashboard
```

## Key Features

### Machine Learning

* Isolation Forest anomaly detection
* IQR-based statistical anomaly detection
* Behavioral transaction analysis
* Time-based anomaly detection
* Multi-signal risk scoring

### Risk Scoring

The final risk score combines multiple detection signals:

| Signal              | Weight |
| ------------------- | -----: |
| Isolation Forest    |    35% |
| Transaction Burst   |    25% |
| IQR Anomaly         |    15% |
| Time-Series Anomaly |    10% |
| Device Change       |     5% |
| Location Change     |     5% |
| Late-Night Activity |     5% |

Risk levels:

* **0–29:** Low
* **30–49:** Medium
* **50–69:** High
* **70–100:** Critical

Transactions with a risk score of 50 or above are classified as alerts.

## Dataset

The project uses a synthetically generated UPI transaction dataset containing:

* 10,000 transactions
* 1,000 users
* Transaction amounts
* User behavior
* Device information
* Location changes
* Transaction frequency
* Time-based features

Suspicious transactions were synthetically injected using behavioral patterns such as unusually high transaction amounts, transaction bursts, device changes, location changes, and late-night activity.

**Important:** Because the dataset and suspicious labels are synthetic, the evaluation results are illustrative and should not be interpreted as real-world fraud detection performance.

## Model Evaluation

Using the selected risk threshold of 50, the system produced:

* Precision: **43.36%**
* Recall: **34.60%**
* F1 Score: **38.49%**
* False Positive Rate: **2.38%**

The system generated **399 alerts** from the synthetic transaction dataset.

These metrics are specific to the synthetic data and injected anomaly-generation process.

## FastAPI Backend

The project exposes the fraud detection system through a FastAPI backend.

### Endpoints

| Method | Endpoint                        | Purpose                          |
| ------ | ------------------------------- | -------------------------------- |
| GET    | `/`                             | API information                  |
| GET    | `/health`                       | Health check                     |
| POST   | `/predict`                      | Analyze a transaction            |
| GET    | `/alerts`                       | Retrieve generated alerts        |
| GET    | `/transaction/{transaction_id}` | Retrieve transaction information |
| GET    | `/docs`                         | Interactive API documentation    |

### Example

A transaction can be submitted to `/predict` with behavioral features such as:

```json
{
  "transaction_id": "TEST_000001",
  "amount": 25000,
  "amount_deviation": 4.5,
  "transactions_last_1h": 8,
  "recipient_repeat_count": 0,
  "device_changed": 1,
  "location_changed": 1,
  "hour": 2,
  "day_of_week": 5,
  "is_weekend": 1,
  "is_late_night": 1
}
```

The API returns a calculated risk score and risk classification.

## Dashboard

A web-based monitoring dashboard is included in:

```text
dashboard/fraud-detection-dashboard.html
```

The dashboard connects directly to the FastAPI backend and provides:

* API connection status
* Total fraud alerts
* High-risk transactions
* Critical-risk transactions
* Risk distribution
* Recent fraud alerts
* Transaction risk analysis
* Risk score visualization

## Technology Stack

**Programming:** Python

**Data Analysis:**

* Pandas
* NumPy

**Machine Learning:**

* Scikit-learn
* Isolation Forest

**Backend:**

* FastAPI
* Uvicorn
* Pydantic

**Visualization:**

* Matplotlib
* Seaborn
* HTML/JavaScript dashboard

**Development:**

* JupyterLab
* Anaconda
* VS Code

## Project Structure

```text
UPI-Fraud-Detection/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── predictor.py
│   └── schemas.py
│
├── dashboard/
│   └── fraud-detection-dashboard.html
│
├── data/
│   ├── raw/
│   │   └── upi_transactions.csv
│   └── processed/
│       ├── features.csv
│       └── alerts.csv
│
├── models/
│   ├── isolation_forest.pkl
│   ├── model_metadata.pkl
│   └── iqr_metadata.pkl
│
├── notebooks/
│   └── Project notebooks
│
├── .gitignore
├── requirements.txt
└── README.md
```

## How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd UPI-Fraud-Detection
```

### 2. Create the environment

```bash
conda create -n upi-fraud python=3.11
conda activate upi-fraud
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

```text
http://127.0.0.1:8000/docs
```

### 5. Open the dashboard

Open:

```text
dashboard/fraud-detection-dashboard.html
```

in a web browser while the FastAPI server is running.

## Limitations

* The dataset is synthetic.
* Suspicious transaction labels are based on injected behavioral patterns.
* The system is intended as a portfolio and demonstration project rather than a production fraud detection system.
* Real-world deployment would require historical transaction data, stronger validation, model monitoring, threshold optimization, and integration with production payment infrastructure.
* Time-series detection requires transaction history and therefore is not independently calculated for a single `/predict` request.

## Future Improvements

Potential improvements include:

* Real transaction data integration
* Advanced anomaly detection models
* Real-time streaming detection
* User-specific behavioral baselines
* Model monitoring and drift detection
* Explainable AI for fraud alerts
* Authentication and API security
* Database integration
* Cloud deployment
* Automated alert notifications

## Author

**Abhinav Yadav**

B.Tech Computer Science

GitHub: `github.com/Abhinav1805003`
