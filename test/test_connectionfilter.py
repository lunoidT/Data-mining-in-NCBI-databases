#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest
from func.namecombiner import combinations

# Because of the wrapper in the filtering.py, which requires user input, it is difficult to call the function from import.
# Therefore the function is inserted directly in this file:
def connectionfilter(pubidnames:dict, min_connections:int, op:str):
    """ Selects entries with a specific amount of connections to same common PubMed ID. """
    from func.namecombiner import combinations

    # creates the instance_dict (here connection_dict to differentiate) whilst filtering
    connection_dict = dict()

    # O(m) (m due to us looping over pubIDs instead of names from the instance_dict)
    for connected_instance in pubidnames:
        if eval(f"{len(pubidnames[connected_instance])} {op} {min_connections}"):
            connection_dict[connected_instance] = pubidnames[connected_instance]

    # creates a dictionary for all combinations with the remaining entires after filtering 
    # O(m*k^2) will be the worst case scenario here. See namecombiner.py for distinctions between cases.
    try:
        combined_dict = combinations(connection_dict)
    # if all entries are removed by filter, combinations will raise ValueError
    except ValueError:
        combined_dict = {}

    # Overall runtime O(m*k^2 + m + 1). Simplified: O(m*k^2)
    return (combined_dict), op

### Input and output ###
@pytest.fixture
def input_dict():
    return {'10339418': {'GAF domain-containing sensor histidine kinase', 'sensor histidine kinase', 'CHASE domain-containing sensor histidine kinase', 'hybrid sensor histidine kinase/response regulator', 'chemotaxis protein CheA', 'ATP-binding protein'}, 
            '31594927': {'50S ribosomal protein L16', '30S ribosomal protein S8', 'cell division protein FtsA', '30S ribosomal protein S21', 'translation initiation factor IF-1', '50S ribosomal protein L28', 'ArsR/SmtB family transcription factor',},
            '15993072': {'TonB-dependent receptor'},
            '19047729': {'LysR family transcriptional regulator ArgP', 'LysR family transcriptional regulator', 'transcriptional regulator GcvA'}}

expected_none = {}

expected_all = combinations({'10339418': {'GAF domain-containing sensor histidine kinase', 'sensor histidine kinase', 'CHASE domain-containing sensor histidine kinase', 'hybrid sensor histidine kinase/response regulator', 'chemotaxis protein CheA', 'ATP-binding protein'}, 
                '31594927': {'50S ribosomal protein L16', '30S ribosomal protein S8', 'cell division protein FtsA', '30S ribosomal protein S21', 'translation initiation factor IF-1', '50S ribosomal protein L28', 'ArsR/SmtB family transcription factor',},
                '15993072': {'TonB-dependent receptor'},
                '19047729': {'LysR family transcriptional regulator ArgP', 'LysR family transcriptional regulator', 'transcriptional regulator GcvA'}})

expected_15993072 = combinations({'15993072': {'TonB-dependent receptor'}})

expected_31594927 = combinations({'31594927': {'50S ribosomal protein L16', '30S ribosomal protein S8', 'cell division protein FtsA', '30S ribosomal protein S21', 'translation initiation factor IF-1', '50S ribosomal protein L28', 'ArsR/SmtB family transcription factor',}})

expected_19047729 = combinations({'19047729': {'LysR family transcriptional regulator ArgP', 'LysR family transcriptional regulator', 'transcriptional regulator GcvA'}})

expected_more3 = combinations({'10339418': {'GAF domain-containing sensor histidine kinase', 'sensor histidine kinase', 'CHASE domain-containing sensor histidine kinase', 'hybrid sensor histidine kinase/response regulator', 'chemotaxis protein CheA', 'ATP-binding protein'}, 
                  '31594927': {'50S ribosomal protein L16', '30S ribosomal protein S8', 'cell division protein FtsA', '30S ribosomal protein S21', 'translation initiation factor IF-1', '50S ribosomal protein L28', 'ArsR/SmtB family transcription factor',}})

expected_neq_expected_15993072 = combinations({'10339418': {'GAF domain-containing sensor histidine kinase', 'sensor histidine kinase', 'CHASE domain-containing sensor histidine kinase', 'hybrid sensor histidine kinase/response regulator', 'chemotaxis protein CheA', 'ATP-binding protein'}, 
                                  '31594927': {'50S ribosomal protein L16', '30S ribosomal protein S8', 'cell division protein FtsA', '30S ribosomal protein S21', 'translation initiation factor IF-1', '50S ribosomal protein L28', 'ArsR/SmtB family transcription factor',},
                                  '19047729': {'LysR family transcriptional regulator ArgP', 'LysR family transcriptional regulator', 'transcriptional regulator GcvA'}})

### Testing ###

@pytest.mark.parametrize("min_connections, expected", [(2,expected_15993072), (1,expected_none), (4,expected_19047729), (8,expected_all)])
def test_connectionfilter_less(input_dict, min_connections, expected):
    assert connectionfilter(input_dict,min_connections,"<") == (expected, "<")
    
@pytest.mark.parametrize("min_connections, expected", [(3,expected_more3), (0,expected_all), (6,expected_31594927), (1,expected_neq_expected_15993072)])
def test_connectionfilter_more(input_dict, min_connections, expected):
    assert connectionfilter(input_dict,min_connections,">") == (expected, ">")

@pytest.mark.parametrize("min_connections, expected", [(1,expected_15993072), (0,expected_none), (3,expected_19047729)])
def test_connectionfilter_eq(input_dict, min_connections, expected):
    assert connectionfilter(input_dict,min_connections,"==") == (expected, "==")

@pytest.mark.parametrize("min_connections, expected", [(1,expected_neq_expected_15993072), (0,expected_all)])
def test_connectionfilter_neq(input_dict, min_connections, expected):
    assert connectionfilter(input_dict,min_connections,"!=") == (expected, "!=")