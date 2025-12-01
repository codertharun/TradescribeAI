# trade_scribe/exporter.py
from typing import Optional, Dict
import os
import pandas as pd

def export_to_excel(trades_df: pd.DataFrame, daily_df: pd.DataFrame, out_path: str, extras: Optional[Dict]=None) -> str:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        trades_df.to_excel(writer, sheet_name="trades", index=False)
        if daily_df is not None and not daily_df.empty:
            daily_df.to_excel(writer, sheet_name="daily", index=False)
        if extras:
            pd.DataFrame([extras]).to_excel(writer, sheet_name="summary", index=False)
    return out_path
