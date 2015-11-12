# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
#	time spent = 3:30

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the sum of the points for letters
	in the word multiplied by the length of the word, plus 50
	points if all n letters are used on the first go.

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # TO DO...
    score = 0
    for char in word:
    	score = score + SCRABBLE_LETTER_VALUES[char]	#sum of the letter scores
    score = score*len(word)
    if len(word) == n:								#bonus for using every letter
    		score = score + 50
    else:
    		score = score
    return score
    
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
	"""
	Assumes that 'hand' has all the letters in word.
	In other words, this assumes that however many times
	a letter appears in 'word', 'hand' has at least as
	many of that letter in it. 
	
	Updates the hand: uses up the letters in the given word
	and returns the new hand, without those letters in it.
	
	Has no side effects: does not modify hand.
	
	word: string
	hand: dictionary (string -> int)    
	returns: dictionary (string -> int)
	"""
	new_hand = {}
	for letter in hand.keys():
		new_hand[letter] = hand[letter]		#assign new variable to avoid mutation
	for letter in word:				#takes a value away for each letter if its in the word
		new_hand[letter] -= 1
	for letter in new_hand.keys():	#if the value for a letter is zero it is removed
		if new_hand[letter] == 0:	#from the dictionary
			del new_hand[letter]
	return new_hand
#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    new_hand = {}
    for letter in hand.keys():
		new_hand[letter] = hand[letter]	
    if word not in word_list:
    	return False					# word not in word list
    else:
    	for letter in word:				
    		if letter in hand.keys():
    			new_hand[letter] -= 1
    		else:
    			return False			# letter not in hand
    	for letter in new_hand.keys():
    		if new_hand[letter] < 0:
    			return False			# not enough letters in hand to make the word
    return True							# passed all the tests, word is valid

def calculate_handlen(hand):
    handlen = 0
    for v in hand.values():
        handlen += v
    return handlen

#
# Problem #4: Playing a hand
#

def play_hand(hand, word_list):
	"""
    Allows the user to play the given hand, as follows:
	
    * The hand is displayed.
	
    * The user may input a word.
	
    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.
	
    * When a valid word is entered, it uses up letters from the hand.
	
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
	
	* The sum of the word scores is displayed when the hand finishes.
	
	* The hand finishes when there are no more unused letters.
	  The user can also finish playing the hand by inputing a single
	  period (the string '.') instead of a word.
	
	  hand: dictionary (string -> int)
	  word_list: list of lowercase strings
	  
	"""
	total_score = 0
	while True:
		print ""
		print "Current Hand: ",
		display_hand(hand)
		word = raw_input('Enter word, or a "." to indicate that you are finished: ')
		if word == ".":
			break
		if is_valid_word(word,hand,word_list) == True:
			score = get_word_score(word,HAND_SIZE)
			total_score += score
			print '"' + word + '"' + " earned " + str(score) + ' points. Total: ' + str(total_score) + ' points'
			hand = update_hand(hand,word)
		else:
			print "Invalid word, please try again."
		if hand == {}:
			break
	print "Total Score: " + str(total_score) + " points."
    
    
    # TO DO ...

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
	print "Welcome to the 6.00 wordgame"
	choice = ''
	hand = deal_hand(HAND_SIZE)
	print choice
	while choice != "e":
		choice = raw_input("Enter 'n' for a new hand\n'r' to play the last hand\nor 'e' to exit the game\n:")
		if choice == "n":
			hand = deal_hand(HAND_SIZE)
		elif choice == "r":
			hand = hand
		play_hand(hand,word_list)


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
