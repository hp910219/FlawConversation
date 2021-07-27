#mut pair
#Rscript APP_mut_pair.R input_mut.tsv out_mut_table.tsv out_mut_matrix.tsv

## generate mut pair table
single_to_pair <- function(snv_matrix){
  ID=c()
  sample=c()
  count=1
  for(s in 1:ncol(snv_matrix)){
    sample_name=colnames(snv_matrix)[s]
    sample_mut_gene=snv_matrix[(!is.na(snv_matrix[,s]) & snv_matrix[,s]!=0),]
    genes=row.names(sample_mut_gene)
    if(length(genes)>1){
      for(i in 1:(length(genes)-1)){
        for(j in i:length(genes)){
          ID[count]=paste(genes[i],genes[j],sep=":")
          sample[count]=sample_name
          count=count+1
        }
      }
    }
  }
  return(data.frame( ID=ID, sample=sample))
}

## mut table 2 mut matrix,  change to 2gene-sample matrix
pair_table_to_matrix <- function(ID,sample,vaf=1){
  O <- data.frame(gene = ID, sample = sample, vaf = vaf)
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
input_mut_file <- args[1]
out_mut_table <- args[2]
out_mut_matrix <- args[3]

snv_matrix <- read.table(file = input_mut_file,header = T,sep = '\t',row.names = 1,check.names = F)
mut_table=single_to_pair(snv_matrix)
write.table(x = mut_table,file = out_mut_table,sep = '\t',quote=F,row.names = F)  
pair_matrix=pair_table_to_matrix(mut_table$ID, mut_table$sample, 1)
write.table(x = pair_matrix,file = out_mut_matrix,sep = '\t',quote=F,row.names = T,col.names = NA)

