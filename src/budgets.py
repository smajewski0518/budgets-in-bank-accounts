from datetime import datetime

# A small value object that wraps currency + amount.
class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        assert self.currency == other.currency
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other):
        assert self.currency == other.currency
        return Money(self.amount - other.amount, self.currency)

    def __repr__(self):
        return f"{self.currency} {self.amount:.2f}"

# A generic account that tracks a balance and holds transactions.
class Account:
    def __init__(self, name: str):
        self.name = name
        self.balance = Money(0)
        self.transactions = []

    def deposit(self, money: Money, note: str = ""):
        self.balance += money
        self.transactions.append(Transaction(money, "deposit", note))

    def withdraw(self, money: Money, note: str = ""):
        if self.balance.amount >= money.amount:
            self.balance -= money
            self.transactions.append(Transaction(money, "withdraw", note))
        else:
            raise ValueError("Insufficient funds")

    def __repr__(self):
        return f"{self.name}: {self.balance}"

# A simple class to track money movement.
class Transaction:
    def __init__(self, amount: Money, type_: str, note: str = ""):
        self.amount = amount
        self.type = type_  # "deposit", "withdraw", "transfer"
        self.date = datetime.now()
        self.note = note

    def __repr__(self):
        return f"{self.date.isoformat()} | {self.type.upper()} | {self.amount} | {self.note}"

# Specialized account for saving toward something.
class GoalAccount(Account):
    def __init__(self, name: str, target: Money, deadline: datetime = None):
        super().__init__(name)
        self.target = target
        self.deadline = deadline

    def progress(self):
        return self.balance.amount / self.target.amount

    def is_complete(self):
        return self.balance.amount >= self.target.amount

    def __repr__(self):
        percent = self.progress() * 100
        return f"{self.name}: {self.balance} (Goal: {self.target}, {percent:.1f}%)"

# Manages accounts and goals and transfers money between them.
class Ledger:
    def __init__(self):
        self.accounts = {}

    def create_account(self, name: str):
        #TODO check if account already exists
        account = Account(name)
        self.accounts[name] = account
        return account

    def create_goal(self, name: str, target: Money = None, deadline: datetime = None):
        #TODO check if account already exists
        account = GoalAccount(name, target, deadline)
        self.accounts[name] = account
        return account

    def get_account(self, name: str) -> Account:
        return self.accounts[name]

    def transfer(self, from_name: str, to_name: str, money: Money, note: str = ""):
        from_account = self.get_account(from_name)
        to_account = self.get_account(to_name)
        from_account.withdraw(money, f"Transfer to {to_name}: {note}")
        to_account.deposit(money, f"Transfer from {from_name}: {note}")
