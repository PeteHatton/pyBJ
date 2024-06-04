import numpy as np
import copy

from Player import *
from Cards import *
from Utilities import *

class Action:
    def __init__(self):
        self.name = ''

    def announce(self):
        log(__name__, self.name, 1, 1)

class Hit(Action):

    def __init__(self):
        super().__init__()
        self.name = 'HIT'
    
    def run(self, shoe : Shoe, person : Player, hand: Hand):
        hand.cards.append(shoe.draw())
        return 0

class DD(Action):
    
    def __init__(self):
        super().__init__()
        self.name = 'DOUBLE DOWN'
    
    def run(self, shoe : Shoe, person : Player, hand: Hand):
        person.bankroll -= hand.bet
        hand.bet *= 2
        hand.cards.append(shoe.draw())
        return 1
    
class Split(Action):
     
    def __init__(self):
        super().__init__()
        self.name = 'SPLIT'

    def run(self, shoe : Shoe, person : Player, hand: Hand):
        
        newHand = Hand()
        newHand.placeBet(person, hand.bet)

        hand.split = 1
        newHand.split = 1

        newHand.cards.append(hand.cards.pop(1))
        hand.cards.append(shoe.draw())
        newHand.cards.append(shoe.draw())
    
        person.hand.append(newHand)
        
        # this controls that we only get 1 card on split A's
        if hand.cards[0] == 'A':
            newHand.completed = 1
            return 1
        else:
            return 0

class Stand(Action):

    def __init__(self):
        super().__init__()
        self.name = 'STAND'

    def run(self, shoe : Shoe, person : Player, hand: Hand):
        return 1 
    
class Bust(Action):
    
    def __init__(self):
        super().__init__()
        self.name = 'BUST!'

    def run(self, shoe : Shoe, person : Player, hand: Hand):
        hand.bust = 1
        return 1
           