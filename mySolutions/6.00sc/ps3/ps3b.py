from ps3a import *
import time
from perm import *


#	time = 1:35
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
	"""
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.
	
	hand: dictionary (string -> int)
	word_list: list (string)
	"""
	words = get_valid_words(hand, word_list)
	best_word = get_best_word(words)
	return best_word

	

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    total_score = 0
    while True:
    	display_hand(hand)
    	word = comp_choose_word(hand,word_list)
    	if word == None:							# the hand is finished
    		print "The computer's turn is over"
    		break
    	elif is_valid_word(word,hand,word_list) == True:	#consistency check
    		score = get_word_score(word,HAND_SIZE)
    		total_score += score
    		print '"' + word + '"' + " earned " + str(score) + ' points. Total: ' + str(total_score) + ' points'
    		hand = update_hand(hand,word)
    	else:										#this should never happen
    		print "something is broken, the computer chose an invalid word"
    		break
    
    return None
    # TO DO ...    
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
	"""Allow the user to play an arbitrary number of hands.
	
	1) Asks the user to input 'n' or 'r' or 'e'.
	* If the user inputs 'n', play a new (random) hand.
	* If the user inputs 'r', play the last hand again.
	* If the user inputs 'e', exit the game.
	* If the user inputs anything else, ask them again.
	
	2) Ask the user to input a 'u' or a 'c'.
	* If the user inputs 'u', let the user play the game as before using play_hand.
	* If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
	* If the user inputs anything else, ask them again.
	
	3) After the computer or user has played the hand, repeat from step 1
	
	word_list: list (string)
	"""
	print "Welcome to the 6.00 wordgame"
	choice = ''
	hand = deal_hand(HAND_SIZE)
	print choice
	while choice != "e":
		player = ''
		choice = raw_input("Enter 'n' for a new hand,\n'r' to play the last hand,\nor 'e' to exit the game\n:")
		if choice == "e":
			break
		elif choice == "n":
			hand = deal_hand(HAND_SIZE)
		elif choice == "r":
			hand = hand
		if player != 'u' and player != 'c':
			player = raw_input("Enter 'u' to play the hand,\nor 'c' to let the computer play the hand\n:")
		if player == 'u':
			play_hand(hand,word_list)
		elif player == 'c':
			comp_play_hand(hand,word_list)

def get_valid_words(hand, word_list):	#return valid words
	words = []						# makes a blank list titled words
	for i in range(1,HAND_SIZE +1):
		words += get_perms(hand,i)	# puts every possible perm into words
	valid_words = []				# creates a new list for valid words
	for word in words:
		if is_valid_word(word, hand, word_list) == True:
			valid_words += [word,]	# adds valid words to valid_words
	return valid_words
	
def get_best_word(words):
	high_score = 0
	for word in words:
		if get_word_score(word,HAND_SIZE) > high_score:
			high_score = get_word_score(word,HAND_SIZE)
			best_word = word
	if high_score == 0:
		best_word = None
	return best_word
		
		

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

play_game(word_list)