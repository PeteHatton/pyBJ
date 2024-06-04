from Player import *
from Cards import *
from Input import *
from Decision import *

import pandas as pd
import numpy as np

class Strategy:
    
    """ Parent class for all strategies """
    
    def __init__(self, params: InputParams):

        self.params = params

    def evaluate(self, activeHand : Hand, passiveHand : Hand, canSplit = 1):
        # overwritten by each strategy
        pass

################################################################################
        # PLAYER STRATEGIES
################################################################################

class Grosvenor_AutoShuffler(Strategy):

    def __init__(self, params : InputParams):
        super().__init__(params)

    def evaluate(self, activeHand : Hand, passiveHand : Hand, canSplit = 1):
        
        activeHand.evaluate()
        passiveHand.evaluate()
        dUpCard = passiveHand.cards[0]
        dUpCardVal = passiveHand.cardDict[dUpCard]

        # bust
        if activeHand.value > 21:
            return Bust()
        
        if dUpCard == 'A':
            
            if activeHand.value >= 17:
                return Stand()
            
            else:
                return Hit()
            
        if dUpCardVal == 7:
            
            if activeHand.value >= 17:
                return Stand()
            
            if activeHand.value == 16:
                return Hit()

class Basic(Strategy):

    """ Basic BJ Strategy """
    """ Based on 8 deck strat: https://wizardofodds.com/games/blackjack/strategy/calculator/"""
        
    def __init__(self, params : InputParams):
        super().__init__(params)

    def evaluate(self, activeHand : Hand, passiveHand : Hand, canSplit = 1):
        
        activeHand.evaluate()
        passiveHand.evaluate()
        dUpCard = passiveHand.cards[0]
        dUpCardVal = passiveHand.cardDict[dUpCard]
        
        # Bust
        if activeHand.value > 21:
            return Bust()
        
        # Splits
        if len(activeHand.cards) == 2 and activeHand.cards[0] == activeHand.cards[1] and canSplit:

            if activeHand.cards[0] == 'A':
                return Split()
            
            elif activeHand.cards[0] == '9':
                if dUpCard == 'A' or dUpCardVal in [7,10]:
                    return Stand()
                else:
                    return Split()
            
            elif activeHand.cards[0] == '8':
                return Split()
            
            elif activeHand.cards[0] == '7':
                if dUpCardVal in [2,3,4,5,6,7]:
                    return Split()
                else:
                    return Hit()
                
            elif activeHand.cards[0] == '6':
                if dUpCardVal in [2,3,4,5,6]:
                    return Split()
                else:
                    return Hit()

            elif activeHand.cards[0] == '4':
                if dUpCardVal in [5,6]:
                    return Split()
                else:
                    return Hit()
            
            elif activeHand.cards[0] == '3':
                if dUpCardVal in [2,3,4,5,6,7]:
                    return Split()
                else:
                    return Hit()

            elif activeHand.cards[0] == '2':
                if dUpCardVal in [2,3,4,5,6,7]:
                    return Split()
                else:
                    return Hit()

        
        # Softs
        if activeHand.soft:
            
            if activeHand.value in [13,14]:
                if dUpCardVal in [5,6] and len(activeHand.cards) == 2:
                    return DD()
                else:
                    return Hit()
                
            if activeHand.value in [15,16]:
                if dUpCardVal in [4,5,6] and len(activeHand.cards) == 2:
                    return DD()
                else:
                    return Hit()
            
            elif activeHand.value == 17:
                if dUpCardVal in [3,4,5,6] and len(activeHand.cards) == 2:
                    return DD()
                else:
                    return Hit()

            elif activeHand.value == 18:
                if dUpCardVal in [3,4,5,6] and len(activeHand.cards) == 2:
                    return DD()
                elif dUpCardVal in [9,10] or dUpCard == 'A':
                    return Hit()
                else:
                    return Stand()

        # Hards
        if activeHand.value <= 8:
            return Hit()
        
        elif activeHand.value == 9:
            if dUpCardVal in [3,4,5,6] and len(activeHand.cards) == 2:
                return DD()
            else:
                return Hit()
            
        elif activeHand.value == 10:
            if dUpCardVal in [2,3,4,5,6,7,8,9] and len(activeHand.cards) == 2:
                return DD()
            else:
                return Hit()

        elif activeHand.value == 11:
            if dUpCard != 'A' and len(activeHand.cards) == 2:
                return DD()
            else:
                return Hit()
            
        elif activeHand.value == 12:
            if dUpCardVal in [4,5,6]:
                return Stand()
            else:
                return Hit()
                
        elif activeHand.value >= 13 and activeHand.value <= 16:
            if dUpCardVal in [2,3,4,5,6]:
                return Stand()
            else:
                return Hit()
        
        elif activeHand.value >= 17:
            return Stand()

        print('ERROR: We didnt make an action')

