#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest

# Because of the wrapper in the filtering.py, which requires user input, it is difficult to call the function from import.
# Therefore the function is inserted directly in this file:
def sumofconnectionfilter(instance_dict:dict, target_sum:int, op:str):
    """ Computes the weighed sum of connections and filters accordingly for each gene entry."""
    connection_dict = dict()

    print("Be aware that this filter requires a substantial amount of time")
    # Due to the three columns in outputfile (and therefore connectiondict) "gene1, gene2, weight", both [0] and [1] are investigated
    # O(k*1*1) 
    for connected_instance in instance_dict:
        # O(1*1), since constant range of for loop.
        for i in range([0,1]):
            # O(1), since connection dict is a dictionary
            if (connected_instance[i] in connection_dict):
                connection_dict[connected_instance[i]] += int(instance_dict[connected_instance])
            else:
                connection_dict[connected_instance[i]] = int(instance_dict[connected_instance])

    # All connections to genes with unacceptable targetsum are removed 
    # O(k*1)
    for key in list(instance_dict.keys()):
        if not eval(f"{connection_dict[key[0]]} {op} {target_sum}"):
            # O(1), since instance_dict is a dictionary
            del instance_dict[key]
        elif not eval(f"{connection_dict[key[1]]} {op} {target_sum}"):
            # O(1)
            del instance_dict[key]

    if len(connection_dict) == len(instance_dict):
        print("OBS! This filter did nothing with your chosen parameters")

    # Overall runtime O(k*1*1 + k*1). After simplifying: O(k)
    return instance_dict, op

### Input and output ###
@pytest.fixture
def input_dict():
    return {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
            ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
            ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
            ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
            ("PadR family transcriptional regulator","response regulator transcription factor"):3}

expected_none = {}

expected_all = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
                ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
                ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
                ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
                ("PadR family transcriptional regulator","response regulator transcription factor"):3}

expected_less5 = {("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
                  ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4}

expected_more3 = {("PadR family transcriptional regulator","response regulator transcription factor"):3,
                  ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
                  ("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3}

expected_more4 = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
                  ("PadR family transcriptional regulator","response regulator transcription factor"):3}

### Testing ###
# Filter seems to be extreme in the amount of entries it removes, but with larger data it can be relevant.
@pytest.mark.parametrize("tagetsum, expected", [(3,expected_none), (4,expected_none), (11,expected_all), (5,expected_none)])
def test_sumofconnectionfilter_less(taget_sum, expected, input_dict):
    assert sumofconnectionfilter(input_dict,taget_sum,"<") == (expected, "<")
    
@pytest.mark.parametrize("tagetsum, expected", [(3,expected_more3), (4,expected_more4), (6,expected_none), (1,expected_all)])
def test_sumofconnectionfilter_more(taget_sum, expected, input_dict):
    assert sumofconnectionfilter(input_dict,taget_sum,">") == (expected, ">")

def test_sumofconnectionfilter_eq():
    input_dict = {("proteinA","proteinB"):3,
                  ("proteinC","proteinD"):1,
                  ("proteinD","proteinE"):2,
                  ("proteinC","proteinE"):2}
    expected = {("proteinA","proteinB"):3,
                ("proteinC","proteinD"):1}
    assert sumofconnectionfilter(input_dict,3,"==") == (expected, "==")

def test_sumofconnectionfilter_neq():
    input_dict = {("proteinA","proteinB"):3,
                  ("proteinC","proteinD"):1,
                  ("proteinD","proteinE"):2,
                  ("proteinA","proteinE"):2}
    expected = {("proteinA","proteinE"):2}
    assert sumofconnectionfilter(input_dict,3,"!=") == (expected, "!=")