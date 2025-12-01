# trade_scribe/analytics.py
import pandas as pd

def daily_metrics(df):
    """
    df: DataFrame from compute_derived
    Returns: DataFrame with daily aggregated metrics (by date)
    """
    if df.empty or "date" not in df.columns:
        return pd.DataFrame()

    # if no date values, return empty
    df2 = df.copy()
    df2["date"] = df2["date"].fillna("unknown")
    agg = df2.groupby("date").agg(
        trades_count=("raw", "count"),
        total_qty=("qty", "sum"),
        total_realized_pl=("realized_pl", "sum")
    ).reset_index()
    return agg

def overall_metrics(df):
    """
    Returns a simple dict of overall metrics.
    """
    if df.empty:
        return {"total_trades": 0, "total_qty": 0, "total_realized_pl": 0.0}

    return {
        "total_trades": int(df.shape[0]),
        "total_qty": int(df["qty"].sum()),
        "total_realized_pl": float(df["realized_pl"].sum())
    }
