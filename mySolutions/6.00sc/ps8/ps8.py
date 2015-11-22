# 6.00 Problem Set 8
#
# Name: Charlie Griffin
# Collaborators:
# Time: 5:00



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):
	"""
    Representation of a virus which can have drug resistance.
    """      
	def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
		self.maxBirthProb = maxBirthProb
		self.clearProb = clearProb
		self.resistances = resistances
		self.mutProb = mutProb
        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """

	def isResistantTo(self, drug):
# 
# 		"""
#         Get the state of this virus particle's resistance to a drug. This method
#         is called by getResistPop() in Patient to determine how many virus
#         particles have resistance to a drug.    
# 
#         drug: The drug (a string)
#         returns: True if this virus instance is resistant to the drug, False
#         otherwise.
#         """
		return self.resistances[drug]


	def reproduce(self, popDensity, activeDrugs):
# 
# 		"""
#         Stochastically determines whether this virus particle reproduces at a
#         time step. Called by the update() method in the Patient class.
# 
#         If the virus particle is not resistant to any drug in activeDrugs,
#         then it does not reproduce. Otherwise, the virus particle reproduces
#         with probability:       
#         
#         self.maxBirthProb * (1 - popDensity).                       
#         
#         If this virus particle reproduces, then reproduce() creates and returns
#         the instance of the offspring ResistantVirus (which has the same
#         maxBirthProb and clearProb values as its parent). 
# 
#         For each drug resistance trait of the virus (i.e. each key of
#         self.resistances), the offspring has probability 1-mutProb of
#         inheriting that resistance trait from the parent, and probability
#         mutProb of switching that resistance trait in the offspring.        
# 
#         For example, if a virus particle is resistant to guttagonol but not
#         grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
#         that the offspring will lose resistance to guttagonol and a 90% 
#         chance that the offspring will be resistant to guttagonol.
#         There is also a 10% chance that the offspring will gain resistance to
#         grimpex and a 90% chance that the offspring will not be resistant to
#         grimpex.
# 
#         popDensity: the population density (a float), defined as the current
#         virus population divided by the maximum population        
# 
#         activeDrugs: a list of the drug names acting on this virus particle
#         (a list of strings). 
#         
#         returns: a new instance of the ResistantVirus class representing the
#         offspring of this virus particle. The child should have the same
#         maxBirthProb and clearProb values as this virus. Raises a
#         NoChildException if this virus particle does not reproduce.         
#         """
		if activeDrugs == []:
			if random.random() < self.maxBirthProb * (1-popDensity):
				newResistances = {}
				for drug in self.resistances:
					if self.isResistantTo(drug):		# inheritance
						if random.random() < 1 - self.mutProb:	# inherits the resistance
							newResistances[drug] = True
						else:
							newResistances[drug] = False
					else:
						if random.random() < self.mutProb:	# switches the trait on
							newResistances[drug] = True
						else:
							newResistances[drug] = False
				return ResistantVirus(self.maxBirthProb,self.clearProb,newResistances,self.mutProb)
			else:
				raise NoChildException
		for drug in activeDrugs:
			if self.isResistantTo(drug):	#resistant to a drug
				if random.random() < self.maxBirthProb *(1 - popDensity):
					newResistances = {}
					for drug in self.resistances:
						if self.isResistantTo(drug):		# inheritance
							if random.random() < 1 - self.mutProb:	# inherits the resistance
								newResistances[drug] = True
							else:
								newResistances[drug] = False
						else:
							if random.random() < self.mutProb:	# switches the trait on
								newResistances[drug] = True
							else:
								newResistances[drug] = False
					return ResistantVirus(self.maxBirthProb,self.clearProb,newResistances,self.mutProb)
		raise NoChildException 			#not resistant to any drugs
				

# maxBirthProb = 1.0
# clearProb = 0.05
# resistances = {'advil':True,'tylenol':False}
# mutProb = 0.01
# virus = ResistantVirus(maxBirthProb,clearProb,resistances,mutProb)
# # for drug in resistances:
# # 	print drug, virus.isResistantTo(drug)
# # print resistances
# activeDrugs = ['tylenol','advil']
# popDensity = 0.5
# virusList = []


