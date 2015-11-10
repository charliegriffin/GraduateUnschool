# This is the template file for Lab #5, Task #2
import lab5
from lab5_1 import ViterbiDecoder

if __name__=='__main__':
    # encode a 500,000 bit message using the specified
    # convolutional encoder, transmit it through a noisy
    # channel and then decode it with an instance of the
    # provided decoder class.  Compare the BER with simply
    # transmitting the raw message across the channel.
    lab5.test_ber(ViterbiDecoder,k=3,glist=(7,6),nbits=500000)

    # try it again with a stronger convolutional code
    lab5.test_ber(ViterbiDecoder,k=4,glist=(0xE,0xD),nbits=500000)