def count_sick_days(total_days):
    sick_days = 0
    for day in range(1,total_days+1):
        if day%2 == 0:  #sick
            sick_days+=1
        elif day%3 == 0:    #traffic
            sick_days+=1
        elif day%5 == 0:
            sick_days+=1
        else:
            pass
    return sick_days

print count_sick_days(300)