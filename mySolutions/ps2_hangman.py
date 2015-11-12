# Problem Set 2
# Name: Charlie Griffin
# Time = 2:40

# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
# time = 2:40
import random
import string

alphabet = "abcdefghijklmnopqrstuvwxyz"

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!

def guess(word, guessed_letters):		#prompts a guess and checks to see if it is valid
	letter = str.lower(raw_input("Please guess a letter:"))
	for char in guessed_letters:
		if letter == char:		#this letter was previously guessed
			print "Oops you already guessed this letter.  Try again."
			letter = guess(word,guessed_letters)
			return letter
	for char in alphabet: 		#checks to see that an appropriate input was made
		if letter == char:
			return letter
		elif char == 'z': #a letter was not entered
			print letter + " is not a valid guess"
			letter = guess(word,guessed_letters)
			return letter
	
def update_available_letters(available_letters,letter):  #updates the list of available letters
	list = ""
	for char in available_letters:  #constructs new list of available letters
		if char == letter:
			list = list #do nothing
		else:
			list = list + char
	available_letters = list
	return list
	
def update_guessed_word(guessed_word, letter, word): #updates the word the user has guessed so far
	new_guessed_word = ""
	for i in range(len(word)):
		if letter == word[i]:
			new_guessed_word = new_guessed_word + letter
		else:
			new_guessed_word = new_guessed_word + guessed_word[i]
	return new_guessed_word

def hangman():		#interactive 1 player hangman game vs computer
	print "Welcome to the game, Hangman!"
	word = choose_word(wordlist)
	available_letters = alphabet
	guesses = 8
	print "I am thinking of a word that is " + str(len(word)) + " letters long."
	
	guessed_word = ""
	for i in range(len(word)):		#constructs a blank guessed word, to be updated as letters are guessed
		guessed_word += "_"
		
	guessed_letters = "" 			#string of letters already guessed
	
	while (guesses > 0) and guessed_word!=word:
		print "------------"
		print "You have " + str(guesses) + " guesses remaining"
		print "Available letters: " + available_letters
		print "You have already guessed: " + guessed_letters
		letter = guess(word,guessed_letters)
		guessed_letters += letter
		for i in range(len(word)):
			if letter == word[i]:
				print "Good Guess!"
				break
			elif i == len(word)-1: 	#letter is not in the word
				print "Bad Guess!"
				guesses -= 1 		#removes a remaining guess
		available_letters = update_available_letters(available_letters, letter)
		guessed_word = update_guessed_word(guessed_word, letter, word)
		print guessed_word
	
	print"------------"
	if guessed_word == word:
		print "Congratulations, you won!"
	else:
		print "Sorry, you lost!"



hangman()
