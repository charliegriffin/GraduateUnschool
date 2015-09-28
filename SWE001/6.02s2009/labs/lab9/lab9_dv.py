import random,sys,math
from optparse import OptionParser
from lab9_net import *
from lab9_router import *
from lab9_random_graph import *

"""Skeleton for distance vector routing lab in 6.02
"""
# use our own node class derived from the node class of network10.py
# so we can override routing behavior
class DVRouter(Router):
    INFINITY = 16
        
    def send_advertisement(self, time):
        adv = self.make_dv_advertisement()
        for link in self.links:
            p = self.network.make_packet(self.address, self.peer(link), 
                                         'ADVERT', time, color='red', ad=adv)
            link.send(self, p)        
            
    # Make a distance vector protocol advertisement, which will be sent
    # by the caller along all the links
    def make_dv_advertisement(self):
		# scan the self.routes and self.spcost tables
		destCostList = []
		for destination in self.spcost.keys():
			destCostList.append((destination,self.spcost[destination]))
		print 'ad = ', destCostList
		return

    def link_failed(self, link):
        for destination in self.spcost.keys():
        	if self.routes[destination] == link:
        		del self.routes[destination]
        		del self.spcost[destination] 
        return

    def process_advertisement(self, p, link, time):
        self.integrate(p.source, p.properties['ad'])

    # Integrate new routing advertisement to update routing table and costs
    def integrate(self,fromnode,adv):
        ## Your code here
        pass

# A network with nodes of type DVRouter.
class DVRouterNetwork(RouterNetwork):
    # nodes should be an instance of DVNode (defined above)
    def make_node(self,loc,address=None):
        return DVRouter(loc,address=address)

########################################################################

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--numnodes", type="int", dest="numnodes", 
                      default=12, help="number of nodes")
    parser.add_option("-t", "--simtime", type="int", dest="simtime", 
                      default=4000, help="simulation time")
    parser.add_option("-r", "--rand", action="store_true", dest="rand", 
                      default=False, help="use randomly generated topology")
#    parser.add_option("-f", "--mttf", type="int", dest="mttf", 
#                      default=10000, help="mean time between failures")
    
    (opt, args) = parser.parse_args()

    if opt.rand == True:
        rg = RandomGraph(opt.numnodes)
        (NODES, LINKS) = rg.genGraph()
    else:
        # build the deterministic test network
        #   A---B   C---D
        #   |   | / | / |
        #   E   F---G---H
        # format: (name of node, x coord, y coord)

        NODES =(('A',0,0), ('B',1,0), ('C',2,0), ('D',3,0),
                ('E',0,1), ('F',1,1), ('G',2,1), ('H',3,1))

        # format: (link start, link end)
        LINKS = (('A','B'),('A','E'),('B','F'),('E','F'),
                 ('C','D'),('C','F'),('C','G'),
                 ('D','G'),('D','H'),('F','G'),('G','H'))

    print 'NODES: ', NODES
    print 'LINKS:', LINKS

    # make a network
    net = DVRouterNetwork(opt.simtime, NODES, LINKS)

    # setup graphical simulation interface
    sim = NetSim()
    sim.SetNetwork(net)
    sim.MainLoop()
########################################################################