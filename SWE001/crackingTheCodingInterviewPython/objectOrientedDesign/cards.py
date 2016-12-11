import random

''' 8.1 Design the data structures for a generic deck of cards.
Explain how you would subclass the data structures to implement
blackjack.'''

# Implementing data structures for a generic deck of cards

class Card:
    def __init__(self,suit,value):
        self.suit = suit
        self.value = value
    def __str__(self):
        return str(self.value) + " of " + self.suit
    def numericalValue(self):
        if type(self.value) == int:
            return self.value
        elif self.value == "Jack" or self.value == "Queen" or self.value == "King":
            return 10
        elif self.value == "Ace":
            return [1,11]    # Aces assume two potential values in BJ

        
class Deck:  # I am assuming that the deck of cards is not shuffled
    def __init__(self):
        self.cards = []
        for suit in ["Hearts", "Spades", "Diamonds", "Clubs"]:
            for value in range(1,10) + ["Jack", "Queen", "King", "Ace"]:
                self.cards.append(Card(suit,value))
    def __str__(self):
        cardList = []
        for card in self.cards:
            cardList.append(str(card))
        return str(cardList)

                
# Implementing/describing the data structures for a game of blackjack

def shuffleDeck(deck):
    random.shuffle(deck.cards)
    
# I would add a method to add and remove cards from a deck (as they
# are delt to players hands). Removing cards as they are delt, and 
# replacing at the bottom of the deck after they are discarded.
# The deck is shuffled between rounds, and the rules of blackjack
# are integrated into a blackjack function.

# test code
    
d = Deck()
print d
shuffleDeck(d)
print d
for card in d.cards:
    print card.numericalValue()
