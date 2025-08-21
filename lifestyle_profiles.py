EXPENSE_CATEGORIES = [
    "Housing", "Utilities", "Food", "Transportation", "Insurance",
    "Phone/Internet", "Childcare", "Health & Wellness", "Subscriptions",
    "Discretionary", "Travel", "Shopping", "Personal Care",
    "Giving", "Investments", "Education", "Other"
]

CATEGORY_HELP = {
    "Housing": "Rent or mortgage, property taxes, HOA fees.",
    "Utilities": "Electricity, water, internet, phone, trash.",
    "Food": "Groceries, dining out, meal delivery.",
    "Transportation": "Gas, public transit, car payments, maintenance.",
    "Insurance": "Health, auto, home, life insurance premiums.",
    "Discretionary": "Entertainment, hobbies, subscriptions, shopping.",
    "Travel": "Flights, hotels, vacations, weekend getaways.",
    "Giving": "Charitable donations, gifts, tithing.",
    "Other": "Pet care, child expenses, miscellaneous costs.",
    "Phone/Internet": "Cell phone, home internet, streaming bundles.",
    "Childcare": "Daycare, babysitting, after-school programs.",
    "Health & Wellness": "Gym, therapy, supplements, out-of-pocket medical.",
    "Subscriptions": "Streaming, software, memberships.",
    "Shopping": "Clothing, household items, online purchases.",
    "Personal Care": "Haircuts, skincare, toiletries.",
    "Investments": "Brokerage, retirement accounts.",
    "Education": "Tuition, courses, books, student loans."
}


BASE_EXPENSES_STUDENT = {
    "🧘‍♀️ Lean & Serene ($)": {
        "Housing": 800, "Utilities": 150, "Food": 300, "Transportation": 150, "Insurance": 200,
        "Phone/Internet": 60, "Childcare": 0, "Health & Wellness": 60, "Subscriptions": 20,
        "Discretionary": 0, "Travel": 50, "Shopping": 80, "Personal Care": 40,
        "Giving": 20, "Investments": 50, "Education": 100, "Other": 50
    },
    "🏙️ Urban Explorer ($$$)": {
        "Housing": 1200, "Utilities": 200, "Food": 500, "Transportation": 250, "Insurance": 300,
        "Phone/Internet": 80, "Childcare": 0, "Health & Wellness": 100, "Subscriptions": 40,
        "Discretionary": 0, "Travel": 150, "Shopping": 150, "Personal Care": 80,
        "Giving": 50, "Investments": 150, "Education": 150, "Other": 80
    },
    "🏡 Suburban Comfort ($$) ($$)": {
        "Housing": 1000, "Utilities": 180, "Food": 400, "Transportation": 200, "Insurance": 250,
        "Phone/Internet": 70, "Childcare": 0, "Health & Wellness": 80, "Subscriptions": 30,
        "Discretionary": 0, "Travel": 100, "Shopping": 120, "Personal Care": 60,
        "Giving": 40, "Investments": 100, "Education": 120, "Other": 70
    },
    "✈️ Jetsetter ($$$$)": {
        "Housing": 1800, "Utilities": 250, "Food": 700, "Transportation": 300, "Insurance": 400,
        "Phone/Internet": 100, "Childcare": 0, "Health & Wellness": 120, "Subscriptions": 60,
        "Discretionary": 0, "Travel": 500, "Shopping": 250, "Personal Care": 120,
        "Giving": 100, "Investments": 250, "Education": 200, "Other": 100
    },
    "🎨 Creative Nomad ($$$)": {
        "Housing": 1100, "Utilities": 200, "Food": 500, "Transportation": 250, "Insurance": 300,
        "Phone/Internet": 80, "Childcare": 0, "Health & Wellness": 100, "Subscriptions": 40,
        "Discretionary": 0, "Travel": 300, "Shopping": 180, "Personal Care": 80,
        "Giving": 60, "Investments": 150, "Education": 150, "Other": 80
    }
}

