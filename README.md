# BlackJack Simulator (pyBJ)

Large scale time-dependent BlackJack simulator for evaluating static decision and betting strategies.

## Table of Contents

- [pyBJ](#pyBJ)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)
  - [Usage](#usage)

## Description

pyBJ enables the evaluation of a pre-defined (static) BlackJack strategy (such as a Basic Strategy) through the calculation of the Profit & Loss and running House Edge (%) value with multi-billions of simulated hands played according the user-defined dealer/player strategy and table ruleset. This process allows for the optimization of the players strategy given an arbitrary rulesets.

Additionally, betting strategies can be evaluated through this process as well. Some simple betting strategies have been encoded such as Flat betting, Martingale and Reverse Martingale with more to come. While betting strategies do not affect the long-time House Edge they can drastically change the variance of the results in the short term.

Unlike other BlackJack simulation tools pyBJ operates in a time-dependent fashion meaning that the concept of a cut card is implemented and the Shoe is updated during the simulation. This means that running pyBJ is exactly equivalent to sitting at a BlackJack table and playing numerous hands back-to-back-to-back.

## Installation

List of third-party python libraries that this code requires to run:

* [numPy](http://www.numpy.org/)
* [matplotlib](http://matplotlib.org/)
* [pandas](https://pandas.pydata.org)

Firstly download the source code with git:
```bash   
git clone git@github.com:PeteHatton/pyBJ.git /path/to/desired/code/location
```

It is recommended that you install these in a conda environment.
For example, setting up your conda environment will look something like this:

```bash   
conda create --name my_env 
conda activate my_env  
conda install -c conda-forge numpy matplotlib pandas
```
This can take some time...

It is then recommended to add these lines to your .zshrc or .bashrc:  
```bash  
export PATH=$PATH:/path/to/pyBJ/  
export PYTHONPATH=$PYTHONPATH:/path/to/pyBJ/
```

## Usage

Firtly, the user must create strategies. Strategies are excel (.xlsx) files which 
encode the action of the player/dealer in a given scenario.
To create a dealer strategy, it is recommended to copy the default strategy provided in the code 
'dealer-strategy_default.xlsx'. Do not edit anything in the file apart from the action column.
Similarly for the player strategy.

Secondly, the user must edit the config file to set up the ruleset of the game. Again it is recommended to copy the config file provided in the code and edit settings there.

Finally, run the code by navigating the desired output folder and simply typing:
```bash  
/path/to/pyBJ/main/bj-main.py
```

The code will run for the user-specified number of rounds and present a value for the House Edge of that strategy with the given ruleset. It will also produce a Profit & Loss graph and a House Edge graph against the number of rounds that were run as well as a results.csv file with the per round data.