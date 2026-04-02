
processedfile = "processedfile.csv"
ID_dict = {}

"""with open(processedfile) as infile:
    for line in infile:
        PubID = line.split()[1]
        gene_name = line.split()[2]
        if PubID not in ID_dict:
            ID_dict[PubID] = [gene_name,None,0]
        elif PubID in ID_dict and ID_dict[PubID][1] == None:
            ID_dict[PubID][1:] = [gene_name,1]
        else:
            """

# made a dict that is {PubmedID, [list of gene names that has this ID]}
with open(processedfile) as infile:
    for line in infile:
        PubID = line.split()[1]
        gene_name = " ".join(line.split()[2:])
        if PubID not in ID_dict:
            ID_dict[PubID] = [gene_name]
        else:
            ID_dict[PubID].append(gene_name)

