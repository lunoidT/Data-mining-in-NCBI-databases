#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest

# Because of the wrapper in the filtering.py, which requires user input, it is difficult to call the function from import.
# Therefore the function is inserted directly in this file:
def weightfilter(instance_dict:dict, weight:int, op:str):
    """ Selects entries with a specific weight in dictionary.
    Dictionary structure: {(x.y):weight} """
    filtered_dict = {}

    # O(n)
    for key in instance_dict: 
        if eval(f"{instance_dict[key]} {op} {weight}"):
            filtered_dict[key] = instance_dict[key]

    # Overall runtime O(n+1). Simplified O(n)
    return filtered_dict, op

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

expected_less4 = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
            ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
            ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
            ("PadR family transcriptional regulator","response regulator transcription factor"):3}

expected_only2 = {("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2}

expected_none = {}

expected_only4 = {("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4}

expected_more2 = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
            ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
            ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
            ("PadR family transcriptional regulator","response regulator transcription factor"):3}


### Testing ###
@pytest.mark.parametrize("weight, expected", [(5,expected_all), (4,expected_less4), (3,expected_only2), (2,expected_none)])
def test_weightfilter_less(weight, expected, input_dict):
    assert weightfilter(input_dict,weight,"<") == (expected, "<")
    
@pytest.mark.parametrize("weight, expected", [(4,expected_none), (3,expected_only4), (2,expected_more2), (1,expected_all)])
def test_weightfilter_more(weight, expected, input_dict):
    assert weightfilter(input_dict,weight,">") == (expected, ">")

@pytest.mark.parametrize("weight, expected", [(4,expected_only4), (2,expected_only2), (6,expected_none)])
def test_weightfilter_eq(weight, expected, input_dict):
    assert weightfilter(input_dict,weight,"==") == (expected, "==")

@pytest.mark.parametrize("weight, expected", [(4,expected_less4), (5,expected_all)])
def test_weightfilter_neq(weight, expected, input_dict):
    assert weightfilter(input_dict,weight,"!=") == (expected, "!=")