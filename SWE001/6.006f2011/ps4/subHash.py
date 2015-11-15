from rollingHash import *

def subsequenceHashes(seq, k):
    # given a sequence, return all k-length subsequences and their hashes
    hashes = []
    subseq = seq[:k]
    roller = RollingHash(subseq)
    yield (subseq,roller.hash())
    for i in range(len(seq)-k):
        prev = subseq[0]
        next = seq[i+k]
        roller.slide(subseq[0],next)
        subseq = subseq[1:] + next
        yield (subseq,roller.hash())

seq = 'ABCDABCDABCDABCDABCDABCD'
# subsequenceHashes(seq,4)
# subsequenceHashes(seq,2)
hashes = subsequenceHashes(seq,12)
for subseq, hash in hashes:
	print subseq, hash