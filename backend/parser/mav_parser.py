# backend/parser/mav_parser.py
from pymavlink import mavutil
import pandas as pd


def parse_bin(filepath: str) -> pd.DataFrame:
    """
    analysis .bin file，return DataFrame（timestamp+normally words）
    """
    mav = mavutil.mavlink_connection(filepath, dialect="ardupilotmega")
    msgs = []

    while True:
        msg = mav.recv_match(blocking=False)
        if msg is None:
            break
        msg_type = msg.get_type()
        if msg_type in ['GPS', 'ATT', 'AHR2', 'BAT', 'BARO', 'CTUN', 'NTUN', 'MODE', 'ERR']:
            d = msg.to_dict()
            d['type'] = msg_type
            d['time'] = getattr(msg, 'TimeUS', None) or getattr(msg, 'time_boot_ms', None)
            msgs.append(d)

    df = pd.DataFrame(msgs)
    df = df.sort_values(by="time").reset_index(drop=True)
    return df
