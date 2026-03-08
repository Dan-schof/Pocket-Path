rom flask import Flask, render_template_string, request
import os

app = Flask(__name__)

BUDGET = 50.00
DAYS_LEFT = 7
FILE_NAME = "history.txt"


def get_stats():
    history = []

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            history = [float(line.strip()) for line in f.readlines() if line.strip()]

    total = sum(history)
    rem = BUDGET - total

    avg_spend = total / len(history) if history else 0
    runway = rem / avg_spend if avg_spend > 0 else DAYS_LEFT

    recent = history[-5:][::-1] # last 5 transactions, newest first

    return rem, runway, total, avg_spend, recent


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>PocketPath Control</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body {
    font-family: sans-serif;
    background: #121212;
    color: white;
    text-align: center;
}

.card {
    background: #1e1e1e;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #333;
    width: 90%;
    max-width: 400px;
    margin: auto;
}

.stat {
    font-size: 1.4em;
    margin: 10px 0;
}

.critical {
    color: #ff4444;
    font-weight: bold;
}

.ontrack {
    color: #00c851;
    font-weight: bold;
}

input {
    padding: 10px;
    border-radius: 5px;
    border: none;
    width: 80%;
}

button {
    padding: 10px 20px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
    margin-top: 10px;
}

.transactions {
    margin-top: 20px;
    text-align: left;
}
</style>
</head>

<body>

<div class="card">

<h2>PocketPath Report</h2>

<div class="stat">Total Spent: £{{ "%.2f"|format(total) }}</div>
<div class="stat">Money Left: £{{ "%.2f"|format(rem) }}</div>
<div class="stat">Average Daily Spend: £{{ "%.2f"|format(avg) }}</div>
<div class="stat">Runway: {{ "%.1f"|format(runway) }} days</div>

<p class="{{ 'critical' if rem < 10 else 'ontrack' }}">
STATUS: {{ "CRITICAL - SLOW DOWN" if rem < 10 else "ON TRACK" }}
</p>

<hr style="border:0.5px solid #333; margin:20px 0;">

<form method="POST">
<input type="number" step="0.01" name="spend" placeholder="Enter amount £">
<br>
<button type="submit">Update Spend</button>
</form>

<div class="transactions">
<h3>Recent Transactions</h3>

{% if recent %}
<ul>
{% for t in recent %}
<li>£{{ "%.2f"|format(t) }}</li>
{% endfor %}
</ul>
{% else %}
<p>No transactions yet</p>
{% endif %}

</div>

</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        new_spend = request.form.get("spend")

        if new_spend:
            with open(FILE_NAME, "a") as f:
                f.write(f"{new_spend}\n")

    rem, runway, total, avg_spend, recent = get_stats()

    return render_template_string(
        HTML_TEMPLATE,
        rem=rem,
        runway=runway,
        total=total,
        avg=avg_spend,
        recent=recent
    )


if __name__ == "__main__":
    app.run()
