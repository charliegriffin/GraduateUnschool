import random, sys, wx, math, time
from lab8_wnode import *
from lab8_util import *

# Channel access simulator.  Network instance repeatedly calls step method
# of node instances to determine which transmissions should take place in
# each time slot.  Default behaviors:
# - packets whose transmissions overlap have their collision flags set
# - nodes transmit packets whose start time has arrived (or past) if the
#   channel isn't busy
#
# NOTE: In the simulator, time is slotted and increments 1 step at a time.  
# Packet lengths are expressed in units of time slots.
#

#defines
NO_COLLISION = 0		# packet experienced no collision
COLLISION = 1			# packet experienced collision
NO_RETRY = 0			# config option: no retries
RETRY = 1			# retry on
SOURCE_NOSKEW = 0		# all nodes contribute roughly equal load
SOURCE_SKEW = 1			# nodes contribute geometrically-spaced loads

################################################################################
#
# WirelessNetConfig -- setting various configuration parameters
# 
################################################################################
class WirelessNetConfig:
    def __init__(self,n,chantype,ptime,dist,load,retry,backoff,
		 skew=SOURCE_NOSKEW,qmax=0,simtime=10000):
	self.numnodes = n	 # number of nodes sharing channel (integer)
	self.chantype = chantype # channel type: stabaloha, CSMA, TDMA (string)
	self.ptime = ptime	# packet length in time-slot units (integer)
	self.dist = dist	# distribution to generate pkts (string)
	self.load = load	# total offered load (integer percentage)
	self.retry = retry	# does a node retry or not?  (RETRY or NO_RETRY)
	self.maxbackoff = 16	# constant specifying max number of backoffs
	self.backoff = backoff	# "None", "binexpo" or "Mine"
	self.skew = skew	# NOSKEW for uniform load; else geom-spaced
        self.qmax = qmax        # max per-node queue size (0 for NO LIMIT)
        self.playstep = 1.0     # 1 second playstep by default
	self.simtime = simtime	# total simulation time (integer)
        self.downlink = 'FIFO'

    # called when user sets number of network nodes
    def set_nodes(self,n):
        print 'set_nodes', n
	self.numnodes = n

    # called when user sets packet time
    def set_packet_time(self,ptime):
        print 'set_packet_time', ptime
        self.ptime = ptime

    # called when user sets total channel load
    def set_load(self,load):
	print 'set_load', load
	self.load = load

    # called when user sets total simulation time (number of time slots)
    def set_sim_time(self,t):
	self.simtime = t
	print 'set_simtime', t

    # called when user sets channel type
    def set_channel_type(self,t):
	if t == '': t = "stabaloha" 
        print 'set_protocol', t
        self.chantype = t

    # called when user sets whether nodes should retry on collision or not
    def set_retry(self,r):
	if r == 'Yes':
            print 'set_retry', RETRY
            self.retry = RETRY
	else: 			# no retry by default
            print 'set_retry', NO_RETRY
            self.retry = NO_RETRY

    # what kind of backoff protocol do we want?
    def set_backoff(self,b):
	if b == '': b = 'binexpo'
	print 'set_backoff ', b
	self.backoff = b
	
    # called when user sets whether nodes should send at skewed or equal rates
    def set_skew(self,s):
	if s == 'Yes':
            print 'set_src_skew SOURCE_SKEW'
            self.skew = SOURCE_SKEW
	else: 			# default is NOSKEW
            print 'set_src_skew SOURCE_NOSKEW'
            self.skew = SOURCE_NOSKEW

    def set_qmax(self,qmax):
        if qmax == 0: print 'set_qmax NO LIMIT'
        else: print 'set_qmax ', qmax
        self.qmax = qmax        # 0 if NO LIMIT on queue size

    def set_downlink(self,dl):
        print 'set_downlink ', dl
        self.downlink = dl

################################################################################
#
# WirelessNetwork -- a collection of network nodes sharing a channel
# Provides the following methods, among others that may be less important
# step() -- the "main body" of this class, which orchestrates what happens
#           in each time step, including calling each node's step() method
# collide() -- internal function used to determine if two or more packets 
#              are concurrently on the channel.  If so, the packet's 
#              coll_flag field is set to COLLISION, if not, NO_COLLISION
# channel_busy() -- Returns True if channel is currently busy, else False
# print_stats() -- prints useful stats about the network and each node

