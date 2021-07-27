pathway_DI<-function(T6.DI,KEGG.gmt,T6){

  sample_DI=matrix(NA,nrow=nrow(KEGG.gmt),ncol=ncol(T6))
  row.names(sample_DI)=row.names(KEGG.gmt)
  colnames(sample_DI)=colnames(T6)

  for(i in 1:nrow(KEGG.gmt)){
    gene <- unlist(KEGG.gmt[i,])
    gene.1 <- intersect(gene,rownames(T6.DI))
    gene.2 <- intersect(gene.1,row.names(T6))
    for(j in 1:ncol(T6)){
      gene_mut=T6[gene.2,j]
      gene_mut[gene_mut[]>0]=1
      gene_di=T6.DI[gene.2,1]
      sum_di=sum(gene_mut*gene_di)
      sample_DI[i,j]=sum_di
    }
  }
  return(sample_DI)
}

args=commandArgs(TRUE)

input_T6.DI_file <- args[1]
input_KEGG.gmt_file <- args[2]
input_T6_sample_file<- args[3]
output_sample_di_file <- args[4]

T6.DI <- read.table(file = input_T6.DI_file,header = T,sep = "\t",quote = "",row.names = 1,check.names = F)
KEGG.gmt <- read.table(file = input_KEGG.gmt_file,header = F,sep = "\t",quote = "",row.names = 1,check.names = F)
T6 <- read.table(file = input_T6_sample_file,header = T,sep = "\t",quote = "",row.names = 1,check.names = F)
KEGG.gmt <- KEGG.gmt[,-1]

sample_DI=pathway_DI(T6.DI,KEGG.gmt,T6)
write.table(sample_DI,file=output_sample_di_file,sep="\t",quote=F,row.names = TRUE,col.names = NA)