BASE_EXPENSES_SINGLE = {
    "🧘‍♀️ Lean & Serene ($)": {
        "Housing": 1200, "Utilities": 200, "Food": 400, "Transportation": 200, "Insurance": 300,
        "Phone/Internet": 80, "Childcare": 0, "Health & Wellness": 80, "Subscriptions": 30,
        "Discretionary": 0, "Travel": 80, "Shopping": 100, "Personal Care": 60,
        "Giving": 50, "Investments": 200, "Education": 50, "Other": 80
    },
    "🏙️ Urban Explorer ($$$)": {
        "Housing": 1800, "Utilities": 250, "Food": 600, "Transportation": 300, "Insurance": 400,
        "Phone/Internet": 100, "Childcare": 0, "Health & Wellness": 120, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 200, "Shopping": 150, "Personal Care": 100,
        "Giving": 100, "Investments": 300, "Education": 100, "Other": 100
    },
    "🏡 Suburban Comfort ($$)": {
        "Housing": 1600, "Utilities": 220, "Food": 500, "Transportation": 250, "Insurance": 350,
        "Phone/Internet": 90, "Childcare": 0, "Health & Wellness": 100, "Subscriptions": 40,
        "Discretionary": 0, "Travel": 150, "Shopping": 120, "Personal Care": 80,
        "Giving": 80, "Investments": 250, "Education": 80, "Other": 90
    },
    "✈️ Jetsetter ($$$$)": {
        "Housing": 2400, "Utilities": 300, "Food": 800, "Transportation": 400, "Insurance": 500,
        "Phone/Internet": 120, "Childcare": 0, "Health & Wellness": 150, "Subscriptions": 80,
        "Discretionary": 0, "Travel": 600, "Shopping": 300, "Personal Care": 150,
        "Giving": 150, "Investments": 400, "Education": 150, "Other": 150
    },
    "🎨 Creative Nomad ($$$)": {
        "Housing": 1400, "Utilities": 220, "Food": 600, "Transportation": 300, "Insurance": 400,
        "Phone/Internet": 100, "Childcare": 0, "Health & Wellness": 120, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 300, "Shopping": 200, "Personal Care": 100,
        "Giving": 100, "Investments": 300, "Education": 100, "Other": 100
    }
}

BASE_EXPENSES_COUPLE = {
    "🧘‍♀️ Lean & Serene ($)": {
        "Housing": 1600, "Utilities": 250, "Food": 600, "Transportation": 250, "Insurance": 400,
        "Phone/Internet": 100, "Childcare": 0, "Health & Wellness": 100, "Subscriptions": 40,
        "Discretionary": 0, "Travel": 150, "Shopping": 150, "Personal Care": 80,
        "Giving": 100, "Investments": 300, "Education": 100, "Other": 100
    },
    "🏙️ Urban Explorer ($$$)": {
        "Housing": 2200, "Utilities": 300, "Food": 900, "Transportation": 400, "Insurance": 600,
        "Phone/Internet": 120, "Childcare": 0, "Health & Wellness": 150, "Subscriptions": 60,
        "Discretionary": 0, "Travel": 300, "Shopping": 250, "Personal Care": 120,
        "Giving": 150, "Investments": 400, "Education": 150, "Other": 150
    },
    "🏡 Suburban Comfort ($$)": {
        "Housing": 2000, "Utilities": 280, "Food": 800, "Transportation": 350, "Insurance": 550,
        "Phone/Internet": 110, "Childcare": 0, "Health & Wellness": 120, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 200, "Shopping": 200, "Personal Care": 100,
        "Giving": 120, "Investments": 350, "Education": 120, "Other": 120
    },
    "✈️ Jetsetter ($$$$)": {
        "Housing": 3000, "Utilities": 400, "Food": 1200, "Transportation": 500, "Insurance": 800,
        "Phone/Internet": 140, "Childcare": 0, "Health & Wellness": 200, "Subscriptions": 100,
        "Discretionary": 0, "Travel": 800, "Shopping": 400, "Personal Care": 200,
        "Giving": 200, "Investments": 600, "Education": 200, "Other": 200
    },
    "🎨 Creative Nomad ($$$)": {
        "Housing": 1800, "Utilities": 280, "Food": 900, "Transportation": 400, "Insurance": 600,
        "Phone/Internet": 120, "Childcare": 0, "Health & Wellness": 150, "Subscriptions": 70,
        "Discretionary": 0, "Travel": 500, "Shopping": 300, "Personal Care": 150,
        "Giving": 150, "Investments": 450, "Education": 150, "Other": 150
    }
}

