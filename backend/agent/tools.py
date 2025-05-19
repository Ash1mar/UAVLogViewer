from langchain.tools import tool
from services.telemetry_store import load_log

@tool
def get_max_altitude(log_id: str) -> float:
    """Returns the maximum altitude recorded in the flight log."""
    df = load_log(log_id)
    return float(df["Alt"].max())

@tool
def first_gps_loss_time(log_id: str) -> str:
    """Returns the timestamp of first GPS loss event in the flight."""
    df = load_log(log_id)
    loss = df[(df['type'] == 'GPS') & (df.get('Status', 1) < 3)]
    if not loss.empty:
        return str(int(loss.iloc[0]['time']))
    return "No GPS loss detected"

@tool
def get_max_voltage(log_id: str) -> float:
    """Returns the maximum battery voltage."""
    df = load_log(log_id)
    return float(df["Volt"].max())

@tool
def get_max_current(log_id: str) -> float:
    """Returns the maximum battery current."""
    df = load_log(log_id)
    return float(df["Curr"].max())

@tool
def get_max_temp(log_id: str) -> float:
    """Returns the maximum temperature from BAT/Temp."""
    df = load_log(log_id)
    return float(df["Temp"].max())

@tool
def get_flight_duration(log_id: str) -> float:
    """Returns the total flight time in seconds."""
    df = load_log(log_id)
    t1 = df["time"].min()
    t2 = df["time"].max()
    return float((t2 - t1) / 1000000.0)  # microseconds to seconds

@tool
def list_critical_errors(log_id: str) -> str:
    """Returns a list of critical ERR messages."""
    df = load_log(log_id)
    errs = df[df["type"] == "ERR"]
    if errs.empty:
        return "No errors found"
    return "\n".join(str(e) for e in errs["Rsn"].unique())

@tool
def detect_anomalies(log_id: str) -> str:
    """Analyze flight log and report any anomalies in battery, GPS or flight pattern."""
    df = load_log(log_id)
    results = []

    try:
        # Voltage to low
        if "Volt" in df.columns and df["Volt"].min() < 10.0:
            results.append("⚠️ Battery voltage dropped below 10V")

        # Current
        if "Curr" in df.columns and df["Curr"].max() > 50.0:
            results.append("⚠️ Current draw exceeded 50A")

        # GPS Fix Lost
        if "type" in df.columns and "Status" in df.columns:
            gps_loss = df[(df["type"] == "GPS") & (df["Status"] < 3)]
            if not gps_loss.empty:
                results.append("⚠️ GPS signal was lost during flight")

        # 飞行高度大幅下降
        if "Alt" in df.columns:
            alt = df["Alt"]
            drops = (alt.shift(1) - alt) > 20  # 相邻时间点下降超过 20m
            if drops.any():
                results.append("⚠️ Sudden altitude drop detected")

        if not results:
            return "✅ No obvious anomalies found"
        return "\n".join(results)

    except Exception as e:
        return f"Error analyzing anomalies: {str(e)}"

