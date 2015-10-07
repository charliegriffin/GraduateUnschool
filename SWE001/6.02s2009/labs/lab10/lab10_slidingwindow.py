# This is the template file for Lab #10, Task #2
import random,sys
from optparse import OptionParser
from lab10_net import *
from lab10_router import *
from lab10_random_graph import *

# ReliableSenderNode extends Router to implement a reliable sender
class ReliableSenderNode(Router):
    TIMEOUT = 20
    ALPHA = 0.125
    BETA = 0.25

    def __init__(self,location,address=None,window=1):
        Router.__init__(self,location,address=address)
        self.window = window           # sliding window size
        self.stream_destination = None  # where to send reliable packet stream
        self.reset()

    def reset(self):
        Router.reset(self)
        self.srtt = 0
        self.rttdev = 0
        self.timeout = self.TIMEOUT
        self.seqnum = 1
        self.sndbuf = []

    def __repr__(self):
        return 'ReliableSenderNode<%s>' % str(self.address)

    def OnClick(self,which):
        if which == 'left':
            if self.network.time > 1:
                print Node.__repr__(self) + \
                    " srtt %.1f rttdev %.1f timeout %.1f" \
                    % (self.srtt, self.rttdev, self.timeout)
            else:
                print self.__repr__()

    # Send a packet at the current time, with specified seqnum,
    # and color ('black', 'gray', 'yellow', etc.).  You may
    # want to pick different colors for retransmissions.
    def send_pkt(self, time, seqnum, color):
        xmit_packet = self.network.make_packet(
            self.address, self.stream_destination, 'DATA', time, 
            seqnum=seqnum, color=color)
        self.forward(xmit_packet)
        return xmit_packet

    def transmit(self, time):
        Router.transmit(self,time)
        if self.stream_destination is not None and time >= 1:
            self.reliable_send(time)

    # Implement the sliding window protocol.  This function is called once each
    # time-slot.  Decide if you should send a packet or not, and if you decide
    # to send a packet, decide if it should be a retransmission.
    # It will be useful to maintain a list of unacknowledged packets.
    # Note also that each packet contains a "start" field that keeps track
    # of the time at which it was sent (every time a packet is sent or re-sent,
    # that field is set to the current time).  You can use that field to 
    # check if a packet should be re-sent.
    #
    # Please note the following useful hints:
    # 1. You may use p.start to get the time at which packet p was sent, 
    # which is a useful way to determine if the sender should retransmit p.
    # 2. Call self.send_pkt() to send a packet specifying the arguments as 
    # in the send_pkt() template shown above.  This method returns the packet.
    # 3. The sequence number of a packet p may be retrieved using 
    # p.properties['seqnum'].
    def reliable_send(self, time):

	# find unacknowledged packet with the largest wait
	packet = None
	longestWait = -1
	for unacked in self.sndbuf:
		if unacked.start > self.timeout + time:
			longestWait = unacked.start	- time
			packet = unacked
	# send a new packet if no packets have timed out and there is room
	if len(self.sndbuf) < self.window and longestWait <= self.timeout:
		print 'adding new unacked packet'
		self.sndbuf.append(self.send_pkt(time,self.seqnum,'green'))
	# resend timed-out package
	elif longestWait > self.timeout:
		print 'resending old packet'
		self.send_pkt(time,packet.properties['seqnum'],'red')


    # An ACK just arrived; process it.  Remember to call calc_timeout with the
    # appropriate information.
    def process_ack(self, time, acknum, timestamp):
		useqnum = None
		# same code, we just go through all the packets to see where it corresponds
		for unacked in self.sndbuf:
			# find the appropriate packet
			if acknum == unacked.properties['seqnum']:
				useqnum = unacked.properties['seqnum']
				break
		
		if useqnum != None:
			self.sndbuf.remove(unacked) # since this package has been acknowledged
			self.timeout = self.calc_timeout(time,timestamp)
			self.seqnum += 1
		else:
			print 'Error: acknowedgement does not corresond to packet in window'

    # Update RTT statistics and compute the sender's timeout value.  The 
    # current time and the timestamp echoed in the ACK from the receiver 
    # are arguments to this function.
    # Copy this function from Task 1 (stop-and-wait protocol) of Lab 10; if
    # that code is correct, it should work unchanged.
    def calc_timeout(self, time, timestamp):
        # this one didn't change
        r = time - timestamp
        self.srtt = self.ALPHA*r + (1-self.ALPHA)*self.rttdev
        dev = abs(r-self.srtt)
        self.rttdev = self.BETA*dev + (1-self.BETA)*self.rttdev
        print 'Smoothed RTT = ',self.srtt
        print 'Sigma(RTT) = ',self.rttdev
        return self.srtt + 4*self.rttdev

    # Process an ACK (and ignore any other packet type)
    def receive(self,p,link,time):
        if p.type != 'ACK': return
        acknum = p.properties.get('seqnum', None)
        timestamp = int(p.properties.get('timestamp', None))
        print "t=%d %s received ACK %d" % (time, self.address, acknum)
        self.process_ack(time, acknum, timestamp)

