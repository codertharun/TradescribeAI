# trade_scribe/cleaner.py
import pandas as pd

def compute_derived(parsed_notes):
    """
    parsed_notes: list of dicts produced by parser.try_parse_notes
    Returns: pandas.DataFrame with normalized numeric fields and simple derived metrics.
    """
    if not parsed_notes:
        return pd.DataFrame(columns=[
            "raw","date","symbol","qty","buy_price","sell_price","action","realized_pl"
        ])

    df = pd.DataFrame(parsed_notes).copy()

    # ensure columns exist
    for c in ["qty","buy_price","sell_price"]:
        if c not in df.columns:
            df[c] = 0

    # numeric conversions
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(0).astype(int)
    df["buy_price"] = pd.to_numeric(df["buy_price"], errors="coerce").fillna(0.0)
    df["sell_price"] = pd.to_numeric(df["sell_price"], errors="coerce").fillna(0.0)

    # simple realized P/L: (sell - buy) * qty if sell exists else 0
    df["realized_pl"] = ((df["sell_price"] - df["buy_price"]) * df["qty"]).fillna(0.0)

    # ensure date column as string (if missing keep None)
    if "date" in df.columns:
        df["date"] = df["date"].astype(object).where(df["date"].notnull(), None)
    else:
        df["date"] = None

    return df
