

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
