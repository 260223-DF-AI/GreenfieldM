# budget_calculator.py - Personal Finance Calculator
# Starter code for e002-exercise-python-intro

"""
Personal Finance Calculator
---------------------------
This program helps users understand their monthly budget by collecting
income and expense information and displaying a formatted summary.

Complete the TODO sections below to finish the program.
"""

print("=" * 44)
print("       PERSONAL FINANCE CALCULATOR")
print("=" * 44)
print()

# =============================================================================
# TODO: Task 1 - Collect User Information
# =============================================================================
# Get the user's name
# Example: name = input("Enter your name: ")
name = input("Please enter your name: ")

# Get monthly income (as a float)
# Remember to convert the input to a float!
income = float(input("Please enter your monthly income: "))


# Get expenses for at least 4 categories:
# - rent: Rent/Housing
# - utilities: Utilities (electric, water, internet)
# - food: Food/Groceries
# - transportation: Transportation (gas, public transit)
rent = float(input("Enter your monthly rent/housing expense: "))
utilities = float(input("Enter your utilities(electric, water, internet) expense: "))
food = float(input("Enter your monthly food/grocery expense: "))
transportation = float(input("Enter your monthly transportation(gas, public transport) expense:  "))


# =============================================================================
# TODO: Task 4 - Add Validation (Optional Enhancement)
# =============================================================================
# Add these validations before calculations:
# - If name is empty, use "Anonymous"
if name == " ":
    name = "Anonymous"
# - If income is <= 0, print error and exit
if income <= 0:
    print("Error: monthly income must be greater than 0")
    exit()
# - If any expense is negative, treat as 0
if rent < 0:
    rent = 0
if utilities < 0:
    utilities = 0
if food < 0:
    food = 0
if transportation < 0:
    transportation = 0


# =============================================================================
# TODO: Task 2 - Perform Calculations
# =============================================================================
# Calculate total expenses
expenses = rent + utilities + food + transportation

# Calculate remaining balance (income - expenses)
remaining = income - expenses

# Calculate savings rate as a percentage
# Formula: (balance / income) * 100
savings = (remaining/income) * 100

# Determine financial status
# - If balance > 0: status = "in the green"
# - If balance < 0: status = "in the red"
# - If balance == 0: status = "breaking even"
if remaining > 0:
    status = "in the green"
elif remaining < 0:
    status = "in the red"
elif remaining == 0:
    status = "breaking even"

# =============================================================================
# TODO: Task 3 - Display Results
# =============================================================================
# Create a formatted budget report
# Use f-strings for formatting
# Dollar amounts should show 2 decimal places: f"${amount:.2f}"
# Percentages should show 1 decimal place: f"{rate:.1f}%"

# Example structure:
# print("=" * 44)
# print("       MONTHLY BUDGET REPORT")
# print("=" * 44)
# print(f"Name: {name}")
# ... continue building the report ...

print('=' * 44)
print("         MONTHLY BUDGET REPORT") #title
print("=" * 44)
print(f"Name: {name}")
print(f"Monthly Income: ${income:.2f}") #first section
print()
print("EXPENSES:")
print(f" -Rent/Housing:     ${rent:.2f}")
print(f" -Utilities:        ${utilities:.2f}")
print(f" -Food/Groceries:   ${food:.2f}")
print(f" -Transportation:   ${transportation:.2f}") #second section
print("-" * 44)
print(f"Total Expenses:     ${expenses:.2f}")
print(f"Remaining Balance:  ${remaining:.2f}")
print(f"Savings Rate:       {savings:.1f}%") #third section
print()
print(f"Status: you are {status}!")
print("=" * 44) #end of report



# =============================================================================
# STRETCH GOAL: Category Percentages
# =============================================================================
# Add a section showing what percentage each expense is of total income
# Example: print(f"  - Rent/Housing:    {(rent/income)*100:.1f}% of income")

print("EXPENSE PERCENTAGES OF TOTAL INCOME:")
print(f"  -Rent/Housing:    {(rent/income)*100:.1f}% of income")
print(f"  -Utilities:       {(utilities/income)*100:.1f}% of income")
print(f"  -Food/Groceries:  {(food/income)*100:.1f}% of income")
print(f"  -Transportation:  {(transportation/income)*100:.1f}% of income")
print("=" * 44)