import math
import os

# system log for previous operations and answers below the screen {via stack perhaps}
# > add a View Full Log input
# ANS for previous answer
# > ANS[2] for second previous answer (displayed in log)
# type manipulation (if both int, answer is int; if at least one float, answer is float)
# add more operands (currently just 2)
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


def printEntryScreen(): 
    os.system('cls')
    printScreen("Welcome to CALCULATHOR!", "~ PYTHON ~", "Made by shankencedric")

def stringToCenteredLine(string, writeableSpaces = 63) -> str:
    totalSpaces = writeableSpaces - len(string)
    leftSpaces = math.floor(totalSpaces / 2)
    rightSpaces = totalSpaces - leftSpaces
    return (" " * leftSpaces) + string + (" " * rightSpaces)
    
def printScreen(*rows):
    os.system('cls')
    centeredRows = tuple(map(lambda arg: stringToCenteredLine(arg), rows))
    print("#################################################################")
    for row in centeredRows: print("#" + row + "#") 
    print("#################################################################\n")
    
def calculatorLoop(): 
    printScreen("", "Enter Input", "")
    answer = calculate(getInput())
    printScreen("", str(answer), "")
    getInput()
    calculatorLoop()
    
def calculate(input : str) -> int | float | None: # 2 numbers only for now
    operation = sorted(input)[0]
    operands = input.split(operation)
    operands = list(map(lambda operand: int(operand.strip()), operands))
    # additionally, do some operand type determination and manipulation (float ba sya or int lang or what)
    match operation:
        case "+":
            return operands[0] + operands[1]
        case "-":
            return operands[0] - operands[1]
        case "*":
            return operands[0] * operands[1]
        case "/":
            return operands[0] / operands[1]
        case "%":
            return operands[0] % operands[1]
        case "^":
            return operands[0] ** operands[1]
        case _:
            return None
        
def getInput():
    return input()
    
def main(): 

    printEntryScreen()
    
    getInput()
    
    calculatorLoop()

    
if __name__ == "__main__": 
    main()