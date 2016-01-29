# highly efficient way to generate a list of primes
# recognizes that all non-prime numbers are divisible by a prime number
# 
# starting with a list of all numbers up through some value max.
# All numbers divisible by 2 are crossed off, then the next prime is searched for,
# and all numbers divisble by that prime number are corssed off.
# At the end we are left with a list of prime numbers from 2 through the max

def soe(max):
    isPrimeList = [False,False] # 0 and 1 are not prime
    for i in range(max-1):
        isPrimeList.append(True)
    count = 0
    prime = 2
    
    while prime <= max**(0.5): # cross off remaining multiples of prime
        crossOff(isPrimeList,prime)
        prime = getNextPrime(isPrimeList,prime)
        if (prime >= len(isPrimeList)):
            break
    
    return isPrimeList

def crossOff(isPrimeList,prime):
    # cross off remaining multiple of prime, starting with prime*prime
    # since k*primes s.t. k<prime would have already been crossed off
    for i in range(prime*prime,len(isPrimeList),prime):
        isPrimeList[i] = False

def getNextPrime(isPrimeList,prime):
    next = prime + 1
    while next < len(isPrimeList) and not isPrimeList[next]:
        next += 1
    return next
    
def printFirstThousandPrimes():
    firstThousand = soe(1000)
    for i in range(len(firstThousand)):
        if firstThousand[i]:
            print i
            
printFirstThousandPrimes()