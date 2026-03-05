# settings
BUDGET = 50.00
DAYS_LEFT = 7

# list to store spending history
history = [5.50, 2.00, 12.00] 

# get new input
new_spend = float(input("how much did you spend today? "))
history.append(new_spend)

def get_stats(bal, spend_list, days):
    total_spent = sum(spend_list)
    rem = bal - total_spent
    allowance = bal / days
    
    # average spend per day
    avg_spend = total_spent / len(spend_list)
    
    if avg_spend > 0:
        survival = rem / avg_spend
    else:
        survival = float('inf')
        
    return allowance, rem, survival, total_spent

# run it
limit, left, days_survived, total = get_stats(BUDGET, history, DAYS_LEFT)

print(f"Total spent so far: {total:.2f}")
print(f"Money left: {left:.2f}")
print(f"Days left (based on average): {days_survived:.1f}")

if total > BUDGET:
    print("overspent")
else:
    print("on track")
