from rollingHash import *

def subsequenceHashes(seq, k):
    # given a sequence, return all k-length subsequences and their hashes
    position = 0
    subseq = seq[:k]
    roller = RollingHash(subseq)
    yield (roller.hash(),(subseq,position))
    for i in range(len(seq)-k):
        position += 1
        prev = subseq[0]
        next = seq[i+k]
        roller.slide(subseq[0],next)
        subseq = subseq[1:] + next
        yield (roller.hash(),(subseq,position))

seq = 'ABCDABCDABCDABCDABCDABCD'
# subsequenceHashes(seq,4)
# subsequenceHashes(seq,2)
hashes = subsequenceHashes(seq,12)
for hash, (subseq,pos) in hashes:
	print hash, subseq, pos