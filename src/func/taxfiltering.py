import os
from func.progress_bar import progressbar
# for runtime analysis:
# n will indicate genenames 
# m will indicate pubmedID's

def taxfilter(file_info,file_gene_2_pubmed,tax_id:str) -> dict:
    """ Creates dict containing Pubmed ID and gene names for given taxid """

    # Variables for progress bar
    progress = 0
    max_len = os.path.getsize(file_info) + os.path.getsize(file_gene_2_pubmed)

    # Create translation dict for finding relevant gene names
    with open(file_info) as infile:
        # geneID_to_name: {GeneID : gene_name }
        geneID_to_name = {}
        # The runtime scales at O(x), where x is the amount of lines in the gene_info file.
        # But since this file is contant size no matter user input, it is arguably of constant time O(1) 
        for line in infile:
            if line.startswith(tax_id):
                line_list = line.strip().split("\t")
                geneID_to_name[line_list[1]] = line_list[8]

            # Updating progress bar
            progress += len(line)
            progressbar(progress,max_len)

    # Create dict containing Pubmed connections
    # pubID2namelist = {PubmedID : {set of gene names that has this ID}}
    pubID2names = {}
    with open(file_gene_2_pubmed) as infile:
        # Simmilarly to above, the file size is constant in the context of our program
        # O(1)
        for line in infile:
            if line.startswith(tax_id):
                line_list = line.split()
                geneID, PubID = line_list[1], line_list[2]
                # O(1) since pubID2names is a dict
                if PubID not in pubID2names:
                    pubID2names[PubID] = set()
                try:
                    pubID2names[PubID].add(geneID_to_name[geneID])
                except KeyError as key_err:
                    # raising again for unittesting
                    raise KeyError(f"Gene ID could not be translated to gene name\nReason: {key_err}")
                    
            # Updating progress bar
            progress += len(line)
            progressbar(progress,max_len)

    print()
    
    # Total runtime O(1)
    return pubID2names
