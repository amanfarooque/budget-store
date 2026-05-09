from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"transactions": [], "goals": []}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    data = load_data()
    transactions = data["transactions"]
    goals = data["goals"]

    total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
    balance = total_income - total_expenses

    # Category breakdown for expenses
    categories = {}
    for t in transactions:
        if t["type"] == "expense":
            categories[t["category"]] = categories.get(t["category"], 0) + t["amount"]

    today = datetime.today().strftime("%Y-%m-%d")
    return render_template("index.html",
        today=today,
        transactions=sorted(transactions, key=lambda x: x["date"], reverse=True),
        goals=goals,
        total_income=total_income,
        total_expenses=total_expenses,
        balance=balance,
        categories=categories,
    )

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = load_data()
    transaction = {
        "id": int(datetime.now().timestamp() * 1000),
        "type": request.form["type"],
        "amount": float(request.form["amount"]),
        "category": request.form["category"],
        "description": request.form["description"],
        "date": request.form["date"] or datetime.today().strftime("%Y-%m-%d"),
    }
    data["transactions"].append(transaction)
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete_transaction/<int:tid>", methods=["POST"])
def delete_transaction(tid):
    data = load_data()
    data["transactions"] = [t for t in data["transactions"] if t["id"] != tid]
    save_data(data)
    return redirect(url_for("index"))

@app.route("/add_goal", methods=["POST"])
def add_goal():
    data = load_data()
    goal = {
        "id": int(datetime.now().timestamp() * 1000),
        "name": request.form["name"],
        "target": float(request.form["target"]),
        "saved": float(request.form.get("saved", 0)),
        "deadline": request.form["deadline"],
    }
    data["goals"].append(goal)
    save_data(data)
    return redirect(url_for("index"))

@app.route("/update_goal/<int:gid>", methods=["POST"])
def update_goal(gid):
    data = load_data()
    for g in data["goals"]:
        if g["id"] == gid:
            g["saved"] = float(request.form["saved"])
            break
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete_goal/<int:gid>", methods=["POST"])
def delete_goal(gid):
    data = load_data()
    data["goals"] = [g for g in data["goals"] if g["id"] != gid]
    save_data(data)
    return redirect(url_for("index"))

@app.route("/api/chart_data")
def chart_data():
    data = load_data()
    transactions = data["transactions"]

    # Monthly income vs expenses
    monthly = {}
    for t in transactions:
        month = t["date"][:7]  # YYYY-MM
        if month not in monthly:
            monthly[month] = {"income": 0, "expense": 0}
        monthly[month][t["type"]] += t["amount"]

    months = sorted(monthly.keys())
    income_data = [monthly[m]["income"] for m in months]
    expense_data = [monthly[m]["expense"] for m in months]

    # Category pie data
    categories = {}
    for t in transactions:
        if t["type"] == "expense":
            categories[t["category"]] = categories.get(t["category"], 0) + t["amount"]

    return jsonify({
        "months": months,
        "income": income_data,
        "expenses": expense_data,
        "cat_labels": list(categories.keys()),
        "cat_values": list(categories.values()),
    })

if __name__ == "__main__":
    os.makedirs("templates", exist_ok=True)
    app.run(debug=True, port=5000)
