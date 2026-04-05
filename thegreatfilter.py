def taxfilter(filename_info,file_gene2pubmed,tax_id:str):
    """ Creates file containing Pubmed ID and genes for given taxid """
    # Create translation dict for finding relevant gene names
    with open(filename_info) as infile:
        # geneID_to_name[GeneID] = gene_name
        geneID_to_name = {}
        for line in infile:
            if tax_id == line.split()[0]:
                geneID_to_name[line.split()[1]] = line.split("\t")[8]

    # Create file containing relevant information about organism
    with open(file_gene2pubmed) as infile, open("processedfile_" + tax_id + ".csv", "w") as outfile:
        outfile.write("#GeneID\tPubMed_ID\tGene_name\n")
        for line in infile:
            if tax_id == line.split()[0]:
                geneID = line.split()[1]
                # write GeneID,PubMed_ID,and the gene name found in the translation dict 
                outfile.write("\t".join(line.split()[1:]) + "\t" + geneID_to_name[geneID] + "\n")
