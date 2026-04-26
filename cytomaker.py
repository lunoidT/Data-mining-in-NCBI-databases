#!/usr/bin/env python3
import sys
import os
from datetime import datetime
from taxfiltering import taxfilter 
from namecombiner import combinations 
from filtering import weightfilter, connectionfilter

# Files
filename_info = "smalldummy_info" #"gene_info"
file_gene2pubmed = "dummy2pubmed"

#### Funtions for parsing commandline ###
def usage(msg=None):
    """ User function for user friendliness """
    if msg is not None:
        print(msg, "\n")

    print("Usage: cytomaker.py <tax_id> [filter] [-q <int> [-s <int>]]")
    print("For more information enter: cytomaker.py help")
    sys.exit(1)

def help():
    """ More information about options """
    print("Usage: cytomaker.py <tax_id> [filter] [-q <int> [-s <int>]]")
    print("Filtering options:")
    print("-w <int> Filtering based on weight of connection between genes")
    print("-c <int> Filtering based on amount of connections to gene")
    print()
    print("-q <int> : Quick Filter option, for experienced users.\nUse if running on tax ID with large amount of data, and computer is unable to processs.") 
    print("Ignores Pubmed articles with too many entries, since that can be a bottleneck for runtime and memory.")
    print("-s <int> : Random sampling option for Quick Filter, instead of ignoring articles with many entries, it randomly reduces them <int>%")
    print("Note: Quckfiltering is ignored if file for tax ID is already loaded")
    sys.exit(1)

def parse_command():
    """ parsing commandline options, returns dictionary with options """
    options = {"tax_id":None, "weight_filtering":None, "connection_filtering":None, "quick_filter":None, "sampling":None}

    filtering = 0
    while len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        
        # First option must be tax ID or "help"
        if options["tax_id"] == None and arg == "help":
            help()
        elif options["tax_id"] == None:
            try:
                int(arg)
            except ValueError:
                usage("tax ID amount must be an integer")
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

        # Activating Quick Filtering
        elif options["quick_filter"] == None and arg == "-q":
            try:
                amount = int(sys.argv.pop(1))
            except ValueError:
                usage("Filter amount must be an integer")
            options["quick_filter"] = amount

        # Quick Filtering sampling option
        elif options["quick_filter"] != None and options["sampling"] == None and arg == "-s":
            try:
                amount = int(sys.argv.pop(1))
                if not (0 < amount < 100):
                    raise ValueError
            except ValueError:
                usage("Sampling percent must be an integer between 0 and 100")
            options["sampling"] = amount

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
                parts = line.strip().split("\t") 
                instance_dict[(parts[0], parts[1])] = parts[2]
    return instance_dict    

def cytowrite(cytofile:str,instance_dict:dict,info_txt=None):
    """ Writes dictionary to file """
    # Making it readable for cytoscape
    with open(cytofile, "w") as outfile:
        # Write info text if any
        if info_txt != None:
            outfile.write(info_txt + "\n")
        if file_options["connection_filtering"] != None:
            outfile.write("#name1\tconnected entries\tamount of entries\n")
            for name, connected_names in instance_dict.items():
                outfile.write(name + "\t" + "\t".join(connected_names) + "\t" + str(len(connected_names)) + "\n")
        else:
            outfile.write("#name1\tname2\tweight\n")
            for names, weight in instance_dict.items():
                outfile.write("\t".join(names) + "\t" + str(weight) + "\n")


#### MAIN ####

# Obtain options from commandline
file_options,filtering = parse_command()
# Obtain date, and add underscore so it can be used in filename
date = "_".join( str(datetime.now()).split() )

try:
    # Find out if Taxid already had been mined, 
    # If so load the cytoscape file to a dict and use that for filtering
    print("Loading files...")
    if "cytofile_" + file_options["tax_id"] + ".csv" in os.listdir():
        instance_dict = cytoload("cytofile_" + file_options["tax_id"] + ".csv")
        print("Loaded files successfully.")
    else:
        # Process infomation from genbank files to a dict
        pubID2names = taxfilter(filename_info,file_gene2pubmed,file_options["tax_id"])
        print("Loaded files successfully to a dictionary.")

        # Process information further
        # If quickfilter is activated articles with less or equal to x amount is ignored, making combinations process faster
        if file_options["quick_filter"] != None:
            print("Combining names...")
            print("Quick filtering activated.")
            instance_dict = combinations(pubID2names,file_options["quick_filter"],file_options["sampling"])
            print(f"Done combining. Writing file to {"cytofile_" + file_options["tax_id"] + "_quick_filtered_" + date + ".csv"}...")
            # writing file
            file_txt = f"#Tax ID: {file_options["tax_id"]}. Quick filtered with max length {file_options["quick_filter"]}. Sampling: {file_options["sampling"]}"
            cytowrite("cytofile_" + file_options["tax_id"] + "_quick_filtered_" + date + ".csv",instance_dict,info_txt=file_txt)
        else:
            print("Combining names...")
            instance_dict = combinations(pubID2names)
            # Save unfiltered version for later use 
            print(f"Done combining. Writing file to {"cytofile_" + file_options["tax_id"] + ".csv"}...")
            file_txt = f"#Tax ID: {file_options["tax_id"]}. Unfiltered cytofile."
            cytowrite("cytofile_" + file_options["tax_id"] + ".csv",instance_dict,info_txt=file_txt)

    # Filter instance dict
    if filtering > 0:
        print("Filtering started...")
        if file_options["weight_filtering"] != None:
            instance_dict = weightfilter(instance_dict,file_options["weight_filtering"])
        if file_options["connection_filtering"] != None:
            instance_dict = connectionfilter(instance_dict,file_options["connection_filtering"])

        # Write filtered file
        print(f"Filtered file successfully. Writing file to {"cytofile_" + file_options["tax_id"] + "_filtered_" + date + ".csv"}...")
        file_txt = f"#Tax ID: {file_options["tax_id"]}. Weight filer: {file_options["weight_filtering"]}. Commection filter: {file_options["connection_filtering"]}"
        cytowrite("cytofile_" + file_options["tax_id"] + "_filtered_" + date + ".csv",instance_dict,info_txt=file_txt)

    print("Program finished.")

except IOError as file_err:
    usage(file_err)