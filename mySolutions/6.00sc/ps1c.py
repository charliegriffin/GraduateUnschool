# Problem Set 1c
# Name: Charlie Griffin
# Time Spent: 1:10

# Uses bisection search to find the smallest monthly payment
# to the cent, that pays off the debt within a year

balance = float(raw_input("Enter the outstanding balance on your credit card: "))
yr_rate = float(raw_input("Enter the annual credit card interest rate as a decimal: "))
mo_rate = yr_rate/12.0
initial_balance = balance

low = balance / 12.0   				#lower bound, paying off just principle
up = (balance *(1 +(yr_rate/12.0))**12.0)/12.0	#upper bound, one large late payment

while up - low > 0.005:	#convergence  #finds the minimum payment
	min_pay = (low + up)/2
	balance = initial_balance
	month = 0
	while month < 12:
		balance += round(balance*mo_rate,2) - min_pay
		month += 1
	if balance > 0:				#if we paid too little
		low = min_pay	#what we paid is our new lower bound
	else:
		up = min_pay
min_pay = round(min_pay + 0.004999,2)	#round minimum payment up the nearest cent
balance = initial_balance
month = 0
while month < 12: #recomputes balance with new minimum payment
	balance += round(balance*yr_rate/12,2) - min_pay
	month +=1
balance = round(balance,2)	
	
print 'RESULT'
print 'Monthly payment to pay off debt in 1 year:  $' + str(min_pay)
print 'Number of months needed: ' + str(month)
print 'Balance $' + str(round(balance,2))