# Class representing a data object
import struct

DATA_STR = 0
DATA_NUM = 1

class StaticData:

    def __init__(self,dtype,content):
        self.content = content
        self.dtype = dtype

    def getType(self):
        return self.dtype

    def getContent(self):
        return self.content

    def getPacked(self):
        if self.dtype == DATA_STR:
            return bytes(self.content,"UTF-8")
        if self.dtype == DATA_NUM:
            return struct.pack("I",self.content)
