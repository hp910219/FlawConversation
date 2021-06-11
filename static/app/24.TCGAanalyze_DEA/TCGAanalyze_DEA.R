#eg:Rscript TCGAanalyze_DEA.R inf_exp.tsv inf_phe.tsv S_I S_II testDEG_out.tsv log
library(TCGAbiolinks)
run_TCGAanalyze_DEA<-function(inf_exp,inf_phe,group1Name,group2Name,outf,type){
  data_exp<-read.table(inf_exp,sep="\t",quote="",header=T,check.names=F,stringsAsFactors=F,na.strings="")
  data_group<-read.table(inf_phe,sep="\t",quote="",header=T,check.names=F,stringsAsFactors=F,na.strings="")
  group1<-data_group[data_group[,2]==group1Name,]
  group2<-data_group[!data_group[,2]==group1Name,]
  mat1<-data_exp[,group1[group1[,1] %in% colnames(data_exp),1]]
  mat2<-data_exp[,group2[group2[,1] %in% colnames(data_exp),1]]
  mat1<-as.matrix(mat1)
  rownames(mat1)<-data_exp[,1]
  mat2<-as.matrix(mat2)
  rownames(mat2)<-data_exp[,1]
  a=paste(colnames(mat1),"a-a-a",sep="-")
  b=paste(colnames(mat2),"a-a-a",sep="-")
  colnames(mat1)=a
  colnames(mat2)=b
  if(type=="log"){
    mat1[,]=sapply(mat1[,],exp)*100
    mat2[,]=sapply(mat2[,],exp)*100
  }
 # mat1[,]=sapply(mat1[,],exp)*100
 # mat2[,]=sapply(mat2[,],exp)*100
  dataDEGs <- TCGAanalyze_DEA(mat1 =mat1,mat2=mat2,Cond1type=group1Name,Cond2type=group2Name)
#  dataDEGs <- TCGAanalyze_DEA(mat1 =mat1,mat2=mat2,Cond1type=group1Name,Cond2type=group2Name,method="glmLRT")
  result=cbind(rownames(dataDEGs),dataDEGs)
  colnames(result)[1]<-"Gene"
  write.table(result,outf,sep="\t",quote=F,col.names=T,row.names=F)
}

args=commandArgs(TRUE)
inf_exp=args[1]
inf_phe=args[2]
group1Name=args[3]
group2Name=args[4]
outf=args[5]
type=args[6]
run_TCGAanalyze_DEA(inf_exp,inf_phe,group1Name,group2Name,outf,type)
