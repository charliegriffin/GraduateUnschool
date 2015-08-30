import math
import lib601.ucSearch as ucSearch
import lib601.util as util
import lib601.basicGridMap as basicGridMap
import lib601.gridMap as gridMap
import lib601.sm as sm

mapTestWorld = ['mapTestWorld.py',0.2,util.Point(2.0,5.5),
				util.Pose(2.0,0.5,0.0)]
bigPlanWorld = ['bigPlanWorld.py',0.25,util.Point(3.0,1.0),
				util.Pose(1.0,1.0,0.0)]

class GridDynamics(sm.SM):
	legalInputs = ['u','ur','r','dr','d','dl','l','ul']
	def __init__(self, theMap):
		self.map = theMap
	def nextState(self,state,inp):
		nextState = list(state)
		sCost = 1.
		dCost = 2.**(0.5)
		if inp == 'u':
			nextState[1] += 1
			cost = sCost
		elif inp == 'ur':
			nextState[0] += 1
			nextState[1] += 1
			cost = dCost
		elif inp == 'r':
			nextState[0] += 1
			cost = sCost
		elif inp == 'dr':
			nextState[0] += 1
			nextState[1] -= 1
			cost = dCost
		elif inp == 'd':
			nextState[1] -= 1
			cost = sCost
		elif inp == 'dl':
			nextState[0] -= 1
			nextState[1] -= 1
			cost = dCost
		elif inp == 'l':
			nextState[0] -= 1
			cost = sCost
		elif inp == 'ul':
			nextState[0] -= 1
			nextState[1] += 1
			cost = dCost
		nextState = tuple(nextState)
		if self.map.robotCanOccupy(nextState):
			return (nextState,cost)
		else:
			return (state,0.)
	def getNextValues(self,state,inp):
		if inp not in self.legalInputs:
			return (state, 0.)
		else:
			return self.nextState(state,inp)

class TestGridMap(gridMap.GridMap):
	def __init__(self, gridSquareSize):
		gridMap.GridMap.__init__(self, 0, gridSquareSize * 5,
								0, gridSquareSize*5, gridSquareSize, 100)
	def makeStartingGrid(self):
		grid = util.make2DArray(5, 5, False)
		for i in range(5):
			grid[i][0] = True
			grid[i][4] = True
		for j in range(5):
			grid[0][j] = True
			grid[4][j] = False
		grid[3][3] = True
		return grid
	def robotCanOccupy(self, (xIndex, yIndex)):
		return not self.grid[xIndex][yIndex]

def testGridDynamics():
	gm = TestGridMap(0.15)
	print 'For TestGridMap(0.15):'
	r = GridDynamics(gm)
	print 'legalInputs', util.prettyString(r.legalInputs)
	ans1 = [r.getNextValues((1,1), a) for a in r.legalInputs]
	print 'starting from (1,1)', util.prettyString(ans1)
	ans2 = [r.getNextValues((2,3), a) for a in r.legalInputs]
	print 'starting from (2,3)', util.prettyString(ans2)
	ans3 = [r.getNextValues((3,2),a) for a in r.legalInputs]
	print 'starting from (3,2)', util.prettyString(ans3)
	gm2 = TestGridMap(0.4)
	print 'for TestGridMap(0.4):'
	r2 = GridDynamics(gm2)
	ans4 = [r2.getNextValues((2,3),a) for a in r2.legalInputs]
	print 'starting from (2,3)', util.prettyString(ans4)

testGridDynamics()
	
def planner(initialPose, goalPoint, worldPath, gridSquareSize):
	pass

def testPlanner(world):
	(worldPath, gridSquareSize, goalPoint, initialPost) = world
	planner(initialPost,goalPoint,worldPath,gridSquareSize)
			