class Patient(SimplePatient):

	"""
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
	"""

	def __init__(self, viruses, maxPop):
# 		"""
#         Initialization function, saves the viruses and maxPop parameters as
#         attributes. Also initializes the list of drugs being administered
#         (which should initially include no drugs).               
# 
#         viruses: the list representing the virus population (a list of
#         SimpleVirus instances)
#         
#         maxPop: the  maximum virus population for this patient (an integer)
#         """
		self.viruses = viruses
		self.maxPop = maxPop
		self.drugsAdministered = []


	def addPrescription(self, newDrug):

# 		"""
#         Administer a drug to this patient. After a prescription is added, the 
#         drug acts on the virus population for all subsequent time steps. If the
#         newDrug is already prescribed to this patient, the method has no effect.
# 
#         newDrug: The name of the drug to administer to the patient (a string).
# 
#         postcondition: list of drugs being administered to a patient is updated
#         """
		# TODO
		# should not allow one drug being added to the list multiple times
		if newDrug not in self.drugsAdministered:
			self.drugsAdministered.append(newDrug)
		return None

	def getPrescriptions(self):

# 		"""
#         Returns the drugs that are being administered to this patient.
#         returns: The list of drug names (strings) being administered to this
#         patient.
#         """
		return self.drugsAdministered
        # TODO
        

	def getResistPop(self, drugResist):
# 		"""
#         Get the population of virus particles resistant to the drugs listed in 
#         drugResist.        
# 
#         drugResist: Which drug resistances to include in the population (a list
#         of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])
# 
#         returns: the population of viruses (an integer) with resistances to all
#         drugs in the drugResist list.
#         """
		resistantPopulation = 0
		for virus in self.viruses:
			for drug in drugResist:		#go through the list of drug resistances we are interested in
				   if virus.isResistantTo(drug):	# virus is resistant to the drug
						resistantPopulation += 1
						break			# since the virus is resistant we don't need to test the remaining drugs
		return resistantPopulation

	def update(self):

#         """
#         Update the state of the virus population in this patient for a single
#         time step. update() should execute these actions in order:
#         
#         - Determine whether each virus particle survives and update the list of 
#           virus particles accordingly          
#         - The current population density is calculated. This population density
#           value is used until the next call to update().
#         - Determine whether each virus particle should reproduce and add
#           offspring virus particles to the list of viruses in this patient. 
#           The listof drugs being administered should be accounted for in the
#           determination of whether each virus particle reproduces. 
# 
#         returns: the total virus population at the end of the update (an
#         integer)
#         """
		survivingViruses = []
		newViruses = []
		for virus in self.viruses:				# determine surviving viruses
			if virus.doesClear() == False:
				survivingViruses.append(virus)
		density = float(self.getTotalPop())/float(self.maxPop)	#calculate density
		for virus in survivingViruses:				# virus reproduction
			try:
				newViruses.append(virus.reproduce(density,self.drugsAdministered))
			except NoChildException:
				pass
		self.viruses = survivingViruses + newViruses
		return self.getTotalPop()


# maxBirthProb = 1.0
# clearProb = 0.05
# resistances = {'advil':True,'tylenol':False}
# resistances2 = {'advil':False,'tylenol':False}
# resistances3 = {'advil':True,'tylenol':True}
# mutProb = 0.01
# # viruses = []
# # viruses.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
# # viruses.append(ResistantVirus(maxBirthProb,clearProb,resistances2,mutProb))
# # viruses.append(ResistantVirus(maxBirthProb,clearProb,resistances3,mutProb))
# # patient = Patient(viruses,100)
# # print patient.getPrescriptions()
# # patient.addPrescription("advil")
# # print patient.getPrescriptions()
# # print patient.addPrescription("advil")
# # print patient.getPrescriptions()
# # print patient.getResistPop(['advil'])
# # print patient.getResistPop(['advil','tylenol'])
# virusList = []
# for i in range(10):
# 	virusList.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
# patient = Patient(virusList,100)
# print patient.update()
#
# PROBLEM 2
#

