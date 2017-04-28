# Class representing a data object
import struct

DATA_STR = 0
DATA_NUMBER = 1

class StaticData:

    def __init__(self,dtype,content):
        self.content = content
        self.dtype = dtype

    def getType(self):
        return self.dtype

    def getContent(self):
        return self.content

    def getPacked(self):
        if self.dtype = DATA_STR:
            return self.content
        if self.dtype == DATA_NUMBER:
            return struct.pack("I",self.content)
