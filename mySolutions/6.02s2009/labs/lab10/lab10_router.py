import random,sys,math
from lab10_net import *

"""Skeleton for link-state routing lab in 6.082
"""
# use our own node class derived from the node class of network10.py
# so we can override routing behavior
class Router(Node):
    HELLO_INTERVAL = 10   # time between HELLO packets
    ADVERT_INTERVAL = 50  # time between route advertisements
        
    def __init__(self,location,address=None):
        Node.__init__(self, location, address=address)
        # additional instance variables
        self.neighbors = {}     # Link -> (timestamp, address, linkcost)
        self.routes = {}        # address -> Link
        self.routes[self.address] = 'Self'
        self.spcost = {}        # address -> shortest path cost to node
        self.spcost[self.address] = 0

    def reset(self):
        Node.reset(self)
        self.spcost[self.address] = 0

    # return the link corresponding to a given neighbor, nbhr
    def getlink(self, nbhr):
        if self.address == nbhr: return None
        for l in self.links: 
            if l.end2.address == nbhr or l.end1.address == nbhr:
                return l
	return None

    def peer(self, link):
        if link.end1.address == self.address: return link.end2.address
        if link.end2.address == self.address: return link.end1.address

    # use routing table to forward packet along appropriate outgoing link
    def forward(self,p):
        link = self.routes.get(p.destination, None)
        if link is None:
            print 'No route for ',p,' at node ',self
        else:
            link.send(self, p)   

    def process(self,p,link,time):
        if p.type == 'HELLO':
            # remember addresses of our neighbors and time of latest update
            self.neighbors[link] = (time, p.source, link.cost)
        elif p.type == 'ADVERT':
            self.process_advertisement(p,link,time)
        else:
            Node.process(self, p, link, time)

    def process_advertisement(self,p,link,time):
        # will be filled in by the specific routing protocol
        return

    def sendHello(self, time): 
        # STEP 1(a): send HELLO packets along all my links to neighbors
        # These periodic HELLOs tell our neighbors I'm still alive
        # The neighbors will get my address from the source address field
        for link in self.links:
            p = self.network.make_packet(self.address, self.peer(link), 
                                         'HELLO', time,color='green')
            link.send(self,p)
        return

    def clearStaleHello(self, time):
        # STEP 1(b) : Look through neighbors table and eliminate
        # out-of-date entries.
        old = time - 2*self.HELLO_INTERVAL
        for link in self.neighbors.keys():
            if self.neighbors[link][0] <= old:
                del self.neighbors[link]
                self.link_failed(link)
        return
    
    def link_failed(self,link):
        return
    
    def clear_routes(self,link):
        clear_list = []
        for dest in self.routes:
            if self.routes[dest] == link:
                clear_list.append(dest)
        for dest in clear_list:
            print self.address, ' clearing route to ', dest
            del self.routes[dest]
            del self.spcost[dest]

    def send_advertisement(self, time):
        return

    def transmit(self, time):
#        if (time % self.HELLO_INTERVAL) == 0:
#            self.sendHello(time)
#            self.clearStaleHello(time)
        if (time % self.ADVERT_INTERVAL) == 0:
            self.send_advertisement(time)
        return

    def OnClick(self,which):
        if which == 'left':
            #print whatever debugging information you want to print
            print self
            print '  neighbors:',self.neighbors.values()
            print '  routes:'
            for (key,value) in self.routes.items():
                print '    ',key,': ',value


# Network with link costs.  By default, the cost of a link is the 
# Euclidean distance between the nodes at the ends of the link
class RouterNetwork(Network):
    def __init__(self,SIMTIME,NODES,LINKS):
        Network.__init__(self,SIMTIME)

        for n,r,c in NODES:
            self.add_node(r,c,address=n)
        for a1,a2 in LINKS:
            n1 = self.addresses[a1]
            n2 = self.addresses[a2]
            self.add_link(n1.location[0],n1.location[1],
                          n2.location[0],n2.location[1])
    
    # nodes should be an instance of LSNode (defined above)
    def make_node(self,loc,address=None):
        return Router(loc,address=address)

    def make_link(self,n1,n2):
        return CostLink(n1,n2)

    def add_cost_link(self,x1,y1,x2,y2):
        n1 = self.find_node(x1,y1)
        n2 = self.find_node(x2,y2)
        if n1 is not None and n2 is not None:
            link = self.make_cost_link(n1,n2)
            link.network = self
            self.links.append(link)
