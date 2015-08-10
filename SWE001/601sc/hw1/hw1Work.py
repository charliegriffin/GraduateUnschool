import pdb
import lib601.sm as sm
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

class Sum(BinaryOp):
    opStr = 'Sum'

class Prod(BinaryOp):
    opStr = 'Prod'

class Quot(BinaryOp):
    opStr = 'Quot'

class Diff(BinaryOp):
    opStr = 'Diff'

class Assign(BinaryOp):
    opStr = 'Assign'
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenize(string):
    tokenList = []
    newToken = ''
    for character in string:
    	if character in seps:
    		tokenList.append(character)
    		if newToken != '':	# adds string made before this char
    			tokenList.append(newToken)
    			newToken = ''
    	elif character == ' ':	# separates spaced strings
    		if newToken !='':
    			tokenList.append(newToken)
    			newToken =''
    	else:
    		newToken += character
#    		print 'newToken = ', newToken
    if newToken != '':		# adds left over string
    	tokenList.append(newToken)
    return tokenList

# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        if numberTok(tokens[index]):	# number
        	return (Number(float(tokens[index])), index + 1)
        elif variableTok(tokens[index]):	# variable
        	return (Variable(str(tokens[index])), index + 1)
        elif tokens[index] == '(':
        	leftTree = parseExp(index + 1)
        	print "leftTree = ", leftTree
        	op = tokens[leftTree[1]]
        	print "op = ", op
        	rightTree = parseExp(leftTree[1]+1)
        	print "rightTree =", rightTree	# everything is working fine, I now need
        									# to figure out what to return
#        	return (parseExp(leftTree op rightTree), rightTree[1])
        else:
        	print tokens[index]  
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')            # prints %, returns user input
        print '%', # your expression here
        print '   env =', env

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession 
        print # your expression here
        print '   env =', env

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')

#testTokenize()
# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))

testParse()
####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
# calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)
