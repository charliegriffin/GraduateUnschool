# This is the template file for Lab #5, Task #1
import numpy
import lab5

def digitize(samples,threshold):
	return 1*(samples > threshold)

class ViterbiDecoder:
    # given the constraint length and a list of parity generator
    # functions, do the initial set up for the decoder.  The
    # following useful instance variables are created:
    #   self.k
    #   self.nstates
    #   self.r
    #   self.predecessor_states
    #   self.expected_parity
    def __init__(self,k,glist):
        self.k = k              # constraint length
        self.nstates = 2**(k-1) # number of states in state machine

        # number of parity bits transmitted for each message bit
        self.r = len(glist)     

        # States are named using (k-1)-bit integers in the range 0 to
        # nstates-1. The bit representation of the integer corresponds
        # to state label in the transition diagram.  So state 10 is
        # named with the integer 2, state 00 is named with the
        # integer 0.

        # for each state s, figure out the two states in the diagram
        # that have transitions ending at state s.  Record these two
        # states as a two-element tuple.
        self.predecessor_states = \
          [((2*s+0) % self.nstates,(2*s+1) % self.nstates)
           for s in xrange(self.nstates)]

        # this is a 2D table implemented as a list of lists.
        # self.expected_parity[s1][s2] returns the r-bit sequence
        # of parity bits the encoder transmitted when make the
        # state transition from s1 to s2.
        self.expected_parity = \
          [[lab5.expected_parity(s1,s2,k,glist) \
            if s1 in self.predecessor_states[s2] else None
            for s2 in xrange(self.nstates)]
           for s1 in xrange(self.nstates)]

    # expected is an r-element list of the expected parity bits
    # (or you can also think of them as voltages given how we send
    # bits down the channel). received is an r-element list of
    # actual sampled voltages for the incoming parity bits.
    # This is a hard-decision branch metric, so, as described in
    # lab write up, digitize the received voltages to get bits and
    # then compute the Hamming distance between the expected sequence
    # and the received sequences, return that as the branch metric.
    # Consider using lab5.hamming(seq1,seq2) which computes the
    # Hamming distance between two binary sequences.
    def branch_metric(self,expected,received):
        assert len(expected) == len(received)	# they must be the same length
        vTh = 0.5
        dSamples = digitize(received,vTh)
        return lab5.hamming(expected,dSamples)
        

    # compute self.PM[...,n] from the batch of r parity bits and
    # the path metrics for self.PM[...,n-1] computed on the previous
    # iteration.  Follow the algorithm described in the lab
    # write up.  In addition to making an entry for self.PM[n,s] for
    # each state s, keep track of the most-likely predecessor
    # for each state in the self.Predecessor array.  You'll probably
    # find the following instance variables and methods useful:
    #    self.predecessor_states
    #    self.expected_parity
    #    self.branch_metric()
    def viterbi_step(self,n,received_voltages):

		for state in xrange(self.nstates):
			(alpha,beta) = self.predecessor_states[state]
			(pAlpha,pBeta) = (self.expected_parity[alpha][state],self.expected_parity[beta][state])

			
#         if received_voltages[0] == 1 and received_voltages[1] == 1:
#         	alpha = [1,0]
#         	beta = [1,1]
#         	# for the state transitions, determine the r parity bits
#         	pAlpha = [0,0]
#         	pBeta = [1,0]
#         	# call the next set of r parity bits p_recieved
    	
    # Identify the most-likely ending state of the encoder by
    # finding the state s which has the mimimum value of PM[s,n]
    # where n points to the last column of the trellis.  If there
    # are several states with the same minimum value, the end of
    # the message has been corrupted by errors, so decrement n
    # and repeat the search. Keep doing this until a unique s is
    # found.  Return the tuple (s,n).
    def most_likely_state(self,n):
        pass  # your code here...

    # starting at state s at time n, use the Predecessor
    # array to find all the states on the most-likely
    # path.  Each state contributes a message bit...
    def traceback(self,s,n):
        message = []
        while n > 0:
            # message bit that caused transition to
            # state s is also the high-order bit of
            # the state name
            message.append(s >> (self.k-2))
            # back to the next earlier state along the path
            s = self.Predecessor[s,n]
            n -= 1
        message.reverse()
        return message

    # figure out what the transmitter sent from info in the
    # received voltages
    def decode(self,received_voltages,debug=False):
        # figure out how many columns they'll be in the trellis
        nreceived = len(received_voltages)
        max_n = (nreceived/2) + 1

        # this is the path metric trellis itself, organized as a
        # 2D array: rows are the states, columns are the time points.
        # PM[s,n] is the metric for the most-likely path through the
        # trellis arriving at state s at time n.
        self.PM = numpy.zeros((self.nstates,max_n),dtype=numpy.float)

        # at time 0, the starting state is the most likely, the other
        # states are "infinitely" worse.
        self.PM[1:self.nstates,0] = 1000000

        # a 2D array: rows are the states, columns are the time
        # points, contents indicate the predecessor state for each
        # current state.
        self.Predecessor = numpy.zeros((self.nstates,max_n),
                                       dtype=numpy.int)

        # use the Viterbi algorithm to compute PM
        # incrementally from the received parity bits.
        n = 0
        for i in xrange(0,nreceived,self.r):
            n += 1

            # Fill in the next columns of PM, Predecessor based
            # on info in the next r incoming parity bits
            self.viterbi_step(n,received_voltages[i:i+self.r])

            # print out what was just added to the trellis state
            if debug:
                print self.PM[:,n],self.Predecessor[:,n]

        # find the most-likely ending state from the last row
        # of the trellis
        s,n = self.most_likely_state(n)

        # reconstruct message by tracing the most likely path
        # back through the matrix using self.Predecessor.
        return self.traceback(s,n)

    # print out final path metrics
    def dump_state(self):
        print self.PM[:,-1]

if __name__=='__main__':
    d = ViterbiDecoder(3,(7,6))
    received = numpy.array([1,1,1,0,1,1,0,0,0,1,1,0,0,0])    
    message = d.decode(received,debug=True)
    print "decoded message =",message