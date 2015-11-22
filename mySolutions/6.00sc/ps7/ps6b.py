import random, pylab

def rollDie():
	return random.choice([1,2,3,4,5,6])
	
def roll(numDie):
	hand = []
	for i in range(numDie):
		hand.append(rollDie())
	return hand
	

def yahtzeeTrial(numRolls,numDie = 5):
	yahtzees = 0
	for i in range(numRolls):
		hand = roll(numDie)
		if hand[0] == hand[1] == hand[2] == hand[3] == hand[4]: # Yahtzee!
			yahtzees += 1
	return yahtzees/float(numRolls)
	
	
def yahtzeeSim(numRollsPerTrial, numTrials, numDie = 5):
	fracYahtzee = []
	for i in range(numTrials):
		fracYahtzee.append(yahtzeeTrial(numRollsPerTrial,numDie))
	mean = sum(fracYahtzee)/float(len(fracYahtzee))
	return mean

print yahtzeeSim(10000,1000)