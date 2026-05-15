from neuralintents.assistants import BasicAssistant
from datetime import datetime

finances = {"income": [], "expenses": [], "balance": 0.0}


def check_balance():
    return f"💰 Current Balance: ${finances['balance']:.2f}"


def add_income():
    try:
        amount = float(input("Enter income amount: $"))
        description = input("Description (optional): ") or "Income"

        finances["income"].append({
            "amount": amount,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

        finances["balance"] += amount
        return f"✅ Added ${amount:.2f} — New balance: ${finances['balance']:.2f}"

    except ValueError:
        return "❌ Invalid amount. Please enter a number."


def add_expense():
    try:
        amount = float(input("Enter expense amount: $"))
        category = input("Category (e.g., food, rent, utilities): ") or "General"

        finances["expenses"].append({
            "amount": amount,
            "category": category,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

        finances["balance"] -= amount
        return f"✅ Recorded ${amount:.2f} expense — New balance: ${finances['balance']:.2f}"

    except ValueError:
        return "❌ Invalid amount. Please enter a number."


def show_summary():
    total_income = sum(item["amount"] for item in finances["income"])
    total_expenses = sum(item["amount"] for item in finances["expenses"])

    lines = []
    lines.append("=" * 40)
    lines.append("📊 FINANCIAL SUMMARY")
    lines.append("=" * 40)
    lines.append(f"Total Income: ${total_income:.2f}")
    lines.append(f"Total Expenses: ${total_expenses:.2f}")
    lines.append(f"Net Balance: ${finances['balance']:.2f}")

    if finances["expenses"]:
        lines.append("")
        lines.append("Expenses by Category:")

        categories = {}
        for exp in finances["expenses"]:
            cat = exp["category"]
            categories[cat] = categories.get(cat, 0) + exp["amount"]

        for cat, amount in categories.items():
            lines.append(f" - {cat}: ${amount:.2f}")

    lines.append("=" * 40)
    return "\n".join(lines)


method_mappings = {
    "balance": check_balance,
    "add_income": add_income,
    "add_expense": add_expense,
    "summary": show_summary
}


assistant = BasicAssistant('intents.json', method_mappings=method_mappings)
assistant.fit_model(epochs=50)
assistant.save_model()

print("\n🤖 Financial Assistant Ready! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Goodbye! 👋")
        break

    if user_input:
        print(assistant.process_input(user_input))
