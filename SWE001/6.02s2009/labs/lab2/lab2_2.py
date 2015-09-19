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
    print name
    message = [1,0,1,0,1,0,1,0]
    inp = lab2_1.transmit(message,10,100)
    out = channel(inp)
    p.subplot(211)
    p.plot(inp)
    p.subplot(212)
    p.plot(out)
    p.savefig(name+'.png')
    p.clf()

if __name__ == '__main__':
    # try out our two channels
    test_channel(lab2.channel1)
    test_channel(lab2.channel2)

    # interact with plots before exiting.  p.show() returns
    # after all plot windows have been closed by the user.
    # Not needed if using ipython
    p.show()  