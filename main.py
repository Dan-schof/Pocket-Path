import engine
import os

BUDGET = 50.00
DAYS_LEFT = 7
FILE_NAME = "history.txt"

# Load history
history = []
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        history = [float(line.strip()) for line in f]

# Get user data
new_spend = float(input("Spend today: "))
history.append(new_spend)

# Save to file
with open(FILE_NAME, "a") as f:
    f.write(f"{new_spend}\n")

# CALL THE ENGINE
rem, days_left, total = engine.calculate_stats(BUDGET, history, DAYS_LEFT)

print(f"\n--- PocketPath Report ---")
print(f"Balance: £{rem:.2f}")
print(f"Runway: {days_left:.1f} days")
print(f"Status: {'CRITICAL' if rem < 10 else 'HEALTHY'}")average): {days_survived:.1f}")
