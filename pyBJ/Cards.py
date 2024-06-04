import numpy as np

from Player import *

class Card:

    def __init__(self):

        self.symbol = ''
        self.val = 0

        self.suit = np.asarray(['A','K','Q','J','10','9','8','7','6','5','4','3','2'])
        self.cardDict = {'A': 1, 'K': 10,'Q': 10,'J': 10,'10': 10,'9': 9,'8': 8,'7': 7,'6': 6,'5': 5,'4': 4,'3': 3,'2': 2}

class Hand(Card):

    def __init__(self):
        super().__init__()
        self.value = 0
        self.cards = [ ]
        self.soft = 0
        self.completed = 0
        self.bust = 0
        self.bj = 0
        self.bet = 0
        self.resolved = 0
        self.split = 0

    def placeBet(self, player, betSize):

        self.bet = betSize
        player.bankroll -= betSize

    def evaluate(self):
        
        value = 0
        self.soft = 0
        
        for c,cardSym in enumerate(self.cards):
            value += self.cardDict[cardSym]

        for i,card in enumerate(self.cards):
            if card == 'A':
                if value <= 11:
                    self.soft = 1
                    value += 10

        self.value = value
         
class Shoe(Card):

    def __init__(self, nDecks = 1):
        super().__init__()

        self.absCount = 0
        self.relativeCount = 0
        
        self.nDecks = nDecks
        
        self.deckSymbols = np.array([])

    def __len__(self):
        return len(self.deckSymbols)

    def draw(self):

        # HACK: This allows the drawing of a card that is already in play... NOT GOOD.
        # if len(self.deckSymbols) == 0:
        #     self.shuffle()

        '''
        # This way of doing it will draw a card from a random point in a ordered deck

        drawnCard = np.random.choice(self.deckSymbols, 1)[0]
        self.deckSymbols = np.delete(self.deckSymbols, np.where(self.deckSymbols == drawnCard)[0][0])
        return drawnCard
        '''
        
        # This way of doing it will draw the top card from a shuffle deck (more realistic ?)
        drawnCard = self.deckSymbols[0]
        self.deckSymbols = self.deckSymbols[1:]
        return drawnCard
        
    def shuffle(self):
        
        # TODO: Shuffle only the cards that are not in play. If we need to shuffle mid-hand (long hand) then this doesnt work...

        self.deckSymbols = np.array([])
        for i in range(4 * self.nDecks):
            self.deckSymbols = np.concatenate((self.deckSymbols,self.suit))

        # adding this shuffle so that we can just take the top card
        np.random.shuffle(self.deckSymbols)


