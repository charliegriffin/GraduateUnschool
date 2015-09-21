import matplotlib.pyplot as p
import matplotlib,math,numpy,random

rel_error = 1e-15

# erf,erfc from http://www.digitalmars.com/archives/cplusplus/3634.html (bottom of page)

def erf(x):
    if abs(x) > 2.2:
        # use continued fraction for large arguments
        return 1.0 - erfc(x)
    sum = x
    term = x
    xsqr = x*x
    j = 1
    while True:
        term *= xsqr/j
        sum -= term/(2*j+1)
        j += 1
        term *= xsqr/j
        sum += term/(2*j+1)
        j += 1
        if sum == 0 or abs(term/sum) <= rel_error:
            break
    return (2.0/math.sqrt(math.pi)) * sum

def erfc(x):
    if abs(x) < 2.2:
        # use series when small arguments
        return 1.0 - erf(x)
    if x < 0:
        # continued fraction only valid for x > 0
        return 2.0 - erfc(-x)
    a = 1; b = x            # last two convergent numerators
    c = x; d = x*x + 0.5    # last two convergent denominators
    q1 = a/c; q2 = b/d      # last two convergents (a/c and b/d)
    n = 1.0
    while True:
        a,b = (b,a*n + b*x)
        c,d = (d,c*n + d*x)
        n += 0.5
        q1,q2 = (q2,b/d)
        if abs(q1-q2)/q2 <= rel_error:
            break
    return (1.0/math.sqrt(math.pi))*math.exp(-x*x)*q2

def unit_normal_cdf(x):
    if x < 0:
        return 1 - unit_normal_cdf(-x)
    else:
        return 0.5 + 0.5*erf(x/math.sqrt(2))

# convert digital sample sequence into voltages, upsample, add noise
# result is numpy array
def transmit(seq,vlow=0.0,vhigh=1.0,samples_per_bit=4,ntaps=0,bw=.08,nmag=0.0,nsigma=0.18):
    ndata = len(seq)*samples_per_bit
    samples = [vlow]*ntaps
    vlast = vlow
    for s in seq:
        v = vlow if s == 0 else vhigh
        dv = v - vlast
        for i in xrange(samples_per_bit):
            adjust = (dv*(i+1.1))/float(samples_per_bit) if i < samples_per_bit-1 else dv
            samples.append(adjust + vlast)
        vlast = v
    voltages = numpy.fromiter(samples,dtype=numpy.float)

    if ntaps > 0:
        taps = compute_taps(ntaps,bw)
        start = 3*ntaps/2
        filtered = numpy.convolve(voltages,taps)[start:start+ndata]
    else:
        filtered = voltages

    if nmag > 0:
        noise = nmag*numpy.random.normal(0,nsigma,ndata)
        """
        n3 = noise[3::4]
        f3 = filtered[3::4]
        print ndata,numpy.sum(f3 < 0.5),numpy.sum(f3 > 0.5),numpy.sum(numpy.abs(n3) > .5)
        err0 = numpy.sum(numpy.logical_and(f3 < 0.5,n3 > 0.5) * 1)
        err1 = numpy.sum(numpy.logical_and(f3 > 0.5,n3 < -0.5) * 1)
        print "errors for sample 3: ",err0+err1
        """
        return filtered+noise
    else:
        return filtered

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

def plot_eye_diagram(samples,samples_per_bit=4):
    p.figure()
    start = 0
    stop = len(samples) - samples_per_bit
    while start < stop:
        p.plot(samples[start:start+2*samples_per_bit+1])
        start += samples_per_bit
    p.title('Eye diagram')
    p.xlabel('Sample number')
    p.ylabel('volts')
    vmin = min(samples)
    vmax = max(samples)
    dv = vmax - vmin
    p.axis([0,2*samples_per_bit,vmin - 0.1*dv,vmax + 0.1*dv])

def plot_sample_histograms(samples,samples_per_bit=4,title='Sample distribution',nbins=100):
    minv = numpy.min(samples)
    maxv = numpy.max(samples)
    bins = numpy.reshape(samples,(-1,samples_per_bit))
    histograms = [numpy.histogram(bins[:,i],bins=nbins,range=(minv,maxv))[0]
                  for i in xrange(samples_per_bit)]
    nsamples = float(len(samples))/samples_per_bit
    maxh = max([max(histograms[i]) for i in xrange(samples_per_bit)])/nsamples
    for i in xrange(samples_per_bit):
        histograms[i] = histograms[i]/nsamples

    y = numpy.arange(minv,maxv,(maxv-minv)/float(nbins))
    p.figure()
    p.subplots_adjust(hspace=0.6)
    for i in xrange(samples_per_bit):
        p.subplot(1,samples_per_bit,i+1)
        p.hlines(y,[0],histograms[i],lw=2)
        p.title(str(i))
        p.axis([0,maxh,-.5,1.5])

message = [random.randint(0,1) for i in xrange(100000)]
samples_per_bit = 4
channel_data = transmit(message,samples_per_bit=samples_per_bit)
noisy_channel_data = transmit(message,samples_per_bit=samples_per_bit,nmag=1.0)

__all__ = ['unit_normal_cdf','transmit','message','channel_data','noisy_channel_data','plot_sample_histograms']

if __name__ == '__main__':
    plot_eye_diagram(channel_data[:100])
    plot_sample_histograms(channel_data)
    plot_sample_histograms(noisy_channel_data)