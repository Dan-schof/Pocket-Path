from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

BUDGET = 50.00
DAYS_LEFT = 7
FILE_NAME = "history.txt"


def get_stats():
    history = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME) as f:
            for line in f:
                if line.strip():
                    amount, category = line.strip().split(",")
                    history.append((float(amount), category))

    total = sum(x[0] for x in history)
    rem = BUDGET - total

    avg_spend = total / len(history) if history else 0
    runway = rem / avg_spend if avg_spend > 0 else DAYS_LEFT

    recent = list(reversed(history[-5:]))

    # category totals
    categories = {}
    for amount, category in history:
        categories[category] = categories.get(category, 0) + amount

    return rem, runway, total, avg_spend, recent, categories


HTML_TEMPLATE = """
<html>
<head>
<title>PocketPath</title>
</head>

<body style="background:#121212;color:white;text-align:center;font-family:sans-serif;">

<h2>PocketPath Report</h2>

<p>Total Spent: £{{ "%.2f"|format(total) }}</p>
<p>Money Left: £{{ "%.2f"|format(rem) }}</p>
<p>Average Daily Spend: £{{ "%.2f"|format(avg) }}</p>
<p>Runway: {{ "%.1f"|format(runway) }} days</p>

<p>
{{ "CRITICAL - SLOW DOWN" if rem < 10 else "ON TRACK" }}
</p>

<hr>

<form method="POST">

<input type="number" step="0.01" name="spend" placeholder="Amount £" required>
<br><br>

<select name="category">
<option value="Food">Food</option>
<option value="Transport">Transport</option>
<option value="Shopping">Shopping</option>
<option value="Entertainment">Entertainment</option>
<option value="Other">Other</option>
</select>

<br><br>

<button type="submit">Add Transaction</button>

</form>

<hr>

<h3>Recent Transactions</h3>

{% for amount, category in recent %}
<p>£{{ "%.2f"|format(amount) }} - {{ category }}</p>
{% endfor %}

<hr>

<h3>Spending Breakdown</h3>

{% for category, amount in categories.items() %}
<p>{{ category }}: £{{ "%.2f"|format(amount) }}</p>
{% endfor %}

</body>
</html>
"""


@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":

        amount = request.form.get("spend")
        category = request.form.get("category")

        if amount and category:
            with open(FILE_NAME, "a") as f:
                f.write(f"{amount},{category}\\n")

    rem, runway, total, avg_spend, recent, categories = get_stats()

    return render_template_string(
        HTML_TEMPLATE,
        rem=rem,
        runway=runway,
        total=total,
        avg=avg_spend,
        recent=recent,
        categories=categories
    )


if __name__ == "__main__":
    app.run()
