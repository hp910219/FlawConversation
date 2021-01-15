##Rscript tTest.R inf_exp.tsv inf_phe.tsv groupA groupB tTest_out.tsv
t_test<-function(inf_exp,inf_phe,groupA_name,groupB_name,outfile){
  data<-read.table(inf_exp,sep="\t",quote = "",stringsAsFactors = FALSE,header = TRUE,check.names=FALSE)
  dataPhe<-read.table(inf_phe,sep="\t",quote = "",stringsAsFactors = FALSE,header = FALSE,check.names=FALSE)
  groupA_cols<-which(dataPhe==1)
  groupB_cols<-which(dataPhe==2)
  data_target<-data[,c(1,groupA_cols,groupB_cols)]
  group=rep(c(groupA_name,groupB_name),c(length(groupA_cols),length(groupB_cols)))
  l<-list()
  for(k in 1:nrow(data_target)){
    dat=as.numeric(data_target[k,2:ncol(data_target)])
    genename=data_target$gene[k]
    t_test=t.test(dat~group,paired=FALSE)
    t_p_value=c(genename,t_test[[1]][[1]],t_test[[3]][[1]])
    l[[k]]=t_p_value
  }
  df = data.frame(l)
  dft = t(df)
  dftf = as.data.frame(dft)
  colnames(dftf)=c("gene","t_value","p_value")
  rownames(dftf)<-1:nrow(dftf)
  mergef1 <- cbind(data_target,dftf)
  mergef <-mergef1[,-(ncol(mergef1)-2)]
  mergef$groupA_median<-apply(mergef[,c(groupA_cols)],1,median)
  mergef$groupB_median<-apply(mergef[,c(groupB_cols)],1,median)
  mergef$fc_median<-mergef$groupA_median-mergef$groupB_median
  write.table(mergef,outfile,col.names = T,row.names = F,quote=F,sep="\t")
}

args<-commandArgs(TRUE)
inf_exp=args[1]
inf_phe=args[2]
groupA_name=args[3]
groupB_name=args[4]
outfile=args[5]

t_test(inf_exp,inf_phe,groupA_name,groupB_name,outfile)
