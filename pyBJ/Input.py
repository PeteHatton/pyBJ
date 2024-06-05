import Globals

import xml.etree.ElementTree as ET

class InputParams:
    def __init__(self):

        # =====================================================================
        # Main parameters
        self.playerStratPath = ''
        self.dealerStratPath = ''
        self.baseBet = 0
        self.totalRounds = 0
        self.deckPenetration = 0
        self.bettingStrategy = None
        self.tableMaxBet = 0
        self.blackjackPaysRatio = ''
        self.blackjackPays = ''
        self.verbose = 1
        self.maxHands = 0
        self.nDecks = 1
        self.dealerDraws = None


def getParams(inputParamFile = "pyBJ-config.xml"):

    INPUT_PARAMS_TAG = "InputParams"
    try:
        tree = ET.parse(inputParamFile)
        root = tree.getroot()
    except (ET.ParseError, FileNotFoundError) as e:
        raise ValueError(f"Error parsing XML file '{inputParamFile}': {e}")
    
    def parse_numerical(value):
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value.strip()

    input_params = InputParams()
    for element in root.iter():
        if element.tag == INPUT_PARAMS_TAG:
            continue
        if element.text and element.text.strip():
            setattr(input_params, element.tag, parse_numerical(element.text))

    ratio = input_params.blackjackPaysRatio.split(':')
    input_params.blackjackPays = int(ratio[0]) / int(ratio[1])

    return input_params

def readGlobals(inputFile="pyBJ-config.xml", inputParams=None):
    """
    Read globals if they haven't already been read.
    
    """
    if Globals.globalsSet:
        pass
    else:
        if not isinstance(inputParams, InputParams):
            inputParams = getParams(inputFile = inputFile)
        
        # assume this method is called while in original working directory
        Globals.verbose = inputParams.verbose
        
if __name__ == "__main__":
    pass