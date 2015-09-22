# template for Lab #4, Task #1
import lab4
 
def decode(received): 
    message = []
    # find_sync returns a list of bit-stuffed interleaved
    # blocks, each element of the list is itself a list
    # of 0's and 1's that make up that particular block.
    for block in lab4.find_sync(received,lab4.sync):

        # undo the bit-stuffing (remove 0 following seven
        # consecutive 1's)
        ... your code here ...

        # now block should have exactly 15*16 elements.
        # use lab4.interleave to deinterleave the block.
        ... your code here ...

        # for each group of 15 bits in the block, extract
        # the (uncorrected) data bits and use lab4.bin2char
        # to convert them to an ASCII character, which you
        # should append to message
        ... your code here ...

    lab4.printmsg(message)

if __name__ == '__main__':
    decode(lab4.message)