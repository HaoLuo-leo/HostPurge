![image](https://github.com/HaoLuo-leo/HostPurge/assets/138950844/bc363a7a-4650-4c6d-979a-5ccc68167174)


HostPurge is a tool for removing host contamination from sequencing reads. It supports four modes, each designed for different scenarios based on the level of host contamination and the need for precision.

# Table of contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Modes](#modes)
* [Result](#result)
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
conda activate hostpurge
pip install hostpurge
```

### Install with conda:

```bash
conda env create -f environment.yml
conda activate hostpurge
conda install hostpurge
```
### Install with download and unzip:
```
#Specify the conda file name
s=hostpurge

#Download the package
wget https://github.com/HaoLuo-leo/HostPurge/releases/download/v1.2.1/hostpurge-1.2.1-linux.tar.gz

#Specify the installation directory
mkdir -p ${soft}/envs/${s}
tar -xvzf ${s}.tar.gz -C ${soft}/envs/${s}

#Boot environment
conda activate ${s}

#Initialize the environment
conda unpack
```
# Usage
![image](https://github.com/user-attachments/assets/4b2c9e35-562b-4e17-989f-619adf70b897)



HostPurge have four models for your choose, and you can choose each of them as our suggested in github.
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

Reference genome fasta file not downloaded from NCBI may need their taxonomy information assigned explicitly.
Such as >GWHBFPX00000001|kraken:taxid|9606  Adapter sequence

The taxnonomy id could be found in https://www.ncbi.nlm.nih.gov/datasets/taxonomy/.

Note: Sometimes, there are plenty of fasta files need modify their  taxonomy information, so we could use the following code to deal with them.

#awk '/^>/ { sub(">", "", $1); $0 = ">" $1 "|kraken:taxid|39947  Adapter sequence" } 1' rice.genome.fasta>rice.genome_1.fasta

#awk '/^>/ { sub(">", "", $1); $0 = ">" $1 "|kraken:taxid|9606  Adapter sequence" } 1' human_genome.fasta>human_genome_1.fasta

```
hostpurge build-db --db-type kmer  --db-name human_kmer_db --add-to-library human.fasta -t 24
```
Download taxonomy might be cost we several times based on the internet of linux, so we could download it from website and upload them to linux.

website of three files needed: 

https://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz;

https://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz;

https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
```
mkdir db_name/taxonomy
gunzip nucl_gb.accession2taxid.gz db_name/taxonomy
gunzip nucl_wgs.accession2taxid.gz db_name/taxonomy
tar zxf taxdump.tar.gz  db_name/taxonomy
```
If you download taxonomy by yourself, please use
```
hostpurge build-db --db-type kmer  --db-name human_kmer_db --add-to-library human.fasta -t 24 --bypass-tax
```
#### alignment_db
```
hostpurge build-db --db-type alignment --input-fasta human.fasta -o human_alignment_db 
```
### Run HostPurge with default mode which is same with mode c:
```
hostpurge run --kmer_db human_kmer_db \
--alignment_db human_alignment_db \
-i1 demohuman0_1.fastq -i2 demohuman0_2.fastq \
-o1 filter_1.fq -o2 filter_2.fq \
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
--alignment_db human_alignment_db \
-i1 demohuman0_1.fastq -i2 demohuman0_2.fastq \
-o1 filter_1.fq -o2 filter_2.fq \
-t 12
```

### Run HostPurge with b mode:
```
hostpurge run --mode b \
--kmer_db human_kmer_db \
-i1 demohuman0_1.fastq -i2 demohuman0_2.fastq \
-o1 filter_1.fq -o2 filter_2.fq \
--taxid 9606 -t 12
```

### Run HostPurge with d mode:
```
hostpurge run --mode d \
--kmer_db human_kmer_db \
--alianment_db human_alignment_db \
-i1 demohuman0_1.fastq -i2 demohuman0_2.fastq \
-o1 filter_1.fq -o2 filter_2.fq \
--taxid 9606 -t 12
```
# Result
The following Python script will generate a table and a visual result.
```
# Download the depletion_rate_with_plot.py script file
wget https://github.com/HaoLuo-leo/HostPurge/blob/main/depletion_rate_with_plot.py

# Install the matplotlib library for plotting
pip install matplotlib

# Run the depletion_rate_with_plot.py script
# -i1 and -i2 specify the input fastq files
# -f1 and -f2 specify the filtered fastq files
# -t specifies the output TSV file
# -p specifies the output PNG file
python depletion_rate_with_plot.py -i1 demo_1.fq -i2 demo_2.fq -f1 filter_1.fq -f2 filter_2.fq -t o.tsv -p o.png

```
The result of demo data is as follow:
![image](https://github.com/user-attachments/assets/a85fe2ea-d8a0-4a69-8ccd-1fa966859cd6)

![image](https://github.com/user-attachments/assets/08fced13-30cc-4a0b-ae86-68555c0dc3c6)



# License

HostPurge is licensed under the MIT License.
