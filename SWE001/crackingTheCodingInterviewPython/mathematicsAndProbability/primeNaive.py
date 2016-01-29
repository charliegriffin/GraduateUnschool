# A naive way to check if an integer is prime or not

def primeNaive(n):
    if n < 2:
        return False
    for i in range(2,n-1): # iterates through all the numbers, checking to see if they are divisible
        if n%i == 0:
           return False
    return True

def test():
    print "is 2 Prime?",primeNaive(2),"should be True"
    print "is 5 Prime?",primeNaive(5),"should be True"
    print "is 27 Prime?",primeNaive(27),"should be False"
    print "is 29 Prime?",primeNaive(29),"should be True"
    print "is 51 Prime?",primeNaive(51),"should be False"
    print "is 53 Prime?",primeNaive(53),"should be True"
    print "is 181 Prime?",primeNaive(181),"should be True"
    print "is 493 Prime?",primeNaive(493),"should be False"
    
test()
