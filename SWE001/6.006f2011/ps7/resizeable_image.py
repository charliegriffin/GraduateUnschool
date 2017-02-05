import imagematrix

inf = 10**10

class ResizeableImage(imagematrix.ImageMatrix):
    '''returns a list of coordinates corresponding to the
    cheapest vertical seam to remove'''
    def best_seam(self):
        print "best seam"
        print "dimensions = " + str(self.height) + "x" + str(self.width)
        self.exploredPath = {}
#         self.seamEnergy = {}
#         self.seamPath = {}
#         self.visit = {}
#         for i in range(self.width):
#             for j in range(self.height):
#                 self.seamEnergy[i,j] = inf
#                 self.seamPath[i,j] = None
#                 self.visit[i,j] = False
#         for i in range(self.width):
#             minSeams += [(i,self.height-1] # init across each horiz pixel
#             print self.energy(i, self.height-1)
        (self.minSeamEnergy,self.minSeam) = self.findMinSeam(0,3)#(self.height-1))
        print self.minSeam
#         for i in range(1,5):#self.width):
#             (pathEnergy,path) = self.findMinSeam(i,3)#(self.height-1))
#             if pathEnergy < self.minSeamEnergy:
#                 self.minSeamEnergy = pathEnergy
#                 self.minSeam = path
#             print path
        print len(self.minSeam), self.height
        print self.minSeam
        return self.minSeam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    def findMinSeam(self,i,j):
#         print i,j,self.energy(i,j)
        if (i,j) in self.exploredPath.keys():  # already explored
#             print i,j,"explored"
            return self.exploredPath[(i,j)]
        else:                                  # not explored
			if j==0:
				self.exploredPath[(i,j)] = (self.energy(i,j),[(i,j)])
				return (self.energy(i,j),[(i,j)]) # return i,j too so you know what's up
			else:
				potentialSubSeams = []
				for k in [-1,0,1]:
					if i+k >= 0 and i+k <= (self.width-1):
						potentialSubSeams.append(self.findMinSeam(i+k,j-1))
				(pathEnergy,currentPath) = min(potentialSubSeams,key=lambda item:item[0])
# 				print "appending",i,j,"to current path"
# 				print currentPath[-1][1],j
				if currentPath[-1][1] == j:    #this shouldn't happen
					print currentPath,i,j    # how did a path this long end up here?
					print potentialSubSeams
				currentPath.append((i,j))
				pathEnergy += self.energy(i,j)
				self.exploredPath[(i,j)] = (pathEnergy,currentPath)
				return (pathEnergy,currentPath)
            