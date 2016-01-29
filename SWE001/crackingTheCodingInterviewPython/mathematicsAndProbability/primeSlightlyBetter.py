# A slightly better way to check if an integer is prime or not

def primeSlightlyBetter(n):
    if n < 2:
        return False
    for i in range(2,int(n**(0.5))): # iterates through all the numbers, up to the square root
        if n%i == 0:
           return False
    return True

def test():
    print "is 2 Prime?",primeSlightlyBetter(2),"should be True"
    print "is 5 Prime?",primeSlightlyBetter(5),"should be True"
    print "is 27 Prime?",primeSlightlyBetter(27),"should be False"
    print "is 29 Prime?",primeSlightlyBetter(29),"should be True"
    print "is 51 Prime?",primeSlightlyBetter(51),"should be False"
    print "is 53 Prime?",primeSlightlyBetter(53),"should be True"
    print "is 181 Prime?",primeSlightlyBetter(181),"should be True"
    print "is 493 Prime?",primeSlightlyBetter(493),"should be False"
    
test()
