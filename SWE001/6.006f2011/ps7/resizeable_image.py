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
        (self.minSeamEnergy,self.minSeam) = self.findMinSeam(15,(self.height-1))
        print self.minSeam
#         for i in range(1,self.width):
#             (pathEnergy,path) = self.findMinSeam(i,(self.height-1))
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
#         print "calling with",(i,j)#,self.energy(i,j)
#         if i==18 and j==0:
#             print "\n\nHere is an early instance of the error\n\n"
#             if (i,j) in self.exploredPath.keys():
#                 print self.exploredPath[(i,j)]
        if (i,j) in self.exploredPath.keys():  # already explored
#             print i,j,"has already been explored"
            return self.exploredPath[(i,j)]
        else:                                  # not explored
#             print i,j,"has not yet been explored"
#             if (18,0) in self.exploredPath.keys():
#                 print "before checking top row\n",self.exploredPath[(18,0)]
            if j==0:
#                 print i,j,"is at the top row and has not been explored"
                self.exploredPath[(i,j)] = (self.energy(i,j),[(i,j)])
#                 print "returning",(self.energy(i,j),[(i,j)])
                return (self.energy(i,j),[(i,j)]) # return i,j too so you know what's up
#             if (18,0) in self.exploredPath.keys():
#                 print "after checking top row\n",self.exploredPath[(18,0)]
            else:
                potentialSubSeams = []
                for k in [-1,0,1]:
                    if i+k >= 0 and i+k <= (self.width-1):
                        potentialSubSeams.append(self.findMinSeam(i+k,j-1))
                (pathEnergy,currentPath) = min(potentialSubSeams,key=lambda item:item[0])
#                 if (18,0) in self.exploredPath.keys():
#                     print "after minimizing\n",self.exploredPath[(18,0)]
                if currentPath[-1][1] == j:    #this shouldn't happen
                    print "\n\n\nERROR, path includes current row\n",currentPath,i,j    # how did a path this long end up here?
                    print potentialSubSeams
                    print self.exploredPath
#                 print "appending",(i,j),"to",currentPath
                currentPath = currentPath[:]+[(i,j)]      #.append((i,j))
#                 if (18,0) in self.exploredPath.keys():
#                     print "after appending\n",self.exploredPath[(18,0)]
                if len(currentPath) > j+1:    # this should happen before the other error
                    print "\n\n\nERROR, path is longer than current height"
                    print "j =",j,"path =",currentPath
                pathEnergy += self.energy(i,j)
                self.exploredPath[(i,j)] = (pathEnergy,currentPath[:])
#                 if (18,0) in self.exploredPath.keys():
#                     print "after storing to explored path\n",self.exploredPath[(18,0)]
                return (pathEnergy,currentPath[:])
            