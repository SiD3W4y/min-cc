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
        begin = line.find('"')
        end = begin
        opened = True # Boolean having the current status for quoted string open/closed status

        for i in range(len(line[begin:])):
            if line[i] == '"' and line[i-1] != '\\':
                opened = not opened
                end += 1

        if opened == True:
            raise Exception("Error : Quoted string not closed")

        result = bytes(line[begin:end],"utf-8").decode("unicode_escape")
        
        return result


    def fromString(self,data):
        code = strutils.cleanCode(data)

        for line in code:
            if line.startswith("str"):
                self.processString(line)
