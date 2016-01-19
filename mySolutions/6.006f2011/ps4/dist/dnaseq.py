#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###
# I wrote this myself, but later found the RollingHash in the dnaseqlib, and 
# decided to use that so my results are as consistent with the tests as possible
# class RollingHash:
#     def __init__(self,s):
#         self.hashbase = 4 # since there are 4 dna letters
#         self.seqlen = len(s)
#         n = self.seqlen - 1
#         h = 0
#         for c in s:
#             h += ord(c) * (self.hashbase ** n)
#             n -= 1
#         self.curhash = h
#     
#     def hash(self):
#         return self.curhash
#         
#     def slide(self,prev,next):
#         self.curhash = self.hashbase*self.curhash + ord(next)
#         self.curhash -= (self.hashbase**self.seqlen)*ord(prev)
#         return self.curhash


# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.dict = {}
        for key, value in pairs:
			self.put(key,value)


    # Associates the value v with the key k.
    def put(self, k, v):
        if k in self.dict.keys():
            self.dict[k].append(v)
        else:
            self.dict[k] = [v]
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if k in self.dict.keys():
            return self.dict[k]
        else:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    try:
        position = 0
        subseq = ''
        for i in range(k):
            subseq += seq.next()
        roller = RollingHash(subseq)
        yield (roller.current_hash(),(subseq,position))
        while True:
            position += 1
            next = seq.next()
            roller.slide(subseq[0],next)
            subseq = subseq[1:] + next
            yield (roller.current_hash(),(subseq,position))
    except StopIteration:
        return

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    try:
        position = 0
        while True:
            subseq = ''
            for i in range(k):
                subseq += seq.next()
            h = RollingHash(subseq)
            yield (h.current_hash(),(subseq,position))
            for i in range(m-k):	# moves the start m values to the right
                seq.next()
            position += m
    except StopIteration:
        return

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    print 'building table ...'
    subSeqDict = Multidict(pairs=intervalSubsequenceHashes(a,k,m))
    print 'table complete'
    print 'comparing hash values...'
    for hash, (seq,pos) in subsequenceHashes(b,k):
        for asubseq, apos in subSeqDict.get(hash):
            if asubseq != seq:
                continue
            yield (apos,pos)
    print 'finished finding matches'
    return

def testMultiDict():
    md = Multidict(pairs=[(1,'a'),(2,'b')])
    md.put(1,'z')
    md.put(3,'c')
    print md.get(1)
    print md.get(7)
    print md.dict
    

if __name__ == '__main__':
#     testGetExact()
    
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