def simulationWithDrug():
	numViruses = 100
	maxPop = 1000
	maxBirthProb = 0.1
	clearProb = 0.05
	resistances = {'guttagonol':False}
	mutProb = 0.005
	virusList = []
	totalPopulations = []
	resistantPopulations = []
	numDataPoints = 150
	timeSteps = 150
	for i in range(numViruses):
		virusList.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
	patient = Patient(virusList,maxPop)
	totalPopulations.append(patient.getTotalPop())
	resistantPopulations.append(patient.getResistPop(['guttagonol']))
	for i in range(numDataPoints):
		for j in range(timeSteps/numDataPoints):
			patient.update()
			totalPopulations.append(patient.getTotalPop())
			resistantPopulations.append(patient.getResistPop(['guttagonol']))
	patient.addPrescription('guttagonol')
	for i in range(numDataPoints):
		for j in range(timeSteps/numDataPoints):
			patient.update()
			totalPopulations.append(patient.getTotalPop())
			resistantPopulations.append(patient.getResistPop(['guttagonol']))
# 	pylab.plot(range(301),totalPopulations)
# 	pylab.plot(range(301),resistantPopulations)
# 	pylab.title("Virus Population in Patient vs. Time (hrs)")
# 	pylab.ylabel("Avg Virus Population")
# 	pylab.xlabel("Time (hrs)")
# 	pylab.show()
 	return {"totalPop":totalPopulations,"resistantPop":resistantPopulations}
# 
#     """
# 
#     Runs simulations and plots graphs for problem 4.
#     Instantiates a patient, runs a simulation for 150 timesteps, adds
#     guttagonol, and runs the simulation for an additional 150 timesteps.
#     total virus population vs. time and guttagonol-resistant virus population
#     vs. time are plotted
#     """
#     # TODO

# numTrials = 1000
# totalDataSets = []
# resistantDataSets = []
# avgTotalData = []
# avgResistantData = []
# totalDataDict = {}
# resistantDataDict = {}
# totalError = []
# resistantError = []
# for i in range(numTrials):
# 	results = simulationWithDrug()
# 	totalDataSets.append(results["totalPop"])
# 	resistantDataSets.append(results["resistantPop"])
# for i in range(len(totalDataSets[0])):
# 	totalDataDict[i] = []
# 	resistantDataDict[i] = []
# 	for j in range(len(totalDataSets)):
# 		totalDataDict[i].append(totalDataSets[j][i])
# 		resistantDataDict[i].append(resistantDataSets[j][i])
# for key in totalDataDict:
# 	avgTotalData.append(sum(totalDataDict[key])/float(len(totalDataDict[key])))
# 	totalError.append(stdDev(totalDataDict[key]))
# for key in resistantDataDict:
# 	avgResistantData.append(sum(resistantDataDict[key])/float(len(resistantDataDict[key])))
# 	resistantError.append(stdDev(resistantDataDict[key]))
# 
# total = pylab.errorbar(range(301),avgTotalData,yerr = totalError,label='total population')
# resistant = pylab.errorbar(range(301),avgResistantData,yerr = resistantError,label='resistant population')
# pylab.title("Virus Population in Patient vs. Time (hrs) (1000 Trials)")
# pylab.ylabel("Avg Virus Population")
# pylab.xlabel("Time (hrs)")
# pylab.legend([total,resistant],['total population','resistant population'])
# pylab.savefig("virusPopWithDrug.png")

#
# PROBLEM 3
#        

