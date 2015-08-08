#
# File:   designLab01Work.py
# Author: 6.01 Staff
# Date:   02-Sep-11
#
# Below are templates for your answers to three parts of Design Lab 1

#-----------------------------------------------------------------------------

# Note from Charlie:  I tested everything, it seems to work.  Assignment complete.

def fib(n):
    if n == 0:
    	return 0
    elif n == 1:
    	return 1
    else:
    	return fib(n-1) + fib(n-2)

#-----------------------------------------------------------------------------

class V2:	#creates a vector out of two numbers
	def __init__(self,x,y):
		#initializes coordinates
		self.x = x
		self.y = y
	def __str__(self):
		return "V2["+str(self.x)+', '+str(self.y)+']'
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def add(self,vector2):
		return V2(self.x + vector2.getX(),self.y + vector2.getY())
	def mul(self,scalar):
		return V2(self.x * scalar,self.y * scalar)
	def __add__(self, v):
		return self.add(v)
	def __mul__(self,s):
		return self.mul(s)

#-----------------------------------------------------------------------------

class Polynomial:
	coeffs = None
	def __init__(self, coefficients):
		# initializes the coefficients to be a list of floats
		self.coefficients = coefficients
		for i in range(len(self.coefficients)):
			self.coefficients[i] = float(self.coefficients[i])
	def coeff(self,i):
		# returns the coefficient of the x^i term of the polynomial 
		if (len(self.coefficients)-1) < i or i < 0: #the i is higher order than the poly or <0
			return 0.
		else:
			return self.coefficients[i]
	def add(self, other):
		# returns a new Polynomial representing the sum of Polynomials self and other
		newCoeffs = []
# 		firstCoeffs = self.coefficients[::-1]
# 		secondCoeffs = other.coefficients[::-1]
# 		print firstCoeffs
		if len(self.coefficients) >= len(other.coefficients): # first is >= order in order
			for i in range(len(self.coefficients)):
				newCoeffs.append(self.coeff(len(self.coefficients)-i-1) + other.coeff(len(other.coefficients)-i-1))
		else: # first is < other in order
			for i in len(other.coefficients):
				newCeoffs.append(self.coeff(len(self.coefficients)-i-1) + other.coeff(len(other.coefficients)-i-1))
		newCoeffs = newCoeffs[::-1]
		return Polynomial(newCoeffs)
	def __add__(self,other):
		return self.add(other)
	def mul(self,other):
		# returns a new Polynomial representing the product of self and other
		newCoeffs = []
		order = (len(self.coefficients)-1)+(len(other.coefficients)-1)
		for i in range(order+1):	# initializes a list of zeros of the correct order
			newCoeffs.append(0.)
		for i in range(len(self.coefficients)):	# I think this is the typical expansion procedure
			for j in range(len(other.coefficients)):
				newCoeffs[i+j] += self.coeff(i)*other.coeff(j)
		return Polynomial(newCoeffs)
	def __str__(self):
		# converts a Polynomial into a string
		string = ""
		for i in range(len(self.coefficients)):
			if i == len(self.coefficients)-1:	# 0th order
				string = string + str(self.coeff(i))
			elif i == len(self.coefficients)-2:	# 1st order
				string = string + str(self.coeff(i)) + "z + "
			else: # higher order terms
				string = string + str(self.coeff(i)) + "z**"+str(len(self.coefficients) - i - 1) + " + "
		return string
	def val(self, v):
		# returns f(v)
		value = 0.
		for i in range(len(self.coefficients)):
			value += self.coeff(i)*v**(len(self.coefficients)-i-1)
		return value
	def roots(self):
		# returns x s.t. f(x) = 0 if 1 < O(f) < 3
		if len(self.coefficients) >= 4 or len(self.coefficients) == 1:
			print "roots only works on order 1 or 2 polynomials"
			return None
		elif len(self.coefficients) == 2: # linear case
			return [-1*self.coeff(1)/self.coeff(0),]
		else: # quadratic
			return [(-self.coeff(1)+complex(self.coeff(1)**2-4.*self.coeff(0)*self.coeff(2),0)**0.5)/(2.*self.coeff(0)),(-self.coeff(1)-complex(self.coeff(1)**2-4.*self.coeff(0)*self.coeff(2),0)**0.5)/(2.*self.coeff(0))]
	def __mul__(self,other):
		return self.mul(other)
	def __call__(self,x):
		return self.val(x)

# I skipped the optional stuff since it's optional, and my goal is hard enough

