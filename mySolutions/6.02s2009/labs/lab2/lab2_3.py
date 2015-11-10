# template for Lab #2, Task #3
import numpy
import matplotlib.pyplot as p
import lab2

# turn on interactive mode, useful if we're using ipython
p.ion()  

def unit_sample_response(channel):
    """
    Return sequence of samples that corresponds to the unit-sample
    response of the channel.  The sequence is truncated at the
    point where the absolute value of 10 consecutive samples is
    less than 1% of the value is the largest magnitude.
    """
    numSamples = 1000
    sampleSequence = [1.0]+[0.0]*numSamples
    sampleResponse = numpy.array(channel(sampleSequence))	# run samples through channel
    maxSample =  max(sampleResponse)
    for index in range(sampleResponse.shape[0]):
		# finds the index where the next 10 values are < 1% of the max
    	if ((sampleResponse[index:index+10] < 0.01*maxSample)*1.).sum() == 10.:
    		break
    truncIndex = index + 10
    return sampleResponse[:truncIndex]

if __name__ == '__main__':
    # plot the unit-sample response of our two channels
    lab2.plot_unit_sample_response(unit_sample_response,lab2.channel1)
    lab2.plot_unit_sample_response(unit_sample_response,lab2.channel2)

    # interact with plots before exiting.  p.show() returns
    # after all plot windows have been closed by the user.
    # Not needed if using ipython
    p.show()  
#     p.savefig('unitSampleResponseOfChannel2.png')