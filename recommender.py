from database import get_summary, get_transactions

def generate_recommendations():
    summary = get_summary()
    txns = get_transactions()
    income = summary["income"]
    expense = summary["expense"]
    balance = summary["balance"]
    by_category = summary["by_category"]

    tips = []

    if not txns:
        return [{
            "title": "Start your money journey",
            "message": "Add a few income and expense transactions. PocketSmart AI will analyze your spending and create personalized suggestions.",
            "level": "info"
        }]

    if income > 0:
        expense_ratio = expense / income
        if expense_ratio >= 0.9:
            tips.append({
                "title": "High spending alert",
                "message": f"Your expenses are about {expense_ratio*100:.0f}% of recorded income. Consider reducing non-essential spending and setting a weekly limit.",
                "level": "warning"
            })
        elif expense_ratio <= 0.6:
            tips.append({
                "title": "Good saving opportunity",
                "message": f"Your recorded expenses are about {expense_ratio*100:.0f}% of income. You could direct part of the remaining amount toward savings.",
                "level": "success"
            })

    if by_category:
        top = by_category[0]
        if expense > 0 and top["total"] / expense >= 0.35:
            tips.append({
                "title": f"{top['category']} is your biggest category",
                "message": f"{top['category']} accounts for about {top['total']/expense*100:.0f}% of your recorded expenses. Review this category for possible savings.",
                "level": "warning"
            })

    food = next((x["total"] for x in by_category if x["category"] == "Food"), 0)
    shopping = next((x["total"] for x in by_category if x["category"] == "Shopping"), 0)

    if food > 0:
        tips.append({
            "title": "Food budget idea",
            "message": "Try planning meals and setting a weekly food budget. Small daily reductions can add up over a month.",
            "level": "tip"
        })

    if shopping > 0:
        tips.append({
            "title": "Smart shopping",
            "message": "Before non-essential purchases, use a 24-hour wait rule and compare alternatives.",
            "level": "tip"
        })

    if balance < 0:
        tips.append({
            "title": "Negative balance",
            "message": "Recorded expenses are higher than recorded income. Review recent expenses and prioritize essential payments.",
            "level": "danger"
        })

    tips.append({
        "title": "PocketSmart rule",
        "message": "A simple starting framework is to plan needs first, savings second, and wants with the remaining amount.",
        "level": "info"
    })
    return tips[:6]
