#!/usr/bin/env python3
import sys
from thegreatfilter import taxfilter
from PubMed_sorter import ID_to_names, combinations, mkcytofile

# Files to be used
processedfile = "processedfile.csv"

#### Funtions for parsing commandline ###
def usage(msg=None):
    """ User function for user friendliness """
    if msg is not None:
        print(msg, "\n")

    print ("Usage: cytomaker.py <tax_id> [filter] <filename>")
    print("Filtering options:\n...")

    sys.exit(1)

def parseCommand():
    """ parsing commandline options, returns dictionary with options """
    options = {"file":None, "taxid":None}

    while len(sys.argv) > 1:
        arg = sys.argv.pop(1)
        
        # first option must be tax id
        if options["tax_id"] == None:
            options["tax_id"] = arg
        # updating filename
        elif options["file"] == None:
            options["file"] = arg
        # filename already provided, terminate
        else:
            usage()

    # Checking if necessary information provided
    if options["file"] is None:
       usage("Please provide filename.")

    return options


#### MAIN ####

# obtain options from commandline
file_options = parseCommand()

try:
    # Process genbank files to a file
    taxfilter(file_options["tax_id"])

    ID_dict = ID_to_names(processedfile)
    instance_dict = combinations(ID_dict)
    # write file
    mkcytofile(file_options["file"],instance_dict)

except IOError as file_err:
    usage(file_err)