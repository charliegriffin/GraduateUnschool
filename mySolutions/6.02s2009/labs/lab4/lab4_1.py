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
        stuffedBit = [1,1,1,1,1,1,1]
        indexesToUnstuff = []
        for index in range(len(block)-7): # find the locations of the stuffed bits
        	if block[index:index+7] == stuffedBit:
        		indexesToUnstuff.append(index+7)
        for i in range(len(indexesToUnstuff)):	# remove the stuffed bits
        	del block[indexesToUnstuff[i]]
        	if i == len(indexesToUnstuff) - 1:
        		break
        	else:
				for j in range(i,len(indexesToUnstuff)):
					indexesToUnstuff[j] -= 1		# update the indexes to reflect the changes we made

		# now all blocks are 15*16 in length
        # now block should have exactly 15*16 elements.
        # use lab4.interleave to deinterleave the block.
        dBlock = lab4.interleave(block,16)
        for num in xrange(len(dBlock)/15):
        	message.append(lab4.bin2char(dBlock[num*15:(num*15)+8]))
    lab4.printmsg(message)

if __name__ == '__main__':
    decode(lab4.message)