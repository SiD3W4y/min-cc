### Min-VM : Small virtual machine

## VM Architecture

Small vm with a few registers :

32bit regs
A,B,C,D,E and F : General purpose registers
I		: Instruction pointer
S		: Stack pointer
B		: Base pointer

8bit flags
Z		: Comp flag
H		: Higher flah
L		: Lower flag


User definable stack size

## Bytecode executable format (.mx)

- 2b magic "MX"
- 4b code section offset
- 4b code entrypoint
- [static data]

4bytes

## Assembly instructions

# Syntax
Based on prefixes, $<register>, 0x<hexnum>, #<name> (data address)

# Ops
add reg/addr reg/number
sub reg/addr reg/number
mul reg/addr reg/number

mov reg reg/number

ldr reg addr ; load 32bit value at address into reg

push reg
pop reg

cmp reg number
cmp reg reg

jmp reg/addr
jne reg/addr
je  reg/addr
jle reg/addr
jbe reg/addr

sys


# Syscalls
A contains the syscall number

0 = write, B with data to write and C with length (limited to stdout for now)
