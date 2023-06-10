# calculate calories 

# Step 1: Calculate Your BMR
# For women, BMR = 655.1 + (9.563 x weight in kg) + (1.850 x height in cm) - (4.676 x age in years)
# For men, BMR = 66.47 + (13.75 x weight in kg) + (5.003 x height in cm) - (6.755 x age in years)

# Step 2: Calculate Your AMR
# Sedentary (little or no exercise): AMR = BMR x 1.2
# Lightly active (exercise 1–3 days/week): AMR = BMR x 1.375
# Moderately active (exercise 3–5 days/week): AMR = BMR x 1.55
# Active (exercise 6–7 days/week): AMR = BMR x 1.725
# Very active (hard exercise 6–7 days/week): AMR = BMR x 1.9

def bmr(gender, weight, height, age):
    if gender == "female":
        num = 655.1 + (9.563* weight) + (1.850 * height) - (4.676 * age)
    elif gender == "male":
        num = 66.47 + (13.75 * weight) + (5.003 * height) - (6.775 * age)
    return num

def amr(fitness_level, bmr_value):
    if fitness_level == 1:
        num = bmr_value * 1.2
    elif fitness_level == 2:
        num = bmr_value * 1.375
    elif fitness_level == 3:
        num = bmr_value * 1.55
    elif fitness_level == 4:
        num = bmr_value * 1.725
    elif fitness_level == 5:
        num = bmr_value * 1.9
    return num