# demo.py
import os
from trade_scribe import parser, cleaner, analytics, export, session

def run_demo(notes_path="sample_notes.txt", out_dir="output"):
    notes = parser.load_notes_from_file(notes_path)
    parsed = parser.try_parse_notes(notes)

    # save to session
    sess = session.SimpleSession(path=os.path.join(out_dir, "session_demo.json"))
    sess.add_trades(parsed)

    df = cleaner.compute_derived(parsed)
    daily = analytics.daily_metrics(df)
    overall = analytics.overall_metrics(df)

    os.makedirs(out_dir, exist_ok=True)
    out_xlsx = os.path.join(out_dir, "trades.xlsx")
    export.export_to_excel(df, daily, out_xlsx, extras=overall)

    # console summary
    print("Demo finished. Output:", out_xlsx)
    print("Overall metrics:")
    for k,v in overall.items():
        print(" ", k, ":", v)

    # short recommendations (toy)
    recs = []
    if overall["total_realized_pl"] < 0:
        recs.append("Review exit strategy: overall P/L negative.")
    else:
        recs.append("P/L positive — review high-performing symbols.")

    return out_xlsx, recs

if __name__ == "__main__":
    run_demo()
