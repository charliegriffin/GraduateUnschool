# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes
#from ps6_verify_movement27 import testRobotMovement

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

# pos1 = Position(1,2)
# print pos1.getX(),pos1.getY()
# #pos1 = pos1.getNewPosition(0,1)
# #print pos1.getX(),pos1.getY()
# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tiles = {}
        for x in range(width):
        	for y in range(height):
        		self.tiles[(x,y)] = "dirty"
#        print "tiles = ",self.tiles
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles[(math.floor(pos.getX()),math.floor(pos.getY()))] = "clean"
#       math.floor() returns the largest integer value <= x, as a float (different than int()

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.tiles[(math.floor(m),math.floor(n))] == "clean":
        	return True
        else :
        	return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width*self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return sum(x == "clean" for x in self.tiles.values()) #sums over the first condition for all the values in the dictionary

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.random()*self.width,random.random()*self.height)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return (math.floor(pos.getX()),math.floor(pos.getY())) in self.tiles.keys()


# room1 = RectangularRoom(3,3)
# room1.cleanTileAtPosition(pos1)
# print room1.isTileCleaned(0,0), "== False"
# print room1.isTileCleaned(1,2), "== True"
# print room1.getNumTiles(), "== 9"
# print room1.getNumCleanedTiles(), "== 1"
# pos1 = pos1.getNewPosition(180,1)
# room1.cleanTileAtPosition(pos1)
# pos1 = pos1.getNewPosition(180,1)
# room1.cleanTileAtPosition(pos1)
# print room1.getNumCleanedTiles(), "== 3"
# for i in range(100):
# 	pos2 = room1.getRandomPosition()
# 	print room1.isPositionInRoom(pos2), "== True"
# out = Position(3,3.1)
# print room1.isPositionInRoom(out), "== False"
# print "\n\n\n\n\n\n\n\n\n\n"

class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room	#initializes robot in room
        self.speed = speed	#initializes speed
        self.dir = random.uniform(0,360)	#gives the robot a random direction
        self.pos = self.room.getRandomPosition()	#gives the robot a random position
        self.room.cleanTileAtPosition(self.pos)		#cleans the tile at that random position

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
		raise notImplementedError
#         newPos = self.pos.getNewPosition(self.dir,self.speed)
#         while self.room.isPositionInRoom(newPos) == False:
#         	self.dir = random.uniform(0,360)
#         	newPos = self.pos.getNewPosition(self.dir,self.speed)
#         	print "hit a wall"   
#         print self.room.isPositionInRoom(newPos), "= True"
#         self.pos = newPos
#         self.room.cleanTileAtPosition(self.pos)

        	

# print "start here"
# room1 = RectangularRoom(3,3)
# robot1 = Robot(room1,1)
# robot1.updatePositionAndClean()

# === Problem 2
class StandardRobot(Robot):	#the main idea is we already have a robot, we just want to add its clearning strategy
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        newPos = self.pos.getNewPosition(self.dir,self.speed)
        if self.room.isPositionInRoom(newPos):
        	self.setRobotPosition(newPos)
        	self.room.cleanTileAtPosition(self.pos)
        else :
        	self.dir = random.uniform(0,360)


""" How to use a standard robot """
# room1 = RectangularRoom(3,3)
# robot1 = StandardRobot(room1,1)
# robot1.updatePositionAndClean()

# === Problem 3
### Remove Comments to Show Animation
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    times = []
    for j in range(num_trials):					# run the trials
#  	anim = ps6_visualize.RobotVisualization(num_robots,width,height,0.25)
    	room = RectangularRoom(width,height)	# initialize the room
    	robots = []								
    	for i in range(num_robots):				# put robots in the room
    		robots += [robot_type(room,speed),]
    	times += [0,]								# starting at time = 0
     	while float(room.getNumCleanedTiles())/float(room.getNumTiles()) < min_coverage:
    		times[j] += 1						# clean the rooms to >= the minimum coverage
#     		anim.update(room,robots)
     		for robot in robots:					# increments over all robots
    			robot.updatePositionAndClean()
