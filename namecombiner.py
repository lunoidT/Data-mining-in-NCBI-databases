
def combinations(ID2names:dict,max_size=-1) -> dict:
    """ From the ID2names dictionary, creates a dictionary with different gene combinations and their weight """
    # combining different Pubmed IDs and counting their weight
    instance_dict = {} # {combination, weight}

    # SEJ SAMPLING AF STORE LIST
    # For progress bar
    progress = 0
    temp_progress = None
    max_len = len(ID2names)

    # Combine names and increment
    for names in ID2names.values():
        names = list(names)
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
        if (int(progress/max_len*100) != temp_progress) and not (int(progress/max_len*100)%10):
            temp_progress = int(progress/max_len*100)
            print(f"progress: {int(progress/max_len*100)}%")

    return instance_dict