# ReliableReceiverNode extends Router to implement reliable
# receiver functionality with path vector routing.
class ReliableReceiverNode(Router):
    def __init__(self,location,address=None,window=1):
        Router.__init__(self,location,address=address)
        self.window = window
        self.reset()

    def reset(self):
        Router.reset(self)
        self.app_seqnum = 0
        self.lastprinttime = 0
        self.rcvbuf = []

    def __repr__(self):
        return 'ReliableReceiverNode<%s>' % str(self.address)

    def OnClick(self,which):
        if which == 'left':
            if self.network.time > 1:
                print Node.__repr__(self) + \
                      " received %d (%g packets/timestep)" % (self.app_seqnum,
                      float(self.app_seqnum)/(self.network.time - 1))
            else:
                print self.__repr__()


    def send_ack(self, sender, time, seqnum, timestamp):
        ack = self.network.make_packet(self.address, sender, 'ACK', time,
                                       seqnum=seqnum, timestamp=timestamp,
                                       color='blue')
        self.forward(ack);

    def receive(self, p, link, time):
        seqnum = p.properties.get('seqnum', None)
        if p.type == 'DATA':
            self.reliable_recv(p.source, time, seqnum, p.start)

    # Process a DATA packet from "sender" with "seqnum" and 
    # specified sender timestamp.  The current time is "time".  
    # Call send_ack with the relevant arguments.  Then call
    # self.app_receive() IF AND ONLY IF the seqnum is one larger than
    # the last one (when you last called app_receive()).  The idea is
    # to deliver the DATA packets to the application in exact incrementing
    # sequence order without any duplicates or gaps.
    # Maintain a list (say, self.rcvbuf) of packet sequence numbers waiting 
    # to be delivered to the application; when a gap fills and a gap-free 
    # sequence of packets can be delivered, call app_receive() for each one.  
    # Also remember to delete the delivered sequence numbers from self.rcvbuf.
    # If your code is correct, the protocol will progress correctly and 
    # app_receive will print out each in-sequence packet sequence that it gets.
    # An error will result either in the receiver "hanging" or in an assertion
    # failure in app_receive().
    def reliable_recv(self, sender, time, seqnum, timestamp):
        buffer = self.rcvbuf[:]
        self.send_ack(sender,time,seqnum,timestamp)
        if seqnum == 1 + self.app_seqnum:
        	self.app_receive(seqnum,time)
        	for sequence in buffer:
        		if sequence == self.app_seqnum + 1:
        			self.send_ack(sender,time,seq,timestamp)
        			self.app_receive(sequence,time)
        			self.rcvbuf.remove(sequence)
        if seqnum <= self.app_seqnum:
        	pass
        else:
        	self.rcvbuf.append(seqnum)

    # app_receive() should be called by receive() for each data packet that 
    # arrives in order of incrementing sequence number (i.e., without gaps)
    def app_receive(self, seqnum, time):
        try:
            assert seqnum == self.app_seqnum + 1, \
                "Expected DATA packet #%d, got #%d" % (self.app_seqnum+1,seqnum)
            print "t=%d %s app_receive seqnum %d" % (time, self, seqnum)
            if time - self.lastprinttime >= 100:
                print "***t=%d app recd %d (%g packets/timestep)" % (time, self.app_seqnum, float(self.app_seqnum)/(self.network.time - 1))
                self.lastprinttime = time
        except AssertionError, a:
            print "*BUG* in app_receive: %s" % a
        self.app_seqnum = seqnum

