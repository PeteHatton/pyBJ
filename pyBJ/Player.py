class Player:

    def __init__(self, strategy):
        
        self.strategy = strategy

        self.initBankroll = 0
        self.bankroll = 0
        
        self.hand = None
        self.control = 1
        