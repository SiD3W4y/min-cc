
# Object replacing the bloated min.data.Instruction

class ArgType:
    ARG_VAL = 0
    ARG_REG = 1
    ARG_REF = 2

class OpArg:
    def __init__(self,argtype,val):
        self.value = val
        self.argtype = argtype
    
    def getType(self):
        return self.argtype

    def getValue(self):
        return self.value

    def setValue(self,val):
        self.value = val
    
    def __str__(self):
        return "[ArgType : {} -> Value : {}]".format(self.argtype,self.value)

class MinInstruction:

    def __init__(self,op,arg1,arg2,position=0):
        self.op = op
        self.first_arg = arg1
        self.second_arg = arg2
        self.position = position

    def getFirst(self):
        return self.first_arg

    def getSecond(self):
        return self.second_arg

    def setFirst(self,arg):
        self.first_arg = arg

    def setSecond(self,arg):
        self.second_arg = arg

    def setPosition(self,val):
        self.position = val

    def getPosition(self):
        return self.position

    def getOpcode(self):
        return self.op

    def setOpcode(self,val):
        self.op = val

    def __eq__(self,other):
        if isinstance(self,type(other)):
            op_eq = self.op == other.getOpcode()
            arg1_type_eq = self.first_arg.getType() == other.getFirst().getType()
            arg2_type_eq = self.second_arg.getType() == other.getSecond().getType()
            arg1_val_eq = self.first_arg.getValue() == other.getFirst().getValue()
            arg2_val_eq = self.first_arg.getValue() == other.getFirst().getValue()

            return (op_eq and arg1_type_eq and arg2_type_eq and arg1_val_eq and arg2_val_eq)
        return False

    def __str__(self):
        return "{} : {} {}".format(self.op,self.first_arg,self.second_arg)
