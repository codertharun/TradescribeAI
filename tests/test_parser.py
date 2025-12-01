# tests/test_parser.py
from trade_scribe import parser

def test_simple_line():
    note = "2025-11-27 10:15 TCS BUY 3450.5 x 10"
    p = parser.try_parse_note(note)
    assert p.get("symbol") == "TCS"
    assert p.get("qty") == 10
    assert isinstance(p.get("buy_price"), float)

def test_bought_pattern():
    note = "Bought 100 shares of INFY @ 1500 exited @ 1525 qty 100 pl 2500"
    p = parser.try_parse_note(note)
    assert p.get("symbol") == "INFY"
    assert int(p.get("qty")) == 100
    assert float(p.get("buy_price")) == 1500.0
