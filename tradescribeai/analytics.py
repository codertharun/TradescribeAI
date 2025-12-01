# trade_scribe/analytics.py
import pandas as pd
from typing import Dict

def daily_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate by date (string) for simple daily metrics."""
    if df.empty or "date" not in df.columns:
        return pd.DataFrame()
    df2 = df.copy()
    df2["date"] = df2["date"].fillna("unknown")
    agg = df2.groupby("date").agg(
        trades_count=("raw", "count"),
        total_qty=("qty", "sum"),
        total_realized_pl=("realized_pl", "sum"),
    ).reset_index()
    return agg

def overall_metrics(df: pd.DataFrame) -> Dict:
    if df.empty:
        return {"total_trades": 0, "total_qty": 0, "total_realized_pl": 0.0}
    return {
        "total_trades": int(df.shape[0]),
        "total_qty": int(df["qty"].sum()),
        "total_realized_pl": float(df["realized_pl"].sum()),
    }
