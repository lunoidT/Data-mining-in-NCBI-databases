#!/usr/bin/env python3

# for runtime analysis:
# n will indicate genenames 
# m will indicate pubmedID's
# k will indicate amount of connections

import sys
import os
from datetime import datetime
from func.taxfiltering import taxfilter 
from func.namecombiner import combinations 
from func.filtering import weightfilter, connectionfilter, namefilter, sumofconnectionfilter

# Files
filename_info = "smalldummy_info" #"gene_info"
file_gene2pubmed = "dummy2pubmed"
file_path = "cytofiles/"

#### Funtions for parsing commandline ###
def usage(msg=None):
    """ User function for user friendliness """
    if msg is not None:
        print(msg, "\n")

    print("Usage: cytomaker.py <tax_id> [filter] [-q <int> [-s]")
    print("For more information enter: cytomaker.py help")
    sys.exit(1)

def help():
    """ More information about options """
    print("Usage: cytomaker.py <tax_id> [filter] [-q <int> [-s]]")
    print("Filtering options:")
    print("-w <int> Filtering based on weight of connections between genes")
    print("-c <int> Filtering based on amount of connections to gene")
    print("-n <str> Filtering based on if a specific gene-name appears in connection")
    print("-u <int> Filtering based on weighed sum of connection")
    print()
    print("-q <int> : Quick Filter option.\nUse if running on tax ID with large amount of data, and computer is unable to processs.") 
    print("Ignores Pubmed articles with too many entries, since that can be a bottleneck for runtime and memory.")
    print("The integer folowing -q is the max amount of entries allowed by the user in each article")
    print("-s : Random sampling option for Quick Filter, instead of ignoring articles with many entries, it randomly reduces to max size")
    print("Note: Quckfiltering is ignored if file for tax ID is already loaded")
    sys.exit(1)

def parse_command():
    """ parsing commandline options, returns dictionary with options """
    options = {"tax_id":None, "weight_filtering":None, "connection_filtering":None, "name_filtering":None, "connectionsummed_filtering":None, "quick_filter":None, "sampling":None}

    filtering = 0
    # constant time with a max of 8 iterations. ignored in runtime evaluatoin
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
        
        # -n is followed by a name which takes up multiple words (spaces) which must all be removed
        elif options["name_filtering"] == None and arg == "-n":
            end_index = False
            for i in range(len(sys.argv)):
                if sys.argv[i] in ("-w", "-c", "-u", "-q", "-s"):
                    end_index = i
                    break
            
            # remove the entire gene name from the parsing arguments to ready for next potential filter
            if end_index:
                name = " ".join(sys.argv[1:end_index])
                del sys.argv[1:end_index]
            
            # if -n <str> are the final argumetns
            else:
                name = " ".join(sys.argv[1:])
            options["name_filtering"] = name
            filtering += 1


        elif options["connectionsummed_filtering"] == None and arg == '-u':
            try:
                amount = int(sys.argv.pop(1))
            except ValueError:
                usage("Filter amount must be an integer")
            options["connectionsummed_filtering"] = amount
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
            options["sampling"] = True

        else:
            usage()

    # Checking if necessary information provided
    if options["tax_id"] is None:
       usage("Please provide a tax ID.")

    return options, filtering

#### Functions for and writing loading files ####
# overall for cytoload: O(n)
def cytoload(oldfile):
    """ Loading cytoscape files from already mined tax IDs """
    with open(oldfile) as infile:
        instance_dict = {}
        for line in infile:
            # O(n-x) where x is the ammount of single-line comments
            if not line.startswith("#"):
                parts = line.strip().split("\t") 

                # not accepting less than 3 tab seperated elements but still ignores empty lines
                if parts == [""]:
                    continue
                if len(parts) < 3:
                    raise ValueError(f"Unable to load from malformed cytofile: {oldfile}")
            
                instance_dict[(parts[0], parts[1])] = int(parts[2])

    # Refuse to load empty file
    if instance_dict == {}:
        raise ValueError(f"Can't load empty file: {oldfile}")

    # Worst case for the function is O(n)
    return instance_dict    

# overall for cytowrite: O(n)
def cytowrite(cytofile:str,instance_dict:dict,info_txt=None):
    """ Writes dictionary to file """
    # Making it readable for cytoscape
    with open(cytofile, "w") as outfile:
        # Write info text if any
        if info_txt != None:
            outfile.write(info_txt + "\n")
            
        outfile.write("#name1\tname2\tweight\n")

        # O(n)
        for names, weight in instance_dict.items():
            outfile.write("\t".join(names) + "\t" + str(weight) + "\n")


#### MAIN ####

