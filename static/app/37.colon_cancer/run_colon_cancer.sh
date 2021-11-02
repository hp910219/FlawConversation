#!/bin/bash

input_file=$1
out_xlsx=$2

mv ${input_file} src/data_v7.csv
python experiment/diff_combination.py --data_version 7 --keys ABC,V4,Sig,DI7,KEGG7
rm src/data_v7.csv
mv temp/data_process/result_v7.xlsx ${out_xlsx}
