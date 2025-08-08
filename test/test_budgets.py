from src.budgets import Ledger, Money

ledger = Ledger()
ledger.create_account("Main")
ledger.create_goal("Vacation", target=Money(2000))

main = ledger.get_account("Main")
vacation = ledger.get_account("Vacation")

main.deposit(Money(5000), "Paycheck")
ledger.transfer("Main", "Vacation", Money(500), "Initial savings")

print(main)
print(vacation)