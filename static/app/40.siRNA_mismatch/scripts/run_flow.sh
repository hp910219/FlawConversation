#$1=scripts_dir,$2=work_dir,$3=siRNA_file,$4=target_seq.fasta,$5=result_dir
#eg:sh scripts/run_flow.sh /mnt/JINGD/data/app/scripts/siRNA_mismatch/scripts/ /mnt/JINGD/data/app/scripts/siRNA_mismatch siRNA.tsv  subject.fasta /mnt/JINGD/data/app/scripts/siRNA_mismatch/results/

##1、建库
#docker run -it -v /mnt/dechao/hbv/:/data bc_biosoft
docker run --rm -v $1:/scripts -v $2:/data -v $5:/result bc_biosoft  makeblastdb -in /data/$4 -dbtype nucl -parse_seqids -out /data/$4

##2、将上传的siRNA序列格式化成input_len.tsv，并输出out.fasta文件
docker run --rm -v $1:/scripts -v $2:/data  -v $5:/result bio_r Rscript /scripts/getFa.R /data/$3 /result/siRNA.fasta /result/siRNA_len.tsv

##blast匹配
#docker run -it -v /mnt/dechao/hbv/:/data bc_biosoft
docker run --rm -v $1:/scripts -v $2:/data -v $5:/result bc_biosoft blastall -p blastn -i /result/siRNA.fasta  -d /data/$4 -o /result/out.blastall -e 500 -m 8 -W 7

##获取需求信息
docker run --rm -v $1:/scripts -v $2:/data -v $5:/result bio_r Rscript /scripts/get_blast_info.R /result/siRNA_len.tsv /result/out.blastall /data/$4 /result/blast_result_all.tsv /result/blast_result_final.tsv

