Part 1: Simulate LTISM

m = LTIXSM([1,2],[1],[3],[4])
Find the values returned by this machine for this input sequence:
o = m.transduce([1,2,3,4,5])

x[-1] = 3, y[-1] = 4
y[n] = x[n] + 2x[n-1] + y[n-1]

1. o[0] = 11
2. o[1] = 15
3. o[2] = 22
4. o[3] = 32
5. o[4] = 45