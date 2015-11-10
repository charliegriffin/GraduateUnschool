import numpy, pylab, time

# convert nbits of int into bit sequences, lsb first
def int_to_bits(n,nbits=8):
    return [(n >> i) & 1 for i in xrange(nbits)]

# encode data into sequence of samples
#  prefix = sequence of bits that appear before data bits
#  postfix = sequence of bits that appear after data bits
#  nbits = number of data bits to encode (LSB first)
#  nsamples = number of samples to generate for each bit
def encode_data(data,prefix=[1],postfix=[0],nbits=8):
    # start with prefix
    result = prefix[:]
    # encode data LSB first
    result.extend(int_to_bits(data,nbits=8))
    # end with postfix bits
    result.extend(postfix)
    return result

# encode string.  See encode_data for details...
def encode_string(s,prefix=[1],postfix=[0],nbits=8):
    result = [0]*5   # start with some zeros
    for ch in s:
        result.extend(encode_data(ord(ch),prefix=prefix,postfix=postfix,nbits=nbits))
    result += [0]*5   # end with some zeros
    return result

# convert digital sample sequence into voltages, upsample, add noise
# result is numpy array
def transmit(seq,vlow=-0.5,vhigh=0.5,upsample=8,ntaps=101,bw=.25,nmag=0.1):
    ndata = len(seq)*upsample
    samples = [vlow]*ntaps
    vlast = vlow
    for s in seq:
        v = vlow if s == 0 else vhigh
        dv = v - vlast
        samples.append(dv*0.5 + vlast)
        samples.append(dv*0.75 + vlast)
        samples.append(dv*0.875 + vlast)
        samples.extend([v]*(upsample-3))
        vlast = v
    voltages = numpy.fromiter(samples,dtype=numpy.float)

    taps = compute_taps(ntaps,bw)
    start = 3*ntaps/2
    filtered = numpy.convolve(voltages,taps)[start:start+ndata]
    noise = numpy.random.triangular(-nmag,0,nmag,size=ndata)
    return filtered+noise

# low-pass filter taps, cutoff is fraction of sample rate
def compute_taps(ntaps,cutoff,gain=1.0):
    order = float(ntaps - 1)
    # hamming window
    window = [0.53836 - 0.46164*numpy.cos((2*numpy.pi*i)/order)
              for i in xrange(ntaps)]

    fc = float(cutoff)
    wc = 2 * numpy.pi * fc
    middle = (ntaps - 1)/2
    taps = [0.0] * ntaps
    fmax = 0  # for low pass, gain @ DC = 1.0
    for i in xrange(ntaps):
        if i == middle:
            coeff = (wc/numpy.pi) * window[i]
            fmax += coeff
        else:
            n = i - middle
            coeff = (numpy.sin(n*wc)/(n*numpy.pi)) * window[i]
            fmax += coeff
        taps[i] = coeff
    gain = gain / fmax
    for i in xrange(ntaps):
        taps[i] *= gain
    return taps

# convert bit sequence (lsb first) to an int
def bits_to_int(bits):
    result = 0
    for i in xrange(len(bits)):
        result += bits[i] * (1 << i)
    return result

# 8b/10 encoder

# two encoder tables: 5b/6b and 3b/4b
# each entry is a tuple of ints
# the two ints of each entry should be the same, or be complements
# RD is -1: use tuple[0]; if tuple[0]!=tuple[1], set RD to +1
# RD is +1: use tuple[1]; if tuple[0]!=tuple[1], set RD to -1

table_5b_6b = [
    (0x39,0x06),  # D.00
    (0x2E,0x11),  # D.01
    (0x2D,0x12),  # D.02
    (0x23,0x23),  # D.03
    (0x2B,0x14),  # D.04
    (0x25,0x25),  # D.05
    (0x26,0x26),  # D.06
    (0x07,0x38),  # D.07
    (0x27,0x18),  # D.08
    (0x29,0x29),  # D.09
    (0x2A,0x2A),  # D.10
    (0x0B,0x0B),  # D.11
    (0x2C,0x2C),  # D.12
    (0x0D,0x0D),  # D.13
    (0x0E,0x0E),  # D.14
    (0x3A,0x05),  # D.15
    (0x36,0x09),  # D.16
    (0x31,0x31),  # D.17
    (0x32,0x32),  # D.18
    (0x13,0x13),  # D.19
    (0x34,0x34),  # D.20
    (0x15,0x15),  # D.21
    (0x16,0x16),  # D.22
    (0x17,0x28),  # D.23
    (0x33,0x0C),  # D.24
    (0x19,0x19),  # D.25
    (0x1A,0x1A),  # D.26
    (0x1B,0x24),  # D.27
    (0x1C,0x1C),  # D.28
    (0x1D,0x22),  # D.29
    (0x1E,0x21),  # D.30
    (0x35,0x0A),  # D.31
    ]

