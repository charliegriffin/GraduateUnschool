# lab1_3.py -- template for your Task #3 design file
import numpy
import matplotlib.pyplot as p
import lab1
import lab1_2

def digitizedToRecieved(d_samples,R):
	counter = 0
	lastSample = d_samples[0]
	recievedSamples = []
	for i in range(len(d_samples)):	# go through the list
		sample = d_samples[i]		
		if sample != lastSample:	# resync at transitions
			counter = 0
		if counter == R/2:			# sample in the middle
			recievedSamples.append(sample)
		lastSample = sample
		counter = (counter+1) % R
	recievedSamples = numpy.asarray(recievedSamples)
	return recievedSamples

def find10BitSequence(recievedSamples):
	startSequence1 = numpy.array([0,0,1,1,1,1,1,0,1,0])
	startSequence2 = numpy.array([1,1,0,0,0,0,0,1,0,1])
	for i in range(len(recievedSamples) - 10):
		currentSequence = numpy.array(recievedSamples[i:i+10])
		if numpy.array_equal(currentSequence,startSequence1) or numpy.array_equal(currentSequence,startSequence2):
			return i+10

def translateCharacter(recievedSamples,startPosition):
	sequence = numpy.array(recievedSamples[startPosition:startPosition+10])
	tenBitIndex = lab1.bits_to_int(sequence)
	eightBitIndex = lab1.table_10b_8b[tenBitIndex]
	character = chr(eightBitIndex)
	return character
	

def receive_8b10b(samples):
	"""
	Convert an array of voltage samples transmitted by a
	8b/10b encoder into a message string.
	"""
	# digitize the incoming voltage samples
	message = ''
	R = 8 # number of received samples per bit
	d_samples = lab1_2.v_samples_to_d_samples(samples)
	recievedSamples = digitizedToRecieved(d_samples,R)
# 	print recievedSamples
	startPosition = find10BitSequence(recievedSamples)
	message += translateCharacter(recievedSamples,startPosition)
	startPosition += 10
	message += translateCharacter(recievedSamples,startPosition)
	return message

# testing code.  Do it this way so we can import this file
# and use its functions without also running the test code.
if __name__ == '__main__':
    # supply some test data....
    lab1.task3_test(receive_8b10b,"yb")
#     lab1.task3_test(receive_8b10b,lab1.long_message)