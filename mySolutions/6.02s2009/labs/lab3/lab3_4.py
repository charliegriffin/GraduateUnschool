# this is the template for Lab #3, Task #4
import matplotlib.pyplot as p
import math,numpy,random
import lab3

def sample_stats(samples,samples_per_bit=4,vth=0.5):
	bins = numpy.reshape(samples,(-1,samples_per_bit))
	avg_dist = []
	for i in xrange(samples_per_bit):
		column = bins[:,i]
		dist = column - vth
		distance = abs(dist)
		avg_dist.append(numpy.average(distance))
	maximum = max(avg_dist)
	for index in range(samples_per_bit):
		if avg_dist[index] == maximum:
			return index

def digitizeSamples(samples,threshold):	# digitizes samples
	return 1*(samples>threshold)

def receive(samples,samples_per_bit=4,vth=0.5):
    """
    Apply a statistical measure to samples to determine which
    sample in the bit cell should be used to determine the
    transmitted message bit.  vth is the digitization threshold.
    Return a sequence or array of received message bits.
    """
    bit = sample_stats(samples,samples_per_bit,vth)	# choose the appropriate location to sample
    dSamples = digitizeSamples(samples,vth)
    rSamples = []
    for index in range(len(dSamples)):	# takes bits from the chosen location
    	if index%samples_per_bit == bit:
    		rSamples.append(dSamples[index])
    return rSamples


def bit_error_rate(seq1,seq2):
    """
    Perform a bit-by-bit comparison of two message sequences,
    returning the fraction of mismatches.
    """
    numErrors = 0
    for index in range(len(seq1)):
    	if seq1[index] != seq2[index]:
    		numErrors += 1
    return numErrors/float(len(seq1))

if __name__ == '__main__':
    message = [random.randint(0,1) for i in xrange(1000000)]
    noisy_data = lab3.transmit(message,samples_per_bit=4,nmag=1.0)
    received_message = receive(noisy_data)
    ber = bit_error_rate(message,received_message)
    print "bit error rate = %g" % ber