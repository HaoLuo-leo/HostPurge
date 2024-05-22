<p align="center"><img src="misc/logo.png" alt="HostPurge" width="600"></p>

HostPurge is a tool for removing host contamination from sequencing reads. It supports four modes, each designed for different scenarios based on the level of host contamination and the need for precision.

# Table of contents

* [Introduction](#introduction)
* [Requirements](#requirements)
* [Installation](#installation)
    * [Install from source](#install-from-source)
* [Usage](#usage)
* [Modes](#modes)
* [Output files](#output-files)
* [Acknowledgements](#acknowledgements)
* [License](#license)

# Introduction

HostPurge is a versatile tool designed to remove host contamination from sequencing reads. It supports multiple modes of operation, allowing it to handle different levels of host contamination and precision requirements.

# Requirements

* Linux or macOS
* Python 3.8 or later
* KneadData 0.12.0 or later
* Kraken2 2.1.2 or later

# Installation

### Install from source

These instructions install the most up-to-date version of HostPurge:

```bash
conda install hostpurge
```
# Usage

### Run HostPurge with the desired mode:
```
hostpurge input_1.fastq input_2.fastq output_dir --mode [a|b|c|d] [additional options]
```
### For detailed help information:
```
hostpurge --help
```
# Modes

HostPurge supports four modes, each suited for different contamination levels and precision needs:

Choosing the right mode

Mode a: Best for samples with low host contamination. This mode is slower but more thorough, making it ideal for sensitive samples where precision is critical.

Mode b: Fastest mode but with lower accuracy. Use this mode when you need quick results and the host contamination level is manageable.

Mode c: Recommended for samples with high host contamination. This mode balances speed and accuracy, providing reliable results for most scenarios.

Mode d: Best for samples with low host contamination but requiring high precision. This mode ensures the highest accuracy by using both KneadData and Kraken2 in sequence.

# Output files

HostPurge generates the following output files in the specified output directory:

cleaned_reads_1.fastq: Cleaned reads from input_1

cleaned_reads_2.fastq: Cleaned reads from input_2

host_contamination_report.txt: Report detailing the host contamination removal process

log.txt: Log file with detailed process information

# Acknowledgements

HostPurge was developed with contributions from the bioinformatics community. Special thanks to the developers of KneadData and Kraken2, whose tools are integral to the functionality of HostPurge.

# License

HostPurge is licensed under the MIT License.
