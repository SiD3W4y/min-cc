

class MinCompiler:

    def __init__(self):
        self.data = [] # List containing program static data
        self.output = "" # Output

    def fromFile(self,path):
        fp = open(path,"r")
        code = fp.read()
        fp.close()

        self.fromString(code)

    def fromString(self,code):
        pass
