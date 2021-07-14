#Rscript mcpCounter.R inf.tsv out.tsv probe HUGO_symbols; data_type="probe" or "non-probe",gene_type="HUGO_symbols" or "ENTREZ_ID" 
library(curl)
library(MCPcounter)
run_mcpCounter<-function(data2,data_type,gene_type){
  if(data_type=="probe"){
    res<-MCPcounter.estimate(log10(data2),featuresType =  c(gene_type)[1])
  }else{res<-MCPcounter.estimate(data2,featuresType =  c(gene_type)[1])}
  return(res)
}

args=commandArgs(TRUE)
inf<-args[1]
outf<-args[2]
data_type<-args[3]
gene_type<-args[4]

data<-read.table(inf,header=TRUE,sep = "\t",quote = "",stringsAsFactors = F,check.names = F)
data1<-aggregate(data[c(2:ncol(data))],by=data[1],FUN=max)
data2<-data1[,2:ncol(data1)]
rownames(data2)<-data1[,1]
res=run_mcpCounter(data2,data_type,gene_type)
res1<-cbind(rownames(res),res)
colnames(res1)[1]<-"Types"
write.table(res1,outf,row.names = F,col.names = T,sep = "\t",quote = F)

