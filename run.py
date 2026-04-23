import argparse
import yaml
import pandas as pd
import numpy as np
import logging
import json
import time
import sys
import os


# =========================
# Logger Setup
# =========================
def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# =========================
# Load Config
# =========================
def load_config(config_path):
    if not os.path.exists(config_path):
        raise Exception("Config file not found")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if not isinstance(config, dict):
        raise Exception("Invalid config structure")

    required_keys = ["seed", "window", "version"]

    for key in required_keys:
        if key not in config:
            raise Exception(f"Missing config key: {key}")

    return config


# =========================
# Load Data
# =========================
def load_data(input_path):
    if not os.path.exists(input_path):
        raise Exception("Description of what went wrong")
        

    try:
        df = pd.read_csv(input_path, sep=None, engine="python")
    except Exception:
        raise Exception("Invalid CSV format")

    if df.empty:
        raise Exception("CSV file is empty")

    # Fix column issues
    df.columns = df.columns.str.strip().str.lower()

    # Detect bad parsing
    if df.shape[1] == 1:
        raise Exception("CSV parsing failed (possible delimiter issue)")

    if "close" not in df.columns:
        raise Exception(f"Missing required column: close. Found columns: {list(df.columns)}")

    return df


# =========================
# Main Function
# =========================
def main(args):
    start_time = time.time()

    try:
        setup_logger(args.log_file)
        logging.info("Job started")

        # Load config
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # Load data
        df = load_data(args.input)
        logging.info(f"Rows loaded: {len(df)}")

        # Rolling mean
        logging.info("Computing rolling mean")
        df["rolling_mean"] = df["close"].rolling(window=window).mean()

        # Signal
        logging.info("Generating signal")
        df["signal"] = np.where(df["close"] > df["rolling_mean"], 1, 0)

        # Remove NaN rows for metric calculation
        valid_df = df.dropna(subset=["rolling_mean"])

        signal_rate = valid_df["signal"].mean()
        rows_processed = len(df)

        # Metrics
        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        # Write metrics
        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=2)

        logging.info(f"Metrics: {metrics}")
        logging.info("Job completed successfully")

        print(json.dumps(metrics, indent=2))
        sys.exit(0)

    except Exception as e:
        error_metrics = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        # MUST write metrics even on error
        with open(args.output, "w") as f:
            json.dump(error_metrics, f, indent=2)

        logging.error("Job failed", exc_info=True)

        print(json.dumps(error_metrics, indent=2))
        sys.exit(1)


# =========================
# CLI Entry
# =========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    main(args)