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

        self.symbols = [] 
        self.resolve = []
        self.entry = 0

    def fromFile(self,path):
        fp = open(path,"r")
        code = fp.read()
        fp.close()

        self.fromString(code)


    def fromString(self,code):
        code = strutils.cleanCode(code)

        header = b"MX"
        header += b"\xff\xff\xff\xff"

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
                self.symbols.append((toks[1],len(self.output)))

            if op == "ldr":
                b = OpcodeBuilder(self,ops.OP_LDR)
                b.setFirstReg(toks[1])
                b.setSecondValue(toks[2])

                generated = b.build()
                self.output += generated

            if op == "sys":
                self.output += struct.pack("bb",ops.OP_SYS,0)

        compiled = header + self.data.getCompiled() + self.output
        v = open("result.bin","wb")
        v.write(compiled)
