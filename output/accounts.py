import datetime

def get_share_price(symbol):
    prices = {"AAPL": 170.0, "TSLA": 250.0, "GOOGL": 120.0}
    return prices.get(symbol, None)

class Account:
    def __init__(self, initial_deposit=0):
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative")
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transactions.append({"type": "deposit", "amount": amount, "timestamp": datetime.datetime.now()})

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transactions.append({"type": "withdrawal", "amount": amount, "timestamp": datetime.datetime.now()})

    def buy(self, symbol, quantity, price):
        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive")
        cost = quantity * price
        if cost > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transactions.append({"type": "buy", "symbol": symbol, "quantity": quantity, "price": price, "timestamp": datetime.datetime.now()})

    def sell(self, symbol, quantity, price):
        if quantity <= 0 or price <= 0:
            raise ValueError("Quantity and price must be positive")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares")
        self.balance += quantity * price
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({"type": "sell", "symbol": symbol, "quantity": quantity, "price": price, "timestamp": datetime.datetime.now()})

    def get_portfolio_value(self):
        portfolio_value = self.balance
        for symbol, quantity in self.holdings.items():
            price = get_share_price(symbol)
            if price is not None:
                portfolio_value += quantity * price
        return portfolio_value

    def get_profit_loss(self):
        return self.get_portfolio_value() - (self.balance - self.get_portfolio_value() + sum(t['amount'] for t in self.transactions if t['type'] == 'deposit'))


    def get_holdings(self):
        return self.holdings

    def get_transactions(self):
        return self.transactions

    def __str__(self):
        return f"Balance: {self.balance:.2f}\nHoldings: {self.holdings}\nTransactions: {self.transactions}"