import json
from datetime import datetime

# Trading Journal Class
class TradingJournal:
    def __init__(self, filename="journal.json"):
        self.filename = filename
        try:
            with open(self.filename, "r") as f:
                self.journal = json.load(f)
        except FileNotFoundError:
            self.journal = []

    def add_trade(self, date, symbol, direction, qty, price, pnl, notes=""):
        trade = {
            "date": date,
            "symbol": symbol.upper(),
            "direction": direction,
            "qty": qty,
            "price": price,
            "pnl": pnl,
            "notes": notes
        }
        self.journal.append(trade)
        self._save()
        print("✅ Trade added successfully!")

    def view_trades(self):
        if not self.journal:
            print("⚠️ No trades yet!")
            return
        for i, trade in enumerate(self.journal, 1):
            print(f"{i}. {trade['date']} | {trade['symbol']} | {trade['direction']} | "
                  f"Qty: {trade['qty']} | Price: {trade['price']} | "
                  f"PnL: {trade['pnl']} | Notes: {trade['notes']}")

    def win_rate(self):
        wins = sum(1 for t in self.journal if t["pnl"] > 0)
        losses = sum(1 for t in self.journal if t["pnl"] <= 0)
        total = wins + losses
        return (wins / total * 100) if total > 0 else 0

    def _save(self):
        with open(self.filename, "w") as f:
            json.dump(self.journal, f, indent=4)


# ------------------ RUNNING THE APP ------------------
if __name__ == "__main__":
    app = TradingJournal()

    while True:
        print("\n📒 Trading Journal Menu")
        print("1. Add Trade")
        print("2. View Trades")
        print("3. Check Win Rate")
        print("4. Exit")
        choice = input("👉 Enter choice: ")

        if choice == "1":
            date = input("Enter Date (YYYY-MM-DD): ") or str(datetime.today().date())
            symbol = input("Enter Symbol: ")
            direction = input("Direction (BUY/SELL): ")
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            pnl = float(input("Profit/Loss: "))
            notes = input("Notes (optional): ")
            app.add_trade(date, symbol, direction, qty, price, pnl, notes)

        elif choice == "2":
            app.view_trades()

        elif choice == "3":
            print(f"📊 Win Rate: {app.win_rate():.2f}%")

        elif choice == "4":
            print("👋 Exiting... Bye!")
            break

        else:
            print("⚠️ Invalid choice! Try again.")
