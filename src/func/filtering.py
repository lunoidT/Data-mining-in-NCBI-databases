from func.progress_bar import progress_bar
# For runtime analysis:
# n will indicate genenames 
# m will indicate pubmedID's
# k will indicate amount of connections

def progresslength(func):
    #  parameter can be either a string or an integer depending on which filter it's used on
    def progressparameter(input_dict:dict, parameter):

        # Variables for progress bar
        prog_len = [0,len(input_dict)]

        return func(input_dict,parameter,prog_len)
    return progressparameter

def filterwrapper(func):
    def compops(input_dict:dict, weight:int, prog_len:list[int,int]):
        op = input(f"You've chosen the {str(func).split(' ')[1]}. Please choose one of the following arguments for the filter: less, great, eq, neq\n"
                   "Eg. all values lesser/greater than selected weight x or (not) equal to amount of connections, etc.\n").strip()        
    
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

    if len(filtered_dict) == len(instance_dict):
        print("OBS! This filter did nothing with your chosen parameters")

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
        #  O(n^2*m) will be the worst case scenario here. See namecombiner.py for distinctions between cases.
        combined_dict = combinations(connection_dict)
    # if all entries are removed by filter, combinations will raise ValueError
    except ValueError:
        combined_dict = {}
    
    if len(pubidnames) == len(connection_dict):
        print("This filter did nothing with your chosen parameters")

    # Overall runtime O(n^2*m + m + 1). Simplified: O(n^2*m)
    return (combined_dict), op

@progresslength
def namefilter(instance_dict:dict, genename:str, prog_len:list[int,int]):
    """ Selects all connections of entries with a specific mentioned gene name."""
        
    # find and return comperative operator for weightfiltering
    op = input("You've selected namefilter. Please choose one of the following arguments: including, excluding\n"
        f"E.g. all entries including/excluding this genename: {genename}\n").strip()

    if op not in {"including", "excluding"}:
            raise ValueError(f"The filter isn't filtering due to wrongful argument {op}")

    print(f"You chose {op}. Initiating:")

    namefitereddict = dict()
     # O(k*2(s+s))
    for instance in instance_dict:
        genes1, genes2 = instance
        if op == "including":
            # O(s+s), where s is the size of the gene1 name or gene2 name.  
            if (genename.lower() in genes1.lower()) or (genename.lower() in genes2.lower()):
                namefitereddict[instance] = instance_dict[instance]

        elif op == "excluding":
            # O(s+s), as mentioned above
            if not (genename.lower() in genes1.lower() or genename.lower() in genes2.lower()):
                namefitereddict[instance] = instance_dict[instance]

        prog_len[0] += 1
        progress_bar(prog_len[0],prog_len[1])

    # This "error" message helps the user realize that a gene perhaps is more/less prevalent than foreseen and lost to filtering
    if instance_dict and not namefitereddict:
        print(f"Warning! The file is now empty due to your filtering preferences. It wasn't before!")    
    
    if len(instance_dict) == len(namefitereddict):
        print("This filter did nothing with your chosen parameters")

    # Overall runtime O(k*2(s+s)). Since s is likely to be insignificant in size compared to k, it is ignored. After simplifying: O(k)
    return namefitereddict, op

# O(1) from filterwrapper
@progresslength
@filterwrapper
def sumofconnectionfilter(instance_dict:dict, targetsum:int, op:str,prog_len:list[int,int]):
    """ Computes the weighed sum of connections and filters accordingly for each gene entry."""
    connection_dict = dict()

    print("Be aware that this filter requires a substantial amount of time")
    # Due to the three columns in outputfile (and therefore connectiondict) "gene1, gene2, weight", both [0] and [1] are investigated
    # O(k*1*1) 
    for connected_instance in instance_dict:
        prog_len[0] += .5
        # O(1*1), since constant range of for loop.
        for i in range([0,1]):
            # O(1), since connection dict is a dictionary
            if (connected_instance[i] in connection_dict):
                connection_dict[connected_instance[i]] += int(instance_dict[connected_instance])
            else:
                connection_dict[connected_instance[i]] = int(instance_dict[connected_instance])
        progress_bar(prog_len[0],prog_len[1])

    # All connections to genes with unacceptable targetsum are removed 
    # O(k*1)
    for key in list(instance_dict.keys()):
        prog_len[0] += .5
        if not eval(f"{connection_dict[key[0]]} {op} {targetsum}"):
            # O(1), since instance_dict is a dictionary
            del instance_dict[key]
        elif not eval(f"{connection_dict[key[1]]} {op} {targetsum}"):
            # O(1)
            del instance_dict[key]
        progress_bar(prog_len[0],prog_len[1])

    if len(connection_dict) == len(instance_dict):
        print("OBS! This filter did nothing with your chosen parameters")

    # Overall runtime O(k*1*1 + k*1). After simplifying: O(k)
    return instance_dict, op