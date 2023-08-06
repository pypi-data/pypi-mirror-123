# This project contains the naive implementation of suffix-tree which is used to store the given string and find a given pattern in the string(stored in the tree)

## Folder structure
- `resources/` - contains our experiment results and test inputs
- `scripts` - contains python scripts(except the `setup.py` file which is in the root)
- The files under project root is required to properly package our script and build the command line tools
## Requirements:
- python version >= 3.9
- setuptools
- pip >= 3.9

## Installation:
- Using Pip:
```commandline
pip install pat-match-st
```
- Build locally:
    - Make sure you fulfil the requirements.
    - Run 
      - `python setup.py install`
      - `pip install .`
    - That's it.
    
- Finally, both the above methods will install this cmd tool: `search-st`.

## Usage:
```commandline
search-st [-h] [-fa FASTA_FILE] [-fq FASTQ_FILE]
```


```text
optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -fa FASTA_FILE, -fasta-file FASTA_FILE
                        fasta file
  -fq FASTQ_FILE, -fastq-file FASTQ_FILE
                        fastq file
```