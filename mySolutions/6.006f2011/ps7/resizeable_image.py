import imagematrix
import sys

inf = 10**10

class ResizeableImage(imagematrix.ImageMatrix):
    '''returns a list of coordinates corresponding to the
    cheapest vertical seam to remove'''
    def best_seam(self):
        # Calculate each energy once.
        energy = {}
        for i in range(self.width):
            for j in range(self.height):
                energy[i,j] = self.energy(i,j)
                
        
        # Find minimum path energies, but not paths
        # First layer
        pathEnergies = {}
        for i in range(self.width):
            pathEnergies[i,0] = energy[i,0]
        
        ''' back pointers are arrows at each level showing which direction
        the path took. This is significantly faster, but just as useful
        as copying the full path'''
        backPointer = {}
        # Bottom-up
        for j in range(1, self.height):
            # Only adds paths that have been shown to be shorter
            for i in range(self.width):
                # Down
                pathEnergies[i,j] = energy[i,j] + pathEnergies[i,j-1]
                backPointer[i,j] = 0
                # Down-left
                if i != 0:
                    if pathEnergies[i,j] > energy[i,j] + pathEnergies[i-1,j-1]:
                        pathEnergies[i,j] = energy[i,j] + pathEnergies[i-1,j-1]
                        backPointer[i,j] = -1
                # Down-right
                if i != self.width-1:
                    if pathEnergies[i,j] > energy[i,j] + pathEnergies[i+1,j-1]:
                        pathEnergies[i,j] = energy[i,j] + pathEnergies[i+1,j-1]
                        backPointer[i,j] = 1
        
        # O(A) at this point because we have 2 size A matrices, built via look-ups
        
        # Finds the bottom pixel with the smallest associated path energy
        bestValue = sys.maxint
        index = None
        for i in range(self.width):
            if pathEnergies[i,self.height-1] < bestValue:
                bestValue = pathEnergies[i,self.height-1]
                # Notes the horizontal position of the minimum path at the end
                index = i
        
        # Rebuilds the path, by following backpointers to the top.
        seam = []
        for j in range(self.height-1, 0, -1):
            seam.append((index, j))
            index = index + backPointer[index,j]
        seam.append((index, 0))
        
        return seam

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())

    '''My solution before I looked at the problem set solutions.
    This solution works but is significantly slower than the
    solution above because: it records the path for every seam at
    every level (not necessary), energies are calculated multiple
    times, and this solution is top-down instead of bottom up.'''
    def findMinSeam(self,i,j):
        if (i,j) in self.exploredPath.keys():  # already explored
            return self.exploredPath[(i,j)]
        else:                                  # not explored
            if j==0:
                self.exploredPath[(i,j)] = (self.energy(i,j),[(i,j)])
                return (self.energy(i,j),[(i,j)])
            else:
                potentialSubSeams = []
                for k in [-1,0,1]:
                    if i+k >= 0 and i+k <= (self.width-1):
                        potentialSubSeams.append(self.findMinSeam(i+k,j-1))
                (pathEnergy,currentPath) = min(potentialSubSeams,key=lambda item:item[0])
                currentPath = currentPath[:]+[(i,j)]
                pathEnergy += self.energy(i,j)
                self.exploredPath[(i,j)] = (pathEnergy,currentPath[:])
                return (pathEnergy,currentPath[:])
            