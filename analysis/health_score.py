def calculate_health_score(metrics, transactions):

    income = metrics["income"]
    expense = metrics["expense"]
    savings = metrics["savings"]
    cash = metrics["cash"]

    score = 100

    # 1. Savings Rate
    if income > 0:
        savings_rate = savings / income
        if savings_rate < 0.2:
            score -= 20
        elif savings_rate < 0.3:
            score -= 10
    else:
        score -= 30

    # 2. High Cash Usage
    if expense > 0:
        cash_ratio = cash / expense
        if cash_ratio > 0.3:
            score -= 15
        elif cash_ratio > 0.2:
            score -= 10

    # 3. Category Overspending (Food example)
    category_totals = {}

    for t in transactions:
        if t["amount"] < 0:
            cat = t["category"]
            category_totals[cat] = category_totals.get(cat, 0) + abs(t["amount"])

    food_spend = category_totals.get("Food", 0)

    if income > 0:
        if food_spend / income > 0.25:
            score -= 15

    # Clamp score
    score = max(0, min(100, score))

    return round(score)