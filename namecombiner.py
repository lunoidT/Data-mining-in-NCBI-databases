
#Note: ignores genes with no connections, should that be changed?
def combinations(ID2names:dict,min_size=1) -> dict:
    """ From the ID2names dictionary, creates a dictionary with different gene combinations and their weight """
    # combining different Pubmed IDs and counting their weight
    instance_dict = {} # {combination, weight}
    for names in ID2names.values():
        if len(names) > min_size:
            # make all combinations
            for i in range(len(names)-1):
                for j in range(i+1,len(names)):

                    # add to dict / increment
                    m = tuple(sorted([names[i],names[j]]))
                    if m not in instance_dict:
                        instance_dict[m] = 1
                    else:
                        instance_dict[m] += 1
    return instance_dict
