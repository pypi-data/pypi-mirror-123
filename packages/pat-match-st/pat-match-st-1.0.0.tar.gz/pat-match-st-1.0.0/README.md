# This project contains two programs viz. search-naive and search-ba to search for patterns in the given string using the naive and border-array appraoch respectively.

## Folder structure
- `resources/` - contains our experiment results and test inputs
- `scripts` - contains python scripts(except the `setup.py` file which is in the root)
- The files under project root is required to properly package our script and build the command line tools
## Requirements:
- python v >= 3.9
- setuptools
- pip

## Installation:
- Using Pip:
```commandline
pip install pat-match
```
- Build locally:
    - Make sure you fulfil the requirements.
    - Run 
      - `python setup.py install`
      - `pip install .`
    - That's it.
    
- Finally, both the above methods will install two cmd tools: `search-naive` and `search-ba`.

## Usage:
```commandline
search-naive [-h] [-fa FASTA_FILE] [-fq FASTQ_FILE]
```

```commandline
search-ba [-h] [-fa FASTA_FILE] [-fq FASTQ_FILE]
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