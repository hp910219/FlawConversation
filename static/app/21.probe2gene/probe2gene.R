##eg:Rscript probe2gene.R inf_probe.tsv inf_exp.tsv out_symbol.tsv out_entrez.tsv
probe2gene<-function(inf_probe,inf_exp,outf_symbol,outf_entrezid){
  probe<-read.table(inf_probe,sep="\t",quote="",stringsAsFactors=F,check.names=F,comment.char="#",header=TRUE)
  if("Gene Symbol" %in% colnames(probe)){
    probe1<-probe[2:nrow(probe),c("ID","ENTREZ_GENE_ID","Gene Symbol")]
  }else{probe1<-probe[2:nrow(probe),c("ID","ENTREZ_GENE_ID","Symbol")]}
  index=grep("///",probe1[,c("Gene Symbol")],value=F) ##一个探针对应多个基因，需要被去除
  if(length(index)==0){
    probe2<-probe1
  }else{probe2<-probe1[-index,]}
 
  probe2<-na.omit(probe2) ##去除na的
  probe3<-probe2[probe2[,c("ENTREZ_GENE_ID")]!="",]##去除entrez id为空的
  
  exp<-read.table(inf_exp,sep="\t",quote="",stringsAsFactors=F,check.names=F,comment.char="!")
  exp1<-exp[2:nrow(exp),]
  colnames(exp1)<-gsub('["]','',exp[1,])
  b<-gsub('["]','',exp1[,1])
  exp2<-cbind(b,exp1[,2:ncol(exp1)])
  exp3<-exp2[exp2[,1] %in% probe3[,1],]
  
  merge_f<-merge(exp3,probe3,by.x="b",by.y="ID")
  merge_f[c(2:ncol(exp3))]<-sapply(merge_f[c(2:ncol(exp3))],as.numeric)
  data_symbol<-aggregate(merge_f[c(2:ncol(exp3))],by=merge_f[ncol(exp3)+2],FUN=mean)
  data_entrezid<-aggregate(merge_f[c(2:ncol(exp3))],by=merge_f[ncol(exp3)+1],FUN=mean)
  write.table(data_symbol,outf_symbol,sep="\t",quote=F,col.names=T,row.names=F)
  write.table(data_entrezid,outf_entrezid,sep="\t",quote=F,col.names=T,row.names=F)
  
}

args<-commandArgs(TRUE)
inf_probe=args[1]
inf_exp=args[2]
outf_symbol=args[3]
outf_entrezid=args[4]
probe2gene(inf_probe,inf_exp,outf_symbol,outf_entrezid)