# index by (byte >> 5) & 0x7
# use D.x.A7 when
#   if RD is -1, and x is 17, 18, 20
#   if RD is +1, and x 11, 13, 14
table_3b_4b = [
    (0xD,0x2),  # D.x.0
    (0x9,0x9),  # D.x.1
    (0xA,0xA),  # D.x.2
    (0x3,0xC),  # D.x.3
    (0xB,0x4),  # D.x.4
    (0x5,0x5),  # D.x.5
    (0x6,0x6),  # D.x.6
    (0x7,0x8),  # D.x.P7
    (0xE,0x1),  # D.x.A7
    ]

# 10-bit sync to use for RD==-1, RD==+1:
sync = (0x17C,0x283)

# (sync,updated rd) = encode_sync_8b10b(rd)
def encode_sync_8b10b(rd):
    if rd == -1:
        return (sync[0],1)
    else:
        return (sync[1],-1)

# (10b,updated rd) = encode_8b_10b(8b,rd)
def encode_data_8b10b(ch,rd):
    # encode low-order 6 bits
    x = ch & 0x1F
    x_6b = table_5b_6b[x]
    if rd == -1:
        xcode = x_6b[0]
        if x_6b[0] != x_6b[1]: rd = 1
    else:   # rd == 1
        xcode = x_6b[1]
        if x_6b[0] != x_6b[1]: rd = -1

    # encode high-order 3 bits
    y = (ch >> 5) & 0x7
    y_4b = table_3b_4b[y]
    if rd == -1:
        if y == 7 and x in (17,18,20):
            # use D.x.A7
            y_4b = table_3b_4b[8]
        ycode = y_4b[0]
        if y_4b[0] != y_4b[0]: rd = 1
    else:  # rd == 1
        if y == 7 and x in (11,13,14):
            # use D.x.A7
            y_4b = table_3b_4b[8]
        ycode = y_4b[1]
        if y_4b[0] != y_4b[0]: rd = -1

    return((ycode << 6) + xcode,rd)

# encode string with 8b/10b inserting syncs every so often
def encode_string_8b10b(s,sync_interval = 16):
    result = [0,1,1]*5   # start with some garbage
    count = 0
    rd = -1   # running disparity starts at -1
    for ch in s:
        if (count % sync_interval) == 0:
            sync,rd = encode_sync_8b10b(rd)
            result.extend(int_to_bits(sync,10))
        code,rd = encode_data_8b10b(ord(ch),rd)
        result.extend(int_to_bits(code,10))
        count += 1
    result += [0]*5   # end with some zeros
    return result

# build the reverse lookup table by encoding each character
# with both possible running disparities and then filling
# in the appropriate entries
table_10b_8b = [None] * 1024
for ch in xrange(256):
    for rd in (-1,1):
        code = encode_data_8b10b(ch,rd)[0]
        #print "0x%x (D.%02x.%x) encodes as 0x%03x when rd=%d" % (ch,ch & 0x1F, ch >> 5,code,rd)
        assert table_10b_8b[code] is None or table_10b_8b[code]==ch,\
               "Oops, duplicate entry in table_10b_8b"
        table_10b_8b[code] = ch

long_message = """
Fourscore and seven years ago our fathers brought forth on this
continent a new nation, conceived in liberty, and dedicated to the
proposition that all men are created equal.

Now we are engaged in a great civil war, testing whether that nation,
or any nation, so conceived and so dedicated, can long endure. We are
met on a great battle-field of that war. We have come to dedicate a
portion of that field as a final resting place for those who here
gave their lives that that nation might live. It is altogether fitting
and proper that we should do this.

But, in a larger sense, we cannot dedicate... we cannot
consecrate... we cannot hallow... this ground. The brave men, living
and dead, who struggled here, have consecrated it far above our poor
power to add or detract. The world will little note nor long remember
what we say here, but it can never forget what they did here. It is
for us, the living, rather, to be dedicated here to the unfinished work
which they who fought here have thus far so nobly advanced. It is
rather for us to be here dedicated to the great task remaining before
us... that from these honored dead we take increased devotion to that
cause for which they gave the last full measure of devotion; that we
here highly resolve that these dead shall not have died in vain; that
this nation, under God, shall have a new birth of freedom; and that
government of the people, by the people, for the people, shall not
perish from the earth.

November 19, 1863
"""

# tester for task 1
def task1_test(f):
    "testjig for Lab #1, Task #1 -- expects your plotting function as an argument"
    data = transmit(encode_string('hi there'))
    f(data)

# tester for task 2
def task2_test(f,message):
    "testjig for Lab #1, Task #2 -- expects your receive function and a string as arguments"
    data = transmit(encode_string(message))
    result = f(data)
    if result != message:
        print 'expected "%s", got "%s"' % (message,result)
    else:
        print 'received message is "%s"' % result

# tester for task 3
def task3_test(f,message):
    "testjig for Lab #1, Task #3 -- expects your receive function and a string as arguments"
    data = transmit(encode_string_8b10b(message))
    result = f(data)
    if result != message:
        print 'expected "%s", got "%s"' % (message,result)
    else:
        print 'received message is "%s"' % result

__all__ = ['task1_test','task2_test','task3_test',
           'bits_to_int','table_10b_8b','long_message']