def filterwrapper(func):
    def compops(instance_dict:dict,weight:int,**kwargs):

        if sum(kwargs.values()) != 1:
            raise ValueError("The filter isn't filtering due to the keywords variables overlapping or lack of arguments")

        for kw in kwargs:
            if kwargs[kw]:
                op = kw
                break
        
        if op == "less":
            return func(instance_dict, weight, "<")
        elif op == "great":
            return func(instance_dict, weight, ">")
        elif op == "eq":
            return func(instance_dict, weight, "==")
        elif op == "neq":
            return func(instance_dict, weight, "!=")
        # remember to update for future functions
        
    return compops

@filterwrapper
def weightfilter(instance_dict:dict, weight:int, op:str, less:bool=False, great:bool=False, eq:bool=False, neq:bool=False) -> dict:
    """ Selects entries with a specific weight in dictionary.

    keyword variables: \n

    Dictionary structure: {x,weights} """
    filtered_dict = {}

    # switch variables
    for key in instance_dict:
        if eval(f"{instance_dict[key]} {op} {weight}"):
            filtered_dict[key] = instance_dict[key]

    return filtered_dict

def connectionfilter(instance_dict:dict, min_connections:int):
    """ Selects entries with a minimum amount of connections"""
    pass