################################################################################
class WirelessNetwork:
    def __init__(self,n,chantype,ptime,dist,load,retry,backoff,
		 skew=SOURCE_NOSKEW,qmax=0,simtime=10000):
	self.config = WirelessNetConfig(n,chantype,ptime,dist,load,retry,
					backoff,skew,qmax,simtime)
	self.stats = Stats(simtime)
        self.ap = None
	self.reset()

    # return network to initial state
    def reset(self):
	numnodes = self.config.numnodes
        self.nodes = {}  # indexed by location tuple (x,y)
        self.nlist = []  # equivalent to self.nodes.values()
        self.max_x = 0
        self.max_y = 0

	for i in xrange(0,numnodes):
	    loc = (math.cos(2*math.pi*i/numnodes)+.3, 
		   math.sin(2*math.pi*i/numnodes)+1)
	    n = self.add_node(loc)

        for n in self.nlist: n.reset()

	# Attach a source traffic distribution w/ the specified rate.
	# By default, each node has uniform rate; override for skewed dists
	load = self.config.load/100.0	# XXX because we're inputting a % load
	load = load/self.config.ptime # load was in pkts/tslot

	dist = self.config.dist
	skew = self.config.skew
	nextrate = load/2.0   # only relevant when skew == SOURCE_SKEW
	for n in self.nlist:
	    if (skew != SOURCE_SKEW):
#		print 'attaching ', 1.0*load/numnodes, ' to node ', n.get_id()
		n.attach_distribution(dist,load/numnodes)
                n.rate = load/numnodes
	    else:		# geometrically-spaced rates
		if n == self.nlist[len(self.nlist)-1]:
		    nextrate = 2.0*nextrate
		print 'attaching ', nextrate, ' to node ', n.get_id()
                n.rate = nextrate
		n.attach_distribution(dist,nextrate)
		nextrate = nextrate/2.0;

        self.time = 0
        self.channel = []
	self.stats.reset(self.config.simtime) # clears all statistics
        if self.ap is not None:
            self.ap.reset()

    # add an access point to the wireless network
    def add_ap(self,ap):
        print 'adding ap'
        self.ap = ap
    
    def make_node(self,loc,retry):
        return WirelessNode(loc,self,retry)

    # add a node to the network, loc should be (x,y) tuple
    def add_node(self,loc):
        n = self.find_node(loc)
        if n is None:
            n = self.make_node(loc,self.config.retry)
            self.max_x = max(self.max_x,loc[0])
            self.max_y = max(self.max_y,loc[1])
            self.nodes[loc] = n
            self.nlist.append(n)
        return n

    # return node instance given its location
    def find_node(self,loc):
        return self.nodes.get(loc,None)

    # given an id, return the node
    def get_node_by_id(self,id):
        return self.nlist[id]

    # apply f to each network node, return list of results
    def map_node(self,f):
        return [f(node) for node in self.nlist]

    # Simulate wireless network one time slot at a time.
    # The ordering of steps here is important; we need to check for 
    # collisions first to avoid edge case problems.  If you reorder things 
    # below, you'd better know what you're doing!
    def step(self,count=1):
        stop_time = self.time + count
        while self.time < stop_time:
            # determine what's happening on channel
            self.collide()            
            # wrap up any transmissions that just ended
            while len(self.channel) > 0 and self.channel[0].end <= self.time:
                p = self.channel.pop(0)
                # invoke node's callback when packet finishes transmitting
		p.sender.transmit_done(p)
		if p.coll_flag == NO_COLLISION:
		    self.stats.success += 1

            # see who wants to start transmitting in the next time slot
            self.new_transmissions = []
            self.stats.pending = 0
            for n in self.nlist:
                self.stats.pending += n.step(self.time) # node may call network's transmit method

            # Step for the access point
            if self.ap != None:
                self.ap.step(1)

            ##### end of time slot ######

	    # end simulation if we reach ending time (simtime)
	    if self.time == self.config.simtime:
		break

            self.time += 1

            ##### beginning of time slot #####

            # start up new transmissions
            self.channel.extend(self.new_transmissions)

	if self.time >= self.config.simtime:
	    self.print_stats()

    # called in "middle" of each time slot to determine what's
    # happening in the channel, ie, are there collisions?
    def collide(self):
        # simple, "perfect" RF channel
        # if there's more than one active transmission, set collision flags
        # for any packets now being transmitted
        if len(self.channel) > 1:
	    for p in self.channel:
		self.stats.collisions += 1
                p.coll_flag = COLLISION

    # called by nodes when they start transmitting a packet; 
    # packets are identified by their original start time.  
    # Nodes will expect a callback to their transmit_done method 
    # after transmission completes.
    # channel is list of lists where each sublist has the form
    # [end_time,node,packet_id,collision_flag]
    # channel is a list of packets
    def transmit(self,node,packet):
	packet.end = self.time+self.config.ptime
	packet.coll_flag = NO_COLLISION
        self.new_transmissions.append(packet)

    # Return True if channel is busy (ie, some node is currently transmitting),
    # used by the channel_access method of WirelessNode.
    def channel_busy(self):
        return len(self.channel) != 0
    
    # print out useful stats about the WirelessNetwork and each WirelessNode
    def print_stats(self):
	for n in self.nlist:
	    n.stats._print(self.time, self.config.ptime, n.get_id())
	self.stats._print(self.time, self.config.ptime, 'net')
        print "Inter-node fairness: %.2f" % self.fairness(0)
        print "Inter-node weighted fairness: %.2f" % self.fairness(1)
        
    def fairness(self, rate_normalized):
        succ_sum = succ_sumsq = 0
        for n in self.nlist:
            if rate_normalized == 0: 
                x = n.stats.success
            else:
                x = 1.0*n.stats.success/n.rate
            succ_sum += x
            succ_sumsq += x*x
        if succ_sumsq > 0:
            return 1.0*succ_sum*succ_sum / (len(self.nlist) * succ_sumsq)
        else:
            return 0

    #########################################################
    # support for graphical simulation interface
    #########################################################

    def draw(self,dc,transform):
        # busy or collision? indicate with different background
        if len(self.channel) > 0:
            if len(self.channel) > 1: color = 'salmon'
            else: color = 'pale green'
            dc.SetBackground(wx.Brush(color))
            dc.Clear()

        # draw nodes
        for node in self.nlist:
            node.draw(dc,transform)

        if self.ap is not None:
            self.ap.draw(dc,transform)

    def click(self,pos,which):
        for node in self.nlist:
            if node.click(pos,which):
                return True
        return False

    def status(self,statusbar,pos):
        for node in self.nlist:
            msg = node.nearby(pos)
            if msg: break
        else:
            msg = ''
        statusbar.SetFieldsCount(5)
        statusbar.SetStatusWidths([100,100,100,100,-1])
        statusbar.SetStatusText('Time: %d' % int(self.time), 0)
        statusbar.SetStatusText('Attempts: %d' % self.stats.attempts, 1)
        statusbar.SetStatusText('Success: %d' % self.stats.success, 2)
