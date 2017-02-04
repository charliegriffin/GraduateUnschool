import imagematrix

inf = 10**10

class ResizeableImage(imagematrix.ImageMatrix):
    '''returns a list of coordinates corresponding to the
    cheapest vertical seam to remove'''
    def best_seam(self):
        print "best seam"
        print "dimensions = " + str(self.height) + "x" + str(self.width)
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
        print self.findMinSeam(self.width/2,(self.height-1)/6)

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    def findMinSeam(self,i,j):
#         print i,j,self.energy(i,j)
        if j==0:
            return (self.energy(i,j),[(i,j)]) # return i,j too so you know what's up
        else:
            potentialSubSeams = []
            for k in [-1,0,1]:
                potentialSubSeams.append(self.findMinSeam(i+k,j-1))
            (pathEnergy,currentPath) = min(potentialSubSeams,key=lambda item:item[0])
            currentPath.append((i,j))
            return (pathEnergy + self.energy(i,j),currentPath)
            