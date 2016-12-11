''' 7.3 Given two lines on a Cartesian plane, determine whether
the two lines would intersect'''

class Line:
    def __init__(self, slope, intersection):
        self.slope = slope
        self.intersection = intersection

def doesIntersect(line1,line2):
    epsillon = 0.000001   #can be tuned to the resolution of the problem
    if abs(line1.slope - line2.slope) < epsillon:
        return False
    else:
        if abs(line1.intersection - line2.intersection) < epsillon:
            return False
        else:
            return True

#test code

l1 = Line(3,4)
l2 = Line(1,2)
print("Expected Result: True\tResult: " + str(doesIntersect(l1,l2)))

l3 = Line(3,4)
l4 = Line(3,5)
print("Expected Result: False\tResult: "+ str(doesIntersect(l3,l4)))