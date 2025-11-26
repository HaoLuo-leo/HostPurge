#!/bin/bash

# Create the bin directory in the prefix path
mkdir -p $PREFIX/bin

# Copy necessary Python scripts to the bin directory
cp $SRC_DIR/build_db.py $PREFIX/bin
cp $SRC_DIR/kneaddata_mode.py $PREFIX/bin
cp $SRC_DIR/kraken2_mode.py $PREFIX/bin
cp $SRC_DIR/hostpurge.py $PREFIX/bin

# Optionally, if there are any directories to be copied and compiled
# cp -rf $SRC_DIR/some_directory $PREFIX/bin

# If there are any make commands to be run, navigate to the appropriate directory and run them
# cd $PREFIX/bin/some_directory
# make



