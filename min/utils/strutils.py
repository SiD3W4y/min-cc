import binascii

def cleanCode(data):
    data = data.split("\n")
    data = list(filter(lambda k: not k.startswith(";"),data))
    new_data = []

    for line in data:
        line = line.strip(' \t\n')
        line = line.replace('\t',' ')
        
        if(len(line) > 1):
            new_data.append(line)

    return new_data

def hexFromInt(value):
    """This is a hack to pass integers to opcode builder"""
    return '0x{0:04x}'.format(value)
