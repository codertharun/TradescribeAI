# trade_scribe/parser.py
from __future__ import annotations
import re
from typing import Dict, Optional

BUY_WORDS = ["buy", "bought", "long"]
SELL_WORDS = ["sell", "sold", "exit", "exited"]

def _safe_float(x: Optional[str]) -> float:
    """Convert x to float if possible; otherwise return 0.0."""
    if x is None:
        return 0.0
    try:
        return float(str(x).replace(",", ""))
    except Exception:
        return 0.0

def try_parse_note(line: str) -> Dict[str, object]:
    """
    Parse a single free-form trading note and return a normalized dict.
    Keys:
      - raw: original text
      - date: optional date string
      - symbol: optional ticker (A-Z)
      - qty: int (defaults 0)
      - buy_price: float (defaults 0.0)
      - sell_price: float (defaults 0.0)
      - action: 'buy' / 'sell' / None
    """
    text = (line or "").strip()
    out = {
        "raw": text,
        "date": None,
        "symbol": None,
        "qty": 0,
        "buy_price": 0.0,
        "sell_price": 0.0,
        "action": None,
    }
    if not text:
        return out

    low = text.lower()
    # symbol: 2-6 uppercase letters
    sym = re.search(r"\b([A-Z]{2,6})\b", text)
    if sym:
        out["symbol"] = sym.group(1)

    # action detection
    for w in BUY_WORDS:
        if w in low:
            out["action"] = "buy"
            break
    if out["action"] is None:
        for w in SELL_WORDS:
            if w in low:
                out["action"] = "sell"
                break

    # qty: last small integer token (1-3 digits)
    qty_tokens = re.findall(r"\b(\d{1,3})\b", text)
    if qty_tokens:
        try:
            out["qty"] = int(qty_tokens[-1])
        except Exception:
            out["qty"] = 0

    # price tokens (decimals allowed)
    price_tokens = re.findall(r"([0-9]+(?:\.[0-9]+)?)", text.replace(",", ""))
    price_vals = [_safe_float(p) for p in price_tokens]

    if out["action"] == "buy":
        out["buy_price"] = price_vals[0] if len(price_vals) >= 1 else 0.0
        out["sell_price"] = price_vals[1] if len(price_vals) >= 2 else 0.0
    elif out["action"] == "sell":
        out["sell_price"] = price_vals[0] if len(price_vals) >= 1 else 0.0
    else:
        if len(price_vals) >= 2:
            out["buy_price"], out["sell_price"] = price_vals[0], price_vals[1]
        elif len(price_vals) == 1:
            out["buy_price"] = price_vals[0]

    return out

def try_parse_notes(lines):
    """Parse list[str] -> list[dict]."""
    return [try_parse_note(l) for l in lines]
