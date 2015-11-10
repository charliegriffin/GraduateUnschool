import numpy
import matplotlib.pyplot as p
import lab2
import lab2_1
import lab2_3

# p.ion()

def transmitMessage(channel):
	# compute the output of the channel when transmitting the message
	# 10101010 with a 10 sample preamble and 100 sample postamble
	message = [1,0,1,0,1,0,1,0]
	inp = lab2_1.transmit(message,10,100)
	return channel(inp)

def convolutionSum(inputSampleSequences,unitSampleResponse):
	inputSampleSequences = numpy.array(inputSampleSequences)
	unitSampleResponse = numpy.array(unitSampleResponse)
	return numpy.convolve(inputSampleSequences,unitSampleResponse)

def predictChannelOutput(channel):
	message = [1,0,1,0,1,0,1,0]
	return convolutionSum(lab2_1.transmit(message,10,100),lab2_3.unit_sample_response(channel))

def produceFigure(computedOutput,predictedOutput,name):
	predictedOutput=predictedOutput[:len(computedOutput)]
	p.figure()
	lower = min(min(computedOutput),min(predictedOutput))
	upper = max(max(computedOutput),max(predictedOutput))
	lower = lower - abs(lower)*0.1
	upper = upper + abs(upper)*0.1
	p.suptitle(name,fontsize=20,fontweight='bold')
	p.subplot(311)
	p.axis([0,len(computedOutput),lower,upper])
	p.plot(computedOutput,'g-')
	p.title('Computed Output')
	p.grid(True)
	p.ylabel('Voltage')
	p.subplot(312)
	p.axis([0,len(predictedOutput),lower,upper])
	p.plot(predictedOutput,'b-')
	p.title('Predicted Output')
	p.grid(True)
	p.ylabel('Voltage')
	difference = computedOutput-predictedOutput
# 	print difference
	p.subplot(313)
	diffUpper = max(difference)
	diffUpper += abs(diffUpper)*0.1
	diffLower = min(difference)
	diffLower -= abs(diffLower)*0.1
	p.axis([0,len(computedOutput),diffLower,diffUpper])
	p.plot(difference,'r-')
	p.title('Difference (computed-predicted)')
	p.grid(True)
	p.ylabel('Voltage')
	p.xlabel('Sample Number')
	p.subplots_adjust(hspace=0.5)	# this spaces the plots out
	p.savefig(name+'Prediction.png')
	p.clf()

if __name__ == '__main__':
	produceFigure(transmitMessage(lab2.channel1),predictChannelOutput(lab2.channel1),lab2.channel1.__name__)
	produceFigure(transmitMessage(lab2.channel2),predictChannelOutput(lab2.channel2),lab2.channel2.__name__)