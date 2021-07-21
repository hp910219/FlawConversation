##eg:Rscript  APP.cal_pathway_mut.R   KEGG.gmt.txt snv.out.tsv pathway.out.matrix.tsv pathway.out.table.tsv pathway.out.pair.tsv
####  T2 to T3/T6_0408 ######

library(plyr)
library(tidyverse)



cal_pathway_mut<-function(snv_matrix,gmt){
  M=matrix(NA,nrow=nrow(gmt), ncol=ncol(snv_matrix))
  row.names(M)=row.names(gmt)
  colnames(M)=colnames(snv_matrix)
  
  pathway_out=c()
  samples_out=c()
  count_out=c()
  n=1
  
  
  
  for(i in  1:nrow(gmt)){
    gene_set=gmt[i,]
    name=row.names(gmt)[i]
    gene=gene_set[c(-1)]
    #gene=intersect(gene,row.names(snv_matrix))
    for(j in 1:ncol(snv_matrix)){
      sample=colnames(snv_matrix)[j]
      gene_j_mutated=intersect(as.vector(t(gene)),row.names(snv_matrix)[!is.na(snv_matrix[,j])])
      M[i,j]=length(gene_j_mutated)
      pathway_out[n]=name
      samples_out[n]=sample
      count_out[n]=length(gene_j_mutated)
      n=n+1
    }
  }
  
  N=data.frame(pathway=pathway_out,sample=samples_out,count=count_out)
  
  
  
  t <- matrix(NA, nrow = nrow(M)*nrow(M), ncol = ncol(M))
  colnames(t)<-colnames(M)
  row.names(t)<-1:nrow(t)
  t_row_count=1
  
  for(ii in 1:(nrow(M)-1)){
    for(jj in (ii+1):nrow(M)){
      pathway1=row.names(M)[ii]
      pathway2=row.names(M)[jj]
      xx=M[ii,]
      yy=M[jj,]
      xx[xx[]>0]=1
      yy[yy[]>0]=1
      name=paste(pathway1,pathway2,sep=":")
      t[t_row_count,]<-xx+yy
      row.names(t)[t_row_count]=name
      t_row_count=t_row_count+1
    }
  }
  return(list(M,N,t))
}

args<-commandArgs(TRUE)
input_gmt_file <- args[1]
input_snv_file <- args[2]
output_pathway_matrix_file <- args[3]
output_pathway_table_file <- args[4]
output_pathway_pair_file <- args[5]




snv_matrix <- read.table(input_snv_file, sep = "\t",  header = T,row.names = 1, check.names = F, quote = "\"")
gmt <- read.table(input_gmt_file, sep = "\t", row.names=1, head =F, check.names = F,  quote = "\"")

pathway_data=cal_pathway_mut(snv_matrix,gmt)
M=pathway_data[[1]]
N=pathway_data[[2]]
t=pathway_data[[3]]
write.table(M, file = output_pathway_matrix_file, sep = "\t", quote = FALSE, row.names = TRUE,col.names = NA)
write.table(N, file = output_pathway_table_file, sep = "\t", quote = FALSE, row.names = FALSE,col.names = T)
write.table(t, file = output_pathway_pair_file, sep = "\t", quote = FALSE, row.names = T,col.names = NA)


