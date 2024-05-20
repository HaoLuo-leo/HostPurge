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
* [Tips](#tips)
    * [Choosing the right mode](#choosing-the-right-mode)
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
