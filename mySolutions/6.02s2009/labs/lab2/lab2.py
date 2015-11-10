import math
import numpy
import matplotlib.pyplot as p

# test the transmit function for Lab 2, Task #1
def test_transmit(transmit):
    def test(bits,npreamble=0,npostamble=0,samples_per_bit=8,v0=0.0,v1=1.0,repeat=1):
        result = transmit(bits,
                          npreamble=npreamble,
                          npostamble=npostamble,
                          samples_per_bit=samples_per_bit,
                          v0=v0,
                          v1=v1,
                          repeat=repeat)
        index = 0
        nresult = len(result)
        while repeat > 0:
            # check preamble
            assert index+npreamble <= nresult,\
                   "expected %d preamble bits but came up short at index %d" % \
                   (npreamble,index)
            for i in xrange(npreamble):
                assert result[index]==v0,\
                       "bad preamble bit at index %d: expected %g got %g" % \
                       (index,v0,result[index])
                index += 1

            # check message bits
            assert index+len(bits)*samples_per_bit <= nresult,\
                   "expected %d message bits but came up short at index %d" % \
                   (len(bits)*samples_per_bit,index)
            for bit in bits:
                expect = v0 if bit==0 else v1
                for i in xrange(samples_per_bit):
                    assert result[index]==expect,\
                       "bad message bit at index %d: expected %g got %g" % \
                       (index,expect,result[index])
                    index += 1

            # check postamble
            assert index+npostamble <= nresult,\
                   "expected %d postamble bits but came up short at index %d" % \
                   (npostamble,index)
            for i in xrange(npostamble):
                assert result[index]==v0,\
                       "bad postamble bit at index %d: expected %g got %g" % \
                       (index,v0,result[index])
                index += 1

            # finished with this repetition
            repeat -= 1

    # test 1: arbitrary values for the args...
    test([1,0,1,0,0,1,1,0,0,0,1,1,1],
         npreamble=7,
         npostamble=22,
         samples_per_bit=11,
         v0=-0.5,
         v1=0.5,
         repeat=4)

    # test 2: unit-sample sequence
    test([1],
         npreamble=100,
         npostamble=100,
         samples_per_bit=1)

# for Task #3
def plot_unit_sample_response(unit_sample_response,channel):
    response = unit_sample_response(channel)
    p.figure()
    p.stem(range(len(response)),response)
    p.title('Unit-sample response of %s' % channel.__name__)
    p.xlabel('Sample number')


######################################################################
###                 DifferenceEquationWithInput
######################################################################

# Linear difference equations of any order, with input
# Note that the inputSource is set when the instance is created

class diff_eq:
    # Solves difference equation:
    # yCoeffs[0]*y(n+K) + .. + yCoeffs[K]*y(n) =
    #                 xCoeffs[0]*x(n+L) + + xCoeffs[L]*x(n)
    # Using initial conditions for y, y[n] = 0, n < 0
    # x is a function which takes an integer argument and x[n] = 0, n < 0
    def __init__(self, yCoeffs, xCoeffs, x):
        # print ("yCoeffs", yCoeffs, "xCoeffs", xCoeffs)
        self.outCoefficients = floatList(yCoeffs)
        self.inputCoefficients = floatList(xCoeffs)
        self.yOrder = len(yCoeffs) - 1
        self.inputOrder = len(self.inputCoefficients)
        self.inputSource = x
        # Put the initial conditions in stored values.
        self.storedValues = {}
        self.storedValues = {}
        for i in range(-1,-(self.yOrder+2),-1): # Make sure y[-1] = 0 even if order = 0
            self.storedValues[i] = 0

    # Uses inputOrder values starting from yOrder points back from n
    def evalInput(self,n):
        K = self.yOrder
        L = self.inputOrder
        Xs = dotProd(self.inputCoefficients,
                     map(self.inputSource,
                         range(n + L - K -1, n - K -1, -1)))
        return Xs
    
    # n is the index for the value        
    def __call__(self, ni):
        assert ni >= 0, 'Can not evaluate equation for n negative'
        if ni in self.storedValues:
            return self.storedValues[ni]
        else:
            n = max(self.storedValues.keys())+1
            vals = [self.storedValues[n-i-1] for i in range(self.yOrder)]
            while n <= ni:
                oldYs = dotProd(self.outCoefficients[1:],vals)
                Xs = self.evalInput(n)
                nextVal = (Xs - oldYs)/self.outCoefficients[0]
                vals = [nextVal] + vals[:-1]
                self.storedValues[n] = nextVal
                n += 1
            return vals[0]

    def __str__( self ):
        cof = self.outCoefficients
        order = len(cof)
        print " + ".join([diffEqStrh(cof[i], order-i-1, "y") for i in range(order)])
        print "="
        cof = self.inputCoefficients
        order = len(cof)
        print " + ".join([diffEqStrh(cof[i], order-i-1, "x") for i in range(order)])
        return("")

# Converts a list in to type float
def floatList(a):
    return [float(a[i]) for i in range(len(a))]

# a and b are lists of numbers, same length
# return sum(a[1]*b[1], ..., a[n]*b[n])
def dotProd(a, b):
    assert len(a) == len(b), 'Mismatched sizes in dotProd'  
    return sum(vectorMult(a,b))

# a and b are lists of numbers, same length
# return (a[1]*b[1], ..., a[n]*b[n])
def vectorMult(a, b):
    assert len(a) == len(b), 'Mismatched sizes in vectorMult'  
    return [ai*bi for (ai,bi) in zip(a,b)]

#########################################################################
###            System Block Boxes (fast and slow)
#########################################################################

def black_box(input, num, den, pad, noise):
    def f(n): # Assumes input is zero before n = 0 and after zero ends
        if n >= 0 and n < len(input):
            return input[n]
        else:
            return 0.0
    output_de = diff_eq(num,den,f)
    output = numpy.array([output_de(n) for n in range(len(input)+pad)])
    noisevals = numpy.random.triangular(-1.0,0,1.0,size=len(output))
    return output + noise*noisevals

def channel1(input, noise=0.0):
    #cjt: changed to not add additional padding -- input will include it
    return black_box(input,[1,-2.7,2.43,-0.729],[1.0e-3],0,noise)

def channel2(input, noise=0.0):
    #cjt: changed to not add additional padding -- input will include it
    return black_box(input,[1, -3.0/2.0, 13.0/16.0],[5.0/16.0,0,0],0,noise)

__all__ = ['test_transmit',    # for Task 1
           'channel1','channel2',   # for Task 2
           'plot_unit_sample_response'
           ]