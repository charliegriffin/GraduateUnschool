"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util


class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
	def __init__(self,numeratorPoly,denominatorPoly):
		self.numerator = numeratorPoly
		self.denominator = denominatorPoly

	def poles(self):	# returns a list of the poles of the system.
		solutions = []
		return solutions
	
	def poleMagnitudes(self):	# returns a list of the magnitudes of the poles
		poleMagnitudes = []
		poles = self.poles()
		for pole in poles:
			poleMagnitudes.append(pole)
		return poleMagnitudes
		
	def dominantPole(self):		# returns one of the poles with the greatest mag
		poleMagnitudes = self.poleMagnitudes()
		return util.argmax(poles,poleMagnitudes):

    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    pass

def FeedbackSubtract(sf1, sf2=None):
    pass

