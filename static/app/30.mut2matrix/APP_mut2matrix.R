####  T2 to T3/T6_0408 ######mut2matrix
#eg:Rscript APP_mut2matrix.R TCGA-STAD.mutect2_snv.tsv out_matrix.tsv
library(plyr)
library(tidyverse)

mut2matrix<-function(snv_filter){
  O <- data.frame(gene = snv_filter$gene, sample = snv_filter$Sample_ID, vaf = snv_filter$dna_vaf)
  colA <- 1
  colB <- 2
  colC <- 3
  X <- unique(O[,colA])
  Y <- unique(O[,colB])
  snv_matrix <- matrix(NA, nrow = length(X), ncol = length(Y),  dimnames=list(X,Y))
  for (i in 1:nrow(O)){
    source_node = O[i,colA]
    target_node = O[i,colB]
    value = O[i,colC]
    snv_matrix[source_node,target_node] = value
  }
  return(snv_matrix)
}

args<-commandArgs(TRUE)
input_snv_file<-args[1]
output_snv_file<-args[2]

snv <- read.table(input_snv_file, sep = "\t",  header = T, check.names = F, quote = "\"")
snv_filter <- snv[(grepl("missense_variant",snv$effect) 
                   | grepl("frameshift_variant",snv$effect) 
                   |grepl("stop_gained",snv$effect) 
                   | grepl("splice_donor_variant",snv$effect) 
                   | grepl("splice_acceptor_variant",snv$effect)
                   | grepl("inframe_deletion",snv$effect)
                   | grepl("stop_lost",snv$effect)
                   | grepl("start_lost",snv$effect)
                   | grepl("inframe_deletion",snv$effect)
                   | grepl("inframe_insertion",snv$effect)
                   | grepl("stop_retained_variant",snv$effect) ),]
snv_filter <- snv_filter[snv_filter$filter=="PASS",]
snv_matrix <- mut2matrix(snv_filter)
write.table(snv_matrix,file = output_snv_file,sep = "\t",quote = FALSE,row.names = TRUE, col.names = NA)

