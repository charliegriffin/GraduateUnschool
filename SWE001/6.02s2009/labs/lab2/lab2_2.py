# template for Lab #2, Task #2
import matplotlib.pyplot as p
import lab2
import lab2_1

# turn on interactive mode, useful if we're using ipython
p.ion()  

def test_channel(channel):
    """
    create a test waveform and plot both it and the output of
    passing the waveform through the channel.
    """
    name = channel.__name__
    message = [1,0,1,0,1,0,1,0]
    inp = lab2_1.transmit(message,10,100)
    out = channel(inp)
    upper = max(max(inp),max(out))
    lower = min(min(inp),min(out))
    upper = upper + abs(upper)*0.1		# leave some space at the edges, unless that edge is 0
    lower = lower - abs(lower)*0.1
    
    p.figure()
    p.suptitle(name,fontsize=20,fontweight='bold')
    p.subplot(211)
    p.axis([0,len(inp),lower,upper])	# custom axis scaling
    p.plot(inp,'g-')
    p.title('Input')
    p.grid(True)
    p.ylabel('Voltage')
    p.subplot(212)
    p.axis([0,len(inp),lower,upper])	# make the axes the same
    p.plot(out,'b-')
    p.title('Output')
    p.grid(True)
    p.ylabel('Voltage')
    p.xlabel('Sample Number')
    p.savefig(name+'.png')
    p.clf()								# clears the figure so we can start blank again

if __name__ == '__main__':
    # try out our two channels
    test_channel(lab2.channel1)
    test_channel(lab2.channel2)

    # interact with plots before exiting.  p.show() returns
    # after all plot windows have been closed by the user.
    # Not needed if using ipython
    p.show()  