with open("gene_info") as infile, open("smalldummy_info", "w") as outfile:
    for line in infile:
        if "24" in line:
            outfile.write(line)