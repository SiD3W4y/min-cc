import unittest

from min.assembly.MinInstruction import *
from min.assembly.Assembler import *

import min.data.ops


class AssemblyTest(unittest.TestCase):

    def test_instruction_comparison(self):
        a1 = MinInstruction(0x2,OpArg(ArgType.ARG_REG,0),OpArg(ArgType.ARG_REG,0))
        a2 = MinInstruction(0x2,OpArg(ArgType.ARG_REG,0),OpArg(ArgType.ARG_REG,0))
        
        return self.assertEqual(a1,a2)

    def test_assemble_noarg(self):
        asm = Assembler()
        a2 = MinInstruction(ops.OP_RET,OpArg(ArgType.ARG_REG,0),OpArg(ArgType.ARG_REG,0))

        return self.assertEqual(a2,asm.assembleInst("ret"))
    
    def test_assemble_single_arg1(self):
        asm = Assembler()
        a2 = MinInstruction(ops.OP_CALL,OpArg(ArgType.ARG_REG,1),OpArg(ArgType.ARG_REG,0))

        return self.assertEqual(a2,asm.assembleInst("call $B"))

    def test_assemble_double_args(self):
        asm = Assembler()
        
        target = MinInstruction(ops.OP_MOV,OpArg(ArgType.ARG_REG,1),OpArg(ArgType.ARG_VAL,0xff))
        generated = asm.assembleInst("mov $B 0xff")

        return self.assertEqual(target,generated)



if __name__ == '__main__':
    unittest.main()
