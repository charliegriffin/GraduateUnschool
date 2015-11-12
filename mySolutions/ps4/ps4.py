# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
# Problem Set 4
# Name : Charles Griffin
# time = 7:00 

import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):	# builds a dictionary for translating letters to encoded letters
	
	lower_alphabet = ' ' + string.ascii_lowercase
	upper_alphabet = ' ' + string.ascii_uppercase
	
	shifted_lower_alphabet = lower_alphabet[shift:] + lower_alphabet[:shift]
	shifted_upper_alphabet = upper_alphabet[shift:] + upper_alphabet[:shift]    
	coder = {}

	for i in range(len(upper_alphabet)):
		coder[upper_alphabet[i]] = shifted_upper_alphabet[i]
		coder[lower_alphabet[i]] = shifted_lower_alphabet[i]
	return coder


def build_encoder(shift):
	assert isinstance(shift, int),"Shift is not an integer"
	assert 0 <= shift < 27 ,"Shift is not between 0 and 26"
	return build_coder(shift)
	
def build_decoder(shift):
	"""
	Returns a dict that can be used to decode an encrypted text. For example, you
	could decrypt an encrypted text by calling the following commands
	>>>encoder = build_encoder(shift)
	>>>encrypted_text = apply_coder(plain_text, encoder)
	>>>decrypted_text = apply_coder(plain_text, decoder)
	
	The cipher is defined by the shift value. Ignores non-letter characters
	like punctuation and numbers.
	
	shift: 0 <= int < 27
	returns: dict
	
	Example:
	>>> build_decoder(3)
	{' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
	'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
	'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
	'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
	'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
	'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
	'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
	'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
	(The order of the key-value pairs may be different.)
	
	HINT : Use build_coder.
	"""
	return build_coder(-1*shift)
 	

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    new_text = ''
    for letter in text:
    	if letter in coder:
    		letter = coder[letter]
    	new_text += letter
    return new_text


def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    return apply_coder(text, build_encoder(shift))
   
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
	"""
	Decrypts the encoded text and returns the plaintext.
	
	text: string
	returns: 0 <= int 27
	
	Example:
	>>> s = apply_coder('Hello, world!', build_encoder(8))
	>>> s
	'Pmttw,hdwztl!'
	>>> find_best_shift(wordlist, s) returns
	8
	>>> apply_coder(s, build_decoder(8)) returns
	'Hello, world!'
	"""
	max_words = 0
	best_shift = 0
	
	for shift in range(27):		# tests all possible shifts
		number_of_words = 0		
		decoded_text = apply_coder(text, build_decoder(shift))
		decoded_text = decoded_text.split()		# splits text into words
		for word in decoded_text:		# checks each word's validity
			if (is_word(wordlist,word) == True):
				number_of_words += 1
		if number_of_words > max_words:	# the shift that returns the most valid word is returned as correct
			max_words = number_of_words	
			best_shift = shift
		if number_of_words == len(decoded_text): 	# if every word is valid the key is correct
			return best_shift
	return best_shift
	
   
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
	"""
	Applies a sequence of shifts to an input text.
	
	text: A string to apply the Ceasar shifts to 
	shifts: A list of tuples containing the location each shift should
	begin and the shift offset. Each tuple is of the form (location,
	shift) The shifts are layered: each one is applied from its
	starting position all the way through the end of the string.  
	returns: text after applying the shifts to the appropriate
	positions
	
	Example:
	>>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
	'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
	"""
	for pair in shifts:
		start_position = pair[0]
		shift = pair[1]
		text = text[:start_position] + apply_shift(text[start_position:],shift)
 	return text
#
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
	"""
	Given a scrambled string, returns a shift key that will decode the text to
	words in wordlist, or None if there is no such key.
	
	Hint: Make use of the recursive function
	find_best_shifts_rec(wordlist, text, start)
	
	wordlist: list of words
	text: scambled text to try to find the words for
	returns: list of tuples.  each tuple is (position in text, amount of shift)
	
	Examples:
	>>> s = random_scrambled(wordlist, 3)
	>>> s
	'eqorqukvqtbmultiform wyy ion'
	>>> shifts = find_best_shifts(wordlist, s)
	>>> shifts
	[(0, 25), (11, 2), (21, 5)]
	>>> apply_shifts(s, shifts)
	'compositor multiform accents'
	>>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
	>>> s
	'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
	>>> shifts = find_best_shifts(wordlist, s)
	>>> print apply_shifts(s, shifts)
	Do Androids Dream of Electric Sheep?
	"""

def find_best_shifts_rec(wordlist, text, start):
	"""
	Given a scrambled string and a starting position from which
	to decode, returns a shift key that will decode the text to
	words in wordlist, or None if there is no such key.	
	
	Hint: You will find this function much easier to implement
	if you use recursion.
	
	wordlist: list of words
	text: scambled text to try to find the words for
	start: where to start looking at shifts
	returns: list of tuples.  each tuple is (position in text, amount of shift)
	"""
	if start >= len(text):	# We have reached the end of the text.
		return []			# Base case, make position_shift an empty list
	for shift in range(27):	# Iterate over every possible shift looking for words
		decoded_text = text[:start] + apply_coder(text[start:], build_encoder(shift))
		if decoded_text[start] == ' ':	# double space
			words = decoded_text[start:]
		else :
			words = decoded_text[start:].split()
		if is_word(wordlist,words[0]):	# We found a word, now we run the next word
			next_start = start + len(words[0]) + 1
			start_shift = find_best_shifts_rec(wordlist,decoded_text,next_start)
			if start_shift != None:
				position_shift = start_shift
				if shift != 0:
					position_shift = [(start,shift),] + position_shift
				break
		if shift == 26:		# There were no valid words found, we made a wrong shift last time
			return None		# Go out so we can correct the wrong shift
	return position_shift


def decrypt_fable():
	"""
	Using the methods you created in this problem set,
	decrypt the fable given by the function get_fable_string().
	Once you decrypt the message, be sure to include as a comment
	at the end of this problem set how the fable relates to your
	education at MIT.
	
	returns: string - fable in plain text
	"""
	fable = get_fable_string()
	shifts = find_best_shifts_rec(wordlist,fable,0)
	return apply_shifts(fable,shifts)
	# The story is important because it tells us we need to write down our procedure so people can reproduce our results.


	
#What is the moral of the story?
#
#
#
#
#

#text = "Do Androids Dream of Electric Sheep?"
#shifts = [(0,6), (3, 18), (12, 16)]
#text = apply_shifts(text,shifts)
#text = random_scrambled(wordlist,100)
#print text
#shifts = find_best_shifts_rec(wordlist,text,0)
#print apply_shifts(text,shifts)
print decrypt_fable()