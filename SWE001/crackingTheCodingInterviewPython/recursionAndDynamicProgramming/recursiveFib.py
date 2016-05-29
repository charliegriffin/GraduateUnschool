def fibonacci(i):
    if i==0:
        return 0
    if i==1:
        return 1
    return fibonacci(i-1) + fibonacci(i-2)
    
for i in range(50):
    print i, fibonacci(i)