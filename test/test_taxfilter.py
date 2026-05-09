#!/usr/bin/env python3
import pytest
import sys

# edit sys path
sys.path.append("..")

from src.func.taxfiltering import taxfilter
filepath = "../testdata/"

# testing a snippet of normal input
def test_normal_input():
    