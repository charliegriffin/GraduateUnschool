''' 9.2 Imagine a robot sitting on the upper left corner 
of an X by Y grid. The robot can only move in two directions:
right and down. How may possible paths are there for the robot
to go from (0,0) to (X,Y)? '''

# assumption: robot moves unit distance in a step
stepSize = 1

def numPaths(X,Y):
    # base/terminating case
    if (X == 0 and Y == 0):   # valid path
        return 1
    elif (X < 0 or Y < 0):    # invalid path
        return 0
    else:
        return numPaths(X-1,Y) + numPaths(X, Y-1)
        
# test code

print "Expected result: 2\tResult: ", numPaths(1,1)
print "Expected result: 1\tResult: ", numPaths(2,0)
print "Expected result: 3\tResult: ", numPaths(2,1)
print "Expected result: 56\tResult: ", numPaths(3,5)

''' FOLLOW UP:
Imagine certain spots are off limits such that
the robot can not step there. Now design an algorithm
to count the number of ways'''

def numPathsForbidden(X,Y,forbiddenSpaces):
    print X,Y
    if (X == 0 and Y == 0):  # valid path
        return 1
    elif (X < 0 or Y < 0):   # invalid path
        return 0
    for (fx,fy) in forbiddenSpaces: # check if robot is on a
        if (X == fx and Y == fy):   # bad space
            return 0
    fDown = [] 
    fRight = []
    for (fx,fy) in forbiddenSpaces: # remap forbidden spaces
        if fy > 0:                  # for subproblems
            fDown.append((fx,fy-1))
        if fx > 0:
            fRight.append((fx-1,fy))
    return numPathsForbidden(X-1,Y,fRight) + numPathsForbidden(X,Y-1,fDown)

# test code
f = [(1,1)]  # forbidden spaces are lists of tuples
print "Expected result: 2\tResult: ", numPathsForbidden(2,2,f)