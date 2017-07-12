import binascii
import struct
import logging
from sys import exit

import min.utils.strutils as strutils
import min.data.StaticData as sd
import min.data.ops as ops

from min.data.StaticDataHolder import StaticDataHolder
from min.data.StaticData import StaticData
from min.compiler.OpcodeBuilder import OpcodeBuilder

from min.data.Instruction import Instruction

class MinCompiler:

    def __init__(self):
        self.data = StaticDataHolder()
        self.output = b"" # Output

        self.symbols = {}
        self.resolve = []
        self.instructions = []
        self.entry = 0

    def fromFile(self,path):
        fp = open(path,"r")
        code = fp.read()
        fp.close()

        #self.fromString(code)
        self.protoInstruction(code)

    def fixRef(self,i):
        fr = i.first_reference
        sr = i.second_reference


        if fr != "":
            if fr in self.symbols:
                i.setFirstSlot(number=self.symbols[fr])
            else:
                logging.error("Undefined symbol (first arg) : {}".format(fr))
                exit(-1)
        if sr != "":
            if sr in self.symbols:
                i.setSecondSlot(number=self.symbols[sr])
            else:
                logging.error("Undefined symbol (second arg) : {}".format(sr))
                exit(-1)
        return i

    def protoInstruction(self,code):
        code = strutils.cleanCode(code)
        ip = 10 # MX + entrypoint + boundary (because python has dumb packing and adds bytes for padding, messing up with last file instructions"

        for line in code:
            toks = line.split(" ")

            op = toks[0]

            if op == "num":
                name = toks[1]
                i = Instruction(ip,symbol=name)
                i.setValue(number=int(toks[2]))
                self.instructions.append(i)
                
                self.symbols[name] = ip
                ip += i.getSize()

            if op == "str":
                name = toks[1]

                begin = line.find('"')
                line = line[begin+1:]
                end = line.find('"')
                line = line[:end]

                i = Instruction(ip,symbol=name)
                i.setValue(string=line+"\x00")
                self.instructions.append(i)
                
                self.symbols[name] = ip
                ip += i.getSize()


            if op == "fn":
                logging.debug("function {}, offset = {}".format(toks[1],ip))
                i = Instruction(ip,itype=Instruction.TYPE_FCN,symbol=toks[1])
                self.symbols[toks[1]] = ip

                self.instructions.append(i)

            if op == "ldr": 
                i = Instruction(ip,itype=Instruction.TYPE_INS,symbol=ops.ops[ops.OP_LDR])
                i.setFirstSlot(reg=toks[1])
                i.setSecondSlot(reference=toks[2])

                self.instructions.append(i)
                ip += i.getSize()

            if op == "sys":
                i = Instruction(ip,itype=Instruction.TYPE_INS,symbol=ops.ops[ops.OP_SYS])
                i.setFirstSlot(reg="$A")
                i.setSecondSlot(reg="$A")

                self.instructions.append(i)
                ip += i.getSize()

            if op == "mov":
                i = Instruction(ip,itype=Instruction.TYPE_INS,symbol=ops.ops[ops.OP_MOV])
                i.setFirstSlot(reg=toks[1])
                
                if toks[2].startswith("$"):
                    i.setSecondSlot(reg=toks[2])
                else:
                    if toks[2].startswith("0x"):
                        i.setSecondSlot(number=toks[2])
                    elif toks[2].startswith("#"):
                        name = toks[2][1:]
                        if name.replace("_","").isalpha():
                            i.setSecondSlot(reference="#"+name)
                        
                        if name.isdigit():
                            i.setSecondSlot(number=int(name))
                    else:
                        logging.error("Incorrect value in second MOV operand : {}".format(toks[2]))
                        exit(-1)

                self.instructions.append(i)
                ip += i.getSize()

            if op == "jmp":
                i = Instruction(ip,itype=Instruction.TYPE_INS,symbol=ops.ops[ops.OP_JMP])
                i.setFirstSlot(reference=toks[1])
                #i.setFirstSlot(number="0xffffffff")
                i.setSecondSlot(reg="$F")
                self.instructions.append(i)

                ip += i.getSize()

        if "main" not in self.symbols:
            logging.error("\"main\" function not found !")
            exit(-1)

        logging.info("First pass finished, now fixing references")
        
        self.instructions = [self.fixRef(i) for i in self.instructions]
        self.instructions = list(filter(lambda k:k.itype != Instruction.TYPE_FCN,self.instructions))
        
        binary_size = sum([i.getSize() for i in self.instructions])+10
        logging.info("Final binary size : {}b".format(binary_size))

        self.output += b"MX" # Magic
        self.output += struct.pack("I",self.symbols["main"]) #Entrypoint
        self.output += struct.pack("I",binary_size)

        for i in self.instructions:
            self.output += i.build()

        for i in self.instructions:
            logging.debug("{} {} sz = {}".format(i.addr,i,len(i.build())))

    
    def write(self,path):
        open(path,"wb").write(self.output)
