import os

# settings
BUDGET = 50.00
DAYS_LEFT = 7
FILE_NAME = "history.txt"

# 1. Load data from file (if it exists)
history = []
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        for line in f:
            history.append(float(line.strip()))

# 2. Get new spend and save it
new_spend = float(input("how much did you spend today? "))
history.append(new_spend)

with open(FILE_NAME, "a") as f:
    f.write(f"{new_spend}\n")

# 3. Calculations
def get_stats(bal, spend_list, days):
    total_spent = sum(spend_list)
    rem = bal - total_spent
    avg_spend = total_spent / len(spend_list)
    
    if avg_spend > 0:
        survival = rem / avg_spend
    else:
        survival = float('inf')
        
    return rem, survival, total_spent

# run it
left, days_survived, total = get_stats(BUDGET, history, DAYS_LEFT)

print(f"--- Session Saved ---")
print(f"Total spent so far: {total:.2f}")
print(f"Money left: {left:.2f}")
print(f"Days left (based on average): {days_survived:.1f}")
