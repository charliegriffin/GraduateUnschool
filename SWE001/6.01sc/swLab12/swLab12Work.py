import lib601.dist as dist
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.util as util

class StateEstimator(sm.SM):
	def __init__(self, model):
		self.model = model
		self.startState = model.startDistribution
	def getNextValues(self, state, inp):
		(o, i) = inp
		print inp
# 		print "state = ", state
# 		print "observation = ", o
# # 		print self.model.observationDistribution(o)
# 		possibleAs = state.support()
# 		print "jdist = ", dist.JDist(state,self.model.observationDistribution)
		sGo = dist.bayesEvidence(state, self.model.observationDistribution,o)
		print "sGo = ", sGo
		aGo = self.bayesEvidence(state,o)
		print "aGo = ", aGo
		dSPrime = dist.totalProbability(sGo,
		self.model.transitionDistribution(i))
		return (dSPrime, dSPrime)
	def bayesEvidence(self,state,observation):	# P(O|S)(observation distribution)*P(S)(state distribution)/P(O)
		joint = dist.JDist(state, self.model.observationDistribution)
		belief = joint.conditionOnVar(1,observation)
		return belief


# Test

transitionTable = \
   {'good': dist.DDist({'good' : 0.7, 'bad' : 0.3}),
    'bad' : dist.DDist({'good' : 0.1, 'bad' : 0.9})}
observationTable = \
   {'good': dist.DDist({'perfect' : 0.8, 'smudged' : 0.1, 'black' : 0.1}),
    'bad': dist.DDist({'perfect' : 0.1, 'smudged' : 0.7, 'black' : 0.2})}

copyMachine = \
 ssm.StochasticSM(dist.DDist({'good' : 0.9, 'bad' : 0.1}),
                # Input is irrelevant; same dist no matter what
                lambda i: lambda s: transitionTable[s],
                lambda s: observationTable[s])
obs = [('perfect', 'step'), ('smudged', 'step'), ('perfect', 'step')]

cmse = StateEstimator(copyMachine)

print cmse.transduce(obs)
# Expected outputs:
# (py26)Charles-Griffins-MacBook-Pro:swLab12 charlesgriffin$ python swLab12Work.py 
# [DDist(bad: 0.308219, good: 0.691781), DDist(bad: 0.754327, good: 0.245673), DDist(bad: 0.466413, good: 0.533587)]
# (py26)Charles-Griffins-MacBook-Pro:swLab12 charlesgriffin$ python swLab12Work.py 
# [DDist(bad: 0.308219, good: 0.691781), DDist(bad: 0.754327, good: 0.245673), DDist(bad: 0.466413, good: 0.533587)]
# (py26)Charles-Griffins-MacBook-Pro:swLab12 charlesgriffin$ python swLab12Work.py 
# [DDist(bad: 0.308219, good: 0.691781), DDist(bad: 0.754327, good: 0.245673), DDist(bad: 0.466413, good: 0.533587)]
# (py26)Charles-Griffins-MacBook-Pro:swLab12 charlesgriffin$ python swLab12Work.py 
# [DDist(bad: 0.308219, good: 0.691781), DDist(bad: 0.754327, good: 0.245673), DDist(bad: 0.466413, good: 0.533587)]
# (py26)Charles-Griffins-MacBook-Pro:swLab12 charlesgriffin$ python swLab12Work.py 
# [DDist(bad: 0.308219, good: 0.691781), DDist(bad: 0.754327, good: 0.245673), DDist(bad: 0.466413, good: 0.533587)]
# 
# 
