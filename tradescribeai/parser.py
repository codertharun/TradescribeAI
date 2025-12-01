# trade_scribe/parser.py
import re

BUY_WORDS = ["buy", "bought", "long"]
SELL_WORDS = ["sell", "sold", "exit", "exited"]

def _safe_float(x):
    """Return float(x) or 0.0 if conversion fails or x is None."""
    try:
        if x is None:
            return 0.0
        return float(str(x).replace(",", ""))
    except Exception:
        return 0.0

def try_parse_note(line):
    """
    Parse a single free-form intraday trading note and return a dict with:
    raw, date (string YYYY-MM-DD or None), symbol, qty (int), buy_price (float),
    sell_price (float), action
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

    # symbol: all-caps 2-6 letters
    m_sym = re.search(r"\b([A-Z]{2,6})\b", text)
    if m_sym:
        out["symbol"] = m_sym.group(1)

    # action: buy or sell
    for w in BUY_WORDS:
        if w in low:
            out["action"] = "buy"
            break
    if out["action"] is None:
        for w in SELL_WORDS:
            if w in low:
                out["action"] = "sell"
                break

    # qty: choose the last small integer token (1-3 digits).
    qty_tokens = re.findall(r"\b(\d{1,3})\b", text)
    if qty_tokens:
        try:
            out["qty"] = int(qty_tokens[-1])
        except Exception:
            out["qty"] = 0

    # price tokens: capture decimal numbers (ignore commas)
    price_tokens = re.findall(r"([0-9]+(?:\.[0-9]+)?)", text.replace(",", ""))
    price_vals = [_safe_float(p) for p in price_tokens]

    # assign prices based on action with safe fallbacks to 0.0
    if out["action"] == "buy":
        out["buy_price"] = price_vals[0] if len(price_vals) >= 1 else 0.0
        out["sell_price"] = price_vals[1] if len(price_vals) >= 2 else 0.0
    elif out["action"] == "sell":
        out["sell_price"] = price_vals[0] if len(price_vals) >= 1 else 0.0
    else:
        # no action known: if two prices, treat as buy then sell; if one price treat as buy
        if len(price_vals) >= 2:
            out["buy_price"], out["sell_price"] = price_vals[0], price_vals[1]
        elif len(price_vals) == 1:
            out["buy_price"] = price_vals[0]

    # final normalization guarantees (int/float types)
    try:
        out["qty"] = int(out["qty"])
    except Exception:
        out["qty"] = 0
    out["buy_price"] = _safe_float(out.get("buy_price"))
    out["sell_price"] = _safe_float(out.get("sell_price"))

    return out

def try_parse_notes(lines):
    """Parse multiple trading notes (list of strings) -> list of dicts."""
    return [try_parse_note(l) for l in lines]

def load_notes_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return [ln.strip() for ln in f.readlines()]
