
# Object replacing the bloated min.data.Instruction

ARG_VAL = 0
ARG_REG = 1
ARG_REF = 2

class OpRef(OpArg):
    def __init__(self,argtype,val):
        self.value = val
        self.argtype = argtype
    
    def getType(self):
        return self.argtype

    def getValue(self):
        return self.value

    def setValue(self,val):
        self.value = val

class MinInstruction:

    def __init__(self,op,arg1,arg2):
        self.first_arg = arg1
        self.second_arg = arg2

    def getFirst(self):
        return self.first_arg

    def getSecond(self):
        return self.second_arg

    def setFirst(self,arg):
        self.first_arg = arg

    def setSecond(self,arg):
        self.second_arg = arg
