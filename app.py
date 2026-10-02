from flask import Flask, render_template, request, jsonify
from database import init_db, get_summary, get_transactions, add_transaction, delete_transaction, get_categories
from recommender import generate_recommendations

app = Flask(__name__)
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/api/summary")
def summary():
    return jsonify(get_summary())

@app.get("/api/transactions")
def transactions():
    return jsonify(get_transactions())

@app.get("/api/categories")
def categories():
    return jsonify(get_categories())

@app.post("/api/transactions")
def create_transaction():
    data = request.get_json(silent=True) or {}
    try:
        amount = float(data.get("amount", 0))
        category = str(data.get("category", "")).strip()
        kind = str(data.get("type", "expense")).strip()
        note = str(data.get("note", "")).strip()
        date = str(data.get("date", "")).strip()
        if amount <= 0 or not category or kind not in ("income", "expense"):
            raise ValueError()
        item = add_transaction(amount, category, kind, note, date)
        return jsonify(item), 201
    except (ValueError, TypeError):
        return jsonify({"error": "Please enter valid transaction details."}), 400

@app.delete("/api/transactions/<int:transaction_id>")
def remove_transaction(transaction_id):
    delete_transaction(transaction_id)
    return jsonify({"success": True})

@app.get("/api/recommendations")
def recommendations():
    return jsonify(generate_recommendations())

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
