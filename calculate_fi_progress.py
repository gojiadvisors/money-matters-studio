# FIRE Progress Calculator

def calculate_fire_number(target_annual_expenses, withdrawal_rate=0.04):
    return target_annual_expenses / withdrawal_rate

def estimate_years_to_fi(current_net_worth, annual_savings, annual_return, fire_number, merit_growth=0.0):
    if current_net_worth >= fire_number:
        return 0, current_net_worth, [current_net_worth]

    years = 0
    net_worth = current_net_worth
    net_worth_history = [net_worth]

    savings = annual_savings  # Start with user's current annual savings
    while net_worth < fire_number and years < 100:
        net_worth += annual_savings
        net_worth *= (1 + annual_return)
        years += 1
        net_worth_history.append(net_worth)
        savings *= (1 + merit_growth)

    return years, net_worth, net_worth_history


# Sample test values (replace these with user inputs later!)
current_net_worth = 100000   # dollars
annual_savings = 30000       # dollars
target_expenses = 40000      # dollars
withdrawal_rate = 0.04       # 4%
annual_return = 0.07         # 7% growth
merit_growth = 0.02  # For example, a 2% annual savings increase

# Run calculations
fire_goal = calculate_fire_number(target_expenses, withdrawal_rate)
years_to_fi, final_net_worth, net_worth_history = estimate_years_to_fi(current_net_worth, annual_savings, annual_return, fire_goal, merit_growth)

# Display results
print(f"FIRE goal: ${fire_goal:,.0f}")
print(f"Estimated years to FI: {years_to_fi} years")
print(f"Projected net worth at FI: ${final_net_worth:,.0f}")
