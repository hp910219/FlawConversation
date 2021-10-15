#!/bin/bash

file_a=$1
file_b=$2
result_file=$3

bedtools intersect -a $file_a -b $file_b  > $result_file
