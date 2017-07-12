### Min-VM : Small virtual machine

## Usage
```
usage: mcc.py [-h] [-d] [-i INPUT_FILE] [-o OUTPUT_FILE]

Assembler/compiler for min assembly language

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enables debugging information
  -i INPUT_FILE, --input INPUT_FILE
                        set input file
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        set output file (default -> a.mx)
```

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
- 4b code entrypoint
- 4b binary size
- [data]

### Opcode format
```
[OP][MODE][FIRST_ARG][SECOND_ARG]
 1    1       2/4       2/4
```

Mode is a byte representing arg type (reg vs addr/value), it is a mask of two bits, bit 0 for arg 1 and bit 1 for arg 2

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
