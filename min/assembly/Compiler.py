from min.assembly.Assembler import Assembler
from min.assembly.MinInstruction import Serializable

import min.utils.strutils as strutils

class DataType:
    DATA_STRING = 0
    DATA_BYTES = 1
    DATA_NUMBER = 2
    DATA_SLOT = 3

class DataObject(Serializable):

    def __init__(self,data_type,value):
        self.data_type = data_type
        self.value = value

    def getType(self):
        return self.data_type

    def setType(self,new_type):
        self.data_type = new_type

    def getValue(self):
        return self.value

    def setValue(self,val):
        self.value = val

    def serialize(self):
        pass
        

"""
The compiler handles references, position and data objects while the Assembler does the dirty work
"""

class Compiler:

    def __init__(self):
        self.symbols = {}
        self.parts = []
        self.output = b""
        self.position = 10 # Magic 'MX' + entrypoint addr + binsize

    def processString(self,line):
        begin = line.find('"')+1
        end = begin
        opened = True # Boolean having the current status for quoted string open/closed status

        for i in range(len(line[begin:])):
            if line[i] == '"' and line[i-1] != '\\':
                opened = not opened
            end += 1

        if opened == True:
            raise Exception("Error : Quoted string not closed")

        result = bytes(line[begin:end-1],"utf-8").decode("unicode_escape")
        return result

    def processNum(self,num):
        if num.startswith("0x"):
            return int(num,16)
        return int(num)

    def fromString(self,data):
        code = strutils.cleanCode(data)

        for line in code:
            tokens = line.split(" ")

            if line.startswith("str"):
                self.symbols[tokens[1]] = position
                string = bytes(self.processString(line),"utf-8")
                self.parts.append(DataObject(DataType.DATA_STRING,string))
                self.position += len(string)

            if line.startswith("slot"):
                self.symbols[toks[1]] = position
                self.parts.append(DataObjects(DataType.DATA_NUMBER,self.processNum(toks[2])))
                self.position += 2 # numbers like regs and addrs are u16

