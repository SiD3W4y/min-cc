import min.data.regs as regs
import min.data.ops as ops

from min.assembly.MinInstruction import *
# Class assembling text assembly to Instruction or byte buffer

FLAG_VAL = 0
FLAG_REG = 1
FLAG_REF = 2

class Assembler:

    def __init__(self):
        self.no_arg = {
                "sys": [],
                "ret": []
                }
        
        self.single_arg = {
                "push": [FLAG_REG],
                "pop": [FLAG_REG],
                "jmp": [FLAG_VAL],
                "jne": [FLAG_VAL],
                "je": [FLAG_VAL],
                "jle": [FLAG_VAL],
                "call": [FLAG_VAL,FLAG_REG]
                }
        
        self.double_arg = {
                "add": ([FLAG_REG],[FLAG_REG,FLAG_VAL]),
                "sub": ([FLAG_REG],[FLAG_REG,FLAG_VAL]),
                "mul": ([FLAG_REG],[FLAG_REG,FLAG_VAL]),
                "ldr": ([FLAG_REG],[FLAG_REG,FLAG_VAL,FLAG_REF]),
                "ldrb": ([FLAG_REG],[FLAG_REG,FLAG_VAL,FLAG_REF]),
                "str": ([FLAG_REG],[FLAG_REG,FLAG_VAL,FLAG_REF]),
                "strb": ([FLAG_REG],[FLAG_REG,FLAG_VAL,FLAG_REF]),
                "mov": ([FLAG_REG],[FLAG_REG,FLAG_VAL,FLAG_REF]),
                "xor": ([FLAG_REG],[FLAG_REG,FLAG_VAL]),
                "and": ([FLAG_REG],[FLAG_REG,FLAG_VAL]),
                "or": ([FLAG_REG],[FLAG_REG,FLAG_VAL]),
                "shr": ([FLAG_REG],[FLAG_REG,FLAG_VAL]),
                "shl": ([FLAG_REG],[FLAG_REG,FLAG_VAL])
                }
    
    def parseArg(self,data):
        if data.startswith("#"):
            return OpArg(ArgType.ARG_REF,data[1:])
        if data.startswith("0x"):
            return OpArg(ArgType.ARG_VAL,int(data,16))
        if data.startswith("$"):
            if data[1:] not in regs.REGS:
                print("Error : Register {} does not exist".format(data[1:]))
                return None
            return OpArg(ArgType.ARG_REG,regs.REGS.index(data[1:]))

        return None


    def buildNone(self,op):
        """ We build an instruction of the form [op reg reg] because it is smaller """
        return MinInstruction(ops.ops.index(op.upper()),OpArg(ArgType.ARG_REG,0),OpArg(ArgType.ARG_REG,0))
    
    def buildSingle(self,op,arg,flags):
        """ The flags are the authorized parameter types for our first argument """
        arg_obj = self.parseArg(arg)

        if arg_obj.getType() not in flags:
            print("Error : Wrong argument type \"{}\" for opcode {}".format(arg,op))
            return None

        return MinInstruction(ops.ops.index(op.upper()),arg_obj,OpArg(ArgType.ARG_REG,0))

    def buildDouble(self,op,arg1,arg2,flags1,flags2):
        """ So many arguments :( """

        arg1_obj = self.parseArg(arg1)
        arg2_obj = self.parseArg(arg2)

        if arg1_obj.getType() not in flags1:
            print("Error : First argument has a wrong type \"{}\" for opcode {}".format(arg1,op))
            return None
        
        if arg2_obj.getType() not in flags2:
            print("Error : Second argument has a wrong type \"{}\" for opcode {}".format(arg2,op))
            return None

        return MinInstruction(ops.ops.index(op.upper()),arg1_obj,arg2_obj)



    def assembleInst(self,data):
        """ Central function creating Instruction object from input assembly """
        toks = data.strip().split(" ")
        tok_number = len(toks)
        
        if tok_number == 0:
            print("Error : Not opcode given")
            return None
        if tok_number == 1:
            if toks[0] not in self.no_arg:
                print("Error : Opcode {} does not exist or has wrong number of arguments".format(toks[0]))
                return None

            return self.buildNone(toks[0])

        if tok_number == 2:
            if toks[0] not in self.single_arg:
                print("Error : Opcode {} does not exist or has wrong number of arguments".format(toks[0]))
                return None

            return self.buildSingle(toks[0],toks[1],self.single_arg[toks[0]])

        if tok_number == 3:
            if toks[0] not in self.double_arg:
                print("Error : Opcode {} does not exist or has wrong number of arguments".format(toks[0]))
                return None
            
            flags1,flags2 = self.double_arg[toks[0]]
            
            return self.buildDouble(toks[0],toks[1],toks[2],flags1,flags2)
        
        return None
