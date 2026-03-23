def calculate_health_score(metrics, transactions):

    income = metrics["income"]
    expense = metrics["expense"]
    savings = metrics["savings"]
    cash = metrics["cash"]

    score = 0

    # 1. Savings Score (0–40)
    if income > 0:
        savings_rate = savings / income
        score += min(40, savings_rate * 40)

    # 2. Expense Control (0–30)
    if income > 0:
        expense_ratio = expense / income
        score += max(0, 30 - (expense_ratio * 30))

    # 3. Cash Usage Penalty (0–20)
    if expense > 0:
        cash_ratio = cash / expense
        score += max(0, 20 - (cash_ratio * 20))

    # 4. Category Balance (0–10)
    category_totals = {}

    for t in transactions:
        if t["amount"] < 0:
            cat = t["category"]
            category_totals[cat] = category_totals.get(cat, 0) + abs(t["amount"])

    food_spend = category_totals.get("Food", 0)

    if income > 0:
        food_ratio = food_spend / income
        score += max(0, 10 - (food_ratio * 10))

    return round(score)