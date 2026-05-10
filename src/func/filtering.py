from func.progress_bar import progress_bar
# For runtime analysis:
# n will indicate genenames 
# m will indicate pubmedID's
# k will indicate amount of connections

def progresslength(func):
    def progressparameter(input_dict:dict, parameter):

        # Variables for progress bar
        prog_len = [0,len(input_dict)]

        return func(input_dict,parameter,prog_len)
    return progressparameter

def filterwrapper(func):
    def compops(input_dict:dict, weight:int, prog_len:list[int,int]):
        op = input(f"You've chosen the {str(func).split(' ')[1]}. Please choose one of the following arguments for the filter: less, great, eq, neq\n"
                   "Eg. all values lesser/greater than selected weight x or (not) equal to amount of connections, etc.\n")
        
        # To confirm valid input and show program hasn't frozen
        print(f"You chose {op}. Initiating:")

        # If the input dictionary is empty, raise error
        if input_dict == {}:
            raise ValueError("Filter recived an empty dict. No filtering can be done.")

        if op not in {"less", "great", "eq", "neq"}: 
            raise ValueError(f"The filter isn't filtering due to wrongful argument {op}")

        # find and return comparative operator for weightfiltering
        if op == "less":
            return func(input_dict, weight, "<", prog_len)
        elif op == "great":
            return func(input_dict, weight, ">", prog_len)
        elif op == "eq":
            return func(input_dict, weight, "==", prog_len)
        elif op == "neq":
            return func(input_dict, weight, "!=", prog_len)      

    # The worst case here within the curriculum is O(1)
    return compops


# O(1) from filterwrapper
@progresslength
@filterwrapper
def weightfilter(instance_dict:dict, weight:int, op:str, prog_len:list[int,int]):
    """ Selects entries with a specific weight in dictionary."""
    filtered_dict = {}

    # compare each weight to target (if "op == less"" this means: len(pubidnames[connected_instance])} < {min_connections})
    # O(k)
    for key in instance_dict: 
        prog_len[0] += 1
        if eval(f"{instance_dict[key]} {op} {weight}"):
            filtered_dict[key] = instance_dict[key]
        progress_bar(prog_len[0],prog_len[1])

    # Overall runtime O(k+1). Simplified O(k)
    return filtered_dict, op

# O(1) from filterwrapper
@progresslength
@filterwrapper
def connectionfilter(pubidnames:dict, min_connections:int, op:str, prog_len:list[int,int]):
    """ Selects entries with a specific amount of connections to the same common pubmedID."""
    from func.namecombiner import combinations

    # creates the instance_dict (here connection_dict to differentiate) whilst filtering
    connection_dict = dict()

    # O(m) (m due to us looping over pubIDs instead of connections from the instance_dict)
    for connected_instance in pubidnames:
        prog_len[0] += 1
        if eval(f"{len(pubidnames[connected_instance])} {op} {min_connections}"):
            connection_dict[connected_instance] = pubidnames[connected_instance]
            progress_bar(prog_len[0],prog_len[1])
        

    # creates a dictionary for all combinations with the remaining entires after filtering 
    try:
        #  O(n^2 * m) will be the worst case scenario here. See namecombiner.py for distinctions between cases.
        combined_dict = combinations(connection_dict)
    # if all entries are removed by filter, combinations will raise ValueError
    except ValueError:
        combined_dict = {}

    # Overall runtime O(n^2 * m + m + 1). Simplified: O(n^2 * m)
    return (combined_dict), op

@progresslength
def namefilter(instancedict:dict, genename:int, prog_len:list[int,int]):
    """ Selects all connections of entries with a specific mentioned gene name."""
        
    # find and return comperative operator for weightfiltering
    op = input("You've selected namefilter. Please choose one of the following arguments: including, excluding\n"
        "E.g. all entries including/excluding this genename\n")

    if op not in {"including","excluding"}:
            raise ValueError("The filter isn't filtering due to  wrongful arguments")

    namefitereddict = dict()
     # O(k)
    for instance in instancedict:
        if op == "including":
            # O(1) since the instance list always has length of 2
            if genename in instance:
                namefitereddict[instance] = instancedict[instance]

        elif op == "excluding":
            # O(1), as mentioned above
            if genename not in instance:
                namefitereddict[instance] = instancedict[instance]

        prog_len[0] += 1
        progress_bar(prog_len[0],prog_len[1])

    # This "error" message helps the user realize that a gene perhaps is more/less prevalent than foreseen and lost to filtering
    if instancedict and not namefitereddict:
        print(f"Warning! The file is now empty due to your filtering preferences. It wasn't before!")    
    
    # Overall runtime O(k+1). After simplifying: O(k)
    return namefitereddict, op

# O(1) from filterwrapper
@progresslength
@filterwrapper
def sumofconnectionfilter(instancedict:dict, targetsum:int, op:str,prog_len:list[int,int]):
    """ Computes the weighed sum of connections and filters accordingly for each gene entry."""
    connectiondict = dict()

    # Due to the three columns in outputfile (and therefore connectiondict) "gene1, gene2, weight", both [0] and [1] are investigated
    # O(k) 
    print("Be aware that this filter requires a substantial amount of time")
    for connected_instance in instancedict:
        prog_len[0] += .5
        for i in range([0,1]):
            if (connected_instance[i] in connectiondict):
                connectiondict[connected_instance[i]] += int(instancedict[connected_instance])
            else:
                connectiondict[connected_instance[i]] = int(instancedict[connected_instance])
        progress_bar(prog_len[0],prog_len[1])

    # All connections to genes with unacceptable targetsum are removed 
    # O(k)
    for key in list(instancedict.keys()):
        prog_len[0] += .5
        if not eval(f"{connectiondict[key[0]]} {op} {targetsum}"):
            del instancedict[key]
        elif not eval(f"{connectiondict[key[1]]} {op} {targetsum}"):
            del instancedict[key]
        progress_bar(prog_len[0],prog_len[1])

    # Overall runtime O(2k). After simplifying: O(k)
    return instancedict, op