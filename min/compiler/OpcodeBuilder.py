# Opcode builder : Object building opcodes in a simple fashion
import struct

import min.data.regs as regs 

class OpcodeBuilder:

    def __init__(self,compiler):
        self.symbols = compiler.symbols
        
        self.first_arg = 0
        self.second_arg = 0

        # Switches to determine whether the argument is a register
        self.first_reg = 0
        self.second_reg = 0

    def setFirstReg(self,reg):
        reg = reg[1:]

        if reg in regs.REGS:
            self.first_reg = 1
            self.first_arg = reg
        else:
            raise ValueError("Register name not valid -> {}".format(reg))

    def setSecondReg(self,reg):
        reg = reg[1:]

        if reg in regs.REGS:
            self.second_reg = 1
            self.second_arg = reg
        else:
            raise ValueError("Register name not valid -> {}".format(reg))

    def setFirstValue(self,val):
        if val.startswith("#"):
            # Data label
            name = val[1:]
            if name in self.symbols:
                self.first_arg = self.symbols[name]
            else:
                raise ValueError("Unknown data label -> {}".format(name)
        if val.startswith("0x"):
            self.first_arg = int(val,16)

    def setSecondValue(self,val):
        if val.startswith("#"):
            # Data label
            name = val[1:]
            if name in self.symbols:
                self.second_arg = self.symbols[name]
            else:
                raise ValueError("Unknown data label -> {}".format(name)
        if val.startswith("0x"):
            self.second_arg = int(val,16)
