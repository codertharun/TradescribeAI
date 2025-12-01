# trade_scribe/session.py
import json
import os
from typing import List, Dict

class SimpleSession:
    def __init__(self, path: str = "session.json"):
        self.path = path
        self.data = {"trades": []}
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"trades": []}

    def add_trades(self, trades):
        self.data.setdefault("trades", [])
        if isinstance(trades, list):
            self.data["trades"].extend(trades)
        else:
            self.data["trades"].append(trades)
        self.save()

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def load_trades(self) -> List[Dict]:
        return self.data.get("trades", [])
