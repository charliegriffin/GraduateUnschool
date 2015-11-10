# Lab 8, Task #4: Carrier Sense Multiple Access (CSMA)

import random, sys, wx, math, time
from optparse import OptionParser
from lab8_wnode import *
from lab8_wnet import *
from lab8_util import *
import matplotlib.pyplot as p

###############################################################

class CSMANode(WirelessNode):
    def __init__(self,location,network,retry):
        WirelessNode.__init__(self,location,network,retry)
        self.pmin = network.pmin
        self.pmax = network.pmax
        self.p = self.pmax
        # any additional state or variables may be set here

    def channel_access(self,time,ptime,numnodes):
        # You can tell if the channel is busy or not using
        # the self.network.channel_busy() function call.
		if not self.network.channel_busy():	# checks for business
			if self.p >= random.random():	# same as aloha with backup
				return True
		return False

    def on_collision(self,packet):
		# again this is all based on 'intuition', not thinking too hard
		if self.network.config.backoff == 'None':
			return
		self.p = self.pmin

    def on_xmit_success(self,packet):
		self.p = self.pmax

################################################################

class CSMAWirelessNetwork(WirelessNetwork):
    def __init__(self,n,chantype,ptime,dist,load,retry,backoff,
		 skew,qmax,pmax,pmin,simtime):
        if backoff == 'None':
            pmin = pmax = 1
        self.pmax = pmax
        self.pmin = pmin        
        WirelessNetwork.__init__(self,n,chantype,ptime,dist,load,retry,backoff,
                                 skew,qmax,simtime)

    def make_node(self,loc,retry):
        return CSMANode(loc,self,retry)

################################################################

if __name__ == '__main__':
#    random.seed(6172538)
    parser = OptionParser()
    parser.add_option("-g", "--gui", action="store_true", dest="gui", 
                      default=False, help="show GUI")
    parser.add_option("-n", "--numnodes", type="int", dest="numnodes", 
                      default=16, help="number of nodes")
    parser.add_option("-t", "--simtime", type="int", dest="simtime", 
                      default=10000, help="simulation time")
    parser.add_option("-b", "--backoff", dest="backoff", 
                      default='Mine', help="backoff scheme (Mine, None)")
    parser.add_option("-s", "--size", type="int", dest="ptime", 
                      default=1, help="packet size (in time units)")
    parser.add_option("-p", "--pmax", type="float", dest="pmax", 
                      default=0.125, help="max probability of xmission")    
    parser.add_option("-q", "--pmin", type="float", dest="pmin", 
                      default=1.0/128, help="min probability of xmission")    
    parser.add_option("-l", "--load", type="int", dest="load", 
                      default=100, help="total load % (in pkts/timeslot)")
    parser.add_option("-r", "--retry", action="store_true", dest="retry", 
                      default=False, help="show GUI")
    parser.add_option("-k", "--skew", action="store_true", dest="skew", 
                      default=False, help="skew source loads")

    (opt, args) = parser.parse_args()
    print 'Protocol: CSMA', 'Backoff: ', opt.backoff

    wnet = CSMAWirelessNetwork(opt.numnodes,'CSMA',opt.ptime,
                               'exponential',opt.load,opt.retry,opt.backoff,
                               opt.skew,0,opt.pmax,opt.pmin,opt.simtime)

    if opt.gui == True:
        sim = NetSim()
        sim.SetNetwork(wnet)
        sim.MainLoop()
    else:
        wnet.step(opt.simtime)
        succ = []
        i = 1
        for node in wnet.nlist:
            succ.append(node.stats.success)
#            p.subplots_adjust(hspace = 0.6)
#            p.subplot(opt.numnodes+1, 1, i)
#            p.ylabel('Probability')
#            p.xlabel('Index')
#            p.plot(node.plist)
#            i += 1

#        p.subplot(opt.numnodes+1,1,i)
        ind = numpy.arange(len(wnet.nlist))
        width = 0.35
        p.bar(ind, succ, width, color = 'r')
        p.ylabel('Throughput')
        p.xlabel('Node #')
        p.show()

################################################################