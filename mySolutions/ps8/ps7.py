# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:  Charles Griffin
# Collaborators:
# Time:	

import numpy
import random
import pylab
import math

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
 

    def doesClear(self):
		""" Stochastically determines whether this virus particle is cleared from the
		patient's body at a time step. 
		returns: True with probability self.clearProb and otherwise returns
		False.
		"""
		if random.random() < self.clearProb:
			return True
		else:
			return False

    
    def reproduce(self, popDensity):
		"""
		Stochastically determines whether this virus particle reproduces at a
		time step. Called by the update() method in the SimplePatient and
		Patient classes. The virus particle reproduces with probability
		self.maxBirthProb * (1 - popDensity).
		
		If this virus particle reproduces, then reproduce() creates and returns
		the instance of the offspring SimpleVirus (which has the same
		maxBirthProb and clearProb values as its parent).         
		
		popDensity: the population density (a float), defined as the current
		virus population divided by the maximum population.         
		
		returns: a new instance of the SimpleVirus class representing the
		offspring of this virus particle. The child should have the same
		maxBirthProb and clearProb values as this virus. Raises a
		NoChildException if this virus particle does not reproduce.               
		"""
		if random.random() < self.maxBirthProb * (1 - popDensity):
			return SimpleVirus(self.maxBirthProb,self.clearProb)
		else:
			raise NoChildException		#For the exception to work we must raise it, not return it
		

class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
		"""
		Initialization function, saves the viruses and maxPop parameters as
		attributes.
		viruses: the list representing the virus population (a list of
		SimpleVirus instances)
		maxPop: the  maximum virus population for this patient (an integer)
		"""
		self.viruses = viruses
		self.maxPop = maxPop


    def getTotalPop(self):
		"""
		Gets the current total virus population. 
		returns: The total virus population (an integer)
		"""
		return len(self.viruses)

    def update(self):
		"""
		Update the state of the virus population in this patient for a single
		time step. update() should execute the following steps in this order:
		
		- Determine whether each virus particle survives and updates the list
		of virus particles accordingly.   
		- The current population density is calculated. This population density
		  value is used until the next call to update() 
		- Determine whether each virus particle should reproduce and add
		  offspring virus particles to the list of viruses in this patient.                    
		returns: The total virus population at the end of the update (an
		integer)
		"""
		density = float(self.getTotalPop())/float(self.maxPop)
		survivingViruses = []
		newViruses = []
		for virus in self.viruses:
			if virus.doesClear() == False:
				survivingViruses.append(virus)
				try:									#this is how exceptions work
					newViruses.append(virus.reproduce(density))
				except NoChildException:
					newViruses = newViruses
		self.viruses = survivingViruses + newViruses
		return self.getTotalPop()
				

# virusList = []
# for i in range(10):
# 	virusList.append(SimpleVirus(.5,.5))
# patient = SimplePatient(virusList,100)
# print patient.update()

#
# PROBLEM 2
#
def simulationWithoutDrug():
	"""
	Run the simulation and plot the graph for problem 2 (no drugs are used,
	viruses do not have any drug resistance).    
	Instantiates a patient, runs a simulation for 300 timesteps, and plots the
	total virus population as a function of time.    
	"""
	numViruses = 100
	maxPop = 1000
	maxBirthProb = 0.1
	clearProb = 0.05
	timeSteps = 300
	numDataPoints = 300
	virusList = []
	time = 0
	data = []
	for i in range(numViruses):
		virusList.append(SimpleVirus(maxBirthProb,clearProb))
	patient = SimplePatient(virusList,maxPop)
	data.append(patient.getTotalPop())
	for i in range(numDataPoints):					# produce a data point
		for j in range(timeSteps/numDataPoints):	# simulate a time step
			patient.update()
			time += 1
			data.append(patient.getTotalPop())
# 	pylab.plot(range(301),data)
# 	pylab.title("Virus Population in Patient vs. Time (hrs)")
# 	pylab.ylabel("Avg Virus Population")
# 	pylab.xlabel("Time (hrs)")
# 	pylab.show()
	return data						# I'm returning a list here because it can be plotted
									# directly, as per the specifications of the assignment
									# the sorting that is done later is to make computing
									# averages and error bars easier

def stdDev(X):						# I understand that the sqrt(sample Var) is a baised
	mean = sum(X)/float(len(X))		# estimator for sigma, however this still yields
	tot = 0.0						# a close estimate for the 1sigma confidence interval
	for x in X:
		tot += (x - mean)**2
	return math.sqrt(tot/len(X))
# 	
# numTrials = 1000
# dataSets = []
# avgData = []
# dataDict = {}
# error = []
# for i in range(numTrials):
# 	dataSets.append(simulationWithoutDrug())
# for i in range(len(dataSets[0])):			# sort the data into {time:[value,...,value]}
# 	dataDict[i] = []
# 	for j in range(len(dataSets)):
# 		dataDict[i].append(dataSets[j][i])
# for key in dataDict:						# loop over the keys
# 	avgData.append(sum(dataDict[key])/float(len(dataDict[key])))
# 	error.append(stdDev(dataDict[key]))
# 
# pylab.errorbar(range(301),avgData,yerr = error)
# pylab.title("Virus Population in Patient vs. Time (hrs) (1000 Trials)")
# pylab.ylabel("Avg Virus Population")
# pylab.xlabel("Time (hrs)")
# pylab.savefig("virusPop.png")

		