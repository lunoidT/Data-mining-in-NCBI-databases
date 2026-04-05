with open("gene_info") as infile, open("smalldummy_info", "w") as outfile:
    for line in infile:
        if line.startswith("24"):
            outfile.write(line)