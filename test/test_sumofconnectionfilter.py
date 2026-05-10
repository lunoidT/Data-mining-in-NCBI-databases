#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest

# Because of the wrapper in the filtering.py, which requires user input, it is difficult to call the function from import.
# Therefore the function is inserted directly in this file:
def sumofconnectionfilter(instancedict:dict, targetsum:int, op:str):
    """ Computes the weighed sum of connections and filters accordingly for each gene entry."""
    connectiondict = dict()

    # Due to the three columns in outputfile (and therefore connectiondict) "gene1, gene2, weight", both [0] and [1] are investigated
    # O(n) 
    for connected_instance in instancedict:
        if (connected_instance[0] in connectiondict):
            connectiondict[connected_instance[0]] += int(instancedict[connected_instance])
        else:
            connectiondict[connected_instance[0]] = int(instancedict[connected_instance])
        if (connected_instance[1] in connectiondict):
            connectiondict[connected_instance[1]] += int(instancedict[connected_instance])
        else:
            connectiondict[connected_instance[1]] = int(instancedict[connected_instance])

    # all connections to genes with unacceptible targetsum are removed 
    # O(n)
    for key in list(instancedict.keys()):
        if not eval(f"{connectiondict[key[0]]} {op} {targetsum}"):
            del instancedict[key]
        elif not eval(f"{connectiondict[key[1]]} {op} {targetsum}"):
            del instancedict[key]

    # Overall runtime O(2n + 1). After simplifying: O(n)
    return instancedict, op

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
def test_sumofconnectionfilter_less(tagetsum, expected, input_dict):
    assert sumofconnectionfilter(input_dict,tagetsum,"<") == (expected, "<")
    
@pytest.mark.parametrize("tagetsum, expected", [(3,expected_more3), (4,expected_more4), (6,expected_none), (1,expected_all)])
def test_sumofconnectionfilter_more(tagetsum, expected, input_dict):
    assert sumofconnectionfilter(input_dict,tagetsum,">") == (expected, ">")

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