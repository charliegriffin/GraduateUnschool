def firstn(n):
	num = 0
	while num < n:
		yield num
		num += 1

def yielder():
	for i in range(10):
		yield i

s = sum(firstn(1000000))
print s
y = yielder()
print sum(y)