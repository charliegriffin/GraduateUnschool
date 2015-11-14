# given two strings s & t does s occur as a substring of t?

# based off p.993 of the text
# I played around with this working implementation before inserting
# it in the dna code
def rabinKarpMatcher(text,pattern,d,q):
	n = len(text)
	m = len(pattern)
	h = pow(d,m-1)%q
	p = 0
	t = 0
	result = []
	for i in range(m): # preprocessing
		p = (d*p+ord(pattern[i]))%q
		t = (d*t+ord(text[i]))%q
	for s in range(n-m+1):
		if p == t:	# check each character
			match = True
			for i in range(m):
				if pattern[i] != text[s+i]:
					match = False
					break
			if match:
				result = result + [s]
		if s < n-m:
			t = (t-h*ord(text[s]))%q # remove letter s
			t = (t*d+ord(text[s+m]))%q # add letter s+m
			t = (t+q)%q #make sure that t >= 0
	return result

print rabinKarpMatcher("3141592653589793","26",267,11)