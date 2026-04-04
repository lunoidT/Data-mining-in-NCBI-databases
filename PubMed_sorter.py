# Files to be used
processedfile = "processedfile.csv"
cytofile = "cytoscaper.csv"


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


# combining different Pubmed IDs and counting their weight
instance_dict = {} # {combination, weight}
for PubID,names in ID_dict.items():
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
            

# making it readable for cytoscape
with open(cytofile, "w") as outfile:
    outfile.write("name1\tname2\tweight\n")
    for names,weight in instance_dict.items():
        outfile.write("\t".join(names) + "\t" + str(weight) + "\n")