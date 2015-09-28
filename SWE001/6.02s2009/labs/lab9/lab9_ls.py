import random,sys,math
from optparse import OptionParser
from lab9_net import *
from lab9_router import *
from lab9_random_graph import *

"""Skeleton for link-state routing lab in 6.02
"""
class LSRouter(Router):
    INFINITY = sys.maxint

    def __init__(self,location,address=None):
        Router.__init__(self, location, address=address)
        self.LSA = {} # address -> (seqnum,(nbr1,cost1),(nbr2,cost2),(nbr3,cost3), ...)
        self.LSA_seqnum = 0     # uniquely identify each LSA broadcast

    def make_ls_advertisement(self):
        # Make a list of all neighbors to send out in an LSA
        ## Your code here
        return

    def send_lsa(self, time):
        self.LSA_seqnum += 1
        lsa_info = self.make_ls_advertisement()
        for link in self.links:
            p = self.network.make_packet(self.address, self.peer(link), 
                                         'ADVERT', time, color='red',
                                         seqnum=self.LSA_seqnum,
                                         neighbors=lsa_info)
            link.send(self, p)
        return

    def send_advertisement(self, time):
        self.send_lsa(time)
        self.clear_stale_lsa(time)
    
    def clear_stale_lsa(self, time):
        # After sending out LSA packets, clear out older LSA entries
        for key,value in self.LSA.items():
            if value[0] < self.LSA_seqnum-1:
                del self.LSA[key]
        return
    
    def process_advertisement(self, p, link, time):
        # Process incoming LSA advertisement.
        # First get sequence number from packet, then see if we have a 
        # previous entry in LSA from the same node
        seq = p.properties['seqnum']
        saved = self.LSA.get(p.source, (-1,))
        if seq > saved[0]:
            # update only if incoming seqnum is larger than saved seqnum
            self.LSA[p.source] = [seq] + p.properties['neighbors']
            # Rebroadcast packet to our neighbors.  We don't _have_ to
            # rebroadcast to the neighbor we just got the LSA from,
            # but we're going to do it anyway...
            for link in self.links:
                link.send(self, self.network.duplicate_packet(p))

    # get_all_nodes scans each node's LSA to visit all the other
    # non-neighbor nodes emulating a breadth first search (BFS).  The
    # reason we do a BFS traversal rather than simply use self.LSA is
    # because we want to have a route to every node that is currently
    # reachable from us.
    def get_all_nodes(self):
        nodes = [self.address]
        for u in nodes:
            if self.LSA.get(u) != None:
                lsa_info = self.LSA[u][1:]
                for i in range(len(lsa_info)):
                    v = lsa_info[i][0]
                    if not v in nodes:
                        nodes.append(v)
        return nodes

    def run_dijkstra(self, nodes):
        ## Your code here
        return

    # Let's clear the current routing table and rebuild it.  The hard work
    # is done by run_dijkstra().
    def integrate(self, time):
        self.routes.clear()
        self.routes[self.address] = 'Self'
        #initialize our own LSA       
        self.LSA[self.address] = [self.LSA_seqnum] + self.make_ls_advertisement()
        nodes = self.get_all_nodes()
        self.spcost = {}
        for u in nodes:
            self.spcost[u] = self.INFINITY
        self.spcost[self.address] = 0 # path cost to myself is 0 (duh)

        self.run_dijkstra(nodes)
        return

    def transmit(self, time):
        Router.transmit(self, time)
        if (time % self.ADVERT_INTERVAL) == self.ADVERT_INTERVAL/2:
            self.integrate(time)
        return

    def OnClick(self,which):
        if which == 'left':
            print self
            print '  LSA:'
            for (key,value) in self.LSA.items():
                print '    ',key,': ',value
        Router.OnClick(self,which)

# A network with nodes of type LSRouter
class LSRouterNetwork(RouterNetwork):
    def make_node(self,loc,address=None):
        return LSRouter(loc,address=address)

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
    net = LSRouterNetwork(opt.simtime, NODES, LINKS)

    # setup graphical simulation interface
    sim = NetSim()
    sim.SetNetwork(net)
    sim.MainLoop()
########################################################################