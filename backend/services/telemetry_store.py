# backend/services/telemetry_store.py
"""
cache + inquery
"""

import pandas as pd
from parser.mav_parser import parse_bin
from pathlib import Path

# simple memo cache：log_id -> DataFrame
telemetry_cache = {}


def load_log(log_id: str) -> pd.DataFrame:
    if log_id in telemetry_cache:
        return telemetry_cache[log_id]

    path = Path(__file__).resolve().parent.parent / "data" / f"{log_id}.bin"
    if not path.exists():
        raise FileNotFoundError(f"log_id {log_id} not found")

    df = parse_bin(str(path))
    telemetry_cache[log_id] = df
    return df


def get_metric(df: pd.DataFrame, name: str):
    if name == "max_altitude":
        alt_col = [col for col in df.columns if "Alt" in col or "alt" in col]
        if alt_col:
            return float(df[alt_col[0]].max())
        else:
            return "No altitude data found"

    elif name == "first_gps_loss_time":
        gps_loss = df[(df['type'] == 'GPS') & (df.get('FixType', 1) < 3)]
        if not gps_loss.empty:
            return int(gps_loss.iloc[0]['time'])
        else:
            return "No GPS loss detected"

    # more names
    else:
        return f"Unknown metric name: {name}"
