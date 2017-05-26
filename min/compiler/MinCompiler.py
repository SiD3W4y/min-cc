import min.utils.strutils as strutils

from min.data.StaticData import StaticData
import min.data.StaticData as sd

from min.data.StaticDataHolder import StaticDataHolder

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

    def build_instr(self,paramA,paramB):
        pass

    def fromString(self,code):
        code = strutils.cleanCode(code)

        self.output += b"MX"
        self.output += b"\xff\xff\xff\xff"

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

                self.data.addVar(name,StaticData(sd.DATA_STR,line))

            if op == "fn":
                self.symbols.append((toks[1],len(self.output)))

            if op == "mov":


        print(self.symbols)
        print(self.data)
