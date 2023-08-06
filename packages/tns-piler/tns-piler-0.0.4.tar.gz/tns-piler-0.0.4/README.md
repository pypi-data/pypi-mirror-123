# Piler

## Requirements
- ``Python >= 3.6``
- ``pysam``
- ``gffuitls``

## Installation

```bash
pip install tns-piler
```

## Usage

Cumulative Pileups of particular genes
```bash
Piler -d [GFFutils formatted annotation] -t [Ensembl transcript ID] -o [Out location] [Indexed bam files]
```

## Output  
CSV with cumulative pileups for each position along the gene, no introns, first column is file name