class Basic(Strategy):

    """ Basic BJ Strategy """
    """ Based on single deck strat: https://wizardofodds.com/games/blackjack/strategy/1-deck/ """
        
    def __init__(self, params : InputParams):
        super().__init__(params)

    def evaluate(self, activeHand : Hand, passiveHand : Hand, canSplit = 1):
        
        activeHand.evaluate()
        passiveHand.evaluate()
        dUpCard = passiveHand.cards[0]
        dUpCardVal = passiveHand.cardDict[dUpCard]
        
        # Bust
        if activeHand.value > 21:
            return Bust()
        
        # Splits
        if len(activeHand.cards) == 2 and activeHand.cards[0] == activeHand.cards[1] and canSplit:

            if activeHand.cards[0] == 'A':
                return Split()
            
            elif activeHand.cards[0] == '9':
                if dUpCard == 'A' or dUpCardVal in [7,10]:
                    return Stand()
                else:
                    return Split()
            
            elif activeHand.cards[0] == '8':
                return Split()
            
            elif activeHand.cards[0] == '7':
                if dUpCardVal in [10]:
                    return Stand()
                elif dUpCardVal in [2,3,4,5,6,7,8]:
                    return Split()
                else:
                    return Hit()
                
            elif activeHand.cards[0] == '6':
                if dUpCardVal in [2,3,4,5,6,7]:
                    return Split()
                else:
                    return Hit()

            elif activeHand.cards[0] == '4':
                if dUpCardVal in [4,5,6]:
                    return Split()
                else:
                    return Hit()
            
            elif activeHand.cards[0] == '3':
                if dUpCardVal in [2,3,4,5,6,7,8]:
                    return Split()
                else:
                    return Hit()


            elif activeHand.cards[0] == '2':
                if dUpCardVal in [2,3,4,5,6,7]:
                    return Split()
                else:
                    return Hit()

        
        # Softs
        if activeHand.soft:
            
            if activeHand.value >= 13 and activeHand.value <= 16:
                if dUpCardVal in [4,5,6] and len(activeHand.cards) == 2:
                    return DD()
                else:
                    return Hit()
            
            elif activeHand.value == 17:
                if dUpCardVal in [2,3,4,5,6] and len(activeHand.cards) == 2:
                    return DD()
                else:
                    return Hit()

            elif activeHand.value == 18:
                if dUpCardVal in [3,4,5,6] and len(activeHand.cards) == 2:
                    return DD()
                elif dUpCardVal in [9,10]:
                    return Hit()
                else:
                    return Stand()

            elif activeHand.value == 19:
                if dUpCardVal in [6] and len(activeHand.cards) == 2:
                    return DD()
                else:
                    return Stand()

        # Hards
        if activeHand.value <= 7:
            return Hit()
        
        if activeHand.value <= 8:
            if dUpCardVal in [5,6] and len(activeHand.cards) == 2:
                return DD()
            else:
                return Hit()
        
        elif activeHand.value == 9:
            if dUpCardVal in [2,3,4,5,6] and len(activeHand.cards) == 2:
                return DD()
            else:
                return Hit()
            
        elif activeHand.value == 10:
            if dUpCardVal in [2,3,4,5,6,7,8,9] and len(activeHand.cards) == 2:
                return DD()
            else:
                return Hit()

        elif activeHand.value == 11:
            if len(activeHand.cards) == 2:
                return DD()
            else:
                return Hit()
            
        elif activeHand.value == 12:
            if dUpCardVal in [4,5,6]:
                return Stand()
            else:
                return Hit()
                
        elif activeHand.value >= 13 and activeHand.value <= 16:
            if dUpCardVal in [2,3,4,5,6]:
                return Stand()
            else:
                return Hit()
        
        elif activeHand.value >= 17:
            return Stand()

        print('ERROR: We didnt make an action')


