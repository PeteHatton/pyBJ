import numpy as np
from Input import InputParams

class BettingStrategy():
    
    def __init__(self, params : InputParams):
        self.params = params

    def run(self):
        pass

class Flat(BettingStrategy):

    def __init__(self, params):
        super().__init__(params)

    def run(self, betSize = None, runningResults = None):
        return betSize

class Martingale(BettingStrategy):

    def __init__(self, params):
        super().__init__(params)

        if self.params.tableMaxBet == -1:
            self.maxBet = np.inf
        else:
            self.maxBet = self.params.tableMaxBet

    def run(self, betSize = None, runningResults = None):
        

        if runningResults[-1] < runningResults[-2]:
            betSize = np.min([self.maxBet, betSize * 2])
        else:
            betSize = self.params.baseBet

        return betSize
    
class ReverseMartingale(BettingStrategy):

    def __init__(self, params):
        super().__init__(params)

        if self.params.tableMaxBet == -1:
            self.maxBet = np.inf
        else:
            self.maxBet = self.params.tableMaxBet

    def run(self, betSize = None, runningResults = None):
        
        if runningResults[-1] < runningResults[-2]:
            betSize = self.params.baseBet
        else:
            betSize = np.min([self.maxBet, betSize * 2])

        return betSize
    
################################################################################

def getBettingStrategy(params):
    
    if params.bettingStrategy == 'Flat':
        return Flat(params)
    
    if params.bettingStrategy == 'Martingale':
        return Martingale(params)
    
    if params.bettingStrategy == 'Reverse Martingale':
        return ReverseMartingale(params)