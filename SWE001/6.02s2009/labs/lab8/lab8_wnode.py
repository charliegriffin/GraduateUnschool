import random, sys, wx, math, time
from lab8_wnet import *
from lab8_util import *

################################################################################
#
# WirelessNode -- a node in a wireless network
#
################################################################################

class WirelessNode:
    def __init__(self,location,network,retry):
        self.location = location
        self.network = network	# our WirelessNetwork object
	self.retry = retry	# retry packets (forever) or not?
	self.stats = Stats(network.config.simtime)
        self.reset()

    def __repr__(self):
        return 'Node<%s>' % str(self.location)

    # reset to initial state
    def reset(self):
        self.transmit_queue = []
        self.transmitting = False
        self.rate = 0
        self.qmax = self.network.config.qmax
        self.nsize = 0		# filled in by draw method
        self.stats.reset(self.network.config.simtime)

    # Get the unique ID for the node; it's a number between 0 and numnodes-1,
    # where numnodes is the number of nodes in the broadcast network
    def get_id(self):
	i = 0
	for n in self.network.nlist:
	    if n == self: return i
	    i = i+1
        return 'error'

    # Add a packet start time to be transmitted from this node.  Transmit queue
    # is kept ordered by packet start time.
    def add_packet(self,start):
        if (self.qmax > 0 and len(self.transmit_queue) == self.qmax):
            print 'q full (max = %d)' % self.qmax
            return
	p = Packet(start,self,ptime=self.network.config.ptime)
        index = 0
        for pp in self.transmit_queue:
            if start < pp.start:
                self.transmit_queue.insert(index,p)
                break
            else: index += 1
        else: self.transmit_queue.append(p)

    # Attach a random process to the node to generate packets
    def attach_distribution(self,dist,rate):
	self.dist = dist
	self.rate = rate

    # Do the actual work to generate packets
    def generate_packet(self,time):
	if self.dist == "exponential":
	    # generate according to exponential interarrival
	    r = random.random()
	    if r <= self.rate: 
		self.add_packet(time)
		return 1
	    return 0

    # Initiate transmission of a packet
    def transmit_start(self,packet):
        # start transmitting a packet, eventually self.transmit_done(start,...)
        # will be called by the network
        self.stats.attempts += 1
	self.network.stats.attempts += 1
        self.transmitting = True
        self.network.transmit(self,packet)

    # Called by network when a packet transmission is complete.  
    # collisions is true if there were collisions with other transmitters 
    # during transmission (ie, some other packet was sent at the same time)
    def transmit_done(self,packet):
        self.transmitting = False
        if packet.coll_flag == lab8_wnet.COLLISION:
            self.stats.collisions += 1
	    # Note: For TDMA, don't remove packet (shd never happen)
	    if (self.retry == lab8_wnet.NO_RETRY and 
		self.network.config.chantype != 'TDMA'):
		self.transmit_queue.remove(packet)
            self.on_collision(packet)
	else:
	    st = self.stats
	    st.success = st.success + 1
	    st.latency = (1.0*(packet.end-packet.start) + 
			  (st.success - 1) * st.latency)/st.success
	    self.transmit_queue.remove(packet)
            self.on_xmit_success(packet)

    def on_xmit_success(self,packet):
        return

    def on_collision(self,packet):
        return

    # called every time step so that node can decide what to do (ie, whether to
    # start transmitting or not).  Returns number of packets whose transmission
    # is not complete.
    def step(self,time):
        if not self.transmitting:
            # and there's a packet queue whose time has come
            if len(self.transmit_queue) > 0 and time >= self.transmit_queue[0].start:
                # and if the access policy allows us to access the channel
                if self.channel_access(time,self.network.config.ptime,
                                       self.network.config.numnodes):
                    # start xmitting first packet on queue in the next time slot
                    self.transmit_start(self.transmit_queue[0])
	
	self.generate_packet(time+1) # try to generate packet in next timeslot
        return len(self.transmit_queue)

    # Channel access routines depending on the type of the channel. 
    # This function is a wrapper around the funtions that do the actual
    # work.  Returns True if node can transmit in this time-slot and False
    # otherwise.
    def channel_access(self,time,ptime,numnodes):
        return True

    #########################################################
    # support for graphical simulation interface
    #########################################################

    # convert our location to screen coordinates
    def net2screen(self,transform):
        return lab8_wnet.net2screen(self.location,transform)

    # draw ourselves on the screen as a colored square with black border
    def draw(self,dc,transform):
        self.nsize = transform[0]/16
        loc = self.net2screen(transform)
        dc.SetPen(wx.Pen('black',1,wx.SOLID))
        if self.transmitting: color = 'green'
        else: color = 'black'
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(loc[0]-self.nsize,loc[1]-self.nsize,
                         2*self.nsize+1,2*self.nsize+1)

        label = str('A=%d,S=%d,Q=%d' %
                    (self.stats.attempts,self.stats.success,
		     len(self.transmit_queue)))
#        dc.SetTextForeground('dark grey')
        dc.SetTextForeground('black')
#        dc.SetFont(wx.Font(max(4,2*self.nsize),wx.SWISS,wx.NORMAL,wx.NORMAL))
        dc.SetFont(wx.Font(max(4,1.5*self.nsize),wx.SWISS,wx.NORMAL,wx.NORMAL))
        dc.DrawText(label,loc[0]+self.nsize,loc[1]+self.nsize-2)

        if self.network.ap is not None:
            label = str('Recd=%d,RecvQ=%d' %
                        (self.stats.downrecd,self.stats.downq))
            dc.SetTextForeground('light grey')
#        dc.SetFont(wx.Font(max(4,2*self.nsize),wx.SWISS,wx.NORMAL,wx.NORMAL))
            dc.SetFont(wx.Font(max(4,1.5*self.nsize),wx.SWISS,wx.NORMAL,wx.NORMAL))
            dc.DrawText(label,loc[0]+self.nsize,loc[1]+self.nsize+13)

    # if pos is near us, return status string
    def nearby(self,pos):
        dx = self.location[0] - pos[0]
        dy = self.location[1] - pos[1]
        if abs(dx) < .1 and abs(dy) < .1:
            return self.status()
        else:
            return None

    def click(self,pos,which):
        dx = self.location[0] - pos[0]
        dy = self.location[1] - pos[1]
        if abs(dx) < .1 and abs(dy) < .1:
            self.OnClick(which)
            return True
        else:
            return False

    def OnClick(self,which):
        pass
        
    # status report to appear in status bar when pointer is nearby
    def status(self):
	t = "Latency = %.1f " % self.stats.latency
	u = "Numbackoffs %d " % self.stats.numbackoffs
	t = str(t) + str(u) + "Q: "
        t = t + str(len(self.transmit_queue)) + " ["
	for p in self.transmit_queue:
	    t = t + str(p.start) + " "
	t = t + "]"
#        t = t + " DownRecd %d" % self.stats.downrecd
	return t