def simulationDelayedTreatment(numTrials):
# 
#     """
#     Runs simulations and make histograms for problem 5.
#     Runs multiple simulations to show the relationship between delayed treatment
#     and patient outcome.
#     Histograms of final total virus populations are displayed for delays of 300,
#     150, 75, 0 timesteps (followed by an additional 150 timesteps of
#     simulation).    
#     """
	finalVirusPop0BeforeDrug = []
	finalVirusPop75BeforeDrug = []
	finalVirusPop150BeforeDrug = []
	finalVirusPop300BeforeDrug = []
	for j in range(numTrials):
		numViruses = 100
		maxPop = 1000
		maxBirthProb = 0.1
		clearProb = 0.05
		resistances = {'guttagonol':False}
		mutProb = 0.005
		virusList = []
		timeStepsAfterDrug = 150
		timeStepsBeforeDrug = 0
		for i in range(numViruses):
			virusList.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
		patient = Patient(virusList,maxPop)
		for i in range(timeStepsBeforeDrug):	# advances time through the delay
			patient.update()
		patient.addPrescription('guttagonol')
		for i in range(timeStepsAfterDrug):		# advances time after drug treatment
			patient.update()
		finalVirusPop0BeforeDrug.append(patient.getTotalPop())
		patient = Patient(virusList,maxPop)		# initializes a new patient before a new trial
		timeStepsBeforeDrug = 75
		patient = Patient(virusList,maxPop)
		for i in range(timeStepsBeforeDrug):	# advances time through the delay
			patient.update()
		patient.addPrescription('guttagonol')
		for i in range(timeStepsAfterDrug):		# advances time after drug treatment
			patient.update()
		finalVirusPop75BeforeDrug.append(patient.getTotalPop())
		patient = Patient(virusList,maxPop)
		timeStepsBeforeDrug = 150
		patient = Patient(virusList,maxPop)
		for i in range(timeStepsBeforeDrug):	# advances time through the delay
			patient.update()
		patient.addPrescription('guttagonol')
		for i in range(timeStepsAfterDrug):		# advances time after drug treatment
			patient.update()
		finalVirusPop150BeforeDrug.append(patient.getTotalPop())
		patient = Patient(virusList,maxPop)
		timeStepsBeforeDrug = 300
		patient = Patient(virusList,maxPop)
		for i in range(timeStepsBeforeDrug):	# advances time through the delay
			patient.update()
		patient.addPrescription('guttagonol')
		for i in range(timeStepsAfterDrug):		# advances time after drug treatment
			patient.update()
		finalVirusPop300BeforeDrug.append(patient.getTotalPop())
	return {0:finalVirusPop0BeforeDrug,75:finalVirusPop75BeforeDrug,150:finalVirusPop150BeforeDrug,300:finalVirusPop300BeforeDrug}
	
# numTrials = 100
# numBins = 10
# binEdges = range(0,25*(numBins+1),25)
# delayedTreatmentData = simulationDelayedTreatment(numTrials)
# for key in delayedTreatmentData:
#   	print delayedTreatmentData[key]
# 	pylab.hist(delayedTreatmentData[key])
# 	pylab.title(str(key)+" Hours without Treatment and 150 Hours with Treatment")
# 	pylab.xlabel('final total virus population')
# 	pylab.ylabel('number of patients (out of 100)')
# 	pylab.savefig(str(key)+'DelayHistogram.png')
# 	pylab.show()
# 	pylab.clf


