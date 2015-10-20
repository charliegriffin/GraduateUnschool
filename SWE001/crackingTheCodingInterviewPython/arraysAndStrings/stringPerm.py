# Given two strings, write a method to decide if one is a permutation of the other.

def makeTable(string):
	dict = {}
	for char in string:
		if char in dict.keys():
			dict[char] += 1
		else:
			dict[char] = 0
	return dict

def isPermutation(one,other):
	if len(one) != len(other):
		return False
	d1 = makeTable(one)
	d2 = makeTable(other)
	if d1.keys() != d2.keys():
		return False
	for key in d1.keys():
		if d1[key] != d2[key]:
			return False
	return True
	
print isPermutation('pizza','zzpia')
print isPermutation('pizza','pizzas')
print isPermutation('pizza','salad')
	