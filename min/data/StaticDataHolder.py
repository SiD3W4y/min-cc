# Class managing static variables

class StaticDataHolder:
    
    def __init__(self):
        self.compiled = b""
        self.vars = {}
        self.offset = 6 # 2b magic, 4b entrypoint offset

    def addVar(self,name,var):
        self.vars[name] = self.offset
        self.offset += len(var.getPacked())
        
        self.compiled += var.getPacked()

    def getVars(self):
        return self.vars

    def getCompiled(self):
        return self.compiled

    def __str__(self):
        return str(self.vars)
