''' 5.1
You are given two 32-bit numbers, N and M, and two bit positions, i and j.
Write a method to insert M into N such that M starts at bit j and ends at
bit i.'''

# this is wrong

def insertBit(N,M,i,j):
    print(N,M)
    return N|(M << i)
    

#test
print("Input: N = 10000000000, M = 10011, i = 2, j = 6")
print("Expected Output: N = ",int('10001001100',2))
print("Output: ",insertBit(int('10000000000',2),int('10011',2),2,6))