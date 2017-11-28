import struct

import min.data.ops as ops
from min.data.Serializable import Serializable

# Object replacing the bloated min.data.Instruction

class ArgType:
    ARG_VAL = 0
    ARG_REG = 1
    ARG_REF = 2

class OpArg(Serializable):
    def __init__(self,argtype,val):
        super().__init__()
        self.value = val
        self.argtype = argtype
    
    def getType(self):
        return self.argtype

    def getValue(self):
        return self.value

    def setValue(self,val):
        self.value = val
    
    def setType(self,new_type):
        self.argtype = new_type

    def __str__(self):
        return "[ArgType : {} -> Value : {}]".format(self.argtype,self.value)

    def serialize(self):
        if self.argtype == ArgType.ARG_REG:
            return struct.pack("H",self.value)
        if self.argtype == ArgType.ARG_VAL:
            return struct.pack("I",self.value)
        if self.argtype == ArgType.ARG_REF:
            raise Exception("Error : Reference to \"{}\" must be resolved before assembling".format(self.value))
        return None

class MinInstruction(Serializable):
    def __init__(self,op,arg1,arg2,position=0):
        super().__init__()
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

    def getSize(self):
        arg1_type = self.first_arg.getType()
        arg2_type = self.second_arg.getType()
        size = 2 # Opcodde + info byte

        if arg1_type in [ArgType.ARG_REF,ArgType.ARG_VAL]:
            size += 4
        else:
            size += 2

        if arg2_type in [ArgType.ARG_REF,ArgType.ARG_VAL]:
            size += 4
        else:
            size += 2

        return size

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

    def serialize(self):
        arg1_type = self.first_arg.getType()
        arg2_type = self.second_arg.getType()

        if arg1_type == ArgType.ARG_REF or arg2_type == ArgType.ARG_REF:
            print("Error : References must be fixed before compilation")
            return None

        result = b""
        info_byte = int(arg2_type << 1 | arg1_type)

        result += struct.pack("B",self.op)
        result += struct.pack("B",info_byte)
        result += self.first_arg.serialize()
        result += self.second_arg.serialize()

        return result
