# engine.py

def calculate_stats(budget, spend_list, days_left):
    total_spent = sum(spend_list)
    remaining = budget - total_spent
    
    # Calculate average burn rate
    if len(spend_list) > 0:
        avg_spend = total_spent / len(spend_list)
    else:
        avg_spend = 0
        
    # How many days until you hit £0
    if avg_spend > 0:
        runway = remaining / avg_spend
    else:
        runway = float('inf')
        
    return remaining, runway, total_spent
