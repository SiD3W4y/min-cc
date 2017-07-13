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

## Instruction coverage
* r = reg
* a = addr
* n = number
* Instructions :
    * [x] **add** {r} {r,n} 
    * [x] **sub** {r} {r,n} 
    * [x] **mul** {r} {r,n}
    * [x] **mov** {r} {r,n}
    * [x] **ldr** {r} {a}
    * [ ] **ldrb** {r} {a}
    * [ ] **str** {r} {a}
    * [ ] **strb** {r} {a}
    * [ ] **push** {r} 
    * [ ] **pop** {r}
    * [x] **cmp** {r} {r,n}
    * [x] **jmp** {a}
    * [x] **jne** {a}
    * [x] **je** {a}
    * [x] **jle** {a}
    * [x] **jbe** {a}
    * [x] **sys**
    * [x] **xor** {r} {r,n}
    * [x] **and** {r} {r,n}
    * [x] **or** {r} {r,n}
    * [x] **shr** {r} {r,n}
    * [x] **shl** {r} {r,n}

# Syscalls

| syscall | A | B | C | D | E | F |
|:---------:|:---:|:---:|:---:|:---:|:---:|:---:|
| **write**   | 0x00 | fd | buff | size | X | X |
| **read**    | 0x01 | fd | buff | size | X | X |
| **exit**    | 0x02 | exit_code | X | X | X | X |
