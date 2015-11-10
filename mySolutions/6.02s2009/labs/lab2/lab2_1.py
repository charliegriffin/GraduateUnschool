# template for Lab #2, Task #1
import lab2

def transmit(bits,npreamble=0,
             npostamble=0,
             samples_per_bit=8,
             v0 = 0.0,
             v1 = 1.0,
             repeat = 1):
    """ generate sequence of voltage samples:
          bits: binary message sequence
          npreamble: number of leading v0 samples
          npostamble: number of trailing v0 samples
          samples_per_bit: number of samples for each message bit
          v0: voltage to output for 0 bits
          v1: voltage to output for 1 bits
          repeat: how many times to repeat whole shebang
    """
    samples = []
    for i in range(npreamble):
    	samples.append(v0)
    for bit in bits:
		if bit == 0:
			for i in range(samples_per_bit):
				samples.append(v0)
		elif bit == 1:
			for i in range(samples_per_bit):
				samples.append(v1)
		else:
			print "unexpected value in bits"
    for i in range(npostamble):
    	samples.append(v0)
    while repeat > 1:
    	samples += samples
    	repeat -= 1
    return samples

if __name__ == '__main__':
    # give the transmit function a workout, report errors
    lab2.test_transmit(transmit)