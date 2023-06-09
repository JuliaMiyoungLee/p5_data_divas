def get_before(current):
    # If it is the first day of a month
    if current[3:5] == "01":
        # If it is January
        if current[:2] == "1":
            return "12-31-" + str(int(current[6:])-1)
        # If it is March
        elif current[:2] == "03":
            return "02-28-" + current[7:]
        # If the previous month has 31 days
        elif current[:2] in [2, 4, 6, 8, 9, 11]:
            return str(int(current[:2]-1)) + "-31-" + current[6:]
        # If the previous month has 30 days
        else:
            return str(int(current[:2]-1)) + "-30-" + current[6:]
    else:
        return current[:3] + str(int(current[3:5])-1) + "-" + current[6:]

