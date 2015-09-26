# Lab 8, Task #2: Aloha with fixed sending probability
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
        self.p = network.p

    def channel_access(self,time,ptime,numnodes):
        # send packet with probability p
        # see web.mit.edu/6.02/www/s2009/handouts/net2-mac.pdf for proof
        # that this code is super simple and I'm not just copying SHY
        if random.random() <= self.p:
        	return True
        else:
        	return False

################################################################

class AlohaWirelessNetwork(WirelessNetwork):
    def __init__(self,n,chantype,ptime,dist,load,retry,backoff,
		 skew,qmax,pxmit,simtime):
        self.p = pxmit
        WirelessNetwork.__init__(self,n,chantype,ptime,dist,load,retry,backoff,
                                 skew,qmax,simtime)

    def make_node(self,loc,retry):
        return AlohaNode(loc,self,retry)

################################################################

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-g", "--gui", action="store_true", dest="gui", 
                      default=False, help="show GUI")
    parser.add_option("-n", "--numnodes", type="int", dest="numnodes", 
                      default=16, help="number of nodes")
    parser.add_option("-t", "--simtime", type="int", dest="simtime", 
                      default=10000, help="simulation time")
    parser.add_option("-s", "--size", type="int", dest="ptime", 
                      default=1, help="packet size (in time units)")
    parser.add_option("-p", "--pxmit", type="float", dest="pxmit", 
                      default=1.0, help="probability of xmission")    
    parser.add_option("-l", "--load", type="int", dest="load", 
                      default=100, help="total load % (in pkts/timeslot)")
    parser.add_option("-r", "--retry", action="store_true", dest="retry", 
                      default=False, help="show GUI")
    parser.add_option("-k", "--skew", action="store_true", dest="skew", 
                      default=False, help="skew source loads")

    (opt, args) = parser.parse_args()
    print 'Protocol: Aloha with fixed probability: ', opt.pxmit
    wnet = AlohaWirelessNetwork(opt.numnodes,'Aloha',opt.ptime,
                                'exponential',opt.load,opt.retry,None,
                                opt.skew,0,opt.pxmit,opt.simtime)
    
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