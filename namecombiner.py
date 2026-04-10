from random import randrange

def progress_bar(current, max_len,bar_len=30):
    """ Progress bar for combinations function """
    progress_text = "█" * int((current/max_len)*bar_len)
    rest_text = "-" * (bar_len - int((current/max_len)*bar_len))
    print(f"\rProgress: [{progress_text}{rest_text}]",end="")


def combinations(ID2names:dict,max_size=-1,sampling=None) -> dict:
    """ From the ID2names dictionary, creates a dictionary with different gene combinations and their weight """
    # combining different Pubmed IDs and counting their weight
    instance_dict = {} # {combination, weight}

    # Variables for progress bar
    progress = 0
    max_len = len(ID2names)

    # Combine names and increment
    for names in ID2names.values():
        names = list(names)

        # Sampling option for Quick Filtering
        if sampling != None:
            try:
                if len(names) > max_size:
                    # New list length and random samples index
                    new_len = int(len(names)*1/sampling)
                    random_sample = randrange(0,new_len)
                    # Reducing data points in list
                    for i in range(len(names)-1,-1,-1):
                        if i not in random_sample:
                            names.pop(i)
            except:
                # Errors might happen if too small max list length.
                # Skipping since samling makes no difference
                sampling = None

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
