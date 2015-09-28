import random,sys,math

"""Random graph generator
"""
from lab9_ls import *

class RandomGraph:
    def __init__(self,numnodes=8):
        self.numnodes = numnodes
        if self.numnodes > 26:
            print "Maximum number of nodes = 26"
            self.numnodes = 26
        elif self.numnodes < 5:
            print "Minimum number of nodes = 5"
            self.numnodes = 5
        
        self.names = ['A', 'B', 'C', 'D', 'E',
                      'F', 'G', 'H', 'I', 'J',
                      'K', 'L', 'M', 'N', 'O',
                      'P', 'Q', 'R', 'S', 'T',
                      'U', 'V', 'W', 'X', 'Y', 'Z']
        self.maxRows = math.ceil(math.sqrt(self.numnodes))
        self.maxCols = math.ceil(math.sqrt(self.numnodes))

    def getCoord(self, i):
        x= i % self.maxCols
        y = math.floor(i/self.maxCols)
        return (x,y)
    
    def getIndex(self, x, y):
        if x<0 or y < 0 or x>=self.maxCols or y>=self.maxRows:
            return -1
        ind = y*self.maxCols + x    
        if ind < self.numnodes:
            return ind
        else:
            return -1
        
    def getAllNgbrs(self, i):
        (x,y) = self.getCoord(i)
        ngbrs = []
        ngbrsX = [x-1, x, x+1]
        ngbrsY = [y-1, y, y+1]
        for nx in ngbrsX:
            for ny in ngbrsY:
                if not (nx==x and ny == y):
                    ind = self.getIndex(nx, ny)
                    if ind>=0:
                        ngbrs.append(ind)
        return ngbrs
    
    def checkLinkExists(self, links, a, b):
        for (c,d) in links:
            if a==c and b==d:
                return True
            if a==d and b==c:
                return True
        return False
    
    def genGraph(self):
        NODES = []
        LINKS = []
        
        for i in range(self.numnodes):
            (x,y) = self.getCoord(i)
            name = self.names[i]
            NODES.append((name,x,y))
        
        for i in range(self.numnodes):
            ngbrs = self.getAllNgbrs(i)
            outdeg = int(random.random()*len(ngbrs)) + 1
            sampleNgbrs = random.sample(ngbrs, outdeg)
            for n1 in sampleNgbrs:
                n = int(n1)
                if not self.checkLinkExists(LINKS, self.names[i], self.names[n]):
                    LINKS.append((self.names[i], self.names[n]))

        return (NODES, LINKS)
    
########################################################################
if __name__ == '__main__':
    numnodes = 8 #can get this from commandline option
    SIMTIME = 10000
    rg = RandomGraph(numnodes)
    (NODES, LINKS) = rg.genGraph()
    print 'NODES: ', NODES
    print 'LINKS:', LINKS
    
    # make a network
    net = LSRouterNetwork(SIMTIME, NODES, LINKS)

    # setup graphical simulation interface
    sim = NetSim()
    sim.SetNetwork(net)
    sim.MainLoop()
########################################################################