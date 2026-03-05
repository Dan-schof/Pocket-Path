import engine
import os

# settings
BUDGET = 50.00
DAYS_LEFT = 7
FILE_NAME = "history.txt"

# 1. Load data from file
history = []
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        # this is a list comprehension - it loads everything in one line
        history = [float(line.strip()) for line in f]

# 2. Get new spend and save it
new_spend = float(input("how much did you spend today? "))
history.append(new_spend)

with open(FILE_NAME, "a") as f:
    f.write(f"{new_spend}\n")

# 3. Call the engine module
rem, runway, total = engine.calculate_stats(BUDGET, history, DAYS_LEFT)

# 4. Results
print(f"\n--- PocketPath Report ---")
print(f"Total spent: £{total:.2f}")
print(f"Money left: £{rem:.2f}")
print(f"Days left at this rate: {runway:.1f}")

if rem < 10:
    print("STATUS: CRITICAL - SLOW DOWN")
else:
    print("STATUS: ON TRACK")
