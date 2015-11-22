# Problem Set 1
# Name: Charlie Griffin
# Time Spent: 0:30

# Calculates the credit card balance after one year
# if only the minimum monthly payment is made

balance = float(raw_input('Enter the outstanding balance on your credit card: '))
yr_rate = float(raw_input('Enter the annual interest rate in decimal form: '))
min_rate = float(raw_input('Enter the minimum monthly payment rate in decimal form: '))
month = 1
tot_paid = 0
while month <= 12:
	print "Month: " + str(month)
	
	min_pay = round(min_rate * balance,2)
	tot_paid = round(tot_paid + min_pay,2)
	print "Minimum monthly payment: $" + str(min_pay)
	
	int_paid = round(yr_rate/12.0*balance,2) #yr_rate/12.0 = monthly rate
	prin_paid = round(min_pay - int_paid,2)
	print "Principle paid: $" + str(prin_paid)
	
	balance = round(balance - prin_paid,2)
	print "Remaining balance: $" + str(balance)
	month += 1
print "RESULT"
print "Total amount paid: $" + str(tot_paid)
print "Remaining balance: $" + str(balance)
	