if __name__ == "__main__":
    # Obtain options from commandline
    file_options,filtering = parse_command()
    # Obtain date, and add underscore so it can be used in filename
    date = "_".join( str(datetime.now()).split() )
    pubID2names = None

    try:
        # Find out if Taxid already had been mined, 
        # If so load the cytoscape file to a dict and use that for filtering
        # For this section the worst-case runtime is O(4n+m+2(m*k^2))
        print("Loading files...")
        if "cytofile_" + file_options["tax_id"] + ".csv" in os.listdir("cytofiles"): 
            # O(n)
            instance_dict = cytoload("cytofiles/cytofile_" + file_options["tax_id"] + ".csv")
            print("Loaded files successfully from existing file into a dictionary.")
        else:
            # Process infomation from genbank files to a dict
            # pubID2names = {PubmedID : {set of gene names that has this ID}}
            # O(n+m) is worst case
            pubID2names = taxfilter(filename_info,file_gene2pubmed,file_options["tax_id"])
            print("Loaded files successfully to a dictionary.")

            # Process information further
            # If quickfilter is activated articles with less or equal to x amount is ignored, making combinations process faster
            if file_options["quick_filter"] != None:
                print("Combining names...")
                print("Quick filtering activated.")
                # O(m*k^2) see namecombiner. 
                instance_dict = combinations(pubID2names,file_options["quick_filter"],file_options["sampling"])
                print(f"Done combining. Writing file to {"cytofile_" + file_options["tax_id"] + "_quick_filtered_" + date + ".csv"}...")
                # writing file
                file_txt = f"#Tax ID: {file_options["tax_id"]}. Quick filtered with max length {file_options["quick_filter"]}. Sampling: {file_options["sampling"]}"
                # O(n)
                cytowrite(file_path + "cytofile_" + file_options["tax_id"] + "_quick_filtered_" + date + ".csv",instance_dict,info_txt=file_txt)
            else:
                print("Combining names...")
                # O(m*k^2) see namecombiner
                instance_dict = combinations(pubID2names)
                # Save unfiltered version for later use 
                print(f"Done combining. Writing file to {"cytofile_" + file_options["tax_id"] + ".csv"}...")
                file_txt = f"#Tax ID: {file_options["tax_id"]}. Unfiltered cytofile."
                # O(n)
                cytowrite(file_path + "cytofile_" + file_options["tax_id"] + ".csv",instance_dict,info_txt=file_txt)
        # Overall runtime for this section: O(4n+m+2(m*k^2)). After simplifying: O(n+m+m*k^2)
        

        # Filter instance dict
        if filtering > 0:
            print("Filtering started...")
            if file_options["connection_filtering"] != None:
                # If file for tax ID is already loaded, instance dict must be made
                if pubID2names == None:
                    # O(n+m)
                    pubID2names = taxfilter(filename_info,file_gene2pubmed,file_options["tax_id"])
                print("Creating connections...")

                #notice that this filter is the only to use pubID2names instead of instance_dict
                # O(m*k^2)
                instance_dict, connction_op = connectionfilter(pubID2names,file_options["connection_filtering"])
                file_options["connection_filtering"] = connction_op + " " + str(file_options["connection_filtering"])
            if file_options["weight_filtering"] != None:
                #  O(n)
                instance_dict, weight_op = weightfilter(instance_dict, file_options["weight_filtering"])
                file_options["weight_filtering"] = weight_op + " " + str(file_options["weight_filtering"]) 
            if file_options["name_filtering"] != None:
                #  O(n)
                instance_dict, name_op = namefilter(instance_dict,file_options["name_filtering"])
                file_options["name_filtering"] = name_op + " " + file_options["name_filtering"]
            if file_options["connectionsummed_filtering"] != None:
                #  O(n)
                instance_dict, con_sum_op = sumofconnectionfilter(instance_dict,file_options["connectionsummed_filtering"])
        # Overall runtime for this section: All of the above may be activated in which case O(n+m+m*k^2)
        

            # Write filtered file
            print(f"Filtered file successfully. Writing file to {"cytofile_" + file_options["tax_id"] + "_filtered_" + date + ".csv"}...")
            file_txt = f"#Tax ID: {file_options["tax_id"]}. Weight filter: {file_options["weight_filtering"]}. Commection filter: {file_options["connection_filtering"]}. Name filter: {file_options["name_filtering"]}. Sum of connections filter: {file_options['connectionsummed_filtering']}."
            # O(n)
            cytowrite(file_path + "cytofile_" + file_options["tax_id"] + "_filtered_" + date + ".csv",instance_dict,info_txt=file_txt)
        # Overall runtime for this section: O(n)

        print("Program finished.")

    except IOError as file_err:
        usage(file_err)

    # In the worst case
    # Overall runtime here is 
    # determined as O(n+m+m*k^2) + O(n+m+m*k^2) + O(n) = After simplifying: O(n+m+m*k^2)