#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment(numTrials):
# 
#     """
#     Runs simulations and make histograms for problem 6.
#     Runs multiple simulations to show the relationship between administration
#     of multiple drugs and patient outcome.
#    
#     Histograms of final total virus populations are displayed for lag times of
#     150, 75, 0 timesteps between adding drugs (followed by an additional 150
#     timesteps of simulation).
#     """
	finalVirusPop0BeforeGrimpex = []
	finalVirusPop75BeforeGrimpex = []
	finalVirusPop150BeforeGrimpex = []
	finalVirusPop300BeforeGrimpex = []
	finalVirusPops = {}
	maxPop = 1000
	numViruses = 100
	maxBirthProb = 0.1
	clearProb = 0.05
	mutProb = 0.005
	timeStepsBeforeGuttagonol = 150
	resistances = {'guttagonol':False,'grimpex':False}
	timeStepsBeforeGrimpex = [0,75,150,300]
	for number in timeStepsBeforeGrimpex:
		finalVirusPops[number] = []
	timeStepsAfterGrimpex = 150
	for j in range(numTrials):
		print j		# use print statements to keep track of the progress of the code
		for timeBeforeGrimpex in timeStepsBeforeGrimpex:
			virusList = []
			for i in range(numViruses):
				virusList.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
			patient = Patient(virusList,maxPop)
	# run the simulation for 150 time steps before administering guttagonol
			for i in range(timeStepsBeforeGuttagonol):
				patient.update()
			patient.addPrescription('guttagonol')
	# run the simulation for 300,150,75,and 0 time steps before administering grimpex
			for i in range(timeBeforeGrimpex):
				patient.update()
			patient.addPrescription('grimpex')
	#	run the simulation for an additional 150 time steps
			for i in range(timeStepsAfterGrimpex):
				patient.update()
			finalVirusPops[timeBeforeGrimpex].append(patient.getTotalPop())
	return finalVirusPops
	#	plot a histogram of the final total virus populations under each condition

# nTrials = 200
# doubleDelayData = simulationTwoDrugsDelayedTreatment(nTrials)
# for key in doubleDelayData:
# 	pylab.hist(doubleDelayData[key])
# 	pylab.title(str(key)+" Hours Between Administration of the Two Drugs")
# 	pylab.xlabel('final total virus population')
# 	pylab.ylabel('number of patients (out of '+str(nTrials)+')')
# 	pylab.savefig(str(key)+'DoubleDelayHistogram.png')
# 	pylab.show()
# 	pylab.clf

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations(numTrials):
# 
#     """
# 
#     Run simulations and plot graphs examining the relationship between
#     administration of multiple drugs and patient outcome.
#     Plots of total and drug-resistant viruses vs. time are made for a
#     simulation with a 300 time step delay between administering the 2 drugs and
#     a simulations for which drugs are administered simultaneously.        
# 
#     """
	# Use the same initialization parameters as you did for problem 4
	totalVirusPops = {}
	guttagonolResistantVirusPops = {}
	grimpexResistantVirusPops = {}
	totalPopsDelay = [[],]
	totalPopsNoDelay = [[],]
	totalPopulations = {0:[],300:[]}
	grimResistPopulations = {0:[],300:[]}
	guttResistPopulations = {0:[],300:[]}
	maxPop = 1000
	numViruses = 100
	maxBirthProb = 0.1
	clearProb = 0.05
	mutProb = 0.005
	timeStepsBeforeGuttagonol = 150
	resistances = {'guttagonol':False,'grimpex':False}
	timeStepsBeforeGrimpex = [0,300]
	for number in timeStepsBeforeGrimpex:
		totalVirusPops[number] = []
		guttagonolResistantVirusPops[number] = []
		grimpexResistantVirusPops[number] = []
	timeStepsAfterGrimpex = 150
	for j in range(numTrials):
		print j+1,'/',numTrials		# use print statements to keep track of the progress of the code
 		for timeBeforeGrimpex in timeStepsBeforeGrimpex:
# 			totalVirusPops[timeBeforeGrimpex][0].append(range(timeStepsBeforeGuttagonol + timeBeforeGrimpex + timeStepsAfterGrimpex))
# 			guttagonolResistantVirusPops[timeBeforeGrimpex][0].append(totalVirusPops[timeBeforeGrimpex][0])
# 			grimpexResistantVirusPops[timeBeforeGrimpex][0].append(totalVirusPops[timeBeforeGrimpex][0])
			totalPopulation = []
			grimResistPopulation = []
			guttResistPopulation = []
			virusList = []
			for i in range(numViruses):
				virusList.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
			patient = Patient(virusList,maxPop)
