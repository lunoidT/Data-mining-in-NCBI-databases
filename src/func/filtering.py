def weightfilterwrapper(func):
    def compops(instance_dict:dict,weight:int):
        op = input("You've selected weightfilter. Please choose one of the following arguments: less, great, eq, neq\n"
                   "Eg. all values lesser/great than selected weight x or equal/not equal to selected weight x\n")
        
        if op not in ("less","great","eq","neq",):
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

@weightfilterwrapper
def weightfilter(instance_dict:dict, weight:int, op:str):
    """ Selects entries with a specific weight in dictionary.
    Dictionary structure: {(x.y):weight} """
    filtered_dict = {}

    for key in instance_dict:
        if eval(f"{instance_dict[key]} {op} {weight}"):
            filtered_dict[key] = instance_dict[key]
    return filtered_dict

def connectionfilter(pubidnames:dict, min_connections:int, op:str):
    """ Selects entries with a minimum amount of connections"""
    from func.namecombiner import combinations

    connection_dict = dict()
    for connected_instance in pubidnames:
        if len(pubidnames[connected_instance]) >= min_connections:
            connection_dict[connected_instance] = pubidnames[connected_instance]
    print(connected_instance)

    return combinations(connection_dict)

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
    
    if not namefitereddict:
        raise ValueError(f"{genename} does not exist in this file")
    
    return namefitereddict