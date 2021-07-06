pathway_DI<-function(input_T6.DI_file,input_KEGG.gmt_file,output_KEGG_file){
  T6.DI <- read.table(file = input_T6.DI_file,header = T,sep = "\t",quote = "",row.names = 1,check.names = F)
  KEGG.gmt <- read.table(file = input_KEGG.gmt_file,header = F,sep = "\t",quote = "",row.names = 1,check.names = F)
  KEGG.gmt <- KEGG.gmt[,-1]
  
  
  sink(output_KEGG_file)
  cat("pathway,SUM.DI,count,count>0\n")
  
  for(i in 1:nrow(KEGG.gmt)){
    gene <- unlist(KEGG.gmt[i,])
    gene.1 <- intersect(gene,rownames(T6.DI))
    qiuhe <- sum(T6.DI[gene.1,])
    A <- T6.DI[gene.1,]
    
    out2 <- length(gene.1)
    out3 <- length(A[A!= 0])
    
    cat(paste(row.names(KEGG.gmt)[i],qiuhe,out2,out3,sep=","))
    cat("\n")
    
  }
  sink()
}

args=commandArgs(TRUE)

input_T6.DI_file <- args[1]
input_KEGG.gmt_file <- args[2]
output_KEGG_file <- args[3]

pathway_DI(input_T6.DI_file,input_KEGG.gmt_file,output_KEGG_file)
