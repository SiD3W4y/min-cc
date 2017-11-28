from min.assembly.Assembler import Assembler
from min.assembly.MinInstruction import MinInstruction,ArgType
from min.data.Serializable import Serializable

import min.utils.strutils as strutils

import struct

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
        if self.data_type == DataType.DATA_STRING:
            return bytes(self.value)
        if self.data_type == DataType.DATA_SLOT:
            return bytes(self.value)
        if self.data_type == DataType.DATA_NUMBER:
            return struct.pack("I",self.value)
        if self.data_type == DataType.DATA_BYTES:
            return self.value

"""
The compiler handles references, position and data objects while the Assembler does the dirty work
"""

class Compiler:

    def __init__(self):
        self.symbols = {}
        self.parts = []
        self.output = b""
        self.assembler = Assembler()
        self.position = 10 # Magic 'MX' + entrypoint addr + binsize

    def processString(self,line):
        begin = line.find('"')+1
        end = begin
        opened = True # Boolean having the current status for quoted string open/closed status

        for i in range(len(line[begin:])):
            if line[i+begin] == '"' and line[(i+begin)-1] != '\\':
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

    def processBytes(self,line):
        begin = line.find("[")
        end = line.find("]")

        if begin == -1 or end == -1:
            raise Exception("Missing square brackets in bytes expression")

        begin += 1
        result = [self.processNum(n.strip()) for n in line[begin:end].split(",")]

        if len(list(filter(lambda x: x < 0 or x > 255,result))) > 0:
            raise Exception("Byte outside of 0 < n < 255 range")

        return bytes(result)

    def fromString(self,data):
        code = strutils.cleanCode(data)

        for line in code:
            tokens = line.split(" ")

            if line.startswith("str"):
                self.symbols[tokens[1]] = self.position
                string = bytes(self.processString(line),"utf-8")
                self.parts.append(DataObject(DataType.DATA_STRING,string))
                self.position += len(string)

            elif line.startswith("slot"):
                self.symbols[tokens[1]] = self.position
                slot_size = self.processNum(tokens[2])
                self.parts.append(DataObjects(DataType.DATA_SLOT,slot_size))
                self.position += slot_size

            elif line.startswith("num"):
                self.symbols[tokens[1]] = self.position
                self.parts.append(DataObject(DataType.DATA_NUMBER,self.processNum(tokens[2])))
                self.position += 4 # Numbers are u32

            elif line.startswith("bytes"):
                self.symbols[tokens[1]] = self.position
                resbytes = self.processBytes(line)
                self.parts.append(DataObject(DataType.DATA_BYTES,resbytes))
                self.position += len(resbytes)
            
            elif line.startswith("fn"):
                self.symbols[tokens[1]] = self.position

            else:
                ins = self.assembler.assembleInst(line)
                self.parts.append(ins)
                self.position += ins.getSize() 



