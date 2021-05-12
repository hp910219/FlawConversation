#!/bin/bash

# please mount oss://biosoft:/home/biosoft oss://数据bucket:/data

input_vcf_file=$1
tumor_id=$2
normal_id=$3
out_maf_file=$4

vcf2maf_path=/opt/mskcc-vcf2maf/vcf2maf.pl
vep_path=/opt/vep/src/ensembl-vep/
vep_dir=/db/vep
GRCh37_vcf=$vep_dir/ExAC.0.3.GRCh37.vcf.gz
ref_fasta=/db/hg19/ucsc.hg19.nochr.fasta
enst_inhouse=/db/hg19/enst_inhouse



# run vcf2maf
perl $vcf2maf_path --input-vcf $input_vcf_file --output-maf $out_maf_file --vep-path $vep_path --vep-data $vep_dir --ncbi-build GRCh37 --species homo_sapiens --ref-fasta $ref_fasta --tumor-id $tumor_id --normal-id $normal_id --custom-enst $enst_inhouse
