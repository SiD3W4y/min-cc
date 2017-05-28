import binascii
import struct

import min.utils.strutils as strutils
import min.data.StaticData as sd
import min.data.ops as ops

from min.data.StaticDataHolder import StaticDataHolder
from min.data.StaticData import StaticData
from min.compiler.OpcodeBuilder import OpcodeBuilder

class MinCompiler:

    def __init__(self):
        self.data = StaticDataHolder()
        self.output = b"" # Output

        self.symbols = {}
        self.resolve = []
        self.entry = 0

    def fromFile(self,path):
        fp = open(path,"r")
        code = fp.read()
        fp.close()

        self.fromString(code)


    def fromString(self,code):
        code = strutils.cleanCode(code)

        for line in code:
            toks = line.split(" ")

            op = toks[0]

            if op == "num":
                name = toks[1]
                self.data.addVar(name,StaticData(sd.DATA_NUM,int(toks[2])))

            if op == "str":
                name = toks[1]

                begin = line.find('"')
                line = line[begin+1:]
                end = line.find('"')
                line = line[:end]

                self.data.addVar(name,StaticData(sd.DATA_STR,line+'\x00'))

            if op == "fn":
                self.symbols[toks[1]] = len(self.output)+len(self.data.getCompiled())+6 # 6 is header length

            if op == "ldr":
                b = OpcodeBuilder(self,ops.OP_LDR)
                b.setFirstReg(toks[1])
                b.setSecondValue(toks[2])

                self.output += b.build()

            if op == "sys":
                self.output += struct.pack("bb",ops.OP_SYS,0)

            if op == "mov":
                b = OpcodeBuilder(self,ops.OP_MOV)
                b.setFirstReg(toks[1])
                
                if toks[2].startswith("$"):
                    b.setSecondReg(toks[2])
                else:
                    b.setSecondValue(toks[2])
                
                self.output += b.build()

            if op == "jmp":
                loc = toks[1]

                if loc not in self.symbols:
                    raise ValueError("Symbol not found -> {}".format(loc))
                else:
                    b = OpcodeBuilder(self,ops.OP_JMP)
                    b.setFirstValue(strutils.hexFromInt(self.symbols[loc]))

                    self.output += b.buildSingle()


        if "main" not in self.symbols:
            raise ValueError("No entrypoint found")

        header = b"MX"
        header += struct.pack("i",self.symbols["main"])
        header += struct.pack("i",len(self.data.getCompiled())) # Knowing how much data to skip while reading

        compiled = header + self.data.getCompiled() + self.output
        v = open("result.bin","wb")
        v.write(compiled)
