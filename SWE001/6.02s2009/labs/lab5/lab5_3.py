# This is the template file for Lab #5, Task #3
import lab5
from lab5_1 import ViterbiDecoder

class SoftViterbiDecoder(ViterbiDecoder):
    # override the default branch metric with one based
    # the square of the Euclidian distance between the
    # expected and received voltages.
    def branch_metric(self,expected,received):
        pass  # your code here...

if __name__=='__main__':
    # try both decoders on exactly the same noisy
    # received voltages
    lab5.test_two(ViterbiDecoder,SoftViterbiDecoder,
                  k=3,glist=(7,6),nbits=100000)