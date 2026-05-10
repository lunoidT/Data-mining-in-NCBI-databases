#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest

# Because of the wrapper in the filtering.py, which requires user input, it is difficult to call the function from import.
# Name filter is even more annoying, because it requires additional user input, this is fixed by creating an additional parameter for the function.
# Therefore the function is inserted directly in this file:
def namefilter(instancedict:dict, genename:int, op:str):
    """ Selects all connections of entries with a specific mentioned gene-name."""
        
    namefitereddict = dict()
    if op == "including":
        # O(n)
        for instance in instancedict:
            if genename in instance:
                namefitereddict[instance] = instancedict[instance]
    elif op == "excluding":
        # O(n)
        for instance in instancedict:
            if genename not in instance:
                namefitereddict[instance] = instancedict[instance]

    # This "error" message helps the user realize that a gene perhaps is more/less prevalent than foreseen and lost to filtering
    if instancedict and not namefitereddict:
        print(f"Warning! The file is now empty due to your filtering preferences. It wasn't before!")    
    
    # Overall runtime O(2n+1). After simplifying: O(n)
    return namefitereddict, op


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
def test_namefilter_including(input_dict, genename, expected):
    assert namefilter(input_dict, genename, "including") == (expected,"including")

@pytest.mark.parametrize("genename, expected", [("winged helix-turn-helix domain-containing protein",expected_winged_helix_excluding), ("hello",expected_all), ("ArsR/SmtB family transcription factor",expected_ArsR_excluding)])
def test_namefilter_excluding(input_dict, genename, expected):
    assert namefilter(input_dict, genename, "excluding") == (expected,"excluding")