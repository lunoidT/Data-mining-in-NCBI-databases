#!/usr/bin/env python3

# for running pytest, run in test directory
import pytest

from taxfiltering import taxfilter
filepath = "../testdata/"

# testing a snippet of normal input
def test_taxfilter_normal_input():
    file_info = filepath + "testgene_info"
    file_gene2pubmed = filepath + "test2pubmed"

    expected_dict = {"19478949":set(["AraC family transcriptional regulator"]), 
                     "18165013":set(["AraC family transcriptional regulator","magnesium transporter","methyl-accepting chemotaxis protein","glutamate-cysteine ligase family protein"]), 
                     "9195888":set(["aldehyde dehydrogenase family protein"]), 
                     "19798051":set(["magnesium transporter"]), 
                     "20738376":set(["methyl-accepting chemotaxis protein"]), 
                     "20206133":set(["DEAD/DEAH box helicase"]), 
                     "18812186":set(["glutamate-cysteine ligase family protein"])}
    
    pubID2names = taxfilter(file_info, file_gene2pubmed,"673")
    assert pubID2names == expected_dict

# testing if removing translation from gene ID to gene name, causes an error
def test_taxfilter_corrupt_gene_info():
    file_info = filepath + "testgene_info_some_removed"
    file_gene2pubmed = filepath + "test2pubmed"
    with pytest.raises(KeyError):
        pubID2names = taxfilter(file_info, file_gene2pubmed,"673")

