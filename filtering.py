
def weightfilter(instance_dict:dict, weight:int) -> dict:
    """ selects enties with a specific weight in dictionary.

    Dictionary structure: {x,weights} """
    filtered_dict = {}
    for key in instance_dict:
        if instance_dict[key] >= weight:
            filtered_dict[key] = instance_dict[key]
    return filtered_dict
    
def connectionfilter():
    pass