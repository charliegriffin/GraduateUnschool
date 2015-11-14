def firstn(n):
	num = 0
	while num < n:
		yield num
		num += 1

s = sum(firstn(1000000))
print s