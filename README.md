# Data-mining-in-NCBI-databases
Authors Luna Thorhauge and Marius Kopp Armangué

# Running cytomaker.py
To properly run this, don't go into the src/ folder. Instead run from the mother folder "DATA-MINING-IN-NCBI-DATABASES" and run using "./src/cytomaker.py <tax_id> [filter] [-q <int> [-s]]"

## The help function
The help function is here of further aid if one is uncertain on how to use the filters. To call it, remain in the same folder and use "./src/cytomaker.py help"

# Running unit tests
CD into the test/ folder and run pytest from there by simply writing "pytest".
The only exception is test_combinations.py, where you need to make an edit before running. See line 38 in namecombiner for this exact case.