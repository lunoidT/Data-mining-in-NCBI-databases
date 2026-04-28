def filterwrapper(func):
    def compops(instance_dict:dict, weight:int):
        op = input(f"You've chosen the {str(func).split(' ')[1]}. Please choose one of the following arguments for the filter: less, great, eq, neq\n"
                   "Eg. all values lesser/great than selected weight x or equal/not equal to amount of connections, etc.x\n")
        
        if op not in ("less", "great", "eq", "neq",):
            raise ValueError("The filter isn't filtering due to an insufficient amount of arguments")

        # find and return comperative operator for weightfiltering
        if op == "less":
            return func(instance_dict, weight, "<")
        elif op == "great":
            return func(instance_dict, weight, ">")
        elif op == "eq":
            return func(instance_dict, weight, "==")
        elif op == "neq":
            return func(instance_dict, weight, "!=")      

    return compops

@filterwrapper
def weightfilter(instance_dict:dict, weight:int, op:str):
    """ Selects entries with a specific weight in dictionary.
    Dictionary structure: {(x.y):weight} """
    filtered_dict = {}

    for key in instance_dict:
        if eval(f"{instance_dict[key]} {op} {weight}"):
            filtered_dict[key] = instance_dict[key]
    return filtered_dict, op

@filterwrapper
def connectionfilter(pubidnames:dict, min_connections:int, op:str):
    """ Selects entries with a specific amount of connections"""
    from func.namecombiner import combinations

    connection_dict = dict()
    for connected_instance in pubidnames:
        if eval(f"{len(pubidnames[connected_instance])} {op} {min_connections}"):
            connection_dict[connected_instance] = pubidnames[connected_instance]

    return combinations(connection_dict), op

def namefilter(instancedict:dict, genename:int):
    """ Selects all connections of entries with a specific mentioned gene-name"""
        
    # find and return comperative operator for weightfiltering
    op = input("You've selected namefilter. Please choose one of the following arguments: including, excluding\n"
        "E.g. all entries including/excluding this genename\n")

    if op not in ("including","excluding"):
            raise ValueError("The filter isn't filtering due to an insufficient amount of arguments")

    namefitereddict = dict()
    if op == "including":
        for instance in instancedict:
            if genename in instance:
                namefitereddict[instance] = instancedict[instance]
    elif op == "excluding":
        for instance in instancedict:
            for instance in instancedict:
                if genename not in instance:
                    namefitereddict[instance] = instancedict[instance]
            
    if instancedict and not namefitereddict:
        print(f"Warning! The file is now empty due to your filtering preferences. It wasn't before!")    
    
    return namefitereddict, op

@filterwrapper
def sumofconnectionfilter(instancedict:dict, targetsum:int, op:str):
    """ Computes the weighed sum of connections and filters accordingly"""
    connectiondict = dict()

    for connected_instance in instancedict:
        if (connected_instance[0] in connectiondict):
            connectiondict[connected_instance[0]] += int(instancedict[connected_instance])
        else:
            connectiondict[connected_instance[0]] = int(instancedict[connected_instance])
        if (connected_instance[1] in connectiondict):
            connectiondict[connected_instance[1]] += int(instancedict[connected_instance])
        else:
            connectiondict[connected_instance[1]] = int(instancedict[connected_instance])

    for key in list(instancedict.keys()):
        print(key, "\t", instancedict[key])

        if not eval(f"{connectiondict[key[0]]} {op} {targetsum}"):
            del instancedict[key]
        elif not eval(f"{connectiondict[key[1]]} {op} {targetsum}"):
            del instancedict[key]

    print(instancedict)

    return instancedict, op