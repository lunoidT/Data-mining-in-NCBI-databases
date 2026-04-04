
def ID_to_names(processedfile:str) -> dict:
    """ From processed file creates dictionaty containting Pubmed ID and list of gene names that has this ID """
    # ID_dict = {PubmedID, [list of gene names that has this ID]}
    ID_dict = {}
    with open(processedfile) as infile:
        for line in infile:
            PubID = line.split()[1]
            gene_name = " ".join(line.split()[2:])
            if PubID not in ID_dict:
                ID_dict[PubID] = [gene_name]
            else:
                ID_dict[PubID].append(gene_name)

    return ID_dict


#Note: ignores genes with no connections, should that be changed?
def combinations(ID_dict:dict) -> dict:
    """ From the ID_to_names dictionary, creates a dictionary with different gene combinations and their weight """
    # combining different Pubmed IDs and counting their weight
    instance_dict = {} # {combination, weight}
    for names in ID_dict.value():
        if len(names) > 1:
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
