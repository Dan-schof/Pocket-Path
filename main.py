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

    categories = {}
    for amount, category in history:
        categories[category] = categories.get(category, 0) + amount

    return rem, runway, total, avg_spend, recent, categories


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>

<head>

<title>PocketPath</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

body{
background:#0f172a;
color:white;
font-family:Arial, sans-serif;
display:flex;
justify-content:center;
align-items:center;
min-height:100vh;
margin:0;
}

.card{
background:#1e293b;
padding:30px;
border-radius:15px;
width:350px;
box-shadow:0 10px 25px rgba(0,0,0,0.4);
text-align:center;
}

h2{
margin-top:0;
}

.stat{
font-size:18px;
margin:8px 0;
}

input, select{
width:90%;
padding:10px;
border-radius:8px;
border:none;
margin-top:8px;
}

button{
background:#2563eb;
color:white;
border:none;
padding:10px 20px;
border-radius:8px;
margin-top:12px;
cursor:pointer;
}

button:hover{
background:#1d4ed8;
}

.section{
margin-top:20px;
padding-top:15px;
border-top:1px solid #334155;
}

.transaction{
margin:4px 0;
}

</style>

</head>


<body>

<div class="card">

<h2>📊 PocketPath</h2>

<div class="stat">Total Spent: £{{ "%.2f"|format(total) }}</div>
<div class="stat">Money Left: £{{ "%.2f"|format(rem) }}</div>
<div class="stat">Average Daily Spend: £{{ "%.2f"|format(avg) }}</div>
<div class="stat">Runway: {{ "%.1f"|format(runway) }} days</div>

<p>
{{ "⚠ CRITICAL - SLOW DOWN" if rem < 10 else "✅ ON TRACK" }}
</p>


<div class="section">

<form method="POST">

<input type="number" step="0.01" name="spend" placeholder="Amount £" required>

<select name="category">

<option value="Food">Food</option>
<option value="Transport">Transport</option>
<option value="Shopping">Shopping</option>
<option value="Entertainment">Entertainment</option>
<option value="Other">Other</option>

</select>

<br>

<button type="submit">Add Transaction</button>

</form>

</div>


<div class="section">

<h3>Recent Transactions</h3>

{% for amount, category in recent %}
<div class="transaction">£{{ "%.2f"|format(amount) }} - {{ category }}</div>
{% endfor %}

</div>


<div class="section">

<h3>Spending Breakdown</h3>

{% for category, amount in categories.items() %}
<div class="transaction">{{ category }}: £{{ "%.2f"|format(amount) }}</div>
{% endfor %}

</div>


</div>

</body>

</html>
"""


@app.route("/", methods=["GET", "POST"])
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
