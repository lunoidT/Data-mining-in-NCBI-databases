#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest

from cytomaker import cytoload
filepath = "../testdata/"

def test_cytoload_normal():
    expected_output = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
                       ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
                       ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
                       ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
                       ("PadR family transcriptional regulator","response regulator transcription factor"):3}
    
    assert cytoload(filepath + "testcytofile.csv") == expected_output

@pytest.mark.parametrize("filename", ["testemptyfile.csv", "testmissingnames.csv", "testnoweight.csv"])
def test_cytoload_malformed(filename):
    with pytest.raises(ValueError):
        cytoload(filepath + filename)

@pytest.mark.parametrize("filename", ["testwhitespace.csv", "testlastnewline.csv"])
def test_cytoload_whitespace(filename):
    expected_output = {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
                       ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
                       ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
                       ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
                       ("PadR family transcriptional regulator","response regulator transcription factor"):3}
    
    assert cytoload(filepath + filename) == expected_output