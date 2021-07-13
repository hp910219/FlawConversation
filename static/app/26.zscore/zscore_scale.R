##zscore scale
##eg:Rscript zscore_scale.R input.tsv out.tsv
zscore_scale<-function(data){
  data_scale<-apply(data[,],1,scale)
  rownames(data_scale)<-colnames(data)
  data_format<-cbind(colnames(data_scale),t(data_scale))
  colnames(data_format)[1]<-"gene"
  return(data_format)
}

args=commandArgs(TRUE)
inf<-args[1]
outf<-args[2]
data<-read.table(inf,sep="\t",quote="",header=TRUE,check.names=FALSE,stringsAsFactors=FALSE,row.names=1)
data_format<-zscore_scale(data)
write.table(data_format,outf,sep="\t",quote=F,col.names=T,row.names=F)
