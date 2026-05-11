# For runtime analysis:
# n will indicate genenames 
# m will indicate pubmedID's

from random import sample
from func.progress_bar import progressbar

def combinations(pub_ID_2_names:dict,max_size=-1,sampling=None) -> dict:
    """ From the ID2names dictionary, creates a dictionary with different gene combinations and their weight """
    # Not accepting empty input
    if len(pub_ID_2_names) == 0:
        raise ValueError("Input dictionary is empty, no combinations can be created.\npubID2names must consist of at least one pubmed ID key with a non-empty value.")

    # Variables for progress bar
    progress = 0
    prog_len = len(pub_ID_2_names)

    if max_size < 2 and max_size != -1:
        raise ValueError("Max size too small.")

    # Combining different Pubmed IDs and counting their weight
    instance_dict = {} # {combination, weight}
    # O(n^2 * m), including nested loops
    for names in pub_ID_2_names.values():
        # Error handling and input control
        if isinstance(names,list):
            # If values are given as lists, they are typecast to sets to avoid repeats
            names = set(names)
        if not isinstance(names,set):
            raise ValueError(f"Values must be either set or lists.\nValue: {names}")
        if len(names) == 0:
            print("Warning: No names associated with PubMed ID. Dictonary is malformed.")
            print("Continuing program...")

        # Names here depends not on values but the amount of names in each value.
        names = list(names)
        # --Uncomment sort if using pytest--
        #names.sort()

        # Sampling option for Quick Filtering
        if sampling != None and len(names) > max_size:
            # New list length 
            names = sample(names,max_size)

        # No quick filtering or quick filtering, but acceptable amount of gene names
        if max_size == -1 or len(names) <= max_size:
            # Make all combinations
            # O(n^2) due to nested loop.
            for i in range(len(names)-1):
                # O(n), worst case
                for j in range(i+1,len(names)):
                    # Create name pair
                    # O(1), since sorted is on a list with a constant length of 2
                    name_pair = tuple(sorted([names[i],names[j]]))
                    # Add to dict / increment
                    # O(1), since instance_dict is a dict
                    if name_pair not in instance_dict:
                        instance_dict[name_pair] = 1
                    else:
                        instance_dict[name_pair] += 1

        # Updating progress
        progress +=1
        progressbar(progress,prog_len)
    # Go to newline after progress bar
    print()
    
    # In worst case scenario, O(n^2 * m) is the outcome. Constant O(1) is ignored since it is insignificant in comparison.
    # If n is much larger than m, m can be neglected but this likely won't be the case.
    return instance_dict
