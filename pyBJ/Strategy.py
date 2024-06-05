from Player import *
from Cards import *
from Input import *
from Decision import *

import pandas as pd
        
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