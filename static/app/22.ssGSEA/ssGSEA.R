library(GSVA)
ssGSEA<-function(inf_set,inf_exp,outf){
  data_set<-read.table(inf_set,sep="\t",quote="",header=T,check.names=F,stringsAsFactors=F)
  data_exp<-read.table(inf_exp,sep="\t",quote="",header=T,check.names=F,stringsAsFactors=F)
  data_exp1<-aggregate(data_exp[c(2:ncol(data_exp))],by=data_exp[1],FUN=max) #重复基因取最大值
  data_exp2<-data_exp1[,2:ncol(data_exp1)]
  rownames(data_exp2)<-data_exp1[,1]
  data_exp<-data_exp2
  data_exp<-data_exp[!apply(data_exp,1,sum)==0,] #去除所有样本中表达为0的基因
  data_exp<-as.matrix(data_exp)
  l<-as.list(data_set)
  ssgsea_score = gsva(data_exp,l, method = "ssgsea", ssgsea.norm = TRUE, verbose = TRUE)
  ssgsea<-cbind(as.data.frame(rownames(ssgsea_score)),ssgsea_score)
  colnames(ssgsea)[1]<-"ID"
  write.table(ssgsea,outf,sep="\t",quote=F,col.names=T,row.names=F)
}

args=commandArgs(TRUE)
inf_set<-args[1]
inf_exp<-args[2]
outf<-args[3]
ssGSEA(inf_set,inf_exp,outf)
