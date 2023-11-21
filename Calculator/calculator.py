import math
import os
from pynput.keyboard import KeyCode, Key, Controller, Listener
import re
import time
import threading

# system log for previous operations and answers below the screen {via stack perhaps}
# > add a View Full Log input
# ANS for previous answer
# > ANS[2] for second previous answer (displayed in log)
# type manipulation (if both int, answer is int; if at least one float, answer is float)
# add more operands (currently just strictly 2 except power)
# > note PEMDAS
# big numbers owo
# revamp screen
# > try 4 writeable rows instead of 3
# > row 2 is previous operation 
# > row 3 is previous answer 
# add customization
# > define screen space
# >> can be presets (small medium large)
# refactor (possibly, stringToCenteredLine can be printAsCentered or smthn)
# handle invalid inputs

CLEAR_SCREEN = 'cls'
EXIT_KEY = 'q'
EXITED = False
APP_CLOSING_TIME = 5 # seconds
OPERATION_REGEX = r'[\+\-\*x/\^]'
PEMDAS = ['^', ['*', '/'], ['+', '-']] # no P yet; # can be modified -- take note that inner lists can only have length of 2
MAX_OPERATIONS = 1000000

def pressExit(key : KeyCode):
    try: 
        if key.char == EXIT_KEY: 
            Controller().press(Key.enter) 
            global EXITED
            EXITED = True  
            return False # turn off listening
    except: None

def printExitScreen():
    printScreen("", "Thanks for using my app!", "")
    print("Closing app in {t} seconds...".format(t=APP_CLOSING_TIME))
    time.sleep(APP_CLOSING_TIME)
    exit()

def stringToCenteredLine(stringToCenter : str, writeableSpaces : int = 63) -> str:
    """Takes in a `stringToCenter` as input and returns it centered in a `writeablesSpaces`-wide space (63 by default)."""
    totalSpaces = writeableSpaces - len(stringToCenter)
    leftSpaces = math.floor(totalSpaces / 2)
    rightSpaces = totalSpaces - leftSpaces
    return (" " * leftSpaces) + stringToCenter + (" " * rightSpaces)

def printEntryScreen(): 
    """Prints the first entry screen of the app."""
    os.system(CLEAR_SCREEN)
    printScreen("Welcome to CALCULATHOR!", "~ PYTHON ~", "Made by shankencedric")

def printScreen(*rows : str):
    """Prints the screen of the app including intermediate `rows` (length of 3 ideally) that are centered.\n
    In other words, this is the template of the app screen."""
    os.system(CLEAR_SCREEN)
    centeredRows = tuple(map(lambda arg: stringToCenteredLine(arg), rows))
    print("#################################################################")
    for row in centeredRows: print("#" + row + "#") 
    print("#################################################################\n")
        
def getInput(print : str = "") -> tuple:
    return parseInput(input(print))

def parseInput(input : str) -> tuple:
    input = input.replace(" ", "")
    operations = re.findall(OPERATION_REGEX, input)
    operands = re.sub(OPERATION_REGEX, " ", input)
    operands = list(map(lambda x: float(x), operands.split(" ")))
    return (operands, operations)
        
def calculatorLoop(): 
    """The main loop of the caclulator."""
    printScreen("", "Enter Input", "")
    
    operands, operations = getInput("Input: ")
    while len(operands) > 1:
        idx = getNextOperation(operations)
        #print("OP: {op1} {op} {op2}".format(op1=operands[idx],op=operations[idx],op2=operands[idx+1]))
        new_operand = compute2(operands[idx], operands.pop(idx+1), operations.pop(idx))
        #print("Answer:", new_operand)
        #input()
        operands[idx] = new_operand

    printScreen("", str(operands[0]), "")
    input()
    
def getNextOperation(operations : list) -> int: # currently: emdas, assumes no grouping
    for ordered_operation in PEMDAS:
        while(True):
            try: 
                if type(ordered_operation) == list:
                    try: _idx1 = operations.index(ordered_operation[0])
                    except: _idx1 = MAX_OPERATIONS
                    try: _idx2 = operations.index(ordered_operation[1])
                    except: _idx2 = MAX_OPERATIONS
                    idx = min(_idx1, _idx2)
                    if idx == MAX_OPERATIONS: break
                else: idx = operations.index(ordered_operation)
                print(idx)
                return idx
            except ValueError: 
                break
    return -1 # done

def compute2(operand1 : int | float, operand2 : int | float, operation : str) -> int | float | None: 
    """Computes 2 operands `operand1` and `operand2` and returns the answer."""
    match operation:
        case "+":
            return operand1 + operand2
        case "-":
            return operand1 - operand2
        case "*":
            return operand1 * operand2
        case "/" | "x":
            return operand1 / operand2
        case "%":
            return operand1 % operand2
        case "^":
            return operand1 ** operand2
        case _:
            return None
      

    
def main(): 
    
    exitThread = threading.Thread(target=lambda: Listener(on_press=pressExit).start())
    exitThread.start()
   
    printEntryScreen()
    print("Anytime, press  [ {key} ]  to exit the app.".format(key=EXIT_KEY))
    input("\nEnter to continue...")
    
    #test_case_1 = "5 + 3 - 2"        # Answer: 6
    #test_case_2 = "4 * 2 / 2"        # Answer: 4.0
    #test_case_3 = "2 ** 3"           # Answer: 8
    #test_case_4 = "10 + 3 * 2 - 5 / 2"  # Answer: 13.5
    #test_case_5 = "4 * (6 / 2) + 1"  # Answer: 13.0
    
    while (EXITED == False): 
        calculatorLoop()
    exitThread.join()
        
    printExitScreen()   
    
if __name__ == "__main__": 
    main()
    
