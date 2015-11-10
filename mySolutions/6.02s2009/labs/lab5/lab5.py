import numpy,random,operator,math

# compute hamming distance of two bit sequences
def hamming(s1,s2):
    return sum(map(operator.xor,s1,s2))

# xor together all the bits in an integer
def xorbits(n):
    result = 0
    while n > 0:
        result ^= (n & 1)
        n >>= 1
    return result

def expected_parity(from_state,to_state,k,glist):
    # x[n] comes from to_state
    # x[n-1] ... x[n-k-1] comes from from_state
    x = ((to_state >> (k-2)) << (k-1)) + from_state
    return [xorbits(g & x) for g in glist]

def convolutional_encoder(bits,k,glist):
    result = []
    state = 0
    for b in bits:
        state = (b << (k-1)) + (state >> 1)
        for g in glist:
            result.append(xorbits(state & g))
    return numpy.array(result)

def transmit(bits,sigma=.18):
    errors = (numpy.random.normal(0,sigma,len(bits)) > 0.5) * 1
    numpy.logical_xor(bits,errors,errors)
    return errors

def test_ber(decoder,k=3,glist=(7,6),nbits=1000000):
    # construct message with nbits
    message = numpy.array([random.randint(0,1) for i in xrange(nbits)])

    # calculated BER if we transmit message without coding
    received_raw = transmit(message)
    BER_raw = numpy.sum((message != received_raw) * 1)/float(nbits)

    # calculate BER if we transmit message using a convolution encoder
    # and a Viterbi decoder.  Note the total number of bits sent
    # is lengthed by a factor of 1/r where r is the code rate of
    # the convolutional code.
    encoded = convolutional_encoder(message,k,glist)
    d = decoder(k,glist)
    received_coded = d.decode(transmit(encoded))
    BER_decoded = numpy.sum((message != received_coded) * 1)/float(nbits)

    # report results
    print "BER: without coding = %g, with coding = %g" % (BER_raw,BER_decoded)
    print "Trellis state at end of decoding:"
    d.dump_state()
    print ""

def test_two(one,two,k=3,glist=(7,6),nbits=100000):
    message = numpy.array([random.randint(0,1) for i in xrange(nbits)])
    encoded = convolutional_encoder(message,k,glist)
    noisy = encoded + numpy.random.normal(0,.25,len(encoded))
    received = numpy.maximum(0.0,numpy.minimum(1.0,noisy))

    done = one(k,glist)
    received_done = done.decode(received)
    BER_done = numpy.sum((message != received_done) * 1)/float(nbits)

    dtwo = two(k,glist)
    received_dtwo = dtwo.decode(received)
    BER_dtwo = numpy.sum((message != received_dtwo) * 1)/float(nbits)

    print "BER: %s = %g, %s = %g" % (one,BER_done,two,BER_dtwo)