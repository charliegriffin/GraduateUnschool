max = 30

# did this one on my own
def numWays(n): #counts the number of ways one can go up n stairs if
                #they have the option of taking 1,2, or 3 stairs at a time
    if n==1: return 1 # num ways to get up 1 stair
    if n==2: return 2 # num ways to get up 2 stairs
    if n==3: return 4 # num ways to get up 3 stairs
    return numWays(n-1) + numWays(n-2) + numWays(n-3) # sum of all possibilities

map = [-2 for i in range(max)]

# needed guidance for this one    
def numWaysDP(n,map):
    if (n<0): return 0
    elif (n==0): return 1
    elif (map[n] > -1): return map[n]
    else: map[n] = numWaysDP(n-1,map) + numWaysDP(n-2,map) + numWaysDP(n-3,map)
    return map[n]

print 'rec'   
for i in range(1,max):
    print i,numWays(i)
    
print 'dp'
for i in range(1,max):
    print i,numWaysDP(i,map)