class LossyLink(Link):
    def __init__(self,n1,n2,lossprob):
        Link.__init__(self,n1,n2)
        self.lossprob = lossprob # probability packet gets dropped
    
    # send one packet from specified node
    # but drop a few along the way!
    def send(self,n,p):
        # we lose packets with probability PLOSS.
        # to make life easy on ourselves, let's pretend we never
        # lose a routing packet.
        if (p.type!='DATA' and p.type!='ACK') or \
                random.random() > self.lossprob:
            Link.send(self,n,p)
        else:
            print 'Dropping packet %s: seqnum=%s'% \
                  (p,str(p.properties.get('seqnum','???')))

class MyNetwork(RouterNetwork):
    def __init__(self, SIMTIME, NODES, LINKS, WINDOW, LOSSPROB):
        self.window = WINDOW
        self.lossprob = LOSSPROB
        RouterNetwork.__init__(self,SIMTIME,NODES,LINKS)

    def make_node(self,loc,address=None):
        if address == 'S':
            return ReliableSenderNode(loc, address, self.window)
        elif address == 'R':
            return ReliableReceiverNode(loc, address, self.window)
        else:
            return Router(loc,address=address)

    def make_link(self,n1,n2):
        return LossyLink(n1,n2,self.lossprob)

    # reset network to its initial state
    def reset(self):
        # parent class handles the details
        Network.reset(self)
        # insert a single packet into the network. Since we don't have code
        # to deliver the packet this just keeps the simulation alive...
        src = self.addresses['S']
        src.stream_destination = 'R'
        src.add_packet(self.make_packet('S','R','DATA',1))

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--simtime", type="int", dest="simtime", 
                      default=2000, help="simulation time")
    parser.add_option("-w", "--window", type="int", dest="window", 
                      default=1, help="window size")
    parser.add_option("-l", "--loss", type="float", dest="lossprob", 
                      default=0.01, help="loss prob for DATA and ACK packets")
    
    (opt, args) = parser.parse_args()
    # build the deterministic test network
    #   A---B   C---R
    #   |   | / | / |
    #   S---F---G---H
    # format: (name of node, x coord, y coord)
    
    NODES =(('A',0,0), ('B',1,0), ('C',2,0), ('R',3,0),
            ('S',0,1), ('F',1,1), ('G',2,1), ('H',3,1))

    # format: (link start, link end)
    LINKS = (('A','B'),('A','S'),('B','F'),('S','F'),
             ('C','R'),('C','F'),('C','G'),
             ('R','G'),('R','H'),('F','G'),('G','H'))

    print 'NODES: ', NODES
    print 'LINKS:', LINKS

    # make a network
    net = MyNetwork(opt.simtime, NODES, LINKS,  opt.window, opt.lossprob)

    for node in net.nlist:
        if node.address == 'S':
            node.routes['R'] = node.getlink('F')
        elif node.address == 'F':
            node.routes['R'] = node.getlink('G')
            node.routes['S'] = node.getlink('S')
        elif node.address == 'G':
            node.routes['R'] = node.getlink('R')
            node.routes['S'] = node.getlink('F')
        elif node.address == 'C':
            node.routes['R'] = node.getlink('R')
            node.routes['S'] = node.getlink('F')            
        elif node.address == 'R':
            node.routes['S'] = node.getlink('C')

    # setup graphical simulation interface
    sim = NetSim()
    sim.SetNetwork(net)
    sim.MainLoop()
########################################################################