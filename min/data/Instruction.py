import logging
from sys import exit

import min.data.regs as regs

"""
Instruction can be considered as an intermediate level between text instruction and binary opcodes
It is used in the middle of compilation for reference resolution.
"""

class Instruction:
    TYPE_INT = 0
    TYPE_STR = 1
    TYPE_INS = 2
    TYPE_FCN = 3


    def __init__(self,addr,itype=None,symbol=None):
        self.addr = addr # Address in the current executable
        self.itype = itype

        self.first_reg = 0
        self.second_reg = 0
        self.symbol = symbol # Named of symbol when fcn/int/str and operand when used with instruction

        self.first_value = 0
        self.second_value = 0

        self.first_reference = ""
        self.second_reference = ""

    def setValue(self,number=None,string=None):
        if number != None:
            self.first_value = number
            self.itype = self.TYPE_INT
        
        if string != None:
            self.first_value = string
            self.itype = self.TYPE_STR

    def setFirstSlot(self,number=None,reg=None,reference=None): # Number will be converted,reg will be too and reference will set a flag so it will be resolved later on
        if number != None:
            if number.startswith("#"):
                self.first_value = int(number[1:])
                return
            if number.startswith("0x"):
                self.first_value = int(number,16)

        if reg != None:
            reg = reg[1:]
            if reg in regs.REGS:
                self.first_reg = 1
                self.first_value = regs.REGS.index(reg)
                return
            else:
                logging.error("Not a valid register : {}".format(reg))
                exit(-1)

        if reference != None:
            self.first_reference = reference
            return

        return

    def setSecondSlot(self,number=None,reg=None,reference=None): # Number will be converted,reg will be too and reference will set a flag so it will be resolved later on
        if number != None:
            if number.startswith("#"):
                self.second_value = int(number[1:])
                return
            if number.startswith("0x"):
                self.second_value = int(number,16)

        if reg != None:
            if reg in regs.REGS:
                self.second_reg = 1
                self.second_value = regs.REGS.index(reg)
                return
            else:
                logging.error("Not a valid register : {}".format(reg))
                exit(-1)

        if reference != None:
            if reference.startswith("#"):
                self.second_reference = reference[1:]
            else:
                logging.error("Invalid reference name -> \"{}\"".format(reference))
                exit(-1)
            return

        return

    def getSize(self):
        if self.itype == self.TYPE_INT:
            return 4
        if self.itype == self.TYPE_STR:
            return len(self.first_value)
        if self.itype == self.TYPE_FCN: # Type fcn is just a marker to an offset
            return 0
        if self.itype == self.TYPE_INS:
            return 2+(2*(4-2*self.first_reg)+(4-2*self.second_reg))

    def __str__(self):
        if self.itype == self.TYPE_INT:
            return "[TYPE_INT] {} = {}".format(self.symbol,self.first_value)
        if self.itype == self.TYPE_STR:
            return "[TYPE_STR] {} = \"{}\"".format(self.symbol,self.first_value)
        if self.itype == self.TYPE_FCN:
            return "[TYPE_FCN] {} -> {}".format(self.symbol,self.addr)
        if self.itype == self.TYPE_INS:
            return "[TYPE_INS] {} {} {}".format(self.symbol,self.first_value,self.second_value)

        logging.error("Undefined Instruction type, aborting")
        exit(-1)
