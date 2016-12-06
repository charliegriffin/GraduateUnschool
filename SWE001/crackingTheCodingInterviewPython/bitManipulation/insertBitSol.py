''' 5.1
You are given two 32-bit numbers, N and M, and two bit positions, i and j.
Write a method to insert M into N such that M starts at bit j and ends at
bit i.'''

def updateBits(n, m, i, j):
    #create a mask to clear bits i through j in n
    allOnes = ~0
    
    #1s before position j, then 0s.
    left = allOnes << (j + 1)
    
    #1s after position i.
    right = ((1 << i) - 1)
    
    #all 1s except for 0s between i and j
    mask = left | right
    
    #clear bits j through i then put m in there
    n_cleared = n & mask
    m_shifted = m<<i
    
    return n_cleared | m_shifted
    
print updateBits(1024,19,2,6)