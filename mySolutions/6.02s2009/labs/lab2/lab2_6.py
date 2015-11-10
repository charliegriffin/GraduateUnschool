# template for Lab #2, Task #6
import numpy,random
import matplotlib.pyplot as p
import lab2
import lab2_5
import lab2_1
import lab2_3

def deconvolver(y,h):
    """
    Take the samples that are the output from a channel (y), and the
    channel's unit-sample response (h), deconvolve the samples, and
    return the reconstructed input.
    """
    # w is the reconstruction sequence
    for index in range(len(h)):	# cut off the leading zeros
    	if h[index] > 0.001:
    		break
    h = h[index+1:]
    if len(h) < len(y):
    	h = numpy.append(h,[0 for zeros in range(len(y)-len(h))])
    w = numpy.zeros(len(y))
    for index in range(len(w)):
		nextValue = y[index]
		for i in range(index):
			nextValue -= h[i+1]*w[index-i-1]
		nextValue /= h[0]
		w[index] = nextValue
    return w

def plot_samples(subplot,inp,size,ylo,yhi,title,color='b-'):	# borrowed from SHY
	xaxis = numpy.arange(size)
	p.subplot(subplot)
	p.plot(xaxis,inp,color)
	p.axis([0,size,ylo,yhi])
	p.grid(True)
	p.title(title)

def testDeconvolver(channel,noise=0.):
	# generates a random 8 bit message
    message = lab2_5.randomMessage(100)
    # generates samples from the bit sequence
    inp = numpy.array(lab2_1.transmit(message,0,100))
    # passes the samples through channel
    out = channel(inp,noise)
    # uses the deconvolver to reconstruct the input
    dMessage = deconvolver(out,lab2_3.unit_sample_response(channel))
    p.figure()	# plot
    p.suptitle('Random Message through '+channel.__name__,fontsize = 20,fontweight='bold')
    plot_samples(311, inp, len(inp), -.1, 1.1, 'Input')
    plot_samples(312, out, len(out), -.1, 1.1, 'Output', 'g-')
    plot_samples(313, dMessage, len(dMessage), -.1, 1.1, 'Deonvolved Result', 'r-')
    p.subplots_adjust(hspace=0.5)
    if noise == 0.:
    	p.savefig(channel.__name__+'Deconvolution.png')
    else:
    	p.savefig(channel.__name__+'Noise'+str(noise)+'Deconvolution.png')
    p.clf()

if __name__ == '__main__':
    """
    Develop test patterns and try using deconvolution to reconstruct
    the input from the output samples for each of the two channels.
    Use 8 samples per bit.  Generate plots comparing your
    reconstruction to the original input and output of the channel.
    Finally, try performing reconstruction with nonzero noise.
    """
    testDeconvolver(lab2.channel1)
    testDeconvolver(lab2.channel2)
    testDeconvolver(lab2.channel1,noise=1.0e-5)
    testDeconvolver(lab2.channel1,noise=1.0e-4)
    testDeconvolver(lab2.channel1,noise=1.0e-3)