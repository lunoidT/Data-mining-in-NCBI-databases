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
def connectionfilter(instance_dict:dict, min_connections:int):
    """ Selects entries with a minimum amount of connections"""

    connection_dict = dict()

    # for line in file:
        # for connection in line
            # connections += 1
        # if connections >= min_connections:
            # instance_dict.add(instance)
    # return instance_dict

    for instance in instance_dict:
        # this needs error handling for good measure (debugging)

        for i in range(len(instance)):
            if instance[i] not in connection_dict:
                connection_dict[instance[i]] = set()
            for j in range(len(instance)):
                if instance[i] != instance[j]:
                    connection_dict[instance[i]].add(instance[j])


    for connected_instance in list(connection_dict.keys()):
        if len(connection_dict[connected_instance]) < min_connections:
            del connection_dict[connected_instance]

    return connection_dict