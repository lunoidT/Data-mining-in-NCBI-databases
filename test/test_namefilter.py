#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest

# Because of the wrapper in the filtering.py, which requires user input, it is difficult to call the function from import.
# Name filter is even more annoying, because it requires additional user input, this is fixed by creating an additional parameter for the function.
# Therefore the function is inserted directly in this file:

def namefilter(instance_dict:dict, gene_name:str):
    """ Selects all connections of entries with a specific mentioned gene name."""

    # find and return operator for weightfiltering (while loop allows for mistakes without crashing the program)
    while op not in {"including", "excluding"}: 
        op = input("You've selected namefilter. Please choose one of the following arguments: including, excluding\n"
            f"E.g. all entries including/excluding this genename: {gene_name}\n").strip()
        if op not in {"including", "excluding"}:
            print(f"The filter isn't filtering due to wrongful argument {op}. Try again!")

    print(f"You chose {op}. Initiating:")
    
    namefitered_dict = dict()
     # O(k*2(s+s))
    for instance in instance_dict:
        genes1, genes2 = instance
        if op == "including":
            # O(s+s), where s is the size of the gene1 name or gene2 name.  
            if (gene_name.lower() in genes1.lower()) or (gene_name.lower() in genes2.lower()):
                namefitered_dict[instance] = instance_dict[instance]

        elif op == "excluding":
            # O(s+s), as mentioned above
            if not (gene_name.lower() in genes1.lower() or gene_name.lower() in genes2.lower()):
                namefitered_dict[instance] = instance_dict[instance]

    # This "error" message helps the user realize that a gene perhaps is more/less prevalent than foreseen and lost to filtering
    if instance_dict and not namefitered_dict:
        print(f"Warning! The file is now empty due to your filtering preferences. It wasn't before!")   

    if len(instance_dict) == len(namefitered_dict):
        print("This filter did nothing with your chosen parameters") 
    
    # Overall runtime O(2n+1). After simplifying: O(n)
    return namefitered_dict, op


### Input and output ###
@pytest.fixture
def input_dict():
    return {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
            ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
            ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
            ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
            ("PadR family transcriptional regulator","response regulator transcription factor"):3}

expected_all = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
                ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
                ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
                ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
                ("PadR family transcriptional regulator","response regulator transcription factor"):3}

expected_none = {}

expected_winged_helix_including ={("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
                                  ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2}

expected_winged_helix_excluding = {("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
                                   ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
                                   ("PadR family transcriptional regulator","response regulator transcription factor"):3}

expected_ArsR_including = {("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2}

expected_ArsR_excluding = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
                           ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
                           ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
                           ("PadR family transcriptional regulator","response regulator transcription factor"):3}

### Testing ### 
@pytest.mark.parametrize("genename, expected", [("winged helix-turn-helix domain-containing protein",expected_winged_helix_including), ("hello",expected_none), ("ArsR/SmtB family transcription factor",expected_ArsR_including)])
def test_namefilter_including(input_dict, gene_name, expected):
    assert namefilter(input_dict, gene_name, "including") == (expected,"including")

@pytest.mark.parametrize("genename, expected", [("winged helix-turn-helix domain-containing protein",expected_winged_helix_excluding), ("hello",expected_all), ("ArsR/SmtB family transcription factor",expected_ArsR_excluding)])
def test_namefilter_excluding(input_dict, gene_name, expected):
    assert namefilter(input_dict, gene_name, "excluding") == (expected,"excluding")