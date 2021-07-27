##matrix2mut
# Rscript APP_matrix2mut.R T2.0401.dudengxuexi.0414.train.mingan.30.txt out_mut.tsv
matrix2mut<-function(mut){
  ID=c()
  sample=c()
  vaf=c()
  
  count=1
  
  for(i in 1:nrow(mut)){
    for(j in 1:ncol(mut)){
      if(mut[i,j]>0 && mut[i,j]!=100 && mut[i,j]!=200){
        sample[count]=colnames(mut)[j]
        ID[count]=row.names(mut)[i]
        vaf[count]=mut[i,j]
        count=count+1;
      }
    }
  }
  return(list(sample,ID,vaf))
}

args<-commandArgs(TRUE)
input_mut_file<-args[1]
out_mut_table<-args[2]

mut <- read.table(file = input_mut_file,header = T,sep = '\t',row.names = 1,check.names = F)
sample=matrix2mut(mut)[[1]]
ID=matrix2mut(mut)[[2]]
vaf=matrix2mut(mut)[[3]]
write.table(x = data.frame(sample=sample, ID=ID,vaf=vaf),file = out_mut_table,sep = '\t',quote=F,row.names = F)
