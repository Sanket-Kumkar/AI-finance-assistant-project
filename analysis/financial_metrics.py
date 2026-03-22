def calculate_metrics(transactions):
    income = 0
    expense = 0
    cash = 0

    for t in transactions:
        amount = t["amount"]
        desc = t["description"]

        if amount > 0:
            income += amount
        else:
            if "atm" in desc:
                cash += abs(amount)
            else:
                expense += abs(amount)

    savings = income - expense

    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "cash": round(cash, 2),
        "savings": round(savings, 2)
    }