# 			totalPopulations[timeBeforeGrimpex].append(patient.getTotalPop())
# 			grimResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['grimpex']))
# 			guttResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['guttagonol']))
			totalPopulation.append(patient.getTotalPop())
			grimResistPopulation.append(patient.getResistPop(['grimpex']))
			guttResistPopulation.append(patient.getResistPop(['guttagonol']))
	# run the simulation for 150 time steps before administering guttagonol
			for i in range(timeStepsBeforeGuttagonol):
				patient.update()
# 				totalPopulations[timeBeforeGrimpex].append(patient.getTotalPop())
# 				grimResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['grimpex']))
# 				guttResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['guttagonol']))
				totalPopulation.append(patient.getTotalPop())
				grimResistPopulation.append(patient.getResistPop(['grimpex']))
				guttResistPopulation.append(patient.getResistPop(['guttagonol']))				
			patient.addPrescription('guttagonol')
	# run the simulation for 300,150,75,and 0 time steps before administering grimpex
			for i in range(timeBeforeGrimpex):
				patient.update()
# 				totalPopulations[timeBeforeGrimpex].append(patient.getTotalPop())
# 				grimResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['grimpex']))
# 				guttResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['guttagonol']))
				totalPopulation.append(patient.getTotalPop())
				grimResistPopulation.append(patient.getResistPop(['grimpex']))
				guttResistPopulation.append(patient.getResistPop(['guttagonol']))
			patient.addPrescription('grimpex')
	#	run the simulation for an additional 150 time steps
			for i in range(timeStepsAfterGrimpex):
				patient.update()
# 				totalPopulations[timeBeforeGrimpex].append(patient.getTotalPop())
# 				grimResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['grimpex']))
# 				guttResistPopulations[timeBeforeGrimpex].append(patient.getResistPop(['guttagonol']))
				totalPopulation.append(patient.getTotalPop())
				grimResistPopulation.append(patient.getResistPop(['grimpex']))
				guttResistPopulation.append(patient.getResistPop(['guttagonol']))
# 			finalVirusPops[timeBeforeGrimpex].append(patient.getTotalPop())
			totalPopulations[timeBeforeGrimpex].append(totalPopulation)
			grimResistPopulations[timeBeforeGrimpex].append(grimResistPopulation)
			guttResistPopulations[timeBeforeGrimpex].append(guttResistPopulation)
#	finalData = {'total':totalVirusPops,'guttagonol':guttagonolResistantVirusPops,'grimpex':grimpexResistantVirusPops}
	return [totalPopulations,grimResistPopulations,guttResistPopulations]
	#	plot a histogram of the final total virus populations under each condition

nTrials = 100
data = simulationTwoDrugsVirusPopulations(nTrials)
# for timeDelay in data[0]:
# 	for populationSets in data:
# 		for set in populationSets:
# 		print len(populationSets[timeDelay])
averagedTotalNoDelay = {}
avgTotalNoDelay = []
totalErrorNoDelay = []
for i in range(len(data[0][0][0])):
	averagedTotalNoDelay[i] = []
for j in range(len(data[0][0])):
	for i in range(len(data[0][0][j])):
 		averagedTotalNoDelay[i].append(data[0][0][j][i])
for key in averagedTotalNoDelay:
 	avgTotalNoDelay.append(sum(averagedTotalNoDelay[key])/float(len(averagedTotalNoDelay[key])))
 	totalErrorNoDelay.append(stdDev(averagedTotalNoDelay[key]))
totalNoDelay = pylab.errorbar(range(301),avgTotalNoDelay,yerr = totalErrorNoDelay,label='total population')
averagedGuttNoDelay = {}
avgGuttNoDelay = []
guttErrorNoDelay = []
for i in range(len(data[2][0][0])):
	averagedGuttNoDelay[i] = []
for j in range(len(data[2][0])):
	for i in range(len(data[2][0][j])):
 		averagedGuttNoDelay[i].append(data[2][0][j][i])
for key in averagedGuttNoDelay:
 	avgGuttNoDelay.append(sum(averagedGuttNoDelay[key])/float(len(averagedGuttNoDelay[key])))
 	guttErrorNoDelay.append(stdDev(averagedGuttNoDelay[key]))
