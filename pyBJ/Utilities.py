from functools import partial
import datetime
import numpy as np

import Globals
from typing import List, Union

def writeTerminalBlock(message : str) -> None:
    
    """
    Writes a message surrounded by '#' characters in a terminal-like block.

    Parameters:
    - message (str): The message to be displayed within the terminal block.

    Returns:
    - None
    
    """

    length = 100
    messagePad = ' ' + message + ' '
    messageLength = len(messagePad)
    if messageLength % 2 != 0:
        messagePad = messagePad + ' '
    
    for _ in range(length): print('#',end='')
    print('')

    for _ in range((length - messageLength) // 2): print('#',end='')
    print(messagePad,end='')
    for _ in range((length - messageLength) // 2): print('#',end='')
    print('')

    for _ in range(length): print('#',end='')
    print('')

def printConsoleHeader():
    # version=versioneer.get_version()
    # writeTerminalBlock(f'Hop-Decorate ({version})')
    writeTerminalBlock(f'Blackjack Simulator')

def printConsoleFooter():
    writeTerminalBlock(f'Fin.')

def log(caller: str, message: str, level: int, indent: int = 0) -> None:

    """
    Log output to the screen with optional indentation.

    The function prints the log message to the screen, including the current timestamp,
    the caller name, and the message. It also supports an optional indentation level
    specified by the 'indent' parameter.

    Parameters:
        caller (str): The name of the caller or log source.
        message (str): The message to be logged.
        indent (int, optional): The number of indentation levels (defaults to 0).

    Returns:
        None
    """
    
    if level <= Globals.verbose:
        # Only print if less than the level set in Input module
        now = datetime.datetime.now().strftime("%d/%m/%y, %H:%M:%S")
        ind = "  " * indent

        try:
            sp = caller.split('.')
            if sp[0] == 'pyBJ':
                caller = sp[-1]
        except:
            pass
        
        for _ in range(indent):
            ind += "  "

        print(f"[{now}]: {ind}{caller} >> {message}", flush = True)