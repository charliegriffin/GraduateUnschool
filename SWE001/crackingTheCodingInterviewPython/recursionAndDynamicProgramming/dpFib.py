max = 50
fib = [0 for i in range(max)]


def fibonacci(i):
    if i==0:  return 0
    if i==1:  return 1
    if fib[i] != 0:  return fib[i] #return cached result.
    fib[i] = fibonacci(i-1) + fibonacci(i-2) #cache result
    return fib[i]
    
for i in range(max):
    print i, fibonacci(i)