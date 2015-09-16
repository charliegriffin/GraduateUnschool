# lab1_1.py -- template for your Task #1 design file
import matplotlib.pyplot as p
import lab1

# if you're using iPython, the following call enable matplotlib's
# interactive mode so plots will appear immediately -- useful
# when experimenting...
p.ion()

def plot_data(data):
	# takes a numpy array
	# plots it as a new figure using routines from matplotlib.pyplot
	p.plot(data)
	p.title('Receiver data')
	p.xlabel('Sample Number')
	p.ylabel('Voltage')
	p.grid(True)
	p.show
	p.savefig('receiverData.pdf')
	# I chose to use a line since it looks like the picture on the assignment page
	return None

# testing code.  Do it this way so we can import this file
# and use its functions without also running the test code.
if __name__ == '__main__':
    # supply some test data to plot_data...
    lab1.task1_test(plot_data)
    