BASE_EXPENSES_KIDS = {
    "🧘‍♀️ Lean & Serene ($)": {
        "Housing": 1800, "Utilities": 250, "Food": 700, "Transportation": 300, "Insurance": 500,
        "Phone/Internet": 80, "Childcare": 500, "Health & Wellness": 100, "Subscriptions": 30,
        "Discretionary": 0, "Travel": 100, "Shopping": 150, "Personal Care": 80,
        "Giving": 100, "Investments": 300, "Education": 100, "Other": 100
    },
    "🏙️ Urban Explorer ($$$)": {
        "Housing": 2200, "Utilities": 300, "Food": 900, "Transportation": 400, "Insurance": 600,
        "Phone/Internet": 100, "Childcare": 700, "Health & Wellness": 150, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 200, "Shopping": 200, "Personal Care": 120,
        "Giving": 150, "Investments": 400, "Education": 200, "Other": 150
    },
    "🏡 Suburban Comfort ($$)": {
        "Housing": 2400, "Utilities": 300, "Food": 900, "Transportation": 500, "Insurance": 700,
        "Phone/Internet": 100, "Childcare": 800, "Health & Wellness": 150, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 300, "Shopping": 250, "Personal Care": 120,
        "Giving": 150, "Investments": 500, "Education": 200, "Other": 150
    },
    "✈️ Jetsetter ($$$$)": {
        "Housing": 3000, "Utilities": 400, "Food": 1200, "Transportation": 600, "Insurance": 800,
        "Phone/Internet": 120, "Childcare": 1000, "Health & Wellness": 200, "Subscriptions": 80,
        "Discretionary": 0, "Travel": 600, "Shopping": 400, "Personal Care": 200,
        "Giving": 200, "Investments": 700, "Education": 300, "Other": 200
    },
    "🎨 Creative Nomad ($$$)": {
        "Housing": 2000, "Utilities": 300, "Food": 800, "Transportation": 400, "Insurance": 600,
        "Phone/Internet": 100, "Childcare": 600, "Health & Wellness": 150, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 400, "Shopping": 250, "Personal Care": 120,
        "Giving": 150, "Investments": 450, "Education": 200, "Other": 150
    },
    "🛠️ Start from scratch": {cat: 0 for cat in EXPENSE_CATEGORIES}
}

BASE_EXPENSES_RETIREE = {
    "🧘‍♀️ Lean & Serene ($)": {
        "Housing": 1400, "Utilities": 200, "Food": 500, "Transportation": 200, "Insurance": 500,
        "Phone/Internet": 80, "Childcare": 0, "Health & Wellness": 150, "Subscriptions": 30,
        "Discretionary": 0, "Travel": 100, "Shopping": 100, "Personal Care": 60,
        "Giving": 100, "Investments": 200, "Education": 0, "Other": 80
    },
    "🏙️ Urban Explorer ($$$)": {
        "Housing": 2000, "Utilities": 250, "Food": 700, "Transportation": 300, "Insurance": 700,
        "Phone/Internet": 100, "Childcare": 0, "Health & Wellness": 200, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 300, "Shopping": 200, "Personal Care": 100,
        "Giving": 150, "Investments": 300, "Education": 0, "Other": 100
    },
    "🏡 Suburban Comfort ($$)": {
        "Housing": 1800, "Utilities": 220, "Food": 600, "Transportation": 250, "Insurance": 600,
        "Phone/Internet": 90, "Childcare": 0, "Health & Wellness": 180, "Subscriptions": 40,
        "Discretionary": 0, "Travel": 200, "Shopping": 150, "Personal Care": 80,
        "Giving": 120, "Investments": 250, "Education": 0, "Other": 90
    },
    "✈️ Jetsetter ($$$$)": {
        "Housing": 2800, "Utilities": 350, "Food": 1000, "Transportation": 400, "Insurance": 900,
        "Phone/Internet": 120, "Childcare": 0, "Health & Wellness": 250, "Subscriptions": 80,
        "Discretionary": 0, "Travel": 1000, "Shopping": 400, "Personal Care": 150,
        "Giving": 200, "Investments": 500, "Education": 0, "Other": 150
    },
    "🎨 Creative Nomad ($$$)": {
        "Housing": 1600, "Utilities": 250, "Food": 700, "Transportation": 300, "Insurance": 600,
        "Phone/Internet": 100, "Childcare": 0, "Health & Wellness": 200, "Subscriptions": 50,
        "Discretionary": 0, "Travel": 500, "Shopping": 250, "Personal Care": 100,
        "Giving": 150, "Investments": 350, "Education": 0, "Other": 100
    }
}

BASE_EXPENSES_BY_HOUSEHOLD = {
    "Married with Kids": BASE_EXPENSES_KIDS,
    "Couple (No Kids)": BASE_EXPENSES_COUPLE,
    "Single Adult": BASE_EXPENSES_SINGLE,
    "Retiree / Empty Nester": BASE_EXPENSES_RETIREE,
    "Student / Early Career": BASE_EXPENSES_STUDENT
}

HOUSEHOLD_TYPES = [
    "Single Adult",
    "Couple (No Kids)",
    "Married with Kids",
    "Retiree / Empty Nester",
    "Student / Early Career"
]

LOCATION_TIERS = [
    "Small Town or Rural Area",
    "Mid-Sized City or Suburb",
    "Major Metro Area",
    "Large Coastal City"
]

LOCATION_MULTIPLIERS = {
    "Small Town or Rural Area": 0.85,
    "Mid-Sized City or Suburb": 1.0,
    "Major Metro Area": 1.2,
    "Large Coastal City": 1.35
}
