# demo.py
import argparse
import logging
import os
from trade_scribe import parser, cleaner, analytics, exporter, session

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("tradescribe")

def run(notes_path: str = "sample_notes.txt", out_dir: str = "output"):
    notes = parser.load_notes_from_file(notes_path)
    parsed = parser.try_parse_notes(notes)

    os.makedirs(out_dir, exist_ok=True)
    sess = session.SimpleSession(path=os.path.join(out_dir, "session_demo.json"))
    sess.add_trades(parsed)

    df = cleaner.compute_derived(parsed)
    daily = analytics.daily_metrics(df)
    overall = analytics.overall_metrics(df)

    out_xlsx = os.path.join(out_dir, "trades.xlsx")
    exporter.export_to_excel(df, daily, out_xlsx, extras=overall)

    logger.info("Demo finished. Output: %s", out_xlsx)
    logger.info("Overall metrics: %s", overall)
    return out_xlsx

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--notes", default="sample_notes.txt")
    p.add_argument("--out", default="output")
    args = p.parse_args()
    run(notes_path=args.notes, out_dir=args.out)
