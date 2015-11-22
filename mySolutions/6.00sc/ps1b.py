# Problem Set 1b
# Name: Charlie Griffin
# Time Spent: 0:20

# calculates the minimum fixed monthly payment
# in order to pay off a credit card balance in
# a year

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
yr_rate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
mo_rate = round(yr_rate/12.0,2)
initial_balance = balance

min_pay = 0

while balance >= 0:
	min_pay += 10					#increments the minimum payment by $10 until fully paid
	balance = initial_balance
	month = 0
	while month < 12 and balance >= 0:
		balance = balance * (1 + mo_rate ) - min_pay
		month += 1
	
print 'RESULT'
print 'Monthly payment to pay off debt in 1 year:  $' + str(min_pay)
print 'Number of months needed: ' + str(month)
print 'Balance $' + str(round(balance,2))