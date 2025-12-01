# trade_scribe/export.py
import os
import pandas as pd

def export_to_excel(trades_df, daily_df, out_path, extras=None):
    """
    trades_df: DataFrame of parsed trades
    daily_df: aggregated daily metrics (DataFrame)
    out_path: path to output excel file
    extras: optional dict to include as a summary sheet
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
        trades_df.to_excel(writer, sheet_name="trades", index=False)
        if daily_df is not None and not daily_df.empty:
            daily_df.to_excel(writer, sheet_name="daily", index=False)
        # write extras summary
        if extras:
            df = pd.DataFrame.from_dict([extras])
            df.to_excel(writer, sheet_name="summary", index=False)
    return out_path