#        statusbar.SetStatusText('Collisions: %d' % self.stats.collisions, 3)
	if self.time > 0: 
	    u = 1.0*self.stats.success*self.config.ptime/self.time
	else: 
	    u = 0.00
        statusbar.SetStatusText('Utilization: %.2f' % u, 3)
        statusbar.SetStatusText('Status: %s' % msg, 4)

################################################################################
#
# NetSim -- a graphical front end for network simulations
#
################################################################################

# convert from network to screen coords
# transform = (scale,(xoffset,yoffset))
def net2screen(loc,transform):
    return (transform[1][0]+loc[0]*transform[0],
            transform[1][1]+loc[1]*transform[0])

# convert from screen to network coords
# transform = (scale,(xoffset,yoffset))
def screen2net(loc,transform):
    return (float(loc[0]-transform[1][0])/transform[0],
            float(loc[1]-transform[1][1])/transform[0])

# is pt within distance of line between end1 and end2?
def nearby(pt,end1,end2,distance):
    if end1[0] == end2[0]:    # vertical wire
        if abs(pt[0] - end1[0]) > distance:
            return False
        y1 = min(end1[1],end2[1])
        y2 = max(end1[1],end2[1])
        return pt[1] >= y1 - distance and pt[1] <= y2 + distance
    elif end1[1] == end2[1]:  # horizontal wire
        if abs(pt[1] - end1[1]) > distance:
            return False
        x1 = min(end1[0],end2[0])
        x2 = max(end1[0],end2[0])
        return pt[0] >= x1 - distance and pt[0] <= x2 + distance
    else:  # non-manhattan wire
        # slope and intercept for line between end1 and end2
        slope1 = float(end1[1] - end2[1])/(end1[0] - end2[0])
        intercept1 = float(end1[1]) - slope1*end1[0]
        # slope and intercept for perpendicular line passing through pt
        slope2 = -1/slope1
        intercept2 = float(pt[1]) - slope2*pt[0]
        # x coordinate of intersection of those two lines
        xi = (intercept2 - intercept1)/(slope1 - slope2)
        if xi < min(end1[0],end2[0]) or xi > max(end1[0],end2[0]):
            return False
        dx = pt[0] - xi;
        dy = pt[1] - (slope2*xi + intercept2)
        return (dx*dx) + (dy*dy) <= distance*distance        

