# lab1_3.py -- template for your Task #3 design file
import numpy
import matplotlib.pyplot as p
import lab1
import lab1_2


def receive_8b10b(samples):
    """
    Convert an array of voltage samples transmitted by a
    8b/10b encoder into a message string.
    """
    # digitize the incoming voltage samples
    d_samples = lab1_2.v_samples_to_d_samples(samples)
    R = 8 # number of received samples per bit
    whereToSample(d_samples,R)
    return None

# testing code.  Do it this way so we can import this file
# and use its functions without also running the test code.
if __name__ == '__main__':
    # supply some test data....
    lab1.task3_test(receive_8b10b,"y")
#     lab1.task3_test(receive_8b10b,lab1.long_message)