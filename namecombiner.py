from random import sample
from progress_bar import progress_bar

def combinations(ID2names:dict,max_size=-1,sampling=None) -> dict:
    """ From the ID2names dictionary, creates a dictionary with different gene combinations and their weight """
    # combining different Pubmed IDs and counting their weight
    instance_dict = {} # {combination, weight}

    # Variables for progress bar
    progress = 0
    max_len = len(ID2names)

    if max_size < 2 and max_size != -1:
        raise ValueError("Max size too small.") # maybe replace with usage

    # Combine names and increment
    for names in ID2names.values():
        names = list(names)

        # Sampling option for Quick Filtering
        if sampling != None:
            if len(names) > max_size:
                # New list length 
                new_len = int(len(names)*sampling/100)
                if new_len < 1:
                    new_len = 1
                names = sample(names,new_len)

        if max_size == -1 or len(names) < max_size:
            # make all combinations
            for i in range(len(names)-1):
                for j in range(i+1,len(names)):

                    # add to dict / increment
                    m = tuple(sorted([names[i],names[j]]))
                    if m not in instance_dict:
                        instance_dict[m] = 1
                    else:
                        instance_dict[m] += 1
        

        # Updating progress
        progress +=1
        progress_bar(progress,max_len)
    # go to newline after progress bar
    print()
    return instance_dict
