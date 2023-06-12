# calculate calories 
# source: https://www.verywellfit.com/how-many-calories-do-i-need-each-day-2506873

# convert inches to cm
# quiz takes height in inches not cm so we need to convert
def in_to_cm(inches):
    return inches * 2.54

# convert lb to kg
# quiz takes weight in pounds not kg so we need to convert
def lb_to_kg(pound):
    return pound / 2.205

# bmr (basal metabolic rate)
def bmr(gender, weight, height, age):
    if gender == "female":
        num = 655.1 + (9.563* weight) + (1.850 * height) - (4.676 * age)
    elif gender == "male":
        num = 66.47 + (13.75 * weight) + (5.003 * height) - (6.775 * age)
    return int(num)

# amr (active metabolic rate): number of calories you need to consume to stay at your current weight
# want to lose weight means calorie intake < amr returned value and/or higher fitness level
def amr(fitness_level, bmr_value):
    num = bmr_value
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
    return int(num)

# source: https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/calories/art-20048065#:~:text=In%20general%2C%20if%20you%20cut,It%20sounds%20simple.
def ur_already_soo_hot_tho(amr): 
    if(amr - 500 > 1200):
        return (amr-500)
    else:
        return 1200 # set a minimum bc starving is a no no!

def show_me_those_gains(amr):
    return amr + 500 

def calories(goal, amr):
    if goal == "lose": 
        return ur_already_soo_hot_tho(amr)
    if goal == "maintain":
        return amr 
    if goal == "gain":
        return show_me_those_gains(amr)
