#!/bin/bash

input_files=$1
out_file=$2

file_list=${input_files//,/ }

awk -F '\t' 'BEGIN{OFS="\t"}{if(FILENAME==ARGV[1]){if(FNR==1){print "id",$0;}else{print FILENAME,$0;}}else{if(FNR!=1){print FILENAME,$0;}}}' ${file_list} > ${out_file}
