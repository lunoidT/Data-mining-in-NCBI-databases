with open("test2pubmed") as infile, open("testgene_info") as infile2, open("newtestgene_info","w") as outfile:
    nameset = set()
    for line in infile:
        nameset.add(line.split()[1])

    for line in infile2:
        if line.split()[1] in nameset:
            outfile.write(line)