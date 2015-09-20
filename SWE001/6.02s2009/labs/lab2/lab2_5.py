# template for Lab #2, Task #5
import random
import matplotlib.pyplot as p
import lab2
import lab2_1
import numpy as np


# turn on interactive mode, useful if we're using ipython
p.ion()  

def randomMessage(length):
	message = []
	for i in range(length):
		message.append(random.randint(0,1))
	return message

def transmitMessage(message,channel,samples_per_bit):
	inp = lab2_1.transmit(message,0,0,samples_per_bit)
	return channel(inp)

def plot_eye_diagram(channel,samples_per_bit=8):
    """
    Plot eye diagram for given channel using a 200-bit random
    message.  samples_per_bit determines how many samples
    are sent for each message bit. plot_samples determines
    how many samples should be included in each plot overlay.
    plot_samples should be an integer multiple of samples_per_bit.
    """
    messageLength = 200
    plot_samples = 2*samples_per_bit
    sample = transmitMessage(randomMessage(messageLength),channel,samples_per_bit)
    p.figure()
    p.title(channel.__name__ + ' Eye Diagram')
    xaxis = np.arange(plot_samples)		# stylistic choice from SHY's solution
    for index in range((messageLength)*samples_per_bit/plot_samples):
    	p.plot(xaxis,sample[index*plot_samples:(index+1)*plot_samples],'m-')
    	# sometimes its scary how similar my code is to SHY's when it was written
    	# independently, maybe he's rubbing off on me
	lower = min(sample) - .1*abs(min(sample))
	upper = max(sample) + .1*abs(max(sample))
	p.axis([0,plot_samples,lower,upper])
    p.xlabel('Samples')
    p.ylabel('Voltage')
    p.grid(True)
    p.savefig(channel.__name__ + 'EyeDiagram.png')
    p.clf()

if __name__ == '__main__':
    # plot the eye diagram for both our channels

    # Experiment with different values of samples_per_bit for both
    # channels until you feel that the eye is open enough to permit
    # successful reception of the transmitted bits.  The result
    # will be different for the two channels.
    plot_eye_diagram(lab2.channel1,samples_per_bit=30)
    plot_eye_diagram(lab2.channel2,samples_per_bit=25)
    # These are the "minimum" values I arrived at

    # interact with plots before exiting.  p.show() returns
    # after all plot windows have been closed by the user.
    # Not needed if using ipython
    p.show()  