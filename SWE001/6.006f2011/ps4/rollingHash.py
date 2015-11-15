# based on the wikipedia article
# H = SUM(c_i*a^(k-i))

class RollingHash:
	def __init__(self,s):
		self.hashbase = 4 # since there are 4 dna letters
		self.seqlen = len(s)
		n = self.seqlen - 1
		h = 0
		for c in s:
			h += ord(c) * self.hashbase ** n
			n -= 1
		self.curhash = h
	
	def hash(self):
		return self.curhash
		
	def slide(self,prev,next):
		self.curhash = self.hashbase*self.curhash + ord(next)
		self.curhash -= pow(self.hashbase,self.seqlen)*ord(prev)
		return self.curhash
		