#   	anim.done()
    avgTime = 0
    for time in times:
    	avgTime += time
    avgTime = avgTime/float(num_trials)
    return avgTime
    
    	
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """    
    
# runSimulation(5, 1.0, 15, 15, 0.8, 30, StandardRobot)
# avg = runSimulation(10, 1.0, 15, 20, 0.8, 30, StandardRobot)
# print runSimulation(1, 1.0, 5, 5, 1., 1000, StandardRobot), "~ 150"
# print runSimulation(1, 2.0, 5, 5, 1., 1000, StandardRobot), "~ 100"
# print runSimulation(1, 1.0, 10, 10, 0.75, 100, StandardRobot), "~ 190"
# print runSimulation(1, 1.0, 10, 10, 0.9, 1000, StandardRobot), "~ 310"
# print runSimulation(1, 1.0, 20, 20, 1., 100, StandardRobot), "~ 3250"

# === Problem 4
#
# 1) How long does it take to clean 80% of a 2020 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    avgTimes = []
    for numRobots in range(1,11):
    	avgTimes += [runSimulation(numRobots, 1.0, 20, 20, 0.8, 1000, StandardRobot),]
    pylab.plot(range(1,11),avgTimes)
    pylab.title("Time to Clean 80% of a 20x20 Room vs. Number of Robots")
    pylab.ylabel("Avg Time to Clean 80% (1000 trials)")
    pylab.xlabel("Number of Robots")
    pylab.show()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    avgTimes = []
    avgTimes += [runSimulation(2, 1.0, 20, 20, 0.8, 100, StandardRobot),]
    avgTimes += [runSimulation(2, 1.0, 25, 16, 0.8, 100, StandardRobot),]
    avgTimes += [runSimulation(2, 1.0, 40, 10, 0.8, 100, StandardRobot),]
    avgTimes += [runSimulation(2, 1.0, 50, 8, 0.8, 100, StandardRobot),]
    avgTimes += [runSimulation(2, 1.0, 80, 5, 0.8, 100, StandardRobot),]
    avgTimes += [runSimulation(2, 1.0, 100, 4, 0.8, 100, StandardRobot),]
    ratios = [20./20.,25./16.,40./10.,50./8.,80./5.,100./4.]
    pylab.plot(ratios,avgTimes)
    pylab.title("Times to Clean Rooms (area 400) of Different Width/Height Ratios")
    pylab.ylabel("Avg Time to Clean 80% (100 trials)")
    pylab.xlabel("Width/Height Ratios")
    pylab.show()


# showPlot1()
# showPlot2()
# === Problem 5

class RandomWalkRobot(Robot):
	#	This robots changes direction randomly after every time step
	def updatePositionAndClean(self):
		newPos = self.pos.getNewPosition(self.dir,self.speed)
		if self.room.isPositionInRoom(newPos):
			self.setRobotPosition(newPos)
			self.room.cleanTileAtPosition(self.pos)
			self.dir = random.uniform(0,360)
		else:
			self.dir = random.uniform(0,360)

#runSimulation(1, 1.0, 15, 15, 0.8, 2, RandomWalkRobot)
# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():	# produces a plot comparing the performance of the two robots
	avgStandardTimes = []
	avgRandomTimes = []
	for roomSideLength in range(5,50,5):
		print roomSideLength
		avgStandardTimes += [runSimulation(1, 1.0, roomSideLength, roomSideLength, 0.8, 20, StandardRobot),]
		avgRandomTimes += [runSimulation(1, 1.0, roomSideLength, roomSideLength, 0.8, 20, RandomWalkRobot),]
	pylab.plot(range(5,50,5),avgStandardTimes,label = "Standard Robot")
	pylab.plot(range(5,50,5),avgRandomTimes,label = "Random Walk Robot")
	pylab.title("Times to Clean 80% of Sqaure Rooms vs. Their Side Length")
	pylab.ylabel("Avg Time to Clean 80% (20 Trials)")
	pylab.xlabel("Room Side Length")
	pylab.show()
		
showPlot3()