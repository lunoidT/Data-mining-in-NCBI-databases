#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from thegreatfilter import taxfilter
from PubMed_sorter import ID_to_names, combinations
from filtering import weightfilter, connectionfilter

# Insert welcome message?
# things to consider:
# - multifiltering

#### Funtions for parsing commandline ###
def usage(msg=None):
    """ User function for user friendliness """
    if msg is not None:
        print(msg, "\n")

    print ("Usage: cytomaker.py <tax_id> [filter]")
    print("Filtering options:\n...")

    sys.exit(1)

def parseCommand():
    """ parsing commandline options, returns dictionary with options """
    options = {"taxid":None, "filtering_type":None, "filtering_amount":None}

    while len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        
        # first option must be tax id
        if options["tax_id"] == None:
            options["tax_id"] = arg
        # saving filter
        elif options["filtering_type"] == None and (arg == "-w" or arg == "-c"):
            options["filtering_type"] = arg
            try:
                amount = int(arg.pop(1))
            except ValueError:
                usage("Amount must be integer")

            options["filtering_amount"] = amount
        else:
            usage()

    # Checking if necessary information provided
    if options["tax_id"] is None:
       usage("Please provide a tax ID.")

    return options

def cytoload(oldfile):
    """ Loading cytoscape files from already mined tax IDs """
    with open(oldfile) as infile:
        instance_dict = {}
        for line in infile:
            if not line.startswith("#"):
                instance_dict[line.split()[0]] = line.split()[1]
    return instance_dict

def cytowrite(cytofile:str,instance_dict:dict):
    """ Writes dictionary to file """
    # making it readable for cytoscape
    with open(cytofile, "w") as outfile:
        outfile.write("name1\tname2\tweight\n")
        for names,weight in instance_dict.items():
            outfile.write("\t".join(names) + "\t" + str(weight) + "\n")

#### MAIN ####

# obtain options from commandline
file_options = parseCommand()

try:
    # find out if Taxid already had been mined, 
    # if so load the cytoscape file to a dict and use that for filtering
    if "cytofile_" + file_options["tax_id"] + ".csv" in os.listdir():
        instance_dict = cytoload("cytofile_" + file_options["tax_id"] + ".csv")
    else:
        # Process infomation from genbank files to a file
        taxfilter(file_options["tax_id"])
        # load into dictionaries
        ID_dict = ID_to_names("processedfile_" + file_options["tax_id"] + ".csv")
        instance_dict = combinations(ID_dict)

    # save unfiltered version for later use 
    cytowrite("cytofile_" + file_options["tax_id"] + ".csv",instance_dict)

    # write filtered file 
    if file_options["filtering_type"] != None:
        if file_options["filtering_type"] == "-w":
            filtered_dict = weightfilter(instance_dict,file_options["filtering_amount"])
            cytowrite("cytofile_" + file_options["tax_id"] + "_filtered_" + str(datetime.now()) + ".csv",instance_dict)
        
        # continue to make filtered versions...

except IOError as file_err:
    usage(file_err)