def harvard_total_income(years):
    ti = 0.
    for i in range(years+1):
        ti += (140000.+25000.*i)*(1./1.03)**i
    return ti
    
def mit_total_income(years):
    ti = 0.
    for i in range(years+1):
        ti += 100000.*(1.15)**i*(1./1.03)**i
    return ti
    
for years_worked in range(45):
    if (mit_total_income(years_worked) > harvard_total_income(years_worked)):
        break

print years_worked