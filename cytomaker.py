#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from thegreatfilter import taxfilter
from PubMed_sorter import ID_to_names, combinations
from filtering import weightfilter, connectionfilter

# Files
filename_info = "smalldummy_info" #"gene_info"
file_gene2pubmed = "dummy2pubmed" #"gene2pubmed"

#### Funtions for parsing commandline ###
def usage(msg=None):
    """ User function for user friendliness """
    if msg is not None:
        print(msg, "\n")

    print ("Usage: cytomaker.py <tax_id> [filter]")
    print("Filtering options:")
    print("-w <int> Filtering based on weight of connection between genes")
    print("-c <int> Filtering based on amount of connections to gene")

    sys.exit(1)

def parseCommand():
    """ parsing commandline options, returns dictionary with options """
    options = {"tax_id":None, "weight_filtering":None, "connection_filtering":None}

    filtering = 0
    while len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        
        # First option must be tax ID
        if options["tax_id"] == None:
            options["tax_id"] = arg

        # Saving filters
        elif options["weight_filtering"] == None and arg == "-w":
            try:
                amount = int(sys.argv.pop(1))
            except ValueError:
                usage("Filter amount must be an integer")
            options["weight_filtering"] = amount
            filtering += 1

        elif options["connection_filtering"] == None and arg == "-c":
            try:
                amount = int(sys.argv.pop(1))
            except ValueError:
                usage("Filter amount must be an integer")
            options["connection_filtering"] = amount
            filtering += 1

        else:
            usage()

    # Checking if necessary information provided
    if options["tax_id"] is None:
       usage("Please provide a tax ID.")

    return options, filtering

#### Functions for and writing loading files ####
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
    # Making it readable for cytoscape
    with open(cytofile, "w") as outfile:
        outfile.write("name1\tname2\tweight\n")
        for names,weight in instance_dict.items():
            outfile.write("\t".join(names) + "\t" + str(weight) + "\n")


#### MAIN ####

# Obtain options from commandline
file_options,filtering = parseCommand()

try:
    # Find out if Taxid already had been mined, 
    # If so load the cytoscape file to a dict and use that for filtering
    print("Loading files...")
    if "cytofile_" + file_options["tax_id"] + ".csv" in os.listdir():
        instance_dict = cytoload("cytofile_" + file_options["tax_id"] + ".csv")
        print("Loaded files successfully.")
    else:
        # Process infomation from genbank files to a file
        taxfilter(filename_info,file_gene2pubmed,file_options["tax_id"])
        # Load into dictionaries
        ID_dict = ID_to_names("processedfile_" + file_options["tax_id"] + ".csv")
        instance_dict = combinations(ID_dict)

        print(f"Loaded files successfully. Writing file to {"cytofile_" + file_options["tax_id"] + ".csv"}")
        # Save unfiltered version for later use 
        cytowrite("cytofile_" + file_options["tax_id"] + ".csv",instance_dict)
    
    # Filter instance dict
    if filtering > 0:
        print("Filtering started...")
        for _ in range(filtering):
            if file_options["weight_filtering"] != None:
                instance_dict = weightfilter(instance_dict,file_options["weight_filtering"])
            elif file_options["connection_filtering"] != None:
                instance_dict = weightfilter(instance_dict,file_options["connection_filtering"])
            else:
                usage("File option not found or missing.")

        # Write filtered file
        print(f"Filtered file successfully. Writing file to {"cytofile_" + file_options["tax_id"] + "_filtered_" + str(datetime.now()) + ".csv"}")
        cytowrite("cytofile_" + file_options["tax_id"] + "_filtered_" + str(datetime.now()) + ".csv",instance_dict)

    print("Program finished.")

except IOError as file_err:
    usage(file_err)