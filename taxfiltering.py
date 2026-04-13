import os
from progress_bar import progress_bar

def taxfilter(filename_info,file_gene2pubmed,tax_id:str) -> dict:
    """ Creates dict containing Pubmed ID and gene names for given taxid """

    # Variables for progress bar
    progress = 0
    max_len = os.path.getsize(filename_info) + os.path.getsize(file_gene2pubmed)

    # Create translation dict for finding relevant gene names
    with open(filename_info) as infile:
        # geneID_to_name: {GeneID : gene_name }
        geneID_to_name = {}
        for line in infile:
            line_list = line.split("\t")
            if tax_id == line_list[0]:
                geneID_to_name[line_list[1]] = line_list[8]

            # Updating progress bar
            progress += len(line)
            progress_bar(progress,max_len)

    # Create dict containing Pubmed connections
    # ID2namelist = {PubmedID : {set of gene names that has this ID}}
    pubID2names = {}
    with open(file_gene2pubmed) as infile:
        for line in infile:
            line_list = line.split()
            if tax_id == line_list[0]:
                geneID, PubID = line_list[1], line_list[2]
                if PubID not in pubID2names:
                    pubID2names[PubID] = set()
                
                pubID2names[PubID].add(geneID_to_name[geneID])
        
            # Updating progress bar
            progress += len(line)
            progress_bar(progress,max_len)

    print()
    
    return pubID2names
