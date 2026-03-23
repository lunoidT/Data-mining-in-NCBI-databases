with open("gene2pubmed") as infile, open("dummy2pubmed", "w") as outfile:
    for line in infile:
        if line.startswith("#"):
            outfile.write(line)
        if "24" == line.split()[0]:
            outfile.write(line)
