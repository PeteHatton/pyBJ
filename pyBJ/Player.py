import numpy as np

class Player:

    def __init__(self, strategy):
        
        self.initBankroll = 0
        self.bankroll = 0
        self.bet = 0
        self.hand = None
        self.control = 1
        self.bust = 0
        self.bj = 0
        self.split = 0
        self.strategy = strategy
        self.splits = 0