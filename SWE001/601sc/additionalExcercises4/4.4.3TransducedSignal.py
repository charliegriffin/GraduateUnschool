import lib601.sm as sm
import lib601.poly as poly
import lib601.sig
from lib601.sig import *
# Part 1: Implementation

def samplesInRange(sig,lo,hi):
	return [sig.sample(i) for i in range(lo,hi)]
	
class TransducedSignal(Signal):
	def __init__(self, s, m):
		self.s = s
		self.m = m
	def sample(self, n):
		if n<0:
			return 0
		else:
			return self.m.transduce(self.s.sample(n))
			
# Part 2: Application
polyList = []
for i in range(51):
	if i == 0 or i == 20 or i == 50:
		polyList.append(100)
	else:
		polyList.append(0)
p = poly.Polynomial(polyList)
inputSig = polyR(UnitSampleSignal(),p)
