import random
# based off of chapter 6 of Introduction to Algorithms: 3rd Edition
inf = 200


class MinHeap:
	def __init__(self,array):
		#heap is initially empty
		self.heap = []
		self.A = array
		self.heapSize = len(array)
		self.buildMinHeap()
		
	def isMinHeap(self):
		#tests min-heap property
		for i in range(1,len(self.A)):
			if self.A[self.parent(i)] > self.A[i]:
				return False
		return True

	def parent(self,i):
		return int(i/2)
	
	def left(self,i):
		return 2*i
		
	def right(self,i):
		return 2*i + 1
		
	def minHeapify(self,i):
		l = self.left(i)
		r = self.right(i)
		if l <= self.heapSize-1 and self.A[l] < self.A[i]:
			smallest = l
		else: smallest = i
		if r <= self.heapSize-1 and self.A[r] < self.A[smallest]:
			smallest = r
		if smallest != i:
			temp = self.A[i]
			self.A[i] = self.A[smallest]
			self.A[smallest] = temp
			self.minHeapify(smallest)
			
	def buildMinHeap(self):
		self.heapSize = len(self.A)
		for i in range((int(len(self.A)/2))-1,-1,-1):
			self.minHeapify(i)
			
	def minimum(self):
		return self.A[0]
		
	def extractMin(self):
		if self.heapSize < 1:
			raise ValueError('heap undeflow')
		min = self.A[0]
		self.A[0] = self.A[self.heapSize-1]
		self.A = self.A[:-1]
		self.heapSize = self.heapSize - 1
		self.minHeapify(0)
		return min
		
	def decreaseKey(self,i,key):
		if key > self.A[i]:
			raise valueError('new key is larger than current key')
		self.A[i] = key
		while(i > 0 and self.A[self.parent(i)] > self.A[i]):
			temp = self.A[i]
			self.A[i] = self.A[self.parent(i)]
			self.A[self.parent(i)] = temp
			i = self.parent(i)
	
	def minHeapInsert(self,key):
		self.heapSize = self.heapSize + 1
		self.A.append(inf)
		self.decreaseKey(self.heapSize-1,key)
			
def testHeap():
	A = [4,3,1,2]
	heap = MinHeap(A)
	print heap.isMinHeap(), '\t\t\t:should be True'
	print heap.A
	B = []
	for i in range(10):
		B.append(int(100*random.random()))
	print B
	heap = MinHeap(B)
	print 'heapsize = ',heap.heapSize
	print heap.isMinHeap(), '\t\t\t:should be True'
	print heap.extractMin()
	print heap.isMinHeap()
	print heap.A
	print 'heapsize = ', heap.heapSize
	print 'inserting 40 into the heap'
	heap.minHeapInsert(40)
	print heap.isMinHeap(), '\t\t\t:should be True'
	print heap.A
	print heap.minimum(), '\t\t\t:should be -1'
	print len(heap.A), heap.heapSize
	heap.extractMin()
	print len(heap.A), heap.heapSize
	print heap.A
	
testHeap()