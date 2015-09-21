# this is the template for Lab #3, Task #1
import numpy
import lab3

def sample_stats(samples,samples_per_bit=4,vth=0.5):
    # reshape array into samples_per_bit columns by as many
    # rows as we need.  Each column represents one of the
    # sample times in a bit cell.
    bins = numpy.reshape(samples,(-1,samples_per_bit))

    # now compute statistics each column
    for i in xrange(samples_per_bit):
        column = bins[:,i]
        dist = column - vth
        distance = abs(dist)	# absolute value measures distance from threshold
        min_dist = numpy.min(dist)
        avg_dist = numpy.average(dist)
        std_dist = numpy.std(dist)	# stdev of differences
        print "sample %d: min_dist=%6.3f, avg_dist=%6.3f, " \
              "std_dist=%6.3f" % (i,min_dist,avg_dist,std_dist)

if __name__ == '__main__':
    sample_stats(lab3.channel_data)