import matplotlib.pyplot as p
import math,random
import numpy as np

def channel_noise(low,high,nsamples):
	return np.sum(np.random.uniform(low,high,nsamples))

def sampleChannelNoise(nTrials,low=-0.001,high=0.001,nsamples=100000):
	return np.array([channel_noise(low,high,nsamples) for n in xrange(10000)])
	
def plotHisto(nBins=100,nTrials=10000):
	p.hist(sampleChannelNoise(nTrials),bins=nBins)
	p.title('Channel Noise Simulation')
	p.xlabel('Voltage Noise (Volts)')
	p.ylabel('Number of Occurances')
	p.grid(True)
	p.savefig('noiseSimulation.png')
	
	

if __name__ == '__main__':
	plotHisto()