with open("gene_info") as infile, open("smalldummy_info", "w") as outfile:
    i = 0
    for line in infile:
        if i < 100:
            outfile.write(line)
        i += 1