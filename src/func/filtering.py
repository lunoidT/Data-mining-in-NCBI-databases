def filterwrapper(func):
    def compops(instance_dict:dict,weight:int):
        op = input("You've selected weightfilter. Please choose one of the following arguments: less, great, eq, neq\n"
                   "Eg. less for all values lesser than selected weight x or neq for not equal selected weight x\n")

        # verify amount of arguments (max 1 )
        if op not in ("less","great","eq","neq"):
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
        # remember to update for future filters

    return compops


@filterwrapper
def weightfilter(instance_dict:dict, weight:int, op:str):
    """ Selects entries with a specific weight in dictionary.
    Dictionary structure: {(x.y):weight} """
    filtered_dict = {}

    for key in instance_dict:
        if eval(f"{instance_dict[key]} {op} {weight}"):
            filtered_dict[key] = instance_dict[key]
    return filtered_dict

# @filterwrapper
def connectionfilter(pubidnames:dict, min_connections:int):
    """ Selects entries with a minimum amount of connections"""
    from namecombiner import combinations

    connection_dict = dict()
    for connected_instance in pubidnames:
        if len(pubidnames[connected_instance]) >= min_connections:
            connection_dict[connected_instance] = pubidnames[connected_instance]
    print(connected_instance)

    return combinations(connection_dict)