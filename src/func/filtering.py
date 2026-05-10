# for runtime analysis:
# n will indicate genenames 
# m will indicate pubmedID's
# k will indicate amount of connections

def filterwrapper(func):
    def compops(input_dict:dict, weight:int):
        op = input(f"You've chosen the {str(func).split(' ')[1]}. Please choose one of the following arguments for the filter: less, great, eq, neq\n"
                   "Eg. all values lesser/greater than selected weight x or equal/not equal to amount of connections, etc.\n")
        
        # To confirm valid input and show program hasn't frozen
        print(f"You chose {op}. Initiating:")

        # If the input dictionary is empty, raise error
        if input_dict == {}:
            raise ValueError("Filter recived an empty dict. No filtering can be done.")

        # O(1) due to membership test in a set
        if op not in ("less", "great", "eq", "neq"): 
            raise ValueError(f"The filter isn't filtering due to wrongful argument {op}")

        # find and return comparative operator for weightfiltering
        if op == "less":
            return func(input_dict, weight, "<")
        elif op == "great":
            return func(input_dict, weight, ">")
        elif op == "eq":
            return func(input_dict, weight, "==")
        elif op == "neq":
            return func(input_dict, weight, "!=")      

    # The worst case here within the curriculum is O(1)
    return compops

# O(1) from filterwrapper
@filterwrapper
def weightfilter(instance_dict:dict, weight:int, op:str):
    """ Selects entries with a specific weight in dictionary."""
    filtered_dict = {}

    # compare each weight to target (if "op == less"" this means: len(pubidnames[connected_instance])} < {min_connections})
    # O(n)
    for key in instance_dict: 
        if eval(f"{instance_dict[key]} {op} {weight}"):
            filtered_dict[key] = instance_dict[key]

    # Overall runtime O(n+1). Simplified O(n)
    return filtered_dict, op

# O(1) from filterwrapper
@filterwrapper
def connectionfilter(pubidnames:dict, min_connections:int, op:str):
    """ Selects entries with a specific amount of connections."""
    from func.namecombiner import combinations

    # creates the instance_dict (here connection_dict to differentiate) whilst filtering
    connection_dict = dict()

    # O(m) (m due to us looping over pubIDs instead of names from the instance_dict)
    for connected_instance in pubidnames:
        if eval(f"{len(pubidnames[connected_instance])} {op} {min_connections}"):
            connection_dict[connected_instance] = pubidnames[connected_instance]

    # creates a dictionary for all combinations with the remaining entires after filtering 
    # O(m*k^2) will be the worst case scenario here. See namecombiner.py for distinctions between cases.
    combined_dict = combinations(connection_dict)

    # Overall runtime O(m*k^2 + m + 1). Simplified: O(m*k^2)
    return (combined_dict), op

def namefilter(instancedict:dict, genename:int):
    """ Selects all connections of entries with a specific mentioned gene-name."""
        
    # find and return comperative operator for weightfiltering
    op = input("You've selected namefilter. Please choose one of the following arguments: including, excluding\n"
        "E.g. all entries including/excluding this genename\n")

    # O(1)
    if op not in ("including","excluding"):
            raise ValueError("The filter isn't filtering due to  wrongful arguments")

    namefitereddict = dict()
    if op == "including":
        # O(n)
        for instance in instancedict:
            if genename in instance:
                namefitereddict[instance] = instancedict[instance]
    elif op == "excluding":
        # O(n)
        for instance in instancedict:
            if genename not in instance:
                namefitereddict[instance] = instancedict[instance]

    # This "error" message helps the user realize that a gene perhaps is more/less prevalent than foreseen and lost to filtering
    if instancedict and not namefitereddict:
        print(f"Warning! The file is now empty due to your filtering preferences. It wasn't before!")    
    
    # Overall runtime O(2n+1). After simplifying: O(n)
    return namefitereddict, op

# O(1) from filterwrapper
@filterwrapper
def sumofconnectionfilter(instancedict:dict, targetsum:int, op:str):
    """ Computes the weighed sum of connections and filters accordingly."""
    connectiondict = dict()

    # Due to the three columns in outputfile (and therefore connectiondict) "gene1, gene2, weight", both [0] and [1] are investigated
    # O(n) 
    for connected_instance in instancedict:
        if (connected_instance[0] in connectiondict):
            connectiondict[connected_instance[0]] += int(instancedict[connected_instance])
        else:
            connectiondict[connected_instance[0]] = int(instancedict[connected_instance])
        if (connected_instance[1] in connectiondict):
            connectiondict[connected_instance[1]] += int(instancedict[connected_instance])
        else:
            connectiondict[connected_instance[1]] = int(instancedict[connected_instance])

    # all connections to genes with unacceptible targetsum are removed 
    # O(n)
    for key in list(instancedict.keys()):
        if not eval(f"{connectiondict[key[0]]} {op} {targetsum}"):
            del instancedict[key]
        elif not eval(f"{connectiondict[key[1]]} {op} {targetsum}"):
            del instancedict[key]

    # Overall runtime O(2n + 1). After simplifying: O(n)
    return instancedict, op