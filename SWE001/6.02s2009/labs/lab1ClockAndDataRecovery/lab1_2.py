import numpy
import matplotlib
import matplotlib.pyplot as p
import lab1

matplotlib.interactive(True)

def v_samples_to_d_samples(samples):
    """
    Convert an array of voltage samples into an array of
    digitized samples.
    """
    return (samples < 0.2)*1

def find_center_of_start_bit(d_samples,start,samples_per_bit):
    """
    Starting at d_samples[start] find the middle of the next
    START bit returning -1 if no start bit is found.
    """
    position = start		# code assumes start bit is a 0
    while (position < len(d_samples)):
    	if d_samples[position] == 1:
    		return position + samples_per_bit/2
    	else:
    		position += samples_per_bit
    return -1

def decode_data(d_samples,start,nbits,samples_per_bit):
    """
    Select specific data bits from digitized samples:
      start is the index of the first selected bit
      nbits is the number of bits to select
      samples_per_bit is the interval between selections
    Return selected bits as a list or array.
    """
    bitList = []
    for i in range(nbits):
    	bitList.append(d_samples[start+i*samples_per_bit])
    return bitList

def receive(samples):
    """
    Convert an array of voltage samples into a message string.
    """
    # digitize the voltage samples
    d_samples = v_samples_to_d_samples(samples)
    nsamples = len(d_samples)

    # search through the samples starting at the beginning
    message = []
    start = 0
    
    start = find_center_of_start_bit(d_samples,start,8)
    while True:
        # locate sample at middle of next START bit
        start = find_center_of_start_bit(d_samples,start,8)
        if start < 0 or start + 10*8 >= nsamples:
            break  # no START bit found or too near end of samples

        # grab the eight data bits which follow
        bits = decode_data(d_samples,start+8,8,8)
        print bits
# 
#         # first convert bit sequence to an int
#         # and then to a character, append to message
#         message.append(chr(lab1.bits_to_int(bits)))
# 
#         # finally skip to the middle of the STOP bit
#         # and start looking for the next START bit
#         start += 9*8
# 
#     # join all the message characters into a single string
#     return "".join(message)


# testing code.  Do it this way so we can import this file
# and use its functions without also running the test code.
if __name__ == '__main__':
    # see if we can decode the message
    lab1.task2_test(receive,'hi there')