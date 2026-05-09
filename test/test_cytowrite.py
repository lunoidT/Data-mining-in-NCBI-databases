#!/usr/bin/env python3

# When running pytest, run in test directory
import pytest

from cytomaker import cytowrite
from cytomaker import cytoload

@pytest.fixture
def input_dict():
    return {("PadR family transcriptional regulator","winged helix-turn-helix domain-containing protein"):3,
            ("ArsR/SmtB family transcription factor","winged helix-turn-helix domain-containing protein"):2,
            ("LacI family DNA-binding transcriptional regulator","response regulator transcription factor"):3,
            ("helix-turn-helix transcriptional regulator","response regulator transcription factor"):4,
            ("PadR family transcriptional regulator","response regulator transcription factor"):3}

def test_cytowrite_normal(tmp_path,input_dict):
    filename = tmp_path / "testfile"
    cytowrite(filename,input_dict,"#testing")
    # using cytoload since it is already tested and safe
    assert cytoload(filename) == input_dict