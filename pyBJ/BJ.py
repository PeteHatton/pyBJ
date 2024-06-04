from Player import *
from Cards import *
from Decision import *
from Strategy import *
from Bet import *
from Input import getParams
from Utilities import *


import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class BlackJack:

    def __init__(self, params: InputParams, shoe : Shoe, player: Player, dealer: Player):

        self.shoe = shoe
        self.player = player
        self.dealer = dealer

        self.params = params

        self.runningResults = []
        self.rounds = 0

    def dealGame(self, forcedDealerHand = None, forcedPlayerHand = None):

        '''
        forcedDealerUpCard is a Hand object. When we train a strategy we use this to fix the dealer hand.
        forcedPlayerHand - similar...
        '''

        if not forcedPlayerHand:
        
            pHand = Hand()
            for _ in range(2):
                pHand.cards.append(self.shoe.draw())
        else:
            pHand = forcedPlayerHand
        
        if not forcedDealerHand:

            dHand = Hand()
            dHand.cards.append(self.shoe.draw())
            if self.params.dealerDraws == 'Before':
                dHand.cards.append(self.shoe.draw())
        else:
            dHand = forcedDealerHand

        self.player.hand = [pHand]
        self.dealer.hand = [dHand]
    
    def resolve(self):
        
        for hand in self.player.hand:
            
            # easy cases
            hand.evaluate()
            if hand.bust or hand.value > 21:
                log(__name__,'Player Bust - Dealer Win', 1, 1)
                hand.resolved = 1

            elif hand.bj and not self.dealer.hand[0].bj:
                log(__name__,'Player got BJ', 1, 1)
                self.player.bankroll += (self.params.blackjackPays + 1) * hand.bet
                hand.resolved = 1

            elif self.dealer.hand[0].bj and not hand.bj:
                log(__name__,'Dealer got BJ', 1, 1)
                hand.resolved = 1

            elif self.dealer.hand[0].bust:
                log(__name__,'Dealer Bust - Player Win', 1, 1)
                self.player.bankroll += 2 * hand.bet
                hand.resolved = 1

            # need to evaluate and compare for these cases
            if not hand.resolved:

                hand.evaluate()
                self.dealer.hand[0].evaluate()

                if self.dealer.hand[0].value == hand.value:
                    log(__name__,'Push', 1, 1)
                    self.player.bankroll += hand.bet
                    hand.resolved = 1
                elif self.dealer.hand[0].value > hand.value:
                    log(__name__,'Dealer Win', 1, 1)
                    hand.resolved = 1
                elif self.dealer.hand[0].value < hand.value:
                    log(__name__,'Player Win', 1, 1)
                    self.player.bankroll += 2 * hand.bet
                    hand.resolved = 1

            if not hand.resolved:
                print('ERROR: Unresolved Hand')
                sys.exit(0)
        
    def muck(self):

        cutCardDepth = self.params.deckPenetration # How deep is the cut card in the shoe?
        # if we've gone past cut card then shuffle
        if len(self.shoe) < self.shoe.nDecks * 52 * (1 - cutCardDepth):
            self.shoe.shuffle()

        self.player.hand = []
        self.dealer.hand = []

        self.player.control = 1
        self.dealer.control = 1

        self.dealer.bj = 0
        self.player.bj = 0

        self.player.bust = 0
        self.dealer.bust = 0

        self.player.split = 0
        self.dealer.split = 0

    def playerPlay(self, person : Player):

        uncompletedHands = person.hand
        while person.control and len(uncompletedHands):

            # take the first hand in the list as the active one
            activeHand = uncompletedHands[0]
            
            log(__name__, activeHand.cards, 1, 1)
            
            # evaluate the persons strategy
            if len(person.hand) >= self.params.maxHands: canSplit = 0
            else: canSplit = 1

            action = evaluatePlayerStrategy(person.strategy, 
                                            activeHand, 
                                            self.dealer.hand[0], 
                                            canSplit = canSplit
                                            )

            action.announce()
            
            # run the action determined by the strategy
            activeHand.completed = action.run(self.shoe, person, activeHand)
            
            # recompile the hands which are not completed
            uncompletedHands = [ hand 
                                for hand in person.hand 
                                if hand.completed == 0 
                                ]

        for hand in person.hand: log(__name__, hand.cards, 1, 1)

    def dealerPlay(self, person : Player):

        uncompletedHands = person.hand
        while person.control and len(uncompletedHands):

            # take the first hand in the list as the active one
            activeHand = uncompletedHands[0]
            
            log(__name__, activeHand.cards, 1, 1)
            
            action = evaluateDealerStrategy(person.strategy, activeHand)
            
            action.announce()
            
            # run the action determined by the strategy
            activeHand.completed = action.run(self.shoe, person, activeHand)
            
            # recompile the hands which are not completed
            uncompletedHands = [ hand 
                                for hand in person.hand 
                                if hand.completed == 0 
                                ]

        for hand in person.hand: log(__name__, hand.cards, 1, 1)

    def run(self, betSize = 1, forcedDealerHand = None, forcedPlayerHand = None):
        
        # deal cards to player and dealer
        self.dealGame(forcedDealerHand = forcedDealerHand, forcedPlayerHand = forcedPlayerHand)
        
        log(__name__, self.dealer.hand[0].cards, 1, 1)
        log(__name__, self.player.hand[0].cards, 1, 1)

        # place the players bet on the current hand
        self.player.hand[0].placeBet(self.player,betSize)

        # check for BJ for dealer and player. Resolve at the end
        # Currently set to peak at A and all 10 values
        self.dealer.hand[0].evaluate()
        if self.dealer.hand[0].value == 21:
            self.dealer.control = 0
            self.player.control = 0
            self.dealer.hand[0].bj = 1
        
        # players turn
        log(__name__, 'Player:', 1, 1)
        self.player.hand[0].evaluate()
        if self.player.hand[0].value == 21:
            self.player.control = 0
            self.dealer.control = 0
            self.player.hand[0].bj = 1
        
        self.playerPlay(self.player)

        # if the player has busted their hands then no need for the dealer to play
        if np.all(np.array([hand.bust for hand in self.player.hand]) == 1):
            self.dealer.control = 0
        
        # dealers turn
        log(__name__, 'Dealer:', 1, 1)
        if self.params.dealerDraws == 'After': 
            self.dealer.hand[0].cards.append(self.shoe.draw())

        self.dealer.hand[0].evaluate()
        if self.dealer.hand[0].value == 21:
            self.dealer.control = 0
            self.player.control = 0
            self.dealer.hand[0].bj = 1

        self.dealerPlay(self.dealer)

        # resolve the action
        self.resolve()

if __name__ == '__main__':
    pass