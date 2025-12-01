# tests/test_parser.py
from trade_scribe import parser

def test_simple_buy_line():
    line = "2025-11-27 10:15 TCS BUY 3450.5 x 10"
    parsed = parser.try_parse_note(line)
    assert parsed["symbol"] == "TCS"
    assert parsed["action"] == "buy"
    assert parsed["qty"] == 10
    assert parsed["buy_price"] == 3450.5

def test_bought_pattern():
    line = "Bought 100 shares of INFY @ 1500 exited @ 1525"
    parsed = parser.try_parse_note(line)
    assert parsed["symbol"] == "INFY"
    assert parsed["qty"] == 100
    assert float(parsed["buy_price"]) == 1500.0