# A panel that displays a network
class NetPanel(wx.Panel):
    def __init__(self,parent,statusbar):
        wx.Panel.__init__(self,parent,-1,wx.DefaultPosition,(10,10))
        self.SetBackgroundColour('white')
        self.SetMinSize((100,100))
        self.statusbar = statusbar
        self.network = None
        self.setupBuffer = False
        self.redraw = False
        self.playmode = False
        self.lastplaytime = 0
        self.transform = (2,(0,0))
        self.SetupBuffer()
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        self.Bind(wx.EVT_SIZE,self.OnSize)
        self.Bind(wx.EVT_IDLE,self.OnIdle)
        self.Bind(wx.EVT_MOTION,self.OnMotion)
        self.Bind(wx.EVT_LEFT_DOWN,self.OnLeftClick)

    def SetupBuffer(self):
        # use an off-screen drawing buffer to reduce flicker
        size = self.GetClientSize()
        self.buffer = wx.EmptyBitmap(size.width,size.height)
        self.setupBuffer = False
        self.redraw = True  # fill up new buffer

    def OnSize(self,event):
        # wait until IDLE to actually do refresh just in case there
        # are multiple SIZE events in a row that we can roll into one
        self.setupBuffer = True

    def OnClick(self,event,which):
        pos = screen2net(event.GetPositionTuple(),self.transform)
        if self.network.click(pos,which):
            self.redraw = True

    def OnLeftClick(self,event):
        self.OnClick(event,'left')

    def OnMotion(self,event):
        pos = screen2net(event.GetPositionTuple(),self.transform)
        self.network.status(self.statusbar,pos)

    def OnIdle(self,event):
        if self.setupBuffer:
            # create a new drawing buffer
            self.SetupBuffer()

        if self.redraw:
            self.DrawNetwork()
            self.Refresh(False)
            self.redraw = False
            self.network.status(self.statusbar,(-10,-10))                

        if self.playmode == True:
            self.redraw = True
            curtime = time.clock()
            delta = curtime - self.lastplaytime
            if delta > self.network.config.playstep:
                if self.network.config.simtime > self.network.time:
                    self.network.step(1)
                    self.lastplaytime = curtime
                else:
                    self.playmode = False
            event.RequestMore()

    def OnPaint(self,event):
        # just refresh the screen from our buffer
        dc = wx.BufferedPaintDC(self,self.buffer)        

    def OnReset(self,event):
        self.playmode = False
        self.network.reset()
        self.network.status(self.statusbar,(-10,-10))
        self.redraw = True

    def OnStats(self,event):
        self.network.print_stats()
        self.network.status(self.statusbar,(-10,-10))
        self.redraw = True

    def OnStep(self,event):
        button = event.GetEventObject().GetLabel()
	arg = button[button.find(' '):]
	if arg == ' all': count = self.network.config.simtime-self.network.time
	else: count = int(arg)
        self.network.step(count=count)
        self.network.status(self.statusbar,(-10,-10))
        self.redraw = True

    def OnPlay(self,event):
        self.playmode = True

    def OnPause(self,event):
        self.playmode = False

    def OnNNodes(self,event):
        nnodes = event.GetEventObject().GetValue()
        self.network.config.set_nodes(nnodes)
        self.redraw = True

    def OnPTime(self,event):
        packetTime = event.GetEventObject().GetValue()
        self.network.config.set_packet_time(packetTime)
        self.redraw = True

    def OnLoad(self,event):
        load = event.GetEventObject().GetValue()
        self.network.config.set_load(load)
        self.redraw = True

    def OnSimTime(self,event):
        simTime = event.GetEventObject().GetValue()
        self.network.config.set_sim_time(simTime)
        self.redraw = True

    def OnCType(self,event):
        cType = event.GetEventObject().GetStringSelection()
        self.network.config.set_channel_type(cType)
        self.redraw = True

    def OnRetry(self,event):
        retry = event.GetEventObject().GetStringSelection()
        self.network.config.set_retry(retry)
        self.redraw = True

    def OnBackoff(self,event):
	backoff = event.GetEventObject().GetStringSelection()
	self.network.config.set_backoff(backoff)
	self.redraw = True

    def OnSkew(self,event):
	skew = event.GetEventObject().GetStringSelection()
	self.network.config.set_skew(skew)
	self.redraw = True

    def OnQMax(self,event):
	qmax = event.GetEventObject().GetValue()
	self.network.config.set_qmax(qmax)
	self.redraw = True

    def OnDownlink(self,event):
	downlink = event.GetEventObject().GetStringSelection()
	self.network.config.set_downlink(downlink)
	self.redraw = True

    def OnExit(self,event):
        self.network.status(self.statusbar,(-10,-10))
        self.redraw = True
	sys.exit(1)

    def DrawNetwork(self):
        # erase buffer
        dc = wx.BufferedDC(None,self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()

        # compute grid size for network
        size = self.GetClientSize()
        netsize = (self.network.max_x+1,self.network.max_y+1)
        grid = min(size[0]/netsize[0],size[1]/netsize[1])
        xoffset = (size[0] - (netsize[0]-1)*grid)/2
        yoffset = (size[1] - (netsize[1]-1)*grid)/2
        self.transform = (grid, (xoffset,yoffset))

        self.network.draw(dc,self.transform)

    def SetNetwork(self,network):
        self.network = network
        self.network.reset()
        self.redraw = True

class NetFrame(wx.Frame):
    def __init__(self,parent=None,id=-1,size=(1000,500),
                 pos=wx.DefaultPosition,title='WSim'):
        wx.Frame.__init__(self,parent,id,title,pos,size)
        self.SetBackgroundColour('white')
        statusbar = self.CreateStatusBar()
        self.network = None

        self.netpanel = NetPanel(self,statusbar)  # panel for showing network

        # sizer for parameters
        parameters = wx.Panel(self,-1)  # simulation parameters
        parameters.SetBackgroundColour('light gray')
        psizer = wx.FlexGridSizer(cols=2,hgap=5,vgap=5)
        parameters.SetSizer(psizer)

        # number of nodes
        psizer.Add(wx.StaticText(parameters,-1,'Num nodes:'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.nNodes = wx.SpinCtrl(parameters,-1,min=1,max=800)
        self.Bind(wx.EVT_SPINCTRL,self.netpanel.OnNNodes,self.nNodes)
        psizer.Add(self.nNodes,0)

	# offered load
        psizer.Add(wx.StaticText(parameters,-1,'Load % (pkts/slot):'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.load = wx.SpinCtrl(parameters,-1,min=0,max=1000,initial=100)
        self.Bind(wx.EVT_SPINCTRL,self.netpanel.OnLoad,self.load)
        psizer.Add(self.load,0)

        # packet time
        psizer.Add(wx.StaticText(parameters,-1,'Pkt time (slots):'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.packetTime = wx.SpinCtrl(parameters,-1,min=1,max=100,initial=1)
        self.Bind(wx.EVT_SPINCTRL,self.netpanel.OnPTime,self.packetTime)
        psizer.Add(self.packetTime,0)

        # simulation time
        psizer.Add(wx.StaticText(parameters,-1,'Sim time (slots):'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.simTime = wx.SpinCtrl(parameters,-1,min=1,max=100000,initial=10000)
        self.Bind(wx.EVT_SPINCTRL,self.netpanel.OnSimTime,self.simTime)
        psizer.Add(self.simTime,0)

        # channel type
        psizer.Add(wx.StaticText(parameters,-1,'MAC protocol:'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        channelTypes = ['Aloha','CSMA','TDMA']
        self.cType = wx.Choice(parameters,-1,choices=channelTypes)
        self.Bind(wx.EVT_CHOICE,self.netpanel.OnCType,self.cType)
        psizer.Add(self.cType,0)

        # retry or not
        psizer.Add(wx.StaticText(parameters,-1,'Retry?'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        retry_choices = ['No','Yes']
        self.retry = wx.Choice(parameters,-1,choices=retry_choices)
        self.Bind(wx.EVT_CHOICE,self.netpanel.OnRetry,self.retry)
        psizer.Add(self.retry,0)

	# type of backoff on collision and retry
	psizer.Add(wx.StaticText(parameters,-1,'Backoff'),
		   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
	backoff_choices = ['None','Binexpo']
	self.backoff = wx.Choice(parameters,-1,choices=backoff_choices)
	self.Bind(wx.EVT_CHOICE,self.netpanel.OnBackoff,self.backoff)
	psizer.Add(self.backoff,0)

 	# source skew
	psizer.Add(wx.StaticText(parameters,-1,'Src skew?'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
	skew_choices = ['No','Yes']
	self.skew = wx.Choice(parameters,-1,choices=skew_choices)
        self.Bind(wx.EVT_CHOICE,self.netpanel.OnSkew,self.skew)
	psizer.Add(self.skew,0)

        # No downlink in lab8
        '''
	# maximum per-node queue size
        psizer.Add(wx.StaticText(parameters,-1,'Max Q (-1 for no limit):'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        self.qmax = wx.SpinCtrl(parameters,-1,min=0,max=10000,initial=0)
        self.Bind(wx.EVT_SPINCTRL,self.netpanel.OnQMax,self.qmax)
        psizer.Add(self.qmax,0)

 	# downlink parameters start here
        # Scheduling method: FIFO, RoundRobin variants
	psizer.Add(wx.StaticText(parameters,-1,'Downlink scheduler'),
                   0,wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
	downlink_choices = ['FIFO','RoundRobin','StickyRR']
	self.downlink = wx.Choice(parameters,-1,choices=downlink_choices)
        self.Bind(wx.EVT_CHOICE,self.netpanel.OnDownlink,self.downlink)
	psizer.Add(self.downlink,0)
        '''

        # holds netpanel and simulation controls
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.netpanel,1,flag=wx.EXPAND)  # expand V and H

        # sizer for controls
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.Add(hsizer,0,flag=wx.EXPAND)

        # reset button -- calls netpanel's OnReset
        button = wx.Button(self,-1,'Reset')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnReset, button)
        hsizer.Add(button,1)
        
        # stats button -- calls netpanel's OnStats
        button = wx.Button(self,-1,'Stats')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnStats, button)
        hsizer.Add(button,1)

        # step buttons -- calls netpanel's OnStep
        button = wx.Button(self,-1,'Step 1')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnStep, button)
        hsizer.Add(button,1)
        button = wx.Button(self,-1,'Step 10')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnStep, button)
        hsizer.Add(button,1)
        button = wx.Button(self,-1,'Step 100')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnStep, button)
        hsizer.Add(button,1)
        button = wx.Button(self,-1,'Step all')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnStep, button)
        hsizer.Add(button,1)
        button = wx.Button(self,-1,'Play')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnPlay, button)
        hsizer.Add(button,1)
        button = wx.Button(self,-1,'Pause')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnPause, button)
        hsizer.Add(button,1)

        # exit button
        button = wx.Button(self,-1,'Exit')
        self.Bind(wx.EVT_BUTTON, self.netpanel.OnExit, button)
        hsizer.Add(button,1)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(parameters,0,flag=wx.EXPAND)
        mainSizer.Add(vsizer,1,flag=wx.EXPAND)

        self.SetSizer(mainSizer)   # layout window

    def SetNetwork(self,network):
        self.netpanel.SetNetwork(network)
#        network.config.set_nodes(self.nNodes.GetValue())
#        network.config.set_packet_time(self.packetTime.GetValue())
#	network.config.set_load(self.load.GetValue())
#	network.config.set_sim_time(self.simTime.GetValue())
#        network.config.set_channel_type(self.cType.GetStringSelection())
#	network.config.set_retry(self.retry.GetStringSelection())
#	network.config.set_backoff(self.backoff.GetStringSelection())
#	network.config.set_skew(self.skew.GetStringSelection())
#	network.config.set_qmax(self.qmax.GetValue())
#	network.config.set_downlink(self.downlink.GetStringSelection())

class NetSim(wx.App):
    def OnInit(self):
        self.frame = NetFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def SetNetwork(self,network):
        self.frame.SetNetwork(network)