def taxfilter(filename_info,file_gene2pubmed,tax_id:str) -> dict:
    """ Creates dict containing Pubmed ID and gene names for given taxid """
    # Create translation dict for finding relevant gene names
    with open(filename_info) as infile:
        # geneID_to_name: {GeneID : gene_name }
        geneID_to_name = {}
        for line in infile:
            if tax_id == line.split()[0]:
                geneID_to_name[line.split()[1]] = line.split("\t")[8]

    # Create dict containing Pubmed connections
    # ID2namelist = {PubmedID : {set of gene names that has this ID}}
    ID2names = {}
    with open(file_gene2pubmed) as infile:
        for line in infile:
            if tax_id == line.split()[0]:
                geneID, PubID = line.split()[1], line.split()[2]

                if PubID not in ID2names:
                    ID2names[PubID] = set(geneID_to_name[geneID])
                else:
                    ID2names[PubID].add(geneID_to_name[geneID])
    
    return ID2names
