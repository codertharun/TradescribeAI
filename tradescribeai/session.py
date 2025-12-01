# trade_scribe/session.py
import json
import os

class SimpleSession:
    def __init__(self, path="session.json"):
        self.path = path
        self.data = {"trades": []}
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"trades": []}

    # backward-compatible API: add_trades and add (both supported)
    def add_trades(self, trades):
        self.data.setdefault("trades", [])
        if isinstance(trades, list):
            self.data["trades"].extend(trades)
        else:
            self.data["trades"].append(trades)
        self.save()

    def add(self, t):
        self.add_trades(t)

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def load_trades(self):
        return self.data.get("trades", [])

