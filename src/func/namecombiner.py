# for runtime analysis:
# n will indicate genenames 
# m will indicate pubmedID's
# k will indicate amount of genenames within each value in the ID2names dictionary

from random import sample
from func.progress_bar import progress_bar

def combinations(ID2names:dict,max_size=-1,sampling=None) -> dict:
    """ From the ID2names dictionary, creates a dictionary with different gene combinations and their weight """
    # combining different Pubmed IDs and counting their weight
    instance_dict = {} # {combination, weight}

    # Variables for progress bar
    progress = 0
    prog_len = len(ID2names)

    if max_size < 2 and max_size != -1:
        raise ValueError("Max size too small.") # maybe replace with usage

    # Combine names and increment
    # O(m) 
    for names in ID2names.values():

        # names here depends not on values but the amount of names in each value.
        names = list(names)

        # Sampling option for Quick Filtering
        if sampling != None and len(names) > max_size:
            # New list length 
            names = sample(names,max_size)

        # This is always true for worst runtime scenario
        if max_size == -1 or len(names) <= max_size:
            # make all combinations
            # O(m*k) due to nested loop. This loop can be much larger than previous so a new variable is declared
            for i in range(len(names)-1):
                # O(m*k^2) due to another nested loop (of equal size to previous)
                for j in range(i+1,len(names)):

                    # add to dict / increment
                    m = tuple(sorted([names[i],names[j]]))
                    if m not in instance_dict:
                        instance_dict[m] = 1
                    else:
                        instance_dict[m] += 1

        # Updating progress
        progress +=1
        progress_bar(progress,prog_len)
    # go to newline after progress bar
    print()

    # In worst case scenario, O(m*k^2) is the outcome. 
    # If k is much larger than m, m can be neglected but this likely won't be the case
    return instance_dict
