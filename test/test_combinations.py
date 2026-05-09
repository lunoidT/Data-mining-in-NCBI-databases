#!/usr/bin/env python3

# for running pytest, run in test directory
import pytest

from namecombiner import combinations
filepath = "../testdata/"
# output used in many tests
expected_output = {("AraC family transcriptional regulator","magnesium transporter"):1,
                    ("AraC family transcriptional regulator","methyl-accepting chemotaxis protein"):1,
                    ("AraC family transcriptional regulator","glutamate-cysteine ligase family protein"):1,
                    ("glutamate-cysteine ligase family protein","magnesium transporter"):1,
                    ("glutamate-cysteine ligase family protein","methyl-accepting chemotaxis protein"):1,
                    ("magnesium transporter","methyl-accepting chemotaxis protein"):1}

### Testing with no quickfilter ###

def test_combinations_normal_input():
    PubmedID2names = {"19478949":set(["AraC family transcriptional regulator"]), 
                     "18165013":set(["AraC family transcriptional regulator","magnesium transporter","methyl-accepting chemotaxis protein","glutamate-cysteine ligase family protein"])}
    assert combinations(PubmedID2names) == expected_output

def test_combinations_list_input():
    PubmedID2names = {"19478949":["AraC family transcriptional regulator"], 
                     "18165013":["AraC family transcriptional regulator","magnesium transporter","methyl-accepting chemotaxis protein","glutamate-cysteine ligase family protein"]}
    assert combinations(PubmedID2names) == expected_output

def test_combinations_empty_dict():
    PubmedID2names = {}
    with pytest.raises(ValueError):
        combinations(PubmedID2names)

@pytest.mark.parametrize("PubmedID2names", [ {"19478949":set(), "18165013":set()},  {"19478949":set(["AraC family transcriptional regulator"]), "18165013":set()}])
def test_combinations_empty_entries(PubmedID2names):
    assert combinations(PubmedID2names) == {}

def test_combinations_repeated_names():
    PubmedID2names = {"19478949":["AraC family transcriptional regulator","AraC family transcriptional regulator"], 
                     "18165013":["magnesium transporter","glutamate-cysteine ligase family protein", "methyl-accepting chemotaxis protein","glutamate-cysteine ligase family protein"]}
    
    output = {("glutamate-cysteine ligase family protein","magnesium transporter"):1,
                       ("glutamate-cysteine ligase family protein","methyl-accepting chemotaxis protein"):1,
                       ("magnesium transporter","methyl-accepting chemotaxis protein"):1}
    
    assert combinations(PubmedID2names) == output

def test_combinations_single_entry():
   PubmedID2names = {"19478949":set(["AraC family transcriptional regulator"])}
   assert combinations(PubmedID2names) == {}

def test_combinations_intkey():
    PubmedID2names = {19478949:set(["AraC family transcriptional regulator"]), 
                     18165013:set(["AraC family transcriptional regulator","magnesium transporter","methyl-accepting chemotaxis protein","glutamate-cysteine ligase family protein"])}
    assert combinations(PubmedID2names) == expected_output


### Testing with quickfilter ###

def test_combinations_quickfilter_no_samp():
    PubmedID2names = {"19478949":set(["AraC family transcriptional regulator"]), 
                     "18165013":set(["AraC family transcriptional regulator","magnesium transporter","methyl-accepting chemotaxis protein","glutamate-cysteine ligase family protein"])}
    assert combinations(PubmedID2names,2) == {}

def test_combinations_quickfilter_w_samp():
    # Note: to use this, names list must be sorted in namecombiner.py
    import random
    random.seed(1000)
    PubmedID2names = {"19478949":set(["AraC family transcriptional regulator"]), 
                     "18165013":set(["AraC family transcriptional regulator","magnesium transporter","methyl-accepting chemotaxis protein","glutamate-cysteine ligase family protein"])}
    output = {('magnesium transporter', 'methyl-accepting chemotaxis protein'):1}
    assert combinations(PubmedID2names,2,True) == output