################################################################################
        # DEALER STRATEGIES
################################################################################
        
# class Dealer(Strategy):

#     """ Dealers actions are coded as a strategy and can be used by player if desired """
#     def __init__(self, params: InputParams):
#         super().__init__(params)

#     def evaluate(self, activeHand : Hand, passiveHand : Hand, canSplit = 1):

#         # get hand value
#         activeHand.evaluate()
#         log(__name__, activeHand.value, 1, 1)

#         if activeHand.value > 21:
#             return Bust()

#         if activeHand.soft and activeHand.value == 17:
#             if self.params.hitSoft17:
#                 return Hit()
#             else:
#                 return Stand()
        
#         if activeHand.value < 17:
#             return Hit()
        
#         if activeHand.value >= 17:
#             return Stand()
        
def readDealerStrategy(path):

    df_HARD = pd.read_excel(path, sheet_name='HARD')
    df_SOFT = pd.read_excel(path, sheet_name='SOFT')

    hardDict = df_HARD.set_index('Dealer Card')['Action']
    softDict = df_SOFT.set_index('Dealer Card')['Action']

    decisionDict = {}
    decisionDict['HARD'] = hardDict
    decisionDict['SOFT'] = softDict

    return decisionDict

def evaluateDealerStrategy(strategy, activeHand : Hand):
    
    activeHand.evaluate()

    if activeHand.value > 21:
        return Bust()

    if activeHand.soft: s = 'SOFT'
    else: s = 'HARD'

    return stringToAction(strategy[s][activeHand.value])

def readPlayerStrategy(path):

    df_HARD = pd.read_excel(path, sheet_name='HARD')
    df_SOFT = pd.read_excel(path, sheet_name='SOFT')
    df_SPLIT = pd.read_excel(path, sheet_name='SPLIT')
    
    hardDF = df_HARD.set_index('Player Value')
    softDF = df_SOFT.set_index('Player Value')
    splitDF = df_SPLIT.set_index('Player Value')

    decisionDict = {}
    decisionDict['HARD'] = hardDF
    decisionDict['SOFT'] = softDF
    decisionDict['SPLIT'] = splitDF

    return decisionDict
    
def evaluatePlayerStrategy(strategy, activeHand : Hand, passiveHand : Hand, canSplit = 0):
    
    activeHand.evaluate()
    passiveHand.evaluate()

    dUpCard = passiveHand.cards[0]
    dUpCardVal = passiveHand.cardDict[dUpCard]

    if activeHand.value > 21:
        return Bust()
    
    if canSplit == 1 and len(activeHand.cards) == 2 and activeHand.cards[0] == activeHand.cards[1]: s = 'SPLIT'
    elif activeHand.soft: s = 'SOFT'
    else: s = 'HARD'

    lookupVal = activeHand.value
    if s == 'SPLIT' and activeHand.soft == 1 and activeHand.cards[0] == 'A' and  activeHand.cards[1] == 'A':
        lookupVal = 2

    actionString = strategy[s].loc[lookupVal][dUpCardVal]

    if actionString == 'Dh':
        if len(activeHand.cards) > 2:
            actionString = 'H'
        else:
            actionString = 'D'

    if actionString == 'Ds':
        if len(activeHand.cards) > 2:
            actionString = 'S'
        else:
            actionString = 'D'

    return stringToAction(actionString)

def stringToAction(actionString):

    if actionString == 'H':
        return Hit()
    elif actionString == 'S':
        return Stand()
    elif actionString == 'P':
        return Split()
    elif actionString == 'D':
        return DD()