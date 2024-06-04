#!/usr/bin/env python3

from pyBJ.Player import *
from pyBJ.Cards import *
from pyBJ.Decision import *
from pyBJ.Strategy import *
from pyBJ.Bet import getBettingStrategy
from pyBJ.BJ import BlackJack

import numpy as np
import matplotlib.pyplot as plt

def main():

    printConsoleHeader()
    log('pyBJ', f'Starting BJ Simulation...', 0, 0)
    
    # read config file
    params = getParams()
    readGlobals(inputParams = params)

    # betting strategy
    bettingStrat = getBettingStrategy(params)
    
    # dealer strategy
    dStrat_dict = readDealerStrategy(params.dealerStratPath)

    # player strategy
    pStrat_dict = readPlayerStrategy(params.playerStratPath)
    
    # setup our player and dealer with their respective strategies
    player = Player(pStrat_dict)
    dealer = Player(dStrat_dict)
    
    # setup shoe with nDecks decks and shuffle them together
    shoe = Shoe(nDecks = params.nDecks)
    shoe.shuffle()
    
    # instantiate a Blackjack session with shoe, player and dealer
    bj = BlackJack(params, shoe, player, dealer)
    betSize = params.baseBet

    # initialize results tracking
    bj.runningResults = [player.bankroll]
    runningTotalRisked = [0]
    totalRisked = 0

    for i in range(params.totalRounds):
        
        log('BJ', f'Round {i} ', 0, 0)

        # run a blackjack round
        bj.run(betSize = betSize)
        
        # update result tracking
        bj.runningResults.append(player.bankroll)
        currentRisk = sum(h.bet for h in player.hand)
        runningTotalRisked.append(runningTotalRisked[-1] + currentRisk)
        totalRisked += currentRisk
        
        # reset the round
        bj.muck()

        # adjust the bet according to the betting strategy
        betSize = bettingStrat.run(betSize = betSize, runningResults = bj.runningResults)

    # results plotting
    runningPayback = (1 + (np.array(bj.runningResults[1:]) / np.array(runningTotalRisked[1:])))
    paybackMean = np.mean(runningPayback[-int(np.ceil(params.totalRounds * 0.1)):])

    log('pyBJ', f'Finished BJ Simulation. Results: ', 0, 0)
    print(f'Payback Percentage: {paybackMean * 100} %')
    print(f'House Edge {(1 - paybackMean) * 100} %')

    df = pd.DataFrame()
    df['Round'] = [ i for i in range(params.totalRounds+1) ]
    df['Bankroll'] = bj.runningResults
    df['RunningTotalRisked'] = runningTotalRisked
    df.to_csv('results.csv')


    fig, axs = plt.subplots(1, 2, figsize = (12,5))
    
    axs[0].plot([ i for i in range(params.totalRounds+1) ], bj.runningResults)
    axs[1].plot([ i for i in range(params.totalRounds) ], 1 - runningPayback)

    axs[1].set_ylim([-0.02,0.02])
    
    if params.totalRounds < 1000000: print('WARNING: House Edge results are not likely not converged due to small number of rounds')
    
    plt.show()
    
    printConsoleFooter()

if __name__== '__main__':
    main()
