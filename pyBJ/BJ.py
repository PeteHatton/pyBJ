from Player import *
from Cards import *
from Decision import *
from Strategy import *
from Bet import *
from Utilities import *

import sys
import numpy as np

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

    def playerPlay(self, person : Player):

        uncompletedHands = person.hand
        while person.control and len(uncompletedHands):

            # take the first hand in the list as the active one
            activeHand = uncompletedHands[0]
            activeHand.evaluate()

            logCards = ''
            for card in activeHand.cards:
                logCards += str(card) + ', '
            logCards += f'= {activeHand.value}'

            log(__name__, logCards, 1, 2)
            
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
        log(__name__, 'Player Result(s):', 1, 2)
        for hand in person.hand: 
            hand.evaluate()
            logCards = ''
            for card in hand.cards:
                logCards += str(card) + ', '
            logCards += f'= {hand.value}'
            log(__name__, logCards, 1, 3)

    def dealerPlay(self, person : Player):

        uncompletedHands = person.hand
        while person.control and len(uncompletedHands):

            # take the first hand in the list as the active one
            activeHand = uncompletedHands[0]
            activeHand.evaluate()
            
            logCards = ''
            for card in activeHand.cards:
                logCards += str(card) + ', '
            logCards += f'= {activeHand.value}'

            log(__name__, logCards, 1, 2)
            
            action = evaluateDealerStrategy(person.strategy, activeHand)
            
            action.announce()
            
            # run the action determined by the strategy
            activeHand.completed = action.run(self.shoe, person, activeHand)
            
            # recompile the hands which are not completed
            uncompletedHands = [ hand 
                                for hand in person.hand 
                                if hand.completed == 0 
                                ]

        log(__name__, 'Dealer Result(s):', 1, 2)
        for hand in person.hand: 
            hand.evaluate()
            logCards = ''
            for card in hand.cards:
                logCards += str(card) + ', '
            logCards += f'= {hand.value}'
            
            log(__name__, logCards, 1, 3)

    def checkBJ(self, hand):
        hand.evaluate()
        if hand.value == 21:
            self.dealer.control = 0
            self.player.control = 0
            hand.bj = 1


    def run(self, betSize = 1, forcedDealerHand = None, forcedPlayerHand = None):
        
        # deal cards to player and dealer
        self.dealGame(forcedDealerHand = forcedDealerHand, forcedPlayerHand = forcedPlayerHand)
        
        
        log(__name__, f" Dealer: {str(self.dealer.hand[0].cards[0])}, - " , 1, 1)

        self.player.hand[0].evaluate()
        log(__name__, f" Player: {str(self.player.hand[0].cards[0])}, {str(self.player.hand[0].cards[1])} = {str(self.player.hand[0].value)}", 1, 1)

        # place the players bet on the current hand
        self.player.hand[0].placeBet(self.player,betSize)

        # check for BJ for dealer and player. Resolve at the end
        # Currently set to always peak
        self.checkBJ(self.dealer.hand[0])
        
        # players turn 
        log(__name__, 'Player:', 1, 1)

        # check for player bj
        self.checkBJ(self.player.hand[0])
        
        # player plays their hand...
        self.playerPlay(self.player)

        # if the player has busted their hands then no need for the dealer to play
        if np.all(np.array([hand.bust for hand in self.player.hand]) == 1):
            self.dealer.control = 0
        
        # dealers turn
        log(__name__, 'Dealer:', 1, 1)
        if self.params.dealerDraws == 'After': 
            self.dealer.hand[0].cards.append(self.shoe.draw())

        # check for dealer bj
        self.checkBJ(self.dealer.hand[0])

        # dealer plays their hand...
        self.dealerPlay(self.dealer)

        # resolve the action
        self.resolve()

if __name__ == '__main__':
    pass