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

def predictChannelOutput(channel):
	print lab2_3.unit_sample_response(channel)

if __name__ == '__main__':
	print transmitMessage(lab2.channel1)
	predictChannelOutput(lab2.channel1)