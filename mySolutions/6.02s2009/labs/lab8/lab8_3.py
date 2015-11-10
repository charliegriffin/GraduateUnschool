# Lab 8, Task #3: Stabilizing the Aloha protocol using random backoffs
import random, sys, wx, math, time
from optparse import OptionParser
from lab8_wnode import *
from lab8_wnet import *
from lab8_util import *
import matplotlib.pyplot as p

###############################################################

class AlohaNode(WirelessNode):
    def __init__(self,location,network,retry):
        WirelessNode.__init__(self,location,network,retry)
        self.pmin = network.pmin
        self.pmax = network.pmax
        self.p = (self.pmin + self.pmax)/2.
        ## Your code to initialize any additional state or variables goes here

    def channel_access(self,time,ptime,numnodes):
        # send packet with probability p
        # see web.mit.edu/6.02/www/s2009/handouts/net2-mac.pdf for proof
        # that this code is super simple and I'm not just copying SHY
        if random.random() <= self.p:
        	return True
        else:
        	return False

    def on_collision(self,packet):
    	# I wrote this by just messing with n and changing the code till it got the results
    	# the project requested, no real intuition here
    	if self.network.config.backoff == 'None':
    		return
    	self.p = (self.pmin + self.p)/2.
    	return

    def on_xmit_success(self,packet):
    	self.p = self.pmax

################################################################

class AlohaWirelessNetwork(WirelessNetwork):
    def __init__(self,n,chantype,ptime,dist,load,retry,backoff,
		 skew,qmax,pmax,pmin,simtime):
        if backoff == 'None':
            pmin = pmax = 1
        self.pmax = pmax
        self.pmin = pmin
        WirelessNetwork.__init__(self,n,chantype,ptime,dist,load,retry,backoff,
                                 skew,qmax,simtime)

    def make_node(self,loc,retry):
        return AlohaNode(loc,self,retry)

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
                      default=1.0, help="max probability of xmission")    
    parser.add_option("-q", "--pmin", type="float", dest="pmin", 
                      default=0.0, help="min probability of xmission")    
    parser.add_option("-l", "--load", type="int", dest="load", 
                      default=100, help="total load % (in pkts/timeslot)")
    parser.add_option("-r", "--retry", action="store_true", dest="retry", 
                      default=False, help="show GUI")
    parser.add_option("-k", "--skew", action="store_true", dest="skew", 
                      default=False, help="skew source loads")

    (opt, args) = parser.parse_args()
    print 'Protocol: Aloha, Backoff: ', opt.backoff
    wnet = AlohaWirelessNetwork(opt.numnodes,'Aloha',opt.ptime,
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
            i += 1

#        p.subplot(opt.numnodes+1,1,i)
        ind = numpy.arange(len(wnet.nlist))
        width = 0.35
        p.bar(ind, succ, width, color = 'r')
        p.ylabel('Throughput')
        p.xlabel('Node #')
        p.show()

################################################################