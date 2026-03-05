# --- Configuration (Constants) ---
BUDGET_LIMIT = 50.00
DAYS_UNTIL_ALLOWANCE = 7

# --- User Input (Variables) ---
spent_today = 6.50 

# --- Logic Engine ---
def calculate_status(balance, spend, days_left):
    daily_allowance = balance / days_left
    remaining_balance = balance - spend
    
    # Logic to prevent DivisionByZero error
    if spend > 0:
        survival_days = remaining_balance / spend
    else:
        survival_days = float('inf')
        
    return daily_allowance, remaining_balance, survival_days

# --- Execution ---
allowance, rem, survival = calculate_status(BUDGET_LIMIT, spent_today, DAYS_UNTIL_ALLOWANCE)

# --- Output ---
print(f"Daily Allowance: £{allowance:.2f}")
print(f"Remaining: £{rem:.2f}")
print(f"Survival: {survival:.1f} days")

if spent_today > allowance:
    print("STATUS: OVERSPENT")
else:
    print("STATUS: WITHIN LIMIT")
