import os
import math
from dataclasses import dataclass

TOTALBITS = 32
TOTALBYTES = 4
ENTRYSIZE = 4

@dataclass
class Number:
    """Custom class for number that can be treated as bin, hex, decimal, or string."""
    
    type signType = str('-') | str('') | str('+')
    type baseType = 2 | 10 | 16 | str("bin") | str("dec") | str("hex")
    
    val : str
    sign : signType
    base : baseType # based on val input, not synced
    
    def __init__(self, value : int | str, sign : signType = '', base : baseType = 10):
        """
        `baseType`: could be `2`/`10`/`16` or `"bin"`/`"dec"`/`"hex"`.\n
        `signType`: could be `'-'`/`''`/`'+'`.
        """
        self.val = str(value)
        self.sign = sign
        self.base = base
        
        #print("New Number was created: ", self)
        self.val = str(self.toBase(10))
        self.base = 10
        
    def toBase(self, newBase : baseType, maxChars : int = 0) -> str | int:
        """`baseType`: could be `2`/`10`/`16` or `"bin"`/`"dec"`/`"hex"`."""
        match newBase:
            case 2 | "bin": 
                toNewBase = bin
                stdMaxChars = TOTALBITS
            case 16 | "hex": 
                toNewBase = hex
                stdMaxChars = TOTALBYTES
            case _: return int(self.val, self.base) 
        
        return toNewBase(int(self.val, self.base))[2:].zfill(stdMaxChars if maxChars == 0 else maxChars)

    
    def machineIndexing(self, start : int, end : int):
        """`start` and `end` are inclusive.\n Returns a new `Number`."""
        # fails at (start, 0)
        ret = self.toBase(2)[::-1][start:end-1:-1]
        return Number("".join(map(lambda x: str(x), ret)), base=2)
    
def printBin(bin : str, label : str = ""):
    """Prints a BINARY string separated with _ for each 4 bits."""
    byte = ""
    print(label + "\t:", end="\t")
    for i in range(len(bin)):
        byte += bin[i]
        if i % 4 == 3 or i == len(bin)-1:
            print(byte, end="")
            byte = ""
            if i != len(bin)-1: print("_", end="")
    print(" [{a} bits]".format(a = len(bin)))

def printAddr(addr : Number, name : str = "?"): 
    """Calls `printBin` to print the BIN value, then prints the HEX value right after (i.e., newline, then after `->`)."""
    printBin(addr.toBase(2), name)
    print("  -> {addr}".format(addr=addr.toBase(16)))

def printHeader(string : str, writeableSpaces : int = 63, fillerChar : str = "-"):
    """Prints the `string` centered in a given `writeableSpaces` space, with the unused spaces filled with the `fillerChar`. """
    totalSpaces = writeableSpaces - len(string)
    leftSpaces = math.floor(totalSpaces / 2)
    rightSpaces = totalSpaces - leftSpaces
    print((fillerChar * leftSpaces), string, (fillerChar * rightSpaces) + "\n")


def VAtoPA(va : Number, PD_base : Number) -> Number: 

    def findEntry(base : Number, index : Number) -> Number: 
        return Number(base.toBase(10) + index.toBase(10) * ENTRYSIZE)
    
    ## PREAMBLE
    os.system('cls')
    printHeader("xv6 VA to PA translator (by me)", fillerChar="=")
    print("NOTE 1: Resize this terminal's width and/or font size to fit the dashes (----) below or equals (====) above in ONE LINE.\n")
    print("NOTE 2: Enter input values WITHOUT '0x' or '0b'. Just the numbers.\n")
    print("NOTE 3: The structure of each step is seen below:\n\n\n")
    printHeader("used variables as the TITLE here")
    print("label / NAME\t:\tvalue in BINARY [NUM of bits, usually 32]")
    print("  -> value in HEX")    
    input("\n\n\n\n\n\n\n(Press enter to continue...)")
    os.system('cls')
    
    ## GIVEN
    printHeader("(GIVEN)")
    printAddr(va, "VA")
    printAddr(PD_base, "PDbase")
    print()
    
    ## 10-10-12 spliting of VA bits
    printHeader("VA")
    PD_idx = va.machineIndexing(31, 22)
    PT_idx = va.machineIndexing(21, 12)
    offset = Number(va.machineIndexing(11, 1).toBase(2, maxChars=11) + va.toBase(2)[len(va.toBase(2))-1], base=2) # just a weird edge case
    printAddr(PD_idx, "PDidx")
    printAddr(PT_idx, "PTidx")
    printAddr(offset, "offset")
    print()
    
    ## compute for which Page Directory Entry (PDE); ie, which entry / where is this entry
    printHeader("PDbase & PDidx")
    pdeAddr = findEntry(PD_base, PD_idx) 
    printAddr(pdeAddr, "PDEaddr")
    print()
    
    ## access (in qemu) the address pointed to by the PDE and input (in here) the value
    printHeader("PDEaddr & (INPUT)")
    pde = input("Access the PDE at [ 0x{addr} ]\n   and then input here the value inside: ".format(addr=pdeAddr.toBase(16)))
    pde = Number(pde, base=16)
    print()
    printAddr(pde, "PDEval")
    print()
    
    ## compute for the Page Table (PT) base
    printHeader("PDE & 0's")
    PT_base = pde.machineIndexing(31, 12).toBase(2, 20) + Number(0).toBase(2, maxChars=12)
    PT_base = Number(PT_base, base=2)
    printAddr(PT_base, "PTbase")
    print()
    
    ## compute for which Page Table Entry (PTE); ie, which entry / where is this entry
    printHeader("PTbase & PTidx")
    pteAddr = findEntry(PT_base, PT_idx) 
    printAddr(pteAddr, "PTEaddr")
    
    ## access (in qemu) the address pointed to by the PTE and input (in here) the value
    printHeader("PTEaddr & (INPUT)")
    pte = input("Access the PTE at [ 0x{addr} ]\n   and then input here the value inside: ".format(addr=pteAddr.toBase(16)))
    pte = Number(pte, base=16)
    print()
    printAddr(pte, "PTEval")
    print()
    
    ## append offset to PN for the FINAL ANSWER (pa)
    printHeader("PTE & OFFSET")
    pn = pte.machineIndexing(31,12).toBase(2, maxChars=20)
    pa = Number(pn + offset.toBase(2, 12), base=2)
    printAddr(pa, "PA")
    print("\n\nHi. - Ced\n\n")



# example 
def main(): 
    os.system('cls') # remove these to not clear terminal
    va = Number("00002de0", base=16)
    pdbase = Number("0df22000", base=16)
    VAtoPA(va, pdbase)

if __name__ == "__main__":
    main()