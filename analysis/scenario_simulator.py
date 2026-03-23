def simulate_savings(transactions, metrics, reduction_amount, category):

    new_transactions = []

    for t in transactions:
        new_t = t.copy()

        # Reduce only selected category
        if t["category"] == category and t["amount"] < 0:
            reduction = min(abs(t["amount"]), reduction_amount)
            new_t["amount"] = t["amount"] + reduction  # less negative

        new_transactions.append(new_t)

    # Recalculate metrics
    income = 0
    expense = 0
    cash = 0

    for t in new_transactions:
        if t["amount"] > 0:
            income += t["amount"]
        else:
            expense += abs(t["amount"])
            if t["category"] == "Cash Withdrawal":
                cash += abs(t["amount"])

    savings = income - expense

    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "cash": round(cash, 2),
        "savings": round(savings, 2)
    }

def simulate_multi_savings(transactions, metrics, reductions):

    new_transactions = []

    # Track how much reduction is left per category
    remaining_reduction = reductions.copy()

    for t in transactions:
        new_t = t.copy()

        if t["amount"] < 0:  # only expenses
            cat = t["category"]

            if cat in remaining_reduction and remaining_reduction[cat] > 0:

                available_reduction = remaining_reduction[cat]

                # Reduce only up to transaction amount
                reduction = min(abs(t["amount"]), available_reduction)

                new_t["amount"] = t["amount"] + reduction

                # Update remaining reduction
                remaining_reduction[cat] -= reduction

        new_transactions.append(new_t)

    # 🔥 Recalculate metrics (same logic as main system)
    income = 0
    expense = 0
    cash = 0

    for t in new_transactions:
        amount = t["amount"]

        if amount > 0:
            income += amount
        else:
            expense += abs(amount)

            if t["category"] == "Cash Withdrawal":
                cash += abs(amount)

    savings = income - expense

    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "cash": round(cash, 2),
        "savings": round(savings, 2)
    }