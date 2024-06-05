# BlackJack Simulator (pyBJ)

Large scale BlackJack simulator for evaluating static decision and betting strategies.

## Table of Contents

- [pyBJ](#pyBJ)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Installation](#installation)

## Description

pyBJ enables the evaluation of a pre-defined (static) BlackJack strategy (such as a Basic Strategy) through the calculation of the Profit & Loss and running House Edge (%) value with multi-billions of simulated hands played according the user-defined dealer/player strategy and table ruleset. This process allows for the optimization of the players strategy given an arbitrary rulesets. 

Additionally, betting strategies can be evaluated through this process as well. Some simple betting strategies have been encoded such as Flat betting, Martingale and Reverse Martingale with more to come. While betting strategies do not affect the long-time House Edge they can drastically change the variance of the results in the short term.

## Installation

List of third-party python libraries that this code requires to run:

* [numPy](http://www.numpy.org/)
* [matplotlib](http://matplotlib.org/)
* [pandas](https://pandas.pydata.org)

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