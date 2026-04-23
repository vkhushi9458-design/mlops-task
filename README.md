# MLOps Batch Job (Rolling Mean Signal Pipeline)

## 📌 Overview

This project implements a minimal MLOps-style batch pipeline in Python.

It demonstrates:

* **Reproducibility**: Config-driven runs using YAML + fixed seed
* **Observability**: Logging + structured JSON metrics
* **Deployment readiness**: Dockerized, one-command execution

The pipeline reads OHLCV data, computes a rolling mean on the `close` column, and generates a binary trading signal.

---

## ⚙️ Features

* YAML configuration
* Data validation (file, format, column checks)
* Rolling mean calculation
* Binary signal generation
* JSON metrics output
* Detailed logging
* Error handling (always writes metrics.json)
* Docker support

---

## 📁 Project Structure

```
mlops-task/
│
├── run.py
├── config.yaml
├── data.csv
├── requirements.txt
├── Dockerfile
├── README.md
├── metrics.json    # generated
└── run.log         # generated
```

---

## ▶️ Run Locally

### 1. Install dependencies

```
pip install -r requirements.txt
```

### 2. Run the pipeline

```
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

---

## 📊 Output (`metrics.json`)

### ✅ Success Example

```
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4991,
  "latency_ms": 44,
  "seed": 42,
  "status": "success"
}
```

### ❌ Error Example

```
{
  "version": "v1",
  "status": "error",
  "error_message": "Description of what went wrong"
}
```

---

## 📝 Logging (`run.log`)

Logs include:

* Job start time
* Config loaded
* Rows processed
* Rolling mean + signal steps
* Metrics summary
* Errors (if any)

---

## 🐳 Docker Usage

### Build image

```
docker build -t mlops-task .
```

### Run container

```
docker run --rm mlops-task
```

---

## ✅ Docker Behavior

* Uses included `data.csv` and `config.yaml`
* Generates:

  * `metrics.json`
  * `run.log`
* Prints metrics JSON to terminal
* Exit code:

  * `0` → success
  * `1` → error

---

## 🧠 Design Decisions

* First `(window - 1)` rows → rolling mean = NaN
  → excluded from metric calculation
* Column names normalized (lowercase + strip)
* CSV delimiter auto-detected
* Errors handled gracefully

---

## 🎯 Evaluation Checklist

✔ CLI-based execution
✔ No hardcoded paths
✔ Deterministic output
✔ Metrics always written
✔ Logging included
✔ Docker works

---

## 🚀 Conclusion

This project demonstrates a clean, production-style batch pipeline with reproducibility, observability, and deployment readiness.