guttNoDelay = pylab.errorbar(range(301),avgGuttNoDelay,yerr = guttErrorNoDelay,label='guttagonol resistant')
averagedGrimNoDelay = {}
avgGrimNoDelay = []
grimErrorNoDelay = []
for i in range(len(data[1][0][0])):
	averagedGrimNoDelay[i] = []
for j in range(len(data[1][0])):
	for i in range(len(data[1][0][j])):
 		averagedGrimNoDelay[i].append(data[1][0][j][i])
for key in averagedGrimNoDelay:
 	avgGrimNoDelay.append(sum(averagedGrimNoDelay[key])/float(len(averagedGrimNoDelay[key])))
 	grimErrorNoDelay.append(stdDev(averagedGrimNoDelay[key]))
grimNoDelay = pylab.errorbar(range(301),avgGrimNoDelay,yerr = grimErrorNoDelay,label='grimpex resistant')
pylab.legend([totalNoDelay,guttNoDelay,grimNoDelay],['total population','guttagonol resistant','grimpex resistant'])
pylab.title("Virus Population in Patient vs. Time (hrs) ("+str(nTrials)+" Trials) no Delay between Drugs")
pylab.ylabel("Avg Virus Population")
pylab.xlabel("Time (hrs)")
pylab.savefig('noDelayBetweenDrugs.png')
pylab.show()
pylab.clf()

averagedTotalDelay = {}
avgTotalDelay = []
totalErrorDelay = []
for i in range(len(data[0][300][0])):
	averagedTotalDelay[i] = []
for j in range(len(data[0][300])):
	for i in range(len(data[0][300][j])):
 		averagedTotalDelay[i].append(data[0][300][j][i])
for key in averagedTotalDelay:
 	avgTotalDelay.append(sum(averagedTotalDelay[key])/float(len(averagedTotalDelay[key])))
 	totalErrorDelay.append(stdDev(averagedTotalDelay[key]))
totalDelay = pylab.errorbar(range(601),avgTotalDelay,yerr = totalErrorDelay,label='total population')
averagedGuttDelay = {}
avgGuttDelay = []
guttErrorDelay = []
for i in range(len(data[2][300][0])):
	averagedGuttDelay[i] = []
for j in range(len(data[2][300])):
	for i in range(len(data[2][300][j])):
 		averagedGuttDelay[i].append(data[2][300][j][i])
for key in averagedGuttDelay:
 	avgGuttDelay.append(sum(averagedGuttDelay[key])/float(len(averagedGuttDelay[key])))
 	guttErrorDelay.append(stdDev(averagedGuttDelay[key]))
guttDelay = pylab.errorbar(range(601),avgGuttDelay,yerr = guttErrorDelay,label='guttagonol resistant')
averagedGrimDelay = {}
avgGrimDelay = []
grimErrorDelay = []
for i in range(len(data[1][300][0])):
	averagedGrimDelay[i] = []
for j in range(len(data[1][300])):
	for i in range(len(data[1][300][j])):
 		averagedGrimDelay[i].append(data[1][300][j][i])
for key in averagedGrimDelay:
 	avgGrimDelay.append(sum(averagedGrimDelay[key])/float(len(averagedGrimDelay[key])))
 	grimErrorDelay.append(stdDev(averagedGrimDelay[key]))
grimDelay = pylab.errorbar(range(601),avgGrimDelay,yerr = grimErrorDelay,label='grimpex resistant')
pylab.legend([totalDelay,guttDelay,grimDelay],['total population','guttagonol resistant','grimpex resistant'])
pylab.title("Virus Population in Patient vs. Time (hrs) ("+str(nTrials)+" Trials) Delay between Drugs")
pylab.ylabel("Avg Virus Population")
pylab.xlabel("Time (hrs)")
pylab.savefig('delayBetweenDrugs.png')
pylab.show()
pylab.clf()