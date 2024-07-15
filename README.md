![image](https://github.com/HaoLuo-leo/HostPurge/assets/138950844/bc363a7a-4650-4c6d-979a-5ccc68167174)


HostPurge is a tool for removing host contamination from sequencing reads. It supports four modes, each designed for different scenarios based on the level of host contamination and the need for precision.

# Table of contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Modes](#modes)
* [Acknowledgements](#acknowledgements)
* [License](#license)

# Introduction

HostPurge is a versatile tool designed to remove host contamination from sequencing reads. It supports multiple modes of operation, allowing it to handle different levels of host contamination and precision requirements.

# Requirements

* Linux 
* Python 3.8 or later
* Bowtie2 2.2 or later
* Kraken2 2.1.2 or later
* krakentools
* fastp 0.23.1 or later

# Installation
Download the environmental file : environment.yml
```
wget https://raw.githubusercontent.com/HaoLuo-leo/HostPurge/main/environment.yml
```
### Install with pip
```
conda env create -f environment.yml
pip install hostpurge
```

These instructions install the most up-to-date version of HostPurge:

```bash
conda install luohao-leo::hostpurge
```
# Usage

### For detailed help information:
```
hostpurge --help
hostpurge qc --help
hostpurge build-db --help
hostpurge run --help 
```
### Quality control
```
hostpurge qc -i1 raw_1.fastq  -i2 raw_2.fastq -o1 clean_1.fastq -o2 clean_2.fastq -t 8
```
### Build database
#### kmer_db
Download NCBI taxonomy id as a part of database
```
mkdir luohao/taxonomy
cd luohao/taxonomy
wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz
wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz
wget ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz
gunzip nucl_gb.accession2taxid.gz nucl_wgs.accession2taxid.gz
tar -xzf taxdump.tar.gz
```
Build the kmer_db(note:'--db-name luohao' is the directory name of NCBI taxonomy id)
```
hostpurge build-db --db-type kmer  --db-name luohao --add-to-library name.fasta -t 8
```
## alignment_db
```
hostpurge build-db --db-type bowtie2 --input-fasta referencegenome.fasta -o db_name -s 1
```
### Run HostPurge with default mode which is same with mode c:
```
hostpurge run --kmer_db database/kraken2/human \
--bowtie2_db /data/meta/db/kneaddata/human/hg37dec_v0.1 \
-i1 anonymous_read0_1.fastq -i2 anonymous_read0_2.fastq \
-o1 aabbbbnony_1.fq -o2 aabbbbnony_2.fq \
--taxid 9606 -t 12
```
# Modes

HostPurge supports four modes, each suited for different contamination levels and precision needs:

Choosing the right mode

Mode a: Best for samples with low host contamination. This mode is slower but more thorough, making it ideal for sensitive samples where precision is critical.

Mode b: Fastest mode but with lower accuracy. Use this mode when you need quick results and the host contamination level is manageable.

Mode c: Recommended for samples with high host contamination. This mode balances speed and accuracy, providing reliable results for most scenarios.

Mode d: Best for samples with low host contamination but requiring high precision. This mode ensures the highest accuracy by using both KneadData and Kraken2 in sequence.

### Run HostPurge with a mode:
```
hostpurge run --mode a \
--bowtie2_db /data/meta/db/kneaddata/human/hg37dec_v0.1 \
-i1 anonymous_read0_1.fastq -i2 anonymous_read0_2.fastq \
-o1 aabbbbnony_1.fq -o2 aabbbbnony_2.fq \
-t 12
```

### Run HostPurge with b mode:
```
hostpurge run --mode b \
--kmer_db database/kraken2/human \
-i1 anonymous_read0_1.fastq -i2 anonymous_read0_2.fastq \
-o1 aabbbbnony_1.fq -o2 aabbbbnony_2.fq \
--taxid 9606 -t 12
```

### Run HostPurge with d mode:
```
hostpurge run --mode d \
--kmer_db database/kraken2/human \
--bowtie2_db /data/meta/db/kneaddata/human/hg37dec_v0.1 \
-i1 anonymous_read0_1.fastq -i2 anonymous_read0_2.fastq \
-o1 aabbbbnony_1.fq -o2 aabbbbnony_2.fq \
--taxid 9606 -t 12
```

# Acknowledgements



# License

HostPurge is licensed under the MIT License.
