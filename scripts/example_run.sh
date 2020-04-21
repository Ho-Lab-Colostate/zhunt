#!/usr/bin/env bash

########################################################################
# Example script for Z-Hunt workflow
########################################################################

INPUT_FILE=./test/data/example_input0.fasta
ZHUNT_OPTS="24 6 24"
ZHUNT_OPTS="$ZHUNT_OPTS $INPUT_FILE"

time ./bin/zhunt $ZHUNT_OPTS
