# demo.py - CLI-driven demo with logging and basic arg parsing
import os
import logging
import argparse
from trade_scribe import parser, cleaner, analytics, export, session

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("tradescribe-demo")

def run_demo(notes_path="sample_notes.txt", out_dir="output"):
    logger.info("Loading notes from %s", notes_path)
    notes = parser.load_notes_from_file(notes_path)
    parsed = parser.try_parse_notes(notes)

    sess = session.SimpleSession(path=os.path.join(out_dir, "session_demo.json"))
    sess.add_trades(parsed)

    df = cleaner.compute_derived(parsed)
    daily = analytics.daily_metrics(df)
    overall = analytics.overall_metrics(df)

    os.makedirs(out_dir, exist_ok=True)
    out_xlsx = os.path.join(out_dir, "trades.xlsx")
    export.export_to_excel(df, daily, out_xlsx, extras=overall)

    logger.info("Demo finished. Output: %s", out_xlsx)
    logger.info("Overall metrics: %s", overall)
    return out_xlsx, overall

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Run TradeScribe demo")
    p.add_argument("--notes", default="sample_notes.txt", help="Path to notes file")
    p.add_argument("--out", default="output", help="Output folder")
    args = p.parse_args()
    run_demo(notes_path=args.notes, out_dir=args.out)
