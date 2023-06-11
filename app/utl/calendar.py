def get_before(current):
    # If it is the first day of a month
    if current[3:5] == "01":
        # If it is January
        if current[:2] == "01":
            return "12-31-" + str(int(current[6:])-1)
        # If it is March
        elif current[:2] == "03":
            return "02-28-" + current[7:]
        # If the previous month has 31 days
        elif int(current[:2]) in [2, 4, 6, 8, 9, 11]:
            # If the previous month will be single digit
            if int(current[:2]) <= 10:
                return "0" + str(int(current[:2])-1) + "-31-" + current[6:]
            else:
                return str(int(current[:2])-1) + "-31-" + current[6:]
        # If the previous month has 30 days
        else:
            # If the previous month will be single digit
            if int(current[:2]) <= 10:
                return "0" + str(int(current[:2])-1) + "-30-" + current[6:]     
            else:      
                return str(int(current[:2])-1) + "-30-" + current[6:]
    elif int(current[3:5]) <= 10:
        return current[:3] + "0" + str(int(current[3:5])-1) + "-" + current[6:]
    else:
        return current[:3] + str(int(current[3:5])-1) + "-" + current[6:]

def get_after(current):
    # If it is the last day of the year
    if current[0:6] == "12-31":
        return "01-01-" + str(int(current[6:])+1)
    # If it is the last day of February
    elif current[:5] == "02-28":
        return "03-01-" + current[6:]
    # If it is the last day of a month with 31 days
    elif int(current[:2]) in [1, 3, 5, 7, 8, 10] and int(current[3:5]) == 31:
        # If the next month is single digit
        if int(current[:2])+1 < 10:
            return "0" + str(int(current[:2])+1) + "-01-" + current[6:]
        else:
            return str(int(current[:2])+1) + "-01-" + current[6:]
    # If it is a month with 30 days
    elif int(current[3:5]) == 30:
        # If the next month is single digit
        if int(current[:2])+1 < 10:
            return "0" + str(int(current[:2])+1) + "-01-" + current[6:]
        else:
            return str(int(current[:2])+1) + "-01-" + current[6:]
    elif int(current[3:5])+1 < 10:
        return current[:3] + "0" + str(int(current[3:5])+1) + "-" + current[6:]
    else:
        return current[:3] + str(int(current[3:5])+1) + "-" + current[6:]

def get_date_fancy(date):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return str(months[int(date[:2])-1]) + date